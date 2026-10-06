"""Puentes de alambre aislado THT, internos y board-only, para PCB de una cara."""
from pathlib import Path
import wx
app=wx.App(False)
import pcbnew as p
import math,json,re
BASE=Path('/Users/agustinmiranda/Documents/UCC/INVESTIGACION ASV/ASV-PCBs/ReceptorASV')
b=p.LoadBoard(str(BASE/'ReceptorASV.kicad_pcb'))
v=lambda a:p.VECTOR2I(p.FromMM(a[0]),p.FromMM(a[1]))
padlayers=p.LSET()
for layer in [p.F_Cu,p.B_Cu,p.F_Mask,p.B_Mask]:padlayers.AddLayer(layer)
mm=lambda a:(p.ToMM(a.x),p.ToMM(a.y))
# Geometry checker for new wire anchor holes and their short B.Cu branches.
def dist_point_seg(a,c,d):
 dx,dy=d[0]-c[0],d[1]-c[1];t=max(0,min(1,((a[0]-c[0])*dx+(a[1]-c[1])*dy)/(dx*dx+dy*dy))) if dx*dx+dy*dy else 0
 return math.hypot(a[0]-c[0]-t*dx,a[1]-c[1]-t*dy)
def proper_cross(a,c,d,e):
 def cross(x,y,z):return (y[0]-x[0])*(z[1]-x[1])-(y[1]-x[1])*(z[0]-x[0])
 return cross(a,c,d)*cross(a,c,e)<0 and cross(d,e,a)*cross(d,e,c)<0
# Check file contains no disconnected fabricated layer before installing wires.
drc=json.loads((BASE/'documentacion/DRC_ruteo.json').read_text());items={str(x.m_Uuid.AsString()):x for x in [*b.GetTracks(),*(pd for f in b.GetFootprints() for pd in f.Pads())]}
# Prune a dangling tail only after a wire has connected it; it becomes a wire branch.
courts=[];silks=[]
for fp in b.GetFootprints():
 if fp.GetReference() in ['U3','U4'] or fp.GetReference().startswith('W'):continue
 shapes=[g.GetBoundingBox() for g in fp.GraphicalItems() if g.GetLayer()==p.F_CrtYd]
 if shapes:courts.append((min(p.ToMM(r.GetLeft()) for r in shapes),min(p.ToMM(r.GetTop()) for r in shapes),max(p.ToMM(r.GetRight()) for r in shapes),max(p.ToMM(r.GetBottom()) for r in shapes)))
for fp in b.GetFootprints():
 for g in fp.GraphicalItems():
  if g.GetLayer()==p.F_SilkS and hasattr(g,'GetShape') and g.GetShape()==p.SHAPE_T_SEGMENT:silks.append((mm(g.GetStart()),mm(g.GetEnd()),p.ToMM(g.GetWidth())))
existing=[]
for f in b.GetFootprints():
 for pd in f.Pads():
  xy=mm(pd.GetPosition());sz=mm(pd.GetSize());dr=mm(pd.GetDrillSize());sz=sz[::-1] if round(pd.GetOrientationDegrees())%180==90 else sz;existing.append(('pad',xy,sz,dr,pd.GetNetCode()))
for t in b.GetTracks():existing.append(('track',mm(t.GetStart()),mm(t.GetEnd()),p.ToMM(t.GetWidth()),t.GetNetCode()))
def rectdist(a,center,size):
 return math.hypot(max(abs(a[0]-center[0])-size[0]/2,0),max(abs(a[1]-center[1])-size[1]/2,0))
def branch_rectdist(anchor,c,center,size):
 count=max(1,int(math.dist(anchor,c)/.1))
 return min(rectdist((anchor[0]+(c[0]-anchor[0])*i/count,anchor[1]+(c[1]-anchor[1])*i/count),center,size) for i in range(count+1))
def valid(c,anchor,net):
 if not(21.5<c[0]<138.5 and 21.5<c[1]<108.5):return False
 # Do not place wire ends inside THT bodies; radio occupies underside, so also avoid its body.
 if 21.4<c[0]<38.6 and 63.2<c[1]<80.8:return False
 if 85.75<c[0]<114.25 and 50.4<c[1]<105.4 and b.FindNet(net).GetNetname()!="/LORA_MOSI":return False
 for x1,y1,x2,y2 in courts:
  if x1-.81<c[0]<x2+.81 and y1-.81<c[1]<y2+.81:return False
 for x,y,width in silks:
  if dist_point_seg(c,x,y)<.65+width/2+.1:return False
 # Carrier can carry insulated wires under the ESP32, but avoid its solder pads.
 for typ,x,y,z,n in existing:
  if typ=='pad':
   # Hole-to-hole and pad-to-pad constraints (conservative bounding-circle).
   if math.hypot(c[0]-x[0],c[1]-x[1])<.4+max(z)/2+.3 or rectdist(c,x,y)<(.4 if n==net else .5+.22):return False
   if n!=net and branch_rectdist(anchor,c,x,y)<.25+.22:return False
  else:
   if n==net:continue
   if dist_point_seg(c,x,y)<.5+z/2+.22:return False
   if proper_cross(anchor,c,x,y) or min(dist_point_seg(anchor,x,y),dist_point_seg(c,x,y),dist_point_seg(x,anchor,c),dist_point_seg(y,anchor,c))<.25+z/2+.22:return False
 return True
