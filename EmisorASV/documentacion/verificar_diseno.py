from pathlib import Path
import json,xml.etree.ElementTree as E,subprocess,math,sys
P=Path(__file__).resolve().parents[1]
def netmap(path):
 return {n.get('name').lstrip('/'):frozenset((x.get('ref'),x.get('pin')) for x in n.findall('node') if not x.get('ref').startswith('#')) for n in E.parse(path).getroot().findall('./nets/net')}
n=netmap(P/'documentacion/EmisorASV.xml')
for sig,ep,lp in [('SCK','28','8'),('MOSI','21','7'),('MISO','27','6'),('NSS','11','9'),('RESET','12','11'),('DIO0','10','10'),('DIO1','9','2'),('DIO2','8','3')]:
 nodes={('U3',ep),('U4',lp)}
 if sig=='NSS':nodes.add(('R1','2'))
 if sig=='RESET':nodes.add(('R2','2'))
 assert n['LORA_'+sig]==frozenset(nodes),(sig,n['LORA_'+sig])
assert n['SYS_5V']==frozenset({('U3','19'),('U2','3'),('C4','1'),('C5','1')})
assert n['LORA_3V3']==frozenset({('U2','2'),('U4','5'),('C6','1'),('C7','1'),('C8','1'),('R1','1'),('R2','1')})
assert n['RF_433']==frozenset({('U4','16'),('JP2','1')})
assert {('U3','14'),('U3','20'),('U3','26'),('U4','1'),('U4','12'),('U4','15'),('U2','1')}<=n['GND']
assert not any(k.startswith('UART') for k in n)
# Independently verify the continuous wires by removing every net label.
sys.path.insert(0,str(P/'documentacion'))
from utilidades import parse,kids,child,val,dump
s=parse((P/'EmisorASV.kicad_sch').read_text());s=[x for x in s if not(isinstance(x,list) and x[0]=='label')];tmp=Path('/tmp/asv-emisor-check');tmp.mkdir(exist_ok=True);(tmp/'EmisorASV.kicad_sch').write_text(dump(s))
subprocess.run(['/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli','sch','export','netlist','--format','kicadxml','--output',str(tmp/'fisico.xml'),str(tmp/'EmisorASV.kicad_sch')],check=True)
assert set(n.values())==set(netmap(tmp/'fisico.xml').values())
import wx
app=wx.App(False)
import pcbnew as p
b=p.LoadBoard(str(P/'EmisorASV.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};assert len(fs)==18,len(fs)
assert all(t.GetLayer()==p.B_Cu and not isinstance(t,p.PCB_VIA) for t in b.GetTracks())
for t in b.GetTracks():
 if t.GetNetname().startswith('/LORA_') and t.GetNetname()!='/LORA_3V3':assert abs(p.ToMM(t.GetWidth())-.5)<1e-5
for ref,f in fs.items():
 if ref=='U4':assert f.GetLayer()==p.B_Cu and all(pd.GetAttribute()==p.PAD_ATTRIB_SMD for pd in f.Pads())
 else:assert all(pd.GetAttribute()!=p.PAD_ATTRIB_SMD for pd in f.Pads())
for r in ['J4','JP2']:assert fs[r].GetAttributes() & p.FP_DNP
rows=json.loads((P/'documentacion/puentes_alambre.json').read_text());assert len(rows)==2
for row in rows:
 f=fs[row['ref']];assert f.GetDuplicatePadNumbersAreJumpers();assert len(list(f.Pads()))==2
 for pd in f.Pads():assert pd.GetNetname()==row['net']
 assert row['pads_mm'][0][0]-.3-40.25>=.9-1e-4
# Direct local supply and return branches must remain present after autorouting.
r=parse((P/'EmisorASV.kicad_pcb').read_text());ts=kids(r,'segment')
def has(a,z):
 return any((math.dist(tuple(map(float,child(t,'start')[1:])),a)<.001 and math.dist(tuple(map(float,child(t,'end')[1:])),z)<.001) or (math.dist(tuple(map(float,child(t,'end')[1:])),a)<.001 and math.dist(tuple(map(float,child(t,'start')[1:])),z)<.001) for t in ts)
for a,z in [((59.08,46),(59.08,50)),((54.08,46.08),(54.08,50)),((56.54,46),(56.54,37)),((54.54,45.46),(54.54,37)),((39.785,59.38),(44,58.6)),((39.785,54.3),(44,53.6)),((44,58.6),(49,58.6))]:assert has(a,z),(a,z)
assert (P/'ASV_Emisor.pretty/ESPRESSIF_ESP32-DEVKITC-32UE.kicad_mod').read_bytes()==(P/'referencias/ESP32-DEVKITC-32UE/ESPRESSIF_ESP32-DEVKITC-32UE.kicad_mod').read_bytes()
d=json.loads((P/'documentacion/DRC.json').read_text());assert not d['violations'] and not d['unconnected_items'] and not d['schematic_parity'],d
assert 'Found 0 ERC violations' in (P/'documentacion/ERC.rpt').read_text() or 'ERC messages: 0' in (P/'documentacion/ERC.rpt').read_text()
print('VERIFICADO: SPI/control, alimentacion USB, cables continuos, 2 puentes, una cara, señales 0,5 mm, desacople local y DRC/ ERC 0.')
