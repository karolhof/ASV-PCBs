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