def candidates(item,net):
 connected={str(item.m_Uuid.AsString()):item};todo=[item]
 while todo:
  current=todo.pop()
  for neighbor in b.GetConnectivity().GetConnectedItems(current):
   uid=str(neighbor.m_Uuid.AsString())
   if uid in items and uid not in connected and items[uid].GetNetCode()==net:
    connected[uid]=items[uid];todo.append(items[uid])
 points=[]
 for thing in connected.values():
  if isinstance(thing,p.PAD):points.append(mm(thing.GetPosition()))
  else:points.extend([mm(thing.GetStart()),mm(thing.GetEnd()),((mm(thing.GetStart())[0]+mm(thing.GetEnd())[0])/2,(mm(thing.GetStart())[1]+mm(thing.GetEnd())[1])/2)])
 points=list(dict.fromkeys(points))
 out=[]
 for anchor in points:
  for rad in [1.7,1.85,2,2.5,3,3.5,4,5,6,8,10,12,16,20,24]:
   for a in range(0,360,5):
    c=(round(anchor[0]+rad*math.cos(math.radians(a)),4),round(anchor[1]+rad*math.sin(math.radians(a)),4))
    if valid(c,anchor,net):out.append((rad,c,anchor))
   if len(out)>12:break
 return sorted(out)[:60]
rows=[]
ordered=sorted(drc['unconnected_items'],key=lambda c: (not any(isinstance(items[i['uuid']],p.PAD) and items[i['uuid']].GetAttribute()==p.PAD_ATTRIB_SMD for i in c['items']), next(items[i['uuid']].GetNetname() for i in c['items'])))
for k,conn in enumerate(ordered,1):
 i1,i2=[items[i['uuid']] for i in conn['items']];net=i1.GetNet();n=net.GetNetCode();assert n==i2.GetNetCode()
 c1,c2=candidates(i1,n),candidates(i2,n)
 if not c1 or not c2:raise RuntimeError(('Sin anclaje libre',k,len(c1),len(c2)))
 pairs=[]
 for a in c1:
  for c in c2:
   length=math.dist(a[1],c[1]);pairs.append((a[0]+c[0]+length*.2,a,c))
 _,a,c=min(pairs)
 if net.GetNetname().endswith("DIO1"):
  viable=[z for z in pairs if z[1][1][1]<65.4]
  if viable:_,a,c=min(viable)
 end1,end2=a[1],c[1];anchor1,anchor2=a[2],c[2]
 f=p.FOOTPRINT(b);b.Add(f);ref='W'+str(k);f.SetReference(ref);f.SetValue('ALAMBRE AISLADO');f.SetAttributes(p.FP_THROUGH_HOLE|p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_POS_FILES);f.SetDuplicatePadNumbersAreJumpers(True)
 origin=((end1[0]+end2[0])/2,(end1[1]+end2[1])/2);f.SetPosition(v(origin));length=math.dist(end1,end2);name=f'Wire_Jumper_{ref}_{length:.2f}mm'.replace('.','_');f.SetFPID(p.LIB_ID('ASV_Receptor',name))
 for end in [end1,end2]:
  pd=p.PAD(f);pd.SetNumber('1');pd.SetAttribute(p.PAD_ATTRIB_PTH);pd.SetShape(p.PAD_SHAPE_CIRCLE);pd.SetSize(v((1.0,1.0)));pd.SetDrillSize(v((.6,.6)));pd.SetLayerSet(padlayers);pd.SetPosition(v(end));pd.SetNet(net);f.Add(pd)
  existing.append(('pad',end,(1.0,1.0),(.6,.6),n))
  # End courtyard only: insulated wires can cross above the assembled PCB.
  shape=p.PCB_SHAPE(f);shape.SetShape(p.SHAPE_T_CIRCLE);shape.SetCenter(v(end));shape.SetEnd(v((end[0]+.65,end[1])));shape.SetWidth(p.FromMM(.05));shape.SetLayer(p.F_CrtYd);f.Add(shape)
 shape=p.PCB_SHAPE(f);shape.SetShape(p.SHAPE_T_SEGMENT);shape.SetStart(v(end1));shape.SetEnd(v(end2));shape.SetWidth(p.FromMM(.3));shape.SetLayer(p.Dwgs_User);f.Add(shape)
 f.Reference().SetPosition(v(origin));f.Reference().SetLayer(p.Dwgs_User);f.Reference().SetTextSize(v((1,1)));f.Value().SetVisible(False)
 for start,finish in [(anchor1,end1),(anchor2,end2)]:
  t=p.PCB_TRACK(b);t.SetStart(v(start));t.SetEnd(v(finish));t.SetWidth(p.FromMM(.5));t.SetLayer(p.B_Cu);t.SetNet(net);b.Add(t);existing.append(('track',start,finish,.5,n))
 # Save each board-only footprint into the project library, retaining exact anchors.
 tmp=p.FOOTPRINT(f);tmp.SetPosition(v((0,0)));p.FootprintSave(str(BASE/'ASV_Receptor.pretty'),tmp)
 print(ref,end1,end2,flush=True)
 rows.append({'ref':ref,'net':net.GetNetname(),'length_mm':round(length,2),'pads_mm':[end1,end2],'anchors_mm':[anchor1,anchor2]})
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(BASE/'ReceptorASV.kicad_pcb'),b)
(BASE/'documentacion/puentes_alambre.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
