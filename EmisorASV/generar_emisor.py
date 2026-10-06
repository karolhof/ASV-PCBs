#!/usr/bin/env python3
"""Genera el esquema KiCad y bibliotecas locales del receptor ASV (revision E - THT + LoRa SMD)."""
from pathlib import Path
import re, json, uuid, math, copy
BASE=Path(__file__).resolve().parent
STD=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols')
q=lambda s:json.dumps(str(s),ensure_ascii=False)
u=lambda:str(uuid.uuid4())
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
def dump(x):return '('+' '.join(map(dump,x))+')' if isinstance(x,list) else str(x)
def child(x,key):return next((t for t in x if isinstance(t,list) and t[0]==key),None)
def kids(x,key):return [t for t in x if isinstance(t,list) and t[0]==key]
def val(x):return json.loads(x) if x.startswith('"') else x
libs={}; custom={}
def standard(lib,name):
 key=lib+':'+name
 if key in libs:return key
 root=parse((STD/(lib+'.kicad_sym')).read_text())
 syms={val(t[1]):t for t in kids(root,'symbol')}
 def expand(n):
  s=copy.deepcopy(syms[n]); ext=child(s,'extends')
  if ext:
   parentname=val(ext[1]); parent=expand(parentname)
   ownprops={val(p[1]) for p in kids(s,'property')}
   body=[t for t in parent[2:] if not (isinstance(t,list) and (t[0]=='property' and val(t[1]) in ownprops))]
   for t in body:
    if isinstance(t,list) and t[0]=='symbol':t[1]=q(val(t[1]).replace(parentname+'_',n+'_'))
   s=['symbol',q(n)]+body+[t for t in s[2:] if not(isinstance(t,list) and t[0]=='extends')]
  return s
 s=expand(name);s[1]=q(key);libs[key]=s;return key
def block(name,pins,w,h):
 # pins: number, name, electrical type, side L/R/T/B, local coordinate along side
 s=['symbol',q(name),['pin_names',['offset','0.8']],['in_bom','yes'],['on_board','yes']]
 for n,v in [('Reference','U'),('Value',name),('Footprint',''),('Datasheet','')]:
  s.append(parse(f'(property {q(n)} {q(v)} (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))'))
 s.append(parse(f'(symbol {q(name+"_0_1")} (rectangle (start {-w} {h}) (end {w} {-h}) (stroke (width 0.254) (type default)) (fill (type background))))'))
 body=['symbol',q(name+'_1_1')]
 for num,pn,typ,side,co in pins:
  x,y,ang={'L':(-w-5.08,co,0),'R':(w+5.08,co,180),'T':(co,h+5.08,270),'B':(co,-h-5.08,90)}[side]
  body.append(parse(f'(pin {typ} line (at {x} {y} {ang}) (length 5.08) (name {q(pn)} (effects (font (size 1.016 1.016)))) (number {q(num)} (effects (font (size 0.889 0.889)))))'))
 s.append(body);custom[name]=copy.deepcopy(s);s[1]=q('ASV_Emisor:'+name);libs['ASV_Emisor:'+name]=s;return 'ASV_Emisor:'+name
# Pins retain their original electrical/footprint numbers; regrouped to make wiring legible.
left=['3V3','EN','GPIO36','GPIO39','GPIO34','GPIO35','GPIO32','GPIO33','GPIO25','GPIO26','GPIO27','GPIO14','GPIO12','GND','GPIO13','SD2','SD3','CMD','5V']
right=['GND','GPIO23','GPIO22','TX0','RX0','GPIO21','GND','GPIO19','GPIO18','GPIO5','GPIO17','GPIO16','GPIO4','GPIO0','GPIO2','GPIO15','SD1','SD0','CLK']
names={str(i+1):n for i,n in enumerate(left+right)}
sig_order=[('28','18 / SCK'),('21','23 / MOSI'),('27','19 / MISO'),('11','27 / NSS'),('12','14 / RESET'),('10','26 / DIO0'),('9','25 / DIO1'),('8','33 / DIO2')]
spi_y=[round(129.54+i*7.62,4) for i in range(8)]
pins=[(n,name,'bidirectional','R',round(171.45-y,4)) for (n,name),y in zip(sig_order,spi_y)]
for n,name,y in [('25','21 / TX1',198.12),('22','22 / RX1',205.74),('30','17 / TX2',220.98),('31','16 / RX2',228.6)]:
 pins.append((n,name,'bidirectional','R',round(171.45-y,4)))
