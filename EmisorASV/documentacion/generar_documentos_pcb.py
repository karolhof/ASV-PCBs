from pathlib import Path
import re,json,subprocess,io
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4,landscape
from pypdf import PdfReader,PdfWriter,Transformation
P=Path(__file__).resolve().parent;rows=json.loads((P/'puentes_alambre.json').read_text())
for name in ['PCB_montaje','PCB_cobre','PCB_puentes']:
 f=P/(name+'.svg');s=f.read_text();s=re.sub(r'width="[^"]+" height="[^"]+"\s+viewBox="[^"]+"','width="95.2mm" height="80.2mm" viewBox="-0.1 -0.1 95.2 80.2"',s,count=1);f.write_text(s)
 subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o','/tmp/emisor-'+name+'.pdf',str(f)],check=True)
def basepage(size,title):
 buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=size);c.setFont('Helvetica-Bold',15);c.drawString(15*mm,size[1]-17*mm,title);return buf,c
w=PdfWriter()
for idx,(art,title,mirror) in enumerate([('PCB_puentes','GUIA DE PUENTES - lado componentes',False),('PCB_cobre','COBRE B.Cu - sin espejo',False),('PCB_cobre','COBRE B.Cu - espejo horizontal',True)]):
 buf,c=basepage(A4,title);c.setFont('Helvetica',10)
 for y,line in [(270,'Emisor ASV | 95 x 80 mm | Imprimir al 100 %, sin ajustar a pagina.'),(263,'Solo B.Cu es cobre real. F.Cu en la guia representa alambres aislados.'),(256,'Elegir sin espejo/espejo segun el proceso de transferencia utilizado.')]:c.drawString(15*mm,y*mm,line)
 c.line(35*mm,70*mm,135*mm,70*mm)
 for x in range(0,101,10):c.line((35+x)*mm,68*mm,(35+x)*mm,72*mm)
 c.drawString(35*mm,62*mm,'Esta regla debe medir exactamente 100 mm.')
 if idx==0:
  c.drawString(15*mm,105*mm,'W1: DIO1 | W2: DIO2. Taladros de alambre: 0,6 mm.')
  c.drawString(15*mm,98*mm,'Alambres aislados arriba; soldaduras abajo. No fabricar F.Cu.')
 c.showPage();c.save();page=PdfReader(buf).pages[0];a=PdfReader('/tmp/emisor-'+art+'.pdf').pages[0];aw=float(a.mediabox.width)
 trans=Transformation().scale(-1,1).translate(55*mm+aw,145*mm) if mirror else Transformation().translate(55*mm,145*mm)
 page.merge_transformed_page(a,trans);w.add_page(page)
with (P/'PCB_Impresion_1a1.pdf').open('wb') as f:w.write(f)
w=PdfWriter();size=landscape(A4);buf,c=basepage(size,'Emisor ASV - ESP32 + LoRa')
c.setFont('Helvetica',9);c.drawString(12*mm,183*mm,'Vista superior. U4 LoRa debajo; todos los demas componentes y alambres arriba.')
scale=1.7;ox=12;oy=42
c.setStrokeColorRGB(.35,.35,.35);c.setDash(3,2);c.rect((ox+3.75*scale)*mm,(oy+29.5*scale)*mm,16.5*scale*mm,17*scale*mm);c.setDash();c.setFillColorRGB(.35,.35,.35);c.drawString((ox+5*scale)*mm,(oy+32*scale)*mm,'U4 (debajo)')
for i,row in enumerate(rows):
 a,b=row['pads_mm'];x1=ox+(a[0]-20)*scale;y1=oy+(100-a[1])*scale;x2=ox+(b[0]-20)*scale;y2=oy+(100-b[1])*scale
 c.setStrokeColorRGB(.8,.1,.05);c.setFillColorRGB(.8,.1,.05);c.setLineWidth(.8);c.line(x1*mm,y1*mm,x2*mm,y2*mm)
 t,dy=(.45,-8) if i==0 else (.7,3)
 c.drawString((x1+(x2-x1)*t)*mm,(y1+(y2-y1)*t+dy)*mm,row['ref'])
c.setFillColorRGB(0,0,0)
lines=['PCB: 95 x 80 mm.','Cobre: cara inferior B.Cu.','Senales: 0,5 mm.','Alimentacion: 0,7 mm.','','Dos puentes aislados:']+[f"{r['ref']}: {r['net'].split('_',1)[-1]}, {r['length_mm']:.2f} mm" for r in rows]+['(distancia entre agujeros).','Cortar unos 50 mm por alambre;','ajustar con holgura y patas.','','Evitar apoyar alambres sobre','capacitores. Pasarlos a su lado.','Instalarlos antes del DevKit.','','ESP32: dos zocalos 1x19','de 2,54 mm, altura >=8 mm.','','USB del celular al DevKit','mediante adaptador OTG.','El telefono debe suministrar energia.','','J4 y JP2: NO MONTAR','con la antena de resorte actual.']
y=178
for line in lines:c.drawString(185*mm,y*mm,line);y-=5.5
c.drawString(12*mm,25*mm,'Rojo = alambres aislados por arriba. No es una segunda cara de cobre.')
c.showPage();c.save();page=PdfReader(buf).pages[0];a=PdfReader('/tmp/emisor-PCB_montaje.pdf').pages[0];blank=PdfWriter().add_blank_page(width=size[0],height=size[1]);blank.merge_transformed_page(a,Transformation().scale(scale).translate(ox*mm,oy*mm));blank.merge_page(page);w.add_page(blank)
buf,c=basepage(A4,'Emisor - capacitores y montaje');c.setFont('Helvetica',10);y=266
lines=['Alimentacion actual: LoRa desde 3V3 del DevKit U3, pad 1.', 'U2, C5 y C6 retirados del esquema y de la PCB.', '', 'C4 47 uF / 25 V: junto al pin 5 V del ESP32.', 'C7 100 nF: junto a VCC del LoRa, rama local de unos 4,3 mm.', 'C8 10 uF / 25 V: junto a C7, reserva de energia del radio.', 'Se mantienen las conexiones cortas de alimentacion y retorno a masa.', '', 'No se agregan puentes por este cambio. Se conserva el pinout.', 'Respetar polaridad de electroliticos y la marca de pin 1 del LoRa.', '', 'Montaje:', '1. Revisar medidas de componentes e impresion al 100 %.', '2. Taladrar; instalar alambres aislados por arriba, soldar abajo.', '3. Montar componentes THT y los zocalos hembra del ESP32.', '4. Revisar cortos; insertar el ESP32 y medir 3,3 V antes del LoRa.', '5. Soldar el LoRa por debajo y conectar su antena de resorte.', '6. Comprobar arranque y tension de 3,3 V durante transmision.', '', 'El regulador del DevKit alimenta ahora al ESP32 y al radio.', 'La corriente disponible depende del DevKit real y debe comprobarse.', 'El hardware todavia no fue ensayado.', '', 'J4 y JP2: no montar con antena de resorte. ANT no va a GND.', 'Emisor: alimentacion USB desde celular host OTG. No aplicar 12 V.']
for line in lines:c.drawString(15*mm,y*mm,line);y-=7
c.showPage();c.save();w.add_page(PdfReader(buf).pages[0])
with (P/'PCB_Emisor_montaje.pdf').open('wb') as f:w.write(f)
print('PDFs creados: montaje (2 paginas) e impresion 1:1 (3 paginas).')
