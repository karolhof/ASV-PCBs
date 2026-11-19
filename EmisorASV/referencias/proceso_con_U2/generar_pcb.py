"""PCB receptora: una cara, capacitores locales y UART con borneras. Python de KiCad."""
from pathlib import Path
import sys,json,xml.etree.ElementTree as E
import wx
app=wx.App(False)
import pcbnew as k
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'documentacion'))
from utilidades import parse,child,kids,val,dump
b=k.BOARD();b.SetFileName(str(P/'EmisorASV.kicad_pcb'));b.GetDesignSettings().SetCopperLayerCount(2);b.GetDesignSettings().m_BoardThickness=k.FromMM(1.6)
v=lambda x,y:k.VECTOR2I(k.FromMM(x),k.FromMM(y))
expected=json.loads((P/'documentacion/conexiones_esperadas.json').read_text());sch=parse((P/'EmisorASV.kicad_sch').read_text());root=val(child(sch,'uuid')[1]);uuids={val(next(x for x in kids(s,'property') if val(x[1])=='Reference')[2]):val(child(s,'uuid')[1]) for s in kids(sch,'symbol')}
nets={};nodes={}
for n in E.parse(P/'documentacion/EmisorASV.xml').getroot().findall('./nets/net'):
 name=n.get('name');net=k.NETINFO_ITEM(b,name);b.Add(net);nets[name]=net
 for a in n.findall('node'):nodes[(a.get('ref'),a.get('pin'))]=net
placements={'U2':(54,46,0),'C5':(59.08,50,180),'C6':(56.54,37,180),'C7':(44,58.6,90),'C8':(49,58.6,90),'C4':(66,93,180),'U3':(84,71,0),'U4':(32,62,0),'R1':(49,75,90),'R2':(56,75,90),'J4':(31,34,0),'JP2':(24.237,50,180)}
fps={}
for r,c in expected.items():
 if r.startswith('#'):continue
 lib,name=c['footprint'].split(':');folder=P/'ASV_Emisor.pretty' if lib=='ASV_Emisor' else Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints')/(lib+'.pretty')
 f=k.FootprintLoad(str(folder),name);b.Add(f);fps[r]=f;f.SetReference(r);f.SetValue(c['value']);f.SetFPID(k.LIB_ID(lib,name));f.SetPath(k.KIID_PATH('/'+root+'/'+uuids[r]));f.SetSheetfile('EmisorASV.kicad_sch');f.SetSheetname('')
 sy=next(s for s in kids(sch,'symbol') if val(child(s,'uuid')[1])==uuids[r]);ds=next((val(x[2]) for x in kids(sy,'property') if val(x[1])=='Datasheet'),'');f.SetField('Datasheet',ds)
 x,y,ang=placements[r];f.SetPosition(v(x,y));f.SetOrientationDegrees(ang)
 if r=='U4':f.Flip(f.GetPosition(),False)
 if r in ['J4','JP2']:f.SetDNP(True)
 for pad in f.Pads():
  if (r,pad.GetNumber()) in nodes:pad.SetNet(nodes[(r,pad.GetNumber())])
 f.Value().SetVisible(False);f.Reference().SetTextSize(v(1,1));f.Reference().SetTextThickness(k.FromMM(.15));f.Reference().SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T));f.Reference().SetPosition(v(x,y-4))
for n,(x,y) in enumerate([(25,25),(110,25),(25,95),(110,95)],1):
 f=k.FootprintLoad('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/MountingHole.pretty','MountingHole_3.2mm_M3');b.Add(f);fps['H'+str(n)]=f;f.SetReference('H'+str(n));f.SetValue('M3');f.SetPosition(v(x,y));f.SetAttributes(k.FP_BOARD_ONLY|k.FP_EXCLUDE_FROM_BOM|k.FP_EXCLUDE_FROM_POS_FILES);f.Reference().SetVisible(False);f.Value().SetVisible(False)
shapes=[]
for a,c in [((20,20),(115,20)),((115,20),(115,100)),((115,100),(20,100)),((20,100),(20,20))]:
 s=k.PCB_SHAPE();s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(v(*a));s.SetEnd(v(*c));s.SetLayer(k.Edge_Cuts);s.SetWidth(k.FromMM(.05));b.Add(s);shapes.append(s)
tracks=[]
def route(net,points,width=.7):
 for a,c in zip(points,points[1:]):
  t=k.PCB_TRACK(b);t.SetStart(v(*a));t.SetEnd(v(*c));t.SetLayer(k.B_Cu);t.SetWidth(k.FromMM(width));t.SetNet(nets['/'+net]);b.Add(t);tracks.append(t)
# Short local capacitor supply and ground paths, fixed before routing.
route('SYS_5V',[(59.08,46),(59.08,50)])
route('GND',[(54,46),(54.08,46.08),(54.08,50)])
route('LORA_3V3',[(56.54,46),(56.54,37)])
route('GND',[(54,46),(54.54,45.46),(54.54,37)])
route('LORA_3V3',[(39.785,59.38),(44,58.6),(49,58.6)])
route('GND',[(39.785,54.3),(44,53.6)])
route('SYS_5V',[(66,93),(69.68,93),(71.3,93.86)])
route('RF_433',[(24.237,54.3),(24.237,50)],.8)
route('RF_SMA',[(24.237,47.46),(24.237,44.763),(31,38),(31,34)],.8)
# Copper keepout under the spring antenna exit, not under the signal fanout.
z=k.ZONE(b);z.SetIsRuleArea(True);z.SetLayer(k.B_Cu);z.SetDoNotAllowTracks(False);z.SetDoNotAllowVias(True);z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowPads(False);o=z.Outline();o.NewOutline()
for x,y in [(20,50),(27,50),(27,78),(20,78)]:o.Append(v(x,y))
b.Add(z)
texts=[]
def text(s,x,y,size=1):
 t=k.PCB_TEXT(b);t.SetText(s);t.SetPosition(v(x,y));t.SetLayer(k.F_SilkS);t.SetTextSize(v(size,size));t.SetTextThickness(k.FromMM(.15));b.Add(t);texts.append(t)
text('ASV EMISOR',58,96,1.2)
text('USB 5V',84,97,1)
text('J4 / JP2: NO MONTAR',42,26,.8)
b.BuildConnectivity();k.SaveBoard(str(P/'EmisorASV.kicad_pcb'),b)
assert k.ExportSpecctraDSN(b,str(P/'documentacion/EmisorASV.dsn'))
dsn=parse((P/'documentacion/EmisorASV.dsn').read_text().replace('(string_quote ")',''));st=child(dsn,'structure');layers=kids(st,'layer');child(layers[0],'type')[1]='power';st.insert(st.index(layers[-1])+1,parse('(autoroute_settings (vias off) (layer_rule F.Cu (active off) (preferred_direction horizontal)) (layer_rule B.Cu (active on) (preferred_direction horizontal)))'));child(st,'rule')[:]=parse('(rule (width 500) (clearance 220) (clearance 220 (type smd_smd)))')
network=child(dsn,'network');powers=['/GND','/SYS_5V','/LORA_3V3','/RF_433','/RF_SMA']
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
(P/'documentacion/EmisorASV_una_cara.dsn').write_text(pretty(dsn).replace('(parser','(parser\n    (string_quote ")'))
print('PCB colocada con capacitores locales y ruteo fijo de desacople.')