pins += [('19','5V','power_in','T',0),('14','GND','power_in','B',-10.16),('20','GND','power_in','B',0),('26','GND','power_in','B',10.16)]
used={p[0] for p in pins}
for i,(n,name) in enumerate((n,name) for n,name in names.items() if n not in used):
 typ='power_out' if name=='3V3' else 'input' if name in ['EN','GPIO36','GPIO39','GPIO34','GPIO35'] else 'bidirectional'
 pins.append((n,name,typ,'L',round(53.34-i*3.81,4)))
esp=block('ESP32_DEVKITC_32UE',pins,20.32,60.96)
loras=[('8','SCK','input'),('7','MOSI','input'),('6','MISO','output'),('9','NSS','input'),('11','RESET','input'),('10','DIO0','bidirectional'),('2','DIO1','bidirectional'),('3','DIO2','bidirectional')]
lp=[(n,name,typ,'L',round(157.48-y,4)) for (n,name,typ),y in zip(loras,spi_y)]
lp += [('5','VCC 3V3','power_in','T',0),('16','ANT','passive','R',27.94),('4','DIO3','bidirectional','R',15.24),('13','DIO4','bidirectional','R',10.16),('14','DIO5','bidirectional','R',5.08),('1','GND','power_in','R',-13.97),('12','GND','power_in','R',-21.59),('15','GND RF','power_in','R',-29.21)]
lora=block('XL1278_SMT_433_VERIFICAR',lp,20.32,38.1)
buck=block('R78E5V_1A',[('1','VIN','power_in','L',0),('3','5V OUT','power_out','R',0),('2','GND','power_in','B',0)],13.97,7.62)
ldo=block('LD1117V33_TO220',[('3','IN','power_in','L',2.54),('2','OUT','power_out','R',2.54),('1','GND','power_in','B',0)],10.16,6.35)
uart=block('UART_3V3',[('2','A RX STM32','passive','L',3.81),('3','DE TX STM32','passive','L',-3.81),('1','GND','passive','R',0)],13.97,8.89)
bat=block('BATERIA_12V',[('1','BAT+','passive','R',2.54),('2','BAT-','passive','R',-2.54)],7.62,6.35)
jump=block('Puente_2P',[('1','1','passive','L',0),('2','2','passive','R',0)],2.54,2.54)
for n in ['R','C','C_Polarized','D_Schottky','D_Zener','Fuse']:standard('Device',n)
rfjump=standard('Jumper','Jumper_2_Open');standard('Connector','Conn_Coaxial');standard('power','PWR_FLAG')
root=u(); elements=[]; instances={}; bom=[]
def fx(size=1.27,justify=''):return f'(effects (font (size {size} {size}))'+(f' (justify {justify})' if justify else '')+')'
def note(txt,x,y,size=1.27):elements.append(f'(text {q(txt)} (at {x} {y} 0) {fx(size,"left top")} (uuid {q(u())}))')
def wire(p1,p2):
 if p1==p2:return
 elements.append(f'(wire (pts (xy {p1[0]} {p1[1]}) (xy {p2[0]} {p2[1]})) (stroke (width 0.2032) (type default)) (uuid {q(u())}))')
def label(net,p,side='R'):
 elements.append(f'(label {q(net)} (at {p[0]} {p[1]} 0) {fx(1.27,"right bottom" if side=="L" else "left bottom")} (uuid {q(u())}))')
