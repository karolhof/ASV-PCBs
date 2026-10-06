from pathlib import Path
import sys,uuid
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'documentacion'))
from utilidades import *
f=P/'EmisorASV.kicad_pcb';b=parse(f.read_text())
# The optional SMA approaches the center from below, between its ground pins.
for t in list(kids(b,'segment')):
 if val(child(t,'net')[1])=='/RF_SMA':b.remove(t)
def route(net,ps,w=.7):
 for a,z in zip(ps,ps[1:]):b.append(parse(f'(segment (start {a[0]} {a[1]}) (end {z[0]} {z[1]}) (width {w}) (layer "B.Cu") (net "{net}") (uuid "{uuid.uuid4()}"))'))
route('/RF_SMA',[(24.237,47.46),(24.237,44.763),(31,38),(31,34)],.8)
route('/SYS_5V',[(71.3,93.86),(71.3,97.5),(113,97.5),(113,22),(64,22),(64,41.08),(59.08,46)])
route('/LORA_3V3',[(39.785,59.38),(36.2,59.38),(36.2,71),(40.2,75),(49,75),(56,75)])
f.write_text(dump(b))
p=P/'generar_pcb.py';s=p.read_text().replace('[(24.237,47.46),(24.237,42.763),(31,36),(31,34)]','[(24.237,47.46),(24.237,44.763),(31,38),(31,34)]');p.write_text(s)
