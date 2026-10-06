from pathlib import Path
import wx
app=wx.App(False)
import pcbnew as k
P=Path(__file__).resolve().parent;b=k.LoadBoard(str(P/'ReceptorASV.kicad_pcb'));assert k.ImportSpecctraSES(b,str(P/'documentacion/ReceptorASV_una_cara.ses'))
v=lambda x,y:k.VECTOR2I(k.FromMM(x),k.FromMM(y))
z=k.ZONE(b);z.SetLayer(k.B_Cu);z.SetNet(b.FindNet('/GND'));z.SetLocalClearance(k.FromMM(.22));z.SetThermalReliefGap(k.FromMM(.3));z.SetThermalReliefSpokeWidth(k.FromMM(.5));z.SetMinThickness(k.FromMM(.2));z.SetPadConnection(k.ZONE_CONNECTION_THERMAL);o=z.Outline();o.NewOutline()
for x,y in [(20.5,20.5),(139.5,20.5),(139.5,109.5),(20.5,109.5)]:o.Append(v(x,y))
b.Add(z);b.BuildConnectivity();k.SaveBoard(str(P/'ReceptorASV.kicad_pcb'),b)
print('Ruteo importado; GND inferior listo para rellenar.')