def put(key,ref,value,x,y,rot=0,foot='',datasheet='',props=None):
 sym=libs[key]; iid=u(); pts={}; angles={}
 for body in kids(sym,'symbol'):
  for p in kids(body,'pin'):
   a=child(p,'at'); px,py=float(a[1]),float(a[2]); rad=math.radians(rot)
   coord=(round(x+px*math.cos(rad)-py*math.sin(rad),4),round(y-py*math.cos(rad)-px*math.sin(rad),4))
   num=val(child(p,'number')[1]);pts[num]=coord;angles[num]=(float(a[3])+rot)%360
 # Use generous property separation for blocks; small parts put labels beside vertical bodies.
 if props is None:
  if key.startswith('ASV_Emisor:'):
   hh={'ESP32_DEVKITC_32UE':38.1,'XL1278_SMT_433_VERIFICAR':27.94,'R78E5V_1A':7.62,'LD1117V33_TO220':6.35,'UART_3V3':7.62,'BATERIA_12V':6.35}[key.split(':')[1]]
   props=[(x,y-hh-7.62),(x,y-hh-3.81)]
  elif key in ['Device:C','Device:C_Polarized','Device:R','Device:Fuse'] and rot==0:props=[(x+4,y-1.27),(x+4,y+1.27)]
  else:props=[(x,y-7.62),(x,y-3.81)]
 ps=''
 for k,v,pos,hide in [('Reference',ref,props[0],False),('Value',value,props[1],False),('Footprint',foot,(x,y),True),('Datasheet',datasheet,(x,y),True)]:
  just='left' if key in ['Device:C','Device:C_Polarized','Device:R','Device:Fuse'] and rot==0 and not hide else ''
  effects=fx(1.27,just)
  if hide:effects=effects[:-1]+' (hide yes))'
  ps+=f'(property {q(k)} {q(v)} (at {pos[0]} {pos[1]} {90 if rot in (90,270) else 0}) {effects})'
 pn=''.join(f'(pin {q(n)} (uuid {q(u())}))' for n in pts)
 elements.append(f'(symbol (lib_id {q(key)}) (at {x} {y} {rot}) (unit 1) (in_bom yes) (on_board yes) (dnp {"yes" if ref in ["JP2","J4"] else "no"}) (uuid {q(iid)}) {ps} {pn} (instances (project "EmisorASV" (path {q("/"+root)} (reference {q(ref)}) (unit 1)))))')
 instances[ref]={'pins':pts,'angles':angles,'nets':{},'value':value,'footprint':foot}
 if not ref.startswith('#'):bom.append((ref,value,foot))
 return ref
def connect(ref,pin,net,length=5.08):
 pin=str(pin);i=instances[ref];p=i['pins'][pin];ang=i['angles'][pin]
 dx,dy={0:(-1,0),180:(1,0),90:(0,1),270:(0,-1)}[ang]
 e=(round(p[0]+length*dx,4),round(p[1]+length*dy,4));wire(p,e);label(net,e,'L' if dx<0 else 'R');i['nets'][pin]=net
 return e
def nc(ref,pin):
 p=instances[ref]['pins'][str(pin)];elements.append(f'(no_connect (at {p[0]} {p[1]}) (uuid {q(u())}))');instances[ref]['nets'][str(pin)]='NC'
def flag(ref,x,y,net):
 put('power:PWR_FLAG',ref,'PWR_FLAG',x,y,props=[(x,y-5),(x,y-2)])
 connect(ref,'1',net,2.54)
CAP='Capacitor_THT:CP_Radial_D5.0mm_P2.00mm';RES='Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal'
CER='Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm'
# Revision B: all connections are continuous drawn wires, including supply and ground.
segments=[]
def wire(p1,p2):
 p1=tuple(round(v,4) for v in p1);p2=tuple(round(v,4) for v in p2)
 if p1==p2:return
 assert p1[0]==p2[0] or p1[1]==p2[1],(p1,p2)
 segments.append((p1,p2))
def route(*pts):
 for a,b in zip(pts,pts[1:]):wire(a,b)
def pp(ref,pin):return instances[ref]['pins'][str(pin)]
def mark(ref,pin,net):instances[ref]['nets'][str(pin)]=net
def link(ra,pa,rb,pb,net,via=()):
 route(pp(ra,pa),*via,pp(rb,pb));mark(ra,pa,net);mark(rb,pb,net)
def tap(ref,pin,net,target,via=()):
 route(pp(ref,pin),*via,target);mark(ref,pin,net)


