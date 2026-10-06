# PCB receptor ASV - montaje

PCB de **120 × 90 mm**, una sola cara física de cobre **B.Cu**. Señales de 0,5 mm; alimentación de 0,7 mm; reserva RF de 0,8 mm. LoRa U4 SMD por debajo; resto THT por arriba. No hay vías. Las STM32 se conectan por J2 y J3, borneras de tres posiciones a 5,08 mm: **1 GND, 2 TX ESP→RX STM, 3 RX ESP←TX STM**; alimentación propia de cada STM32.

## Cuatro puentes

Alambre **aislado** de conductor 0,35–0,45 mm, por la cara superior. Taladros de 0,6 mm y pads de 1 mm. Soldar por debajo. Montar antes de insertar el DevKit. Dos zócalos hembra 1×19 de 2,54 mm, altura al menos 8 mm, permiten pasar los cables debajo del DevKit. Recorridos indicados en `ReceptorASV_Vista_puentes.kicad_pcb` y PDF de montaje.

La PCB principal contiene solo cobre inferior y las huellas de los puentes, marcadas como conexiones internas. La copia `Vista_puentes` usa F.Cu exclusivamente para mostrar los alambres y sus agujeros: **no fabricar una cara superior de cobre ni usar esa copia para Gerbers**.

| Puente | Señal | Distancia entre taladros |
|---|---|---:|
| W1 | DIO0 | 45,60 mm |
| W2 | DIO1 | 46,99 mm |
| W3 | DIO2 | 46,16 mm |
| W4 | MOSI | 76,03 mm |

Añadir longitud para patas y un recorrido con holgura. Los cables pueden cruzarse porque están aislados. Se redujeron los once puentes del diseño anterior a cuatro, conservando el pinout del esquema; no se afirma un mínimo matemático absoluto.

## Capacitores

| Referencia | Ubicación y función |
|---|---|
| C1 | Entrada protegida, reserva de energía de batería |
| C2 | Entrada VIN/GND del buck U1, ramas locales |
| C3 | Salida del buck y JP1, filtrado de 5 V |
| C4 | Junto al pin 5 V del ESP32, reserva local |
| C5 | Entrada/GND de LD1117 U2, ramas de aproximadamente 4 mm |
| C6 | Salida/GND de U2, ramas de aproximadamente 8 mm; estabilidad |
| C7 | VCC del LoRa, rama de aproximadamente 4,3 mm y retorno corto |
| C8 | Junto a C7, reserva local del LoRa |

C5/C6 y C7/C8 no dependen de puentes de alambre. Hay plano GND inferior y retornos cortos además de las pistas directas. Respetar polaridad de electrolíticos. C6 de 22 µF mantiene margen sobre los 10 µF mínimos de la [ficha ST](https://www.st.com/resource/en/datasheet/ld1117.pdf); verificar estabilidad del prototipo. C2/C3 siguen la disposición de filtrado local de la [ficha RECOM](https://recom-power.com/pdf/Innoline/R-78E-1.0.pdf).

El courtyard del LoRa se ajustó por el lado de contactos a 0,115 mm más allá del cobre de sus pads, sin cambiar cuerpo, posiciones, paso ni tamaño de pads. Los agujeros de los alambres quedan fuera del cuerpo real, con al menos 0,9 mm entre borde de taladro y cuerpo. Esto permite soldar sus extremos junto a las castellations sin poner agujeros debajo del módulo.

## Montaje y archivos

- Retirar JP1 antes de conectar USB. La entrada J1 es batería 12 V; pin 1 positivo, pin 2 GND.
- Antena actual: resorte del LoRa. **J4 y JP2 no se montan**. ANT no se conecta a GND.
- `PCB_Impresion_1a1.pdf`: guía superior de alambres, cobre sin espejo y cobre con espejo. Imprimir al 100 %, sin ajuste; regla de 100 mm para comprobar escala. Elegir orientación de cobre según proceso de transferencia.
- `PCB_Receptor_montaje.pdf`: ubicación de componentes y cuatro alambres.
- `fabricacion/Gerber/`: solo B.Cu, B.Mask, ambas serigrafías, contorno y taladros. Sin F.Cu ni archivo de trabajo que prescriba dos caras.

Antes de insertar los módulos, comprobar cortos y medir 5 V / 3,3 V; después ensayar UART y LoRa. DRC y coincidencia PCB/esquema se verifican por software; el hardware no fue ensayado.

`generar_pcb.py` regenera la colocación inicial y borra el ruteo manual. Los scripts de ruteo intermedio no reproducen automáticamente el resultado final: el archivo principal `.kicad_pcb` es el diseño entregado.
