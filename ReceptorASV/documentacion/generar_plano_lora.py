from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from verificar_revision_C import parse,kids,child,val
B=Path(__file__).resolve().parents[1]
f=B/'ASV_Receptor.pretty/XL1278_SMT_16P_16.5x17mm_P1.27mm.kicad_mod'
root=parse(f.read_text()); pads=kids(root,'pad')
out=B/'documentacion/Huella_LoRa_XL1278_SMD.pdf'
c=canvas.Canvas(str(out),pagesize=A4);c.setTitle('Huella SMD LoRa XL1278-SMT - Receptor ASV');c.setAuthor('ASV')
def text(x,y,s,size=9,bold=False):
 c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.setFillColor(black);c.drawString(x*mm,y*mm,s)
def draw(cx,cy,scale,nums):
 def xy(x,y):return ((cx+x*scale)*mm,(cy-y*scale)*mm)
 c.setStrokeColor(HexColor('#475569'));c.setFillColor(HexColor('#f1f5f9'));c.setLineWidth(.4)
 x,y=xy(-8.25,8.5);c.rect(x,y,16.5*scale*mm,17*scale*mm,fill=1,stroke=1)
 for p in pads:
  n=val(p[1]);a=child(p,'at');sz=child(p,'size');x,y=float(a[1]),float(a[2]);w,h=float(sz[1]),float(sz[2]);ang=float(a[3]) if len(a)>3 else 0
  if ang%180:w,h=h,w
  px,py=xy(x-w/2,y+h/2)
  c.setFillColor(HexColor('#d97706'));c.setStrokeColor(HexColor('#92400e'));c.roundRect(px,py,w*scale*mm,h*scale*mm,min(w,h)*scale*.2*mm,stroke=1,fill=1)
  if nums:
   c.setFillColor(black);c.setFont('Helvetica-Bold',8);tx,ty=xy(x,y);c.drawCentredString(tx,ty-2.5,n)
 px,py=xy(-9.65,-7.7);c.setStrokeColor(black);c.circle(px,py,.25*scale*mm,fill=0,stroke=1)
 c.setFillColor(HexColor('#334155'));c.setFont('Helvetica-Bold',12 if nums else 3);c.drawCentredString(cx*mm,cy*mm,'XL1278-SMT')
 if nums:
  c.setFont('Helvetica',8);c.drawCentredString(cx*mm,(cy-4)*mm,'cara superior / sin espejo')
text(18,280,'LoRa XL1278-SMT',21,True)
text(18,271,'Huella SMD para el módulo completo - receptor ASV / revisión C',10)
c.setStrokeColor(HexColor('#cbd5e1'));c.line(18*mm,266*mm,192*mm,266*mm)
text(18,261,'VISTA AMPLIADA 5:1',10,True)
draw(64,207,5,True)
# Dimensions refer to module body, not the overall copper extent.
c.setStrokeColor(black);c.setLineWidth(.5)
x1=(64-8.25*5)*mm;x2=(64+8.25*5)*mm;y=252*mm
c.line(x1,y,x2,y)
for x in [x1,x2]:c.line(x,y-2*mm,x,y+2*mm)
c.setFont('Helvetica',9);c.drawCentredString((x1+x2)/2,y+2.3*mm,'16,5 mm (cuerpo)')
x=113*mm;y1=(207-8.5*5)*mm;y2=(207+8.5*5)*mm
c.line(x,y1,x,y2)
for y in [y1,y2]:c.line(x-2*mm,y,x+2*mm,y)
c.saveState();c.translate(117*mm,207*mm);c.rotate(90);c.setFont('Helvetica',9);c.drawCentredString(0,0,'17 mm (cuerpo)');c.restoreState()
text(130,256,'CONTACTOS',10,True)
labels={1:'GND',2:'DIO1',3:'DIO2',4:'DIO3',5:'VCC / 3,3 V',6:'MISO',7:'MOSI',8:'SCK',9:'NSS / CS',10:'DIO0',11:'RESET',12:'GND',13:'DIO4',14:'DIO5',15:'GND RF',16:'ANT'}
for n in range(1,17):
 yy=248-(n-1)*5.9
 text(131,yy,f'{n:02}',9,True);text(144,yy,labels[n],9)
text(18,146,'Paso principal: 1,27 mm  |  Pads: 2,4 × 0,9 mm  |  16 contactos SMD',10,True)
text(18,139,'Capas: cobre frontal, máscara y pasta. Sin perforaciones.',9)
text(18,133,'El punto exterior marca el pin 1. La antena corresponde al pin 16.',9)
text(18,119,'COMPROBACIÓN A ESCALA REAL 1:1',10,True)
draw(41,101,1,False)
text(66,106,'Imprimir al 100 % / tamaño real.',10,True)
text(66,99,'Desactivar “ajustar a página”.',9)
text(66,92,'Apoyar el módulo sobre el dibujo y comprobar todos los pads.',8)
text(18,79,'Regla de control de impresión: debe medir exactamente 100 mm.',9)
c.setStrokeColor(black);c.line(18*mm,71*mm,118*mm,71*mm)
for t in range(0,101,10):
 x=(18+t)*mm;c.line(x,69*mm,x,73*mm);c.setFont('Helvetica',7);c.drawCentredString(x,66*mm,str(t))
text(18,54,'Estado: huella creada; ajuste físico pendiente de cotejo.',10,True)
text(18,47,'Medidas globales y paso aportados por el usuario. Posiciones de contactos',9)
text(18,42,'según referencia XL1278-SMT; verificar orientación y dimensiones en la unidad real.',9)
text(18,32,'Referencia geométrica: github.com/matburnham/kicad-libs',8)
text(18,26,'Archivo: XL1278_SMT_16P_16.5x17mm_P1.27mm.kicad_mod',8)
text(18,17,'05/10/2026  |  La escala 1:1 corresponde solo al dibujo pequeño y a la regla.',8)
c.save();print(out)