note('EMISOR ASV - ESP32 + LoRa 433 MHz',15.24,12.7,2.54)
note('USB del celular al DevKit. Solo LoRa SMD; resto THT.',15.24,20.32,1.524)
put(esp,'U3','ESP32-DEVKITC-32UE',101.6,171.45,foot='ASV_Emisor:ESPRESSIF_ESP32-DEVKITC-32UE',props=[(66.04,106.68),(66.04,110.49)])
put(lora,'U4','LoRa SX1278 / 433 MHz',269.24,157.48,foot='ASV_Emisor:XL1278_SMT_16P_16.5x17mm_P1.27mm',props=[(301,107.95),(301,111.76)])
put(ldo,'U2','LD1117V33 / 3,3 V LoRa',340.36,45.72,foot='Package_TO_SOT_THT:TO-220-3_Vertical',datasheet='https://www.st.com/resource/en/datasheet/ld1117.pdf',props=[(348,30.48),(348,34.29)])
for ref,x,key,value,foot in [('C4',292.1,'Device:C_Polarized','47u / 25 V',CAP),('C5',317.5,'Device:C','100n / 50 V',CER),('C6',375.92,'Device:C_Polarized','22u / 25 V',CAP)]:
 put(key,ref,value,x,63.5,foot=foot)
route(pp('U3',19),(101.6,43.18),pp('U2',3));mark('U3',19,'SYS_5V');mark('U2',3,'SYS_5V');label('SYS_5V',(210.82,43.18))
for ref in ['C4','C5']:tap(ref,1,'SYS_5V',(pp(ref,1)[0],43.18))
route(pp('U2',2),(398.78,43.18),(398.78,95.25),(180.34,95.25));mark('U2',2,'LORA_3V3')
tap('C6',1,'LORA_3V3',(375.92,43.18));tap('U4',5,'LORA_3V3',(269.24,95.25));label('LORA_3V3',(360.68,95.25))
label('GND',(91.44,248.92));route((91.44,248.92),(393.7,248.92));route((393.7,83.82),(393.7,248.92));route((292.1,83.82),(393.7,83.82))
for ref,pin in [('U2',1),('C4',2),('C5',2),('C6',2)]:tap(ref,pin,'GND',(pp(ref,pin)[0],83.82))
for pin in [14,20,26]:tap('U3',pin,'GND',(pp('U3',pin)[0],248.92))
for (ep,_),(lp,name,_),y in zip(sig_order,loras,spi_y):link('U3',ep,'U4',lp,'LORA_'+name);label('LORA_'+name,(137.16,y))
for ref,x,signal,y in [('R1',180.34,'NSS',spi_y[3]),('R2',205.74,'RESET',spi_y[4])]:
 put('Device:R',ref,'10k',x,114.3,foot=RES);tap(ref,1,'LORA_3V3',(x,95.25));tap(ref,2,'LORA_'+signal,(x,y))
for pin in [1,12,15]:
 pt=pp('U4',pin);tap('U4',pin,'GND',(312.42,pt[1]))
route((312.42,171.45),(312.42,190.5),(393.7,190.5))
for pin in [4,13,14]:nc('U4',pin)
for pin in instances['U3']['pins']:
 if pin not in instances['U3']['nets']:nc('U3',pin)
put('Connector:Conn_Coaxial','J4','SMA FUTURO - NO MONTAR',337.82,129.54,foot='Connector_Coaxial:SMA_Amphenol_132134_Vertical',props=[(337.82,117.475),(337.82,121.285)])
put(rfjump,'JP2','ABIERTO con resorte',311.15,129.54,foot='Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',props=[(310,100.33),(310,104.14)])
link('U4',16,'JP2',1,'RF_433');label('RF_433',(299.72,129.54));link('JP2',2,'J4',1,'RF_SMA');label('RF_SMA',(321.31,129.54));tap('J4',2,'GND',(337.82,190.5))
for ref,x,key,value,foot in [('C7',355.6,'Device:C','100n / 50 V',CER),('C8',381,'Device:C_Polarized','10u / 25 V',CAP)]:
 put(key,ref,value,x,160.02,foot=foot);tap(ref,1,'LORA_3V3',(x,95.25));tap(ref,2,'GND',(x,190.5))
