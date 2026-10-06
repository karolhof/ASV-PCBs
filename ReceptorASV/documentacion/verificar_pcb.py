from pathlib import Path
import json,math,sys
import wx
app=wx.App(False)
import pcbnew as p
BASE=Path(__file__).resolve().parents[1]
b=p.LoadBoard(str(BASE/'ReceptorASV.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()}
assert len(fs)==31,len(fs)
assert all(t.GetLayer()==p.B_Cu and not isinstance(t,p.PCB_VIA) for t in b.GetTracks())
power={'/GND','/VIN_PROT','/BAT_POS','/BAT_FUSED','/BUCK_5V','/SYS_5V','/LORA_3V3','/RF_433','/RF_SMA'}
for t in b.GetTracks():
 if t.GetNetname() not in power:assert abs(p.ToMM(t.GetWidth())-.5)<.00001,(t.GetNetname(),p.ToMM(t.GetWidth()))
for ref,f in fs.items():
 if ref=='U4':assert f.GetLayer()==p.B_Cu and all(pd.GetAttribute()==p.PAD_ATTRIB_SMD for pd in f.Pads())
 else:assert all(pd.GetAttribute()!=p.PAD_ATTRIB_SMD for pd in f.Pads()),ref
rows=json.loads((BASE/'documentacion/puentes_alambre.json').read_text());assert len(rows)==4
for row in rows:
 f=fs[row['ref']];assert f.GetDuplicatePadNumbersAreJumpers();assert len(list(f.Pads()))==2
 for pd in f.Pads():
  xy=(p.ToMM(pd.GetPosition().x),p.ToMM(pd.GetPosition().y));assert pd.GetNetname()==row['net']
  # Ends beside the bottom-mounted LoRa: >=0.9 mm from hole edge to actual module body.
  if xy[0]<50:assert xy[0]-.3-38.25>=.9-1e-4
# Check local capacitor branches survived routing, including their ground returns.
sys.path.insert(0,str(BASE/'documentacion'))
from verificar_revision_C import parse,child,kids,val
raw=parse((BASE/'ReceptorASV.kicad_pcb').read_text())
segments=kids(raw,'segment')
def has(a,z):
 for s in segments:
  x=tuple(map(float,child(s,'start')[1:]));y=tuple(map(float,child(s,'end')[1:]));
  if (math.dist(x,a)<.001 and math.dist(y,z)<.001) or (math.dist(y,a)<.001 and math.dist(x,z)<.001):return True
 return False
for a,z in [((62.08,63),(62.08,67)),((57.08,63.08),(57.08,67)),((59.54,63),(59.54,55.2)),((57.54,62.46),(57.54,55.2)),((37.785,69.38),(42,68.6)),((37.785,64.3),(42,63.6)),((42,68.6),(47,68.6))]:assert has(a,z),(a,z)
for ref in ['J2','J3']:
 pads=sorted(fs[ref].Pads(),key=lambda a:a.GetNumber());assert len(pads)==3
 assert abs(p.ToMM((pads[1].GetPosition()-pads[0].GetPosition()).EuclideanNorm())-5.08)<.001
for ref in ['J4','JP2']:assert fs[ref].GetAttributes() & p.FP_DNP
assert (BASE/'ASV_Receptor.pretty/ESPRESSIF_ESP32-DEVKITC-32UE.kicad_mod').read_bytes()==(BASE/'referencias/ESP32-DEVKITC-32UE/ESPRESSIF_ESP32-DEVKITC-32UE.kicad_mod').read_bytes()
drc=json.loads((BASE/'documentacion/DRC.json').read_text());assert not drc['unconnected_items'];assert not drc['schematic_parity'];assert not drc['violations'],drc['violations']
print('PCB verificada: 31 huellas; 4 puentes; señales 0,5 mm; cobre B.Cu; capacitores locales; 0 DRC y 0 conexiones pendientes.')
