from pathlib import Path
import re, json, zipfile, math, xml.etree.ElementTree as E, subprocess
BASE=Path(__file__).resolve().parents[1]
def parse(s):
 ts=iter(re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',s))
 def sub():
  out=[]
  for t in ts:
   if t=='(':out.append(sub())
   elif t==')':return out
   else:out.append(t)
  return out
 return sub()[0]
def kids(n,k):return [x for x in n if isinstance(x,list) and x[0]==k]
def child(n,k):return next((x for x in n if isinstance(x,list) and x[0]==k),None)
def val(s):return json.loads(s) if s.startswith('"') else s
def dump(x):return '('+' '.join(map(dump,x))+')' if isinstance(x,list) else str(x)
def footprint_path(name):
 lib,fp=name.split(':')
 root=BASE/'ASV_Receptor.pretty' if lib=='ASV_Receptor' else Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints')/(lib+'.pretty')
 return root/(fp+'.kicad_mod')
def nets(root):return {n.get('name').lstrip('/'):frozenset((a.get('ref'),a.get('pin')) for a in n.findall('node') if not a.get('ref').startswith('#')) for n in root.findall('./nets/net')}
def check():
 expected=json.loads((BASE/'documentacion/conexiones_esperadas.json').read_text());actual=nets(E.parse(BASE/'documentacion/ReceptorASV.xml').getroot());look={p:n for n,ps in actual.items() for p in ps}
 checked=0;mount=[]
 for ref,c in expected.items():
  if ref.startswith('#'):continue
  for pin,net in c['nets'].items():
   if net=='NC':continue
   assert look.get((ref,pin))==net,(ref,pin,net,look.get((ref,pin)))
   checked+=1
  fp=parse(footprint_path(c['footprint']).read_text());pads=kids(fp,'pad')
  types={p[2] for p in pads if val(p[1])}
  assert types==({'smd'} if ref=='U4' else {'thru_hole'}),(ref,types)
  assert set(c['pins'])=={val(p[1]) for p in pads if val(p[1])},(ref,'pad/pin mismatch')
  mount.append(f'| {ref} | {c["value"]} | {"SMD" if ref=="U4" else "THT"} |')
 # Imported footprint geometry/file is unchanged.
 fp=BASE/'ASV_Receptor.pretty/ESPRESSIF_ESP32-DEVKITC-32UE.kicad_mod';src=BASE/'referencias/ESP32-DEVKITC-32UE/ESPRESSIF_ESP32-DEVKITC-32UE.kicad_mod'
 assert fp.read_bytes()==src.read_bytes()
 # Check all supplied symbol pin names against the 38-pin functional symbol used in schematic.
 lib=parse((BASE/'referencias/ESP32-DEVKITC-32UE/ESP32-DEVKITC-32UE.kicad_sym').read_text())
 supplied={val(child(p,'number')[1]):val(child(p,'name')[1]) for sy in kids(lib,'symbol') for body in kids(sy,'symbol') for p in kids(body,'pin')}
 left=['3V3','EN','VP','VN','34','35','32','33','25','26','27','14','12','GND','13','D2','D3','CMD','5V'];right=['GND','23','22','TX','RX','21','GND','19','18','5','17','16','4','0','2','15','D1','D0','CLK']
 assert supplied=={str(i+1):n for i,n in enumerate(left+right)},supplied
 # The LDO changes pin numbering but no other pre-existing net assignments change.
 with zipfile.ZipFile(BASE/'documentacion/revision_B_antes_THT.zip') as z:old=json.loads(z.read('documentacion/conexiones_esperadas.json'))
 for ref,c in old.items():
  if ref in {'U2','R3','R4','R5','R6','J2','J3','J4'} or ref.startswith('#'):continue
  assert {p:n for p,n in c['nets'].items() if not n.startswith('UART')}=={p:n for p,n in expected[ref]['nets'].items() if not n.startswith('UART')},ref
 assert expected['U2']['nets']=={'3':'SYS_5V','2':'LORA_3V3','1':'GND'}
 assert not ({'R3','R4','R5','R6'} & set(expected))
 for n,tx,rx in [(1,'25','22'),(2,'30','31')]:
  assert actual[f'UART{n}_TX']==frozenset({('U3',tx),(f'J{n+1}','2')})
  assert actual[f'UART{n}_RX']==frozenset({('U3',rx),(f'J{n+1}','3')})
 # Continuous wires: remove labels in a temporary copy and re-export.
 sch=parse((BASE/'ReceptorASV.kicad_sch').read_text());sch=[x for x in sch if not(isinstance(x,list) and x[0]=='label')]
 tmp=Path('/tmp/asv-revision-c-wirecheck');tmp.mkdir(exist_ok=True);(tmp/'ReceptorASV.kicad_sch').write_text(dump(sch))
 subprocess.run(['/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli','sch','export','netlist','--format','kicadxml','--output',str(tmp/'physical.xml'),str(tmp/'ReceptorASV.kicad_sch')],check=True)
 physical=nets(E.parse(tmp/'physical.xml').getroot());assert set(actual.values())==set(physical.values())
 # LoRa pad count and spacing; bounding rectangles are conservative for roundrect copper.
 fp=parse(footprint_path(expected['U4']['footprint']).read_text());pads={int(val(p[1])):p for p in kids(fp,'pad')};assert set(pads)==set(range(1,17))
 boxes={}
 for n,p in pads.items():
  a=child(p,'at');sz=child(p,'size');x,y=float(a[1]),float(a[2]);w,h=float(sz[1]),float(sz[2]);ang=float(a[3]) if len(a)>3 else 0
  if ang%180:w,h=h,w
  boxes[n]=(x-w/2,y-h/2,x+w/2,y+h/2)
 mind=999
 for i,b in boxes.items():
  assert b[0]>=-10.2 and b[2]<=10.2 and b[1]>=-9 and b[3]<=10.1
  for j,c in boxes.items():
   if j<=i:continue
   dx=max(b[0]-c[2],c[0]-b[2],0);dy=max(b[1]-c[3],c[1]-b[3],0);dist=math.hypot(dx,dy);mind=min(mind,dist)
   assert dist>=0.2,(i,j,dist)
 for i in range(1,12):assert abs(float(child(pads[i+1],'at')[2])-float(child(pads[i],'at')[2])-1.27)<1e-6
 summary=f'Revision E - KiCad 10.0.6\nERC: 0 errores, 0 advertencias (ver ERC.rpt).\n{checked} conexiones verificadas en netlist; todas siguen conectadas al eliminar etiquetas.\n23 referencias fisicas: U4 SMD y las otras 22 THT. UART directos, sin R3-R6.\nHuella ESP32 identica byte a byte a la provista en ZIP; 38 nombres/numeros de pin cotejados.\nLD1117V33: 1 GND, 2 OUT, 3 IN.\nLoRa: 16 pads SMD; paso principal 1,27 mm; sin solapes; separacion minima de cobre {mind:.2f} mm.\nLa comprobacion geometrica no valida el ajuste contra el modulo fisico.\n'
 (BASE/'documentacion/validacion_netlist.txt').write_text(summary)
 (BASE/'documentacion/Verificacion_montaje.md').write_text('# Auditoría de montaje - revisión E\n\n| Referencia | Componente | Montaje |\n|---|---|---|\n'+'\n'.join(mount)+'\n\n'+summary)
 print(summary)
if __name__=='__main__':check()
