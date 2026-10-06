from pathlib import Path
import sys,json,uuid
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'documentacion'))
from verificar_revision_C import *
p=P/'ReceptorASV.kicad_pcb';b=parse(p.read_text());dsn=parse((P/'documentacion/ReceptorASV.dsn').read_text().replace('(string_quote ")',''))
for wire in kids(child(dsn,'wiring'),'wire'):
 a=child(wire,'path');width=float(a[2])/1000;coords=list(map(float,a[3:]));net=val(child(wire,'net')[1]);points=[(coords[i]/1000,-coords[i+1]/1000) for i in range(0,len(coords),2)]
 for start,end in zip(points,points[1:]):b.append(parse(f'(segment (start {start[0]} {start[1]}) (end {end[0]} {end[1]}) (width {width}) (layer "B.Cu") (net "{net}") (uuid "{uuid.uuid4()}"))'))
seen={}
for t in list(kids(b,'segment')):
 key=(val(child(t,'net')[1]),val(child(t,'layer')[1]),tuple(sorted((tuple(map(float,child(t,'start')[1:])),tuple(map(float,child(t,'end')[1:]))))))
 if key in seen:b.remove(t)
 else:seen[key]=t
p.write_text(dump(b))
