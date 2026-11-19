from pathlib import Path
import wx
app=wx.App(False)
import pcbnew as p
P=Path(__file__).resolve().parent;b=p.LoadBoard(str(P/'EmisorASV.kicad_pcb'))
xy={'U2':(64,45),'C5':(64,50),'C6':(56,32),'C7':(44,51.5),'C8':(53,57),'C4':(65,98),'R1':(46,72),'R2':(60,72),'U3':(84,42),'U4':(32,73),'J4':(37,34),'JP2':(30,48)}
for f in b.GetFootprints():
 if f.GetReference() in xy:
  x,y=xy[f.GetReference()];r=f.Reference();r.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));r.SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));r.SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)));r.SetTextThickness(p.FromMM(.12))
p.SaveBoard(str(P/'EmisorASV.kicad_pcb'),b)
