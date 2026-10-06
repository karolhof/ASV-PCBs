from pathlib import Path
import re,json,subprocess,io
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4,landscape
from pypdf import PdfReader,PdfWriter,Transformation
P=Path(__file__).resolve().parent
rows=json.loads((P/'puentes_alambre.json').read_text())
# Correct native SVG's clipped page bounds without scaling its geometries.
for name in ['PCB_montaje','PCB_cobre','PCB_puentes']:
 f=P/(name+'.svg');s=f.read_text();s=re.sub(r'width="[^"]+" height="[^"]+"\s+viewBox="[^"]+"','width="120.2mm" height="90.2mm" viewBox="-0.1 -0.1 120.2 90.2"',s,count=1);f.write_text(s)
 subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o','/tmp/'+name+'.pdf',str(f)],check=True)
def basepage(size,title):
 buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=size);c.setFont('Helvetica-Bold',15);c.drawString(15*mm,size[1]-17*mm,title);return buf,c
# Three actual-size print pages, vector artwork + scale ruler.
w=PdfWriter()
for idx,(art,title,mirror) in enumerate([('PCB_puentes','GUIA DE PUENTES - lado componentes',False),('PCB_cobre','COBRE B.Cu - sin espejo',False),('PCB_cobre','COBRE B.Cu - espejo horizontal',True)]):
 buf,c=basepage(A4,title);c.setFont('Helvetica',10)
 c.drawString(15*mm,270*mm,'Receptor ASV | 120 x 90 mm | Imprimir al 100 %, sin ajustar a pagina.')
 c.drawString(15*mm,263*mm,'Solo B.Cu se fabrica en cobre. F.Cu en la guia representa alambres aislados.')
 c.drawString(15*mm,256*mm,'Elegir sin espejo/espejo segun el proceso de transferencia utilizado.')
 c.line(35*mm,70*mm,135*mm,70*mm)
 for x in range(0,101,10):c.line((35+x)*mm,68*mm,(35+x)*mm,72*mm)
 c.drawString(35*mm,62*mm,'Esta regla debe medir exactamente 100 mm.')
 if idx==0:
  c.drawString(15*mm,95*mm,'W1: DIO0 | W2: DIO1 | W3: DIO2 | W4: MOSI')
  c.drawString(15*mm,89*mm,'Agujeros de puentes: 0,6 mm. Montar alambres por arriba; soldar abajo.')
 c.showPage();c.save();page=PdfReader(buf).pages[0];artpage=PdfReader('/tmp/'+art+'.pdf').pages[0];aw=float(artpage.mediabox.width)
 trans=Transformation().scale(-1,1).translate(35*mm+aw,145*mm) if mirror else Transformation().translate(35*mm,145*mm)
 page.merge_transformed_page(artpage,trans);w.add_page(page)
with (P/'PCB_Impresion_1a1.pdf').open('wb') as f:w.write(f)
# Assembly guide with a large top view and an explicit wire overlay.
w=PdfWriter();size=landscape(A4);buf,c=basepage(size,'Receptor ASV - montaje de una cara')
c.setFont('Helvetica',9)
c.drawString(12*mm,183*mm,'Vista superior. LoRa U4 se monta debajo; el resto y los alambres, arriba.')
scale=1.5;ox=12;oy=42
c.setStrokeColorRGB(.35,.35,.35);c.setDash(3,2);c.rect((ox+1.75*scale)*mm,(oy+29.5*scale)*mm,16.5*scale*mm,17*scale*mm);c.setDash();c.setFillColorRGB(.35,.35,.35);c.drawString((ox+3*scale)*mm,(oy+32*scale)*mm,'U4 (debajo)')
for row in rows:
 a,b=row['pads_mm'];x1=ox+(a[0]-20)*scale;y1=oy+(110-a[1])*scale;x2=ox+(b[0]-20)*scale;y2=oy+(110-b[1])*scale
 c.setStrokeColorRGB(.8,.1,.05);c.setFillColorRGB(.8,.1,.05);c.setLineWidth(.8);c.line(x1*mm,y1*mm,x2*mm,y2*mm);t,dy={'W1':(.62,2),'W2':(.3,-6),'W3':(.6,-3),'W4':(.75,2)}[row['ref']];c.drawString((x1+(x2-x1)*t)*mm,(y1+(y2-y1)*t+dy)*mm,row['ref'])
