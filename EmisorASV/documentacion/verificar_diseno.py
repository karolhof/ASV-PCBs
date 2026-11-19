from pathlib import Path
import json,sys,subprocess,xml.etree.ElementTree as E
P=Path(__file__).resolve().parents[1];name=P.name
sys.path.insert(0,str(P/'documentacion'))
from utilidades import parse,kids,child,val,dump

def nets(path):
 return {n.get('name').lstrip('/'):frozenset((x.get('ref'),x.get('pin')) for x in n.findall('node') if not x.get('ref').startswith('#')) for n in E.parse(path).getroot().findall('./nets/net')}
n=nets(P/'documentacion'/(name+'.xml'))
assert n['LORA_3V3']==frozenset({('U3','1'),('U4','5'),('R1','1'),('R2','1'),('C7','1'),('C8','1')})
for sig,ep,lp in [('SCK','28','8'),('MOSI','21','7'),('MISO','27','6'),('NSS','11','9'),('RESET','12','11'),('DIO0','10','10'),('DIO1','9','2'),('DIO2','8','3')]:
 ps={('U3',ep),('U4',lp)}
 if sig in ['NSS','RESET']:ps.add(('R1' if sig=='NSS' else 'R2','2'))
 assert n['LORA_'+sig]==frozenset(ps)
assert n['RF_433']==frozenset({('U4','16'),('JP2','1')})
assert {('U3','14'),('U3','20'),('U3','26'),('U4','1'),('U4','12'),('U4','15'),('C7','2'),('C8','2')}<=n['GND']
if name=='ReceptorASV':
 for no,tx,rx in [(1,'25','22'),(2,'30','31')]:
  assert n[f'UART{no}_TX']==frozenset({('U3',tx),(f'J{no+1}','2')});assert n[f'UART{no}_RX']==frozenset({('U3',rx),(f'J{no+1}','3')})
else:assert n['SYS_5V']==frozenset({('U3','19'),('C4','1')})
s=parse((P/(name+'.kicad_sch')).read_text());s=[x for x in s if not(isinstance(x,list) and x[0]=='label')];tmp=Path('/tmp/asv-sin-u2-check')/name;tmp.mkdir(parents=True,exist_ok=True);(tmp/(name+'.kicad_sch')).write_text(dump(s))
subprocess.run(['/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli','sch','export','netlist','--format','kicadxml','--output',str(tmp/'fisico.xml'),str(tmp/(name+'.kicad_sch'))],check=True)
assert set(n.values())==set(nets(tmp/'fisico.xml').values()),'Las conexiones deben ser cables reales, sin depender de etiquetas'
import wx
app=wx.App(False)
import pcbnew as p
b=p.LoadBoard(str(P/(name+'.kicad_pcb')));fs={f.GetReference():f for f in b.GetFootprints()};assert not {'U2','C5','C6'}&set(fs)
assert all(t.GetLayer()==p.B_Cu and not isinstance(t,p.PCB_VIA) for t in b.GetTracks())
for t in b.GetTracks():
 if t.GetNetname().startswith('/LORA_') and t.GetNetname()!='/LORA_3V3':assert abs(p.ToMM(t.GetWidth())-.5)<1e-5
for ref,f in fs.items():assert all(pd.GetAttribute()==p.PAD_ATTRIB_SMD if ref=='U4' else pd.GetAttribute()!=p.PAD_ATTRIB_SMD for pd in f.Pads())
assert next(pd.GetNetname() for pd in fs['U3'].Pads() if pd.GetNumber()=='1')=='/LORA_3V3'
for ref in ['J4','JP2']:assert fs[ref].GetAttributes() & p.FP_DNP
rows=json.loads((P/'documentacion/puentes_alambre.json').read_text());assert len(rows)==(2 if name=='EmisorASV' else 4)
for row in rows:
 f=fs[row['ref']];assert f.GetDuplicatePadNumbersAreJumpers();assert len(list(f.Pads()))==2
 for pd in f.Pads():assert pd.GetNetname()==row['net']
lib='ASV_Emisor.pretty' if name=='EmisorASV' else 'ASV_Receptor.pretty'
assert (P/lib/'ESPRESSIF_ESP32-DEVKITC-32UE.kicad_mod').read_bytes()==(P/'referencias/ESP32-DEVKITC-32UE/ESPRESSIF_ESP32-DEVKITC-32UE.kicad_mod').read_bytes()
d=json.loads((P/'documentacion/DRC.json').read_text());assert not d['violations'] and not d['unconnected_items'] and not d['schematic_parity'],d
assert 'ERC messages: 0' in (P/'documentacion/ERC.rpt').read_text()
print(name+': sin U2/C5/C6; LoRa desde 3V3 DevKit; GPIO sin cambios; una cara; ERC/DRC 0.')
