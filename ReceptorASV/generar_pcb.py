"""PCB receptora: una cara, capacitores locales y UART con borneras. Python de KiCad."""
from pathlib import Path
import sys,json,xml.etree.ElementTree as E
import wx
app=wx.App(False)
import pcbnew as k
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'documentacion'))
from verificar_revision_C import parse,child,kids,val,dump
b=k.BOARD();b.SetFileName(str(P/'ReceptorASV.kicad_pcb'));b.GetDesignSettings().SetCopperLayerCount(2);b.GetDesignSettings().m_BoardThickness=k.FromMM(1.6)
v=lambda x,y:k.VECTOR2I(k.FromMM(x),k.FromMM(y))
expected=json.loads((P/'documentacion/conexiones_esperadas.json').read_text());sch=parse((P/'ReceptorASV.kicad_sch').read_text());root=val(child(sch,'uuid')[1]);uuids={val(next(x for x in kids(s,'property') if val(x[1])=='Reference')[2]):val(child(s,'uuid')[1]) for s in kids(sch,'symbol')}
nets={};nodes={}
for n in E.parse(P/'documentacion/ReceptorASV.xml').getroot().findall('./nets/net'):
 name=n.get('name');net=k.NETINFO_ITEM(b,name);b.Add(net);nets[name]=net
 for a in n.findall('node'):nodes[(a.get('ref'),a.get('pin'))]=net
placements={'J1':(130,28,270),'F1':(100,26,0),'D1':(80,26,0),'D2':(77,44,0),'C1':(77,35,0),'C2':(93,44,0),'U1':(95,38,0),'C3':(106,47.6,180),'JP1':(103,43,90),'U2':(57,63,0),'C5':(62.08,67,180),'C6':(59.54,55.2,180),'C7':(42,68.6,90),'C8':(47,68.6,90),'C4':(82,103,180),'U3':(100,81,0),'U4':(30,72,0),'R1':(48,83.5,90),'R2':(55,83.5,90),'J2':(132,73,270),'J3':(132,91,270),'J4':(27,46,0),'JP2':(22.237,60,180)}
fps={}
for r,c in expected.items():
 if r.startswith('#'):continue
 lib,name=c['footprint'].split(':');folder=P/'ASV_Receptor.pretty' if lib=='ASV_Receptor' else Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints')/(lib+'.pretty')
 f=k.FootprintLoad(str(folder),name);b.Add(f);fps[r]=f;f.SetReference(r);f.SetValue(c['value']);f.SetFPID(k.LIB_ID(lib,name));f.SetPath(k.KIID_PATH('/'+root+'/'+uuids[r]));f.SetSheetfile('ReceptorASV.kicad_sch');f.SetSheetname('')
 sy=next(s for s in kids(sch,'symbol') if val(child(s,'uuid')[1])==uuids[r]);ds=next((val(x[2]) for x in kids(sy,'property') if val(x[1])=='Datasheet'),'');f.SetField('Datasheet',ds)
 x,y,ang=placements[r];f.SetPosition(v(x,y));f.SetOrientationDegrees(ang)
 if r=='U4':f.Flip(f.GetPosition(),False)
 if r in ['J4','JP2']:f.SetDNP(True)
 for pad in f.Pads():
  if (r,pad.GetNumber()) in nodes:pad.SetNet(nodes[(r,pad.GetNumber())])
 f.Value().SetVisible(False);f.Reference().SetTextSize(v(1,1));f.Reference().SetTextThickness(k.FromMM(.15));f.Reference().SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T));f.Reference().SetPosition(v(x,y-4))
for n,(x,y) in enumerate([(25,25),(136,42),(25,105),(120,105)],1):
 f=k.FootprintLoad('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/MountingHole.pretty','MountingHole_3.2mm_M3');b.Add(f);fps['H'+str(n)]=f;f.SetReference('H'+str(n));f.SetValue('M3');f.SetPosition(v(x,y));f.SetAttributes(k.FP_BOARD_ONLY|k.FP_EXCLUDE_FROM_BOM|k.FP_EXCLUDE_FROM_POS_FILES);f.Reference().SetVisible(False);f.Value().SetVisible(False)
shapes=[]
for a,c in [((20,20),(140,20)),((140,20),(140,110)),((140,110),(20,110)),((20,110),(20,20))]:
 s=k.PCB_SHAPE();s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(v(*a));s.SetEnd(v(*c));s.SetLayer(k.Edge_Cuts);s.SetWidth(k.FromMM(.05));b.Add(s);shapes.append(s)
tracks=[]
def route(net,points,width=.7):
 for a,c in zip(points,points[1:]):
  t=k.PCB_TRACK(b);t.SetStart(v(*a));t.SetEnd(v(*c));t.SetLayer(k.B_Cu);t.SetWidth(k.FromMM(width));t.SetNet(nets['/'+net]);b.Add(t);tracks.append(t)
