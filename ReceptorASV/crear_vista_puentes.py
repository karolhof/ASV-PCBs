from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'documentacion'))
from verificar_revision_C import parse,child,kids,val,dump
BASE=Path(__file__).resolve().parent
root=parse((BASE/'ReceptorASV.kicad_pcb').read_text())
netcodes={val(n[2]):n[1] for n in kids(root,'net') if len(n)>2}
for row in json.loads((BASE/'documentacion/puentes_alambre.json').read_text()):
 a,b=row['pads_mm'];root.append(['segment',['start',*map(str,a)],['end',*map(str,b)],['width','.5'],['layer','"F.Cu"'],['net',json.dumps(row['net'])]])
for f in kids(root,'footprint'):
 if any(val(x[1])=='Reference' and val(x[2]).startswith('W') for x in kids(f,'property')):
  f[:]=[x for x in f if not(isinstance(x,list) and x[0]=='fp_line' and val(child(x,'layer')[1])=='Dwgs.User')]
(BASE/'ReceptorASV_Vista_puentes.kicad_pcb').write_text(dump(root))
