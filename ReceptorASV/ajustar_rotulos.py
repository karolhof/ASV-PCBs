from pathlib import Path
import wx
app=wx.App(False)
import pcbnew as p
BASE=Path(__file__).resolve().parent
b=p.LoadBoard(str(BASE/'ReceptorASV.kicad_pcb'))
positions={'J1':(137.5,31),'F1':(111.25,34),'D1':(86,21.5),'D2':(84,47.5),'C1':(77,30),'C2':(90,49),'U1':(95,30),'C3':(111,47),'JP1':(106,38),'C4':(82,108),'U2':(68,61),'C5':(66,67),'C6':(59,50.5),'C7':(42,61.5),'C8':(51,67),'R1':(45,80),'R2':(59,80),'U3':(100,53),'U4':(30,83),'J2':(133,87.1),'J3':(124,104),'J4':(33,46),'JP2':(28,58)}
for f in b.GetFootprints():
 if f.GetReference() in positions:
  r=f.Reference();x,y=positions[f.GetReference()];r.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));r.SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));r.SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)));r.SetTextThickness(p.FromMM(.12))
p.SaveBoard(str(BASE/'ReceptorASV.kicad_pcb'),b)
