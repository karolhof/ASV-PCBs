from pathlib import Path
import sys,uuid
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'documentacion'))
from utilidades import *
f=P/'EmisorASV.kicad_pcb';b=parse(f.read_text())
for t in list(kids(b,'segment')):
 a=tuple(map(float,child(t,'start')[1:]));z=tuple(map(float,child(t,'end')[1:]));n=val(child(t,'net')[1])
 if n=='/LORA_DIO1' or (n=='/LORA_3V3' and a in [(39.785,59.38),(36.2,59.38),(36.2,71)] and z in [(36.2,59.38),(36.2,71),(40.2,75)]) or (n=='/GND' and a==(55.6864,35.5852) and z==(77.8257,35.5852)):b.remove(t)
def route(net,ps,w=.7):
 for a,z in zip(ps,ps[1:]):b.append(parse(f'(segment (start {a[0]} {a[1]}) (end {z[0]} {z[1]}) (width {w}) (layer "B.Cu") (net "{net}") (uuid "{uuid.uuid4()}"))'))
route('/LORA_3V3',[(39.785,59.38),(36.2,59.38),(36.2,73),(38.2,75),(40.2,75)])
route('/GND',[(71.3,81.16),(74,79.89),(100,79.89),(100,48.14),(96.7,48.14)],.5)
f.write_text(dump(b))