# Capacitor loops established first; these routes are fixed during autorouting.
route('VIN_PROT',[(95,38),(93,40),(93,44)])
route('GND',[(97.54,38),(97.54,41.46),(95,44)])
route('BUCK_5V',[(100.08,38),(103,40.92),(103,43)])
route('GND',[(97.54,38),(97.54,40.54),(104,47.6)])
route('SYS_5V',[(105.54,43),(106,43.46),(106,47.6)])
route('SYS_5V',[(62.08,63),(62.08,67)])
route('GND',[(57,63),(57.08,63.08),(57.08,67)])
route('LORA_3V3',[(59.54,63),(59.54,55.2)])
route('GND',[(57,63),(57.54,62.46),(57.54,55.2)])
route('LORA_3V3',[(37.785,69.38),(42,68.6),(47,68.6)])
route('GND',[(37.785,64.3),(42,63.6)])
route('SYS_5V',[(82,103),(84.68,103),(87.3,103.86)])
route('RF_433',[(22.237,64.3),(22.237,60)],.8)
route('RF_SMA',[(22.237,57.46),(22.237,54.763),(27,50),(27,46)],.8)
# Copper keepout under the spring antenna exit, not under the signal fanout.
z=k.ZONE(b);z.SetIsRuleArea(True);z.SetLayer(k.B_Cu);z.SetDoNotAllowTracks(False);z.SetDoNotAllowVias(True);z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowPads(False);o=z.Outline();o.NewOutline()
for x,y in [(20,60),(25,60),(25,88),(20,88)]:o.Append(v(x,y))
b.Add(z)
texts=[]
def text(s,x,y,size=1):
 t=k.PCB_TEXT(b);t.SetText(s);t.SetPosition(v(x,y));t.SetLayer(k.F_SilkS);t.SetTextSize(v(size,size));t.SetTextThickness(k.FromMM(.15));b.Add(t);texts.append(t)
text('ASV RECEPTOR - REV F',66,105,1.2);text('ABRIR JP1 ANTES DE USB',105,55,.85)
text('12V AGM',128,40);text('+',124,28);text('-',124,33.08)
for r,y in [('J2',73),('J3',91)]:
 text(r+' / UART 3V3',124,y-5, .9)
 for s,yy in [('GND',y),('TX > RX',y+5.08),('RX < TX',y+10.16)]:text(s,123,yy,.85)
text('J4 / JP2: NO MONTAR',44,29,.8)
b.BuildConnectivity();k.SaveBoard(str(P/'ReceptorASV.kicad_pcb'),b)
assert k.ExportSpecctraDSN(b,str(P/'documentacion/ReceptorASV.dsn'))
dsn=parse((P/'documentacion/ReceptorASV.dsn').read_text().replace('(string_quote ")',''));st=child(dsn,'structure');layers=kids(st,'layer');child(layers[0],'type')[1]='power';st.insert(st.index(layers[-1])+1,parse('(autoroute_settings (vias off) (layer_rule F.Cu (active off) (preferred_direction horizontal)) (layer_rule B.Cu (active on) (preferred_direction horizontal)))'));child(st,'rule')[:]=parse('(rule (width 500) (clearance 220) (clearance 220 (type smd_smd)))')
network=child(dsn,'network');powers=['/GND','/BAT_POS','/BAT_FUSED','/VIN_PROT','/BUCK_5V','/SYS_5V','/LORA_3V3','/RF_433','/RF_SMA']
for cls in kids(network,'class'):
 cls[:]=[x for x in cls if not(isinstance(x,str) and val(x) in powers)]
 for rule in kids(cls,'rule'):cls.remove(rule)
 cls.append(parse('(rule (width 500) (clearance 220))'))
network.append(parse('(class GND /GND (rule (width 700) (clearance 220)))'))
network.append(parse('(class Power '+ ' '.join(json.dumps(n) for n in powers if n!='/GND')+' (rule (width 700) (clearance 220)))'))
for wire in kids(child(dsn,'wiring'),'wire'):
 typ=child(wire,'type')
 if typ:typ[1]='fix'
 else:wire.append(['type','fix'])
def pretty(x,depth=0):
 if not isinstance(x,list):return str(x)
 return '('+''.join(('\n'+'  '*(depth+1)+pretty(a,depth+1)) if isinstance(a,list) else ' '+str(a) for a in x).lstrip()+')'
(P/'documentacion/ReceptorASV_una_cara.dsn').write_text(pretty(dsn).replace('(parser','(parser\n    (string_quote ")'))
print('PCB colocada con capacitores locales y ruteo fijo de desacople.')