for ref,x,y,net in [('#FLG01',137.16,248.92,'GND'),('#FLG02',160.02,43.18,'SYS_5V')]:
 put('power:PWR_FLAG',ref,'PWR_FLAG',x,y,props=[(x,y-8),(x,y-3.81)]);mark(ref,1,net)
note('USB DEL DEVKIT = ENTRADA DE ALIMENTACION 5 V',154.94,30.48,1.524)
note('El celular debe funcionar como host USB OTG y suministrar energia.\nNo aplicar 12 V ni tension de bateria al DevKit. Sin borneras UART.\nR1/R2: pull-ups NSS y RESET. C5/C6 junto a U2; C7/C8 junto al radio.\nAntena actual: resorte. No montar J4/JP2; ANT no va a GND.\nPunto = union; cruce sin punto = cables separados.',25.4,261.62,1.27)
# Split conductors at branch endpoints, add explicit junctions only where conductors join.
ends={p for seg in segments for p in seg}
ends.update(p for inst in instances.values() for p in inst['pins'].values())
for item in elements:
 node=parse(item)
 if node[0]=='label':
  a=child(node,'at');ends.add((float(a[1]),float(a[2])))
edges=set()
for a,b in segments:
 cuts=[p for p in ends if (a[0]==b[0]==p[0] and min(a[1],b[1])<=p[1]<=max(a[1],b[1])) or (a[1]==b[1]==p[1] and min(a[0],b[0])<=p[0]<=max(a[0],b[0]))]
 cuts.sort()
 for p1,p2 in zip(cuts,cuts[1:]):edges.add(tuple(sorted((p1,p2))))
from collections import Counter
deg=Counter(p for seg in edges for p in seg)
for p,d in deg.items():
 if d>=3:elements.append(f'(junction (at {p[0]} {p[1]}) (diameter 0.762) (color 0 0 0 0) (uuid {q(u())}))')
for p1,p2 in sorted(edges):
 elements.append(f'(wire (pts (xy {p1[0]} {p1[1]}) (xy {p2[0]} {p2[1]})) (stroke (width 0.2032) (type default)) (uuid {q(u())}))')
# Serialize self-contained schematic and local symbol library.
header=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {q(root)}) (paper "A3") (title_block (title "ASV - Emisor LoRa 433 MHz") (date "2026-10-05") (rev "A") (company "UCC - ASV") (comment 1 "USB del celular / ESP32 DevKit / LoRa") (comment 2 "ESP: huella del ZIP. Solo LoRa SMD; resto THT"))'
(BASE/'EmisorASV.kicad_sch').write_text(header+'\n(lib_symbols\n'+'\n'.join(dump(s) for s in libs.values())+')\n'+'\n'.join(elements)+f'\n(sheet_instances (path "/" (page "1")))\n)\n')
(BASE/'ASV_Emisor.kicad_sym').write_text('(kicad_symbol_lib (version 20241209) (generator "kicad_symbol_editor")\n'+'\n'.join(dump(s) for s in custom.values())+'\n)')
(BASE/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "ASV_Emisor") (type "KiCad") (uri "${KIPRJMOD}/ASV_Emisor.kicad_sym") (options "") (descr "Simbolos locales receptor ASV")))\n')
(BASE/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "ASV_Emisor") (type "KiCad") (uri "${KIPRJMOD}/ASV_Emisor.pretty") (options "") (descr "Huellas de referencia: verificar antes de fabricar")))\n')
if not (BASE/'EmisorASV.kicad_pro').exists():
 (BASE/'EmisorASV.kicad_pro').write_text(json.dumps({'meta':{'filename':'EmisorASV.kicad_pro','version':1},'net_settings':{'classes':[{'name':'Default','clearance':0.2,'track_width':0.25,'via_diameter':0.6,'via_drill':0.3,'microvia_diameter':0.3,'microvia_drill':0.1,'diff_pair_width':0.2,'diff_pair_gap':0.25,'diff_pair_via_gap':0.25}],'meta':{'version':4}}},indent=2))

(BASE/'documentacion/conexiones_esperadas.json').write_text(json.dumps(instances,indent=2))
print('Emisor generado')