c.setFillColorRGB(0,0,0)
lines=['PCB: 120 x 90 mm.','Cobre: cara inferior B.Cu.','Senales: 0,5 mm.','Alimentacion: 0,7 mm.','','4 alambres aislados:']+[f"{r['ref']}: {r['net'].split('_',1)[-1]}, {r['length_mm']:.1f} mm" for r in rows]+['(distancia entre agujeros).','Agregar margen para las patas.','','Usar dos zocalos hembra 1x19','para ESP32, altura >= 8 mm.','Pasar los alambres antes de','insertar el DevKit.','','J2 y J3: 1 GND / 2 TX / 3 RX.','TX ESP a RX STM; RX ESP a TX STM.','STM32: alimentacion propia.','','Retirar JP1 antes de usar USB.','J4 y JP2: no montar con resorte.']
y=178
for line in lines:c.drawString(202*mm,y*mm,line);y-=5.5
c.drawString(12*mm,25*mm,'Los cables rojos de esta guia son alambres; no son una segunda cara de cobre.')
c.showPage();c.save();page=PdfReader(buf).pages[0]
# Place artwork below overlay by merging its vector layer first, then text and wire overlay.
art=PdfReader('/tmp/PCB_montaje.pdf').pages[0];blank=PdfWriter().add_blank_page(width=size[0],height=size[1]);blank.merge_transformed_page(art,Transformation().scale(scale).translate(ox*mm,oy*mm));blank.merge_page(page);w.add_page(blank)
buf,c=basepage(A4,'Capacitores y montaje')
c.setFont('Helvetica',10);y=266
lines=['Ubicacion de capacitores: pistas locales a alimentacion y masa.','','C1 47 uF / 50 V: reserva de energia de la entrada protegida.','C2 10 uF / 50 V: junto a VIN y GND del convertidor U1.','C3 10 uF / 25 V: junto a JP1 y salida de 5 V del convertidor.','C4 47 uF / 25 V: junto al pin 5 V del ESP32.','C5 100 nF: junto a entrada y GND del LD1117 U2; ramas de 4 mm.','C6 22 uF / 25 V: junto a salida y GND de U2; ramas de unos 8 mm.','C7 100 nF: junto a VCC del LoRa; conexion de unos 4,3 mm.','C8 10 uF / 25 V: junto a C7, para reserva local del radio.','','C5/C6 y C7/C8 tienen retornos locales cortos, sin puentes.','Respetar polaridad de electroliticos, diodos y la marca de pin 1 del LoRa.','','Secuencia sugerida:','1. Revisar impresion 1:1 y medidas de las piezas reales.','2. Taladrar; montar los cuatro alambres aislados por arriba.','3. Soldar componentes THT y zocalos, respetando las polaridades.','4. Sin ESP32 ni LoRa montados, comprobar cortos y medir 5 V / 3,3 V.','5. Soldar el LoRa SMD por debajo. Mantener libre el area de antena.','6. Insertar el DevKit; probar UART y recepcion LoRa.','','El LoRa es el unico componente SMD. Borneras UART: paso 5,08 mm.','Los agujeros de los puentes quedan fuera del cuerpo real del LoRa,','con >= 0,9 mm desde el borde del agujero hasta el cuerpo.','Se ajusto su margen de courtyard sin modificar pads ni dimensiones.','','Estado de archivos: DRC y coincidencia con esquema comprobados.','El hardware aun requiere las mediciones y pruebas del prototipo.']
for line in lines:c.drawString(15*mm,y*mm,line);y-=7
c.showPage();c.save();w.add_page(PdfReader(buf).pages[0])
with (P/'PCB_Receptor_montaje.pdf').open('wb') as f:w.write(f)
print('PDFs creados: montaje (2 paginas) e impresion 1:1 (3 paginas).')
