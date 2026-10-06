# Montaje del emisor ASV

PCB **95 × 80 mm**, una sola cara real de cobre **B.Cu**. Señales de 0,5 mm; alimentación de 0,7 mm; algunas ramas de masa de 0,5 mm para pasar entre pads con la separación comprobada por DRC. Reserva RF de 0,8 mm. No hay vías.

LoRa U4 SMD por debajo; ESP32 en dos zócalos hembra THT 1×19, paso 2,54 mm, altura ≥8 mm. Todo lo demás THT. Los cuatro agujeros de montaje son M3 de 3,2 mm.

## Dos alambres por arriba

| Referencia | Señal | Distancia entre agujeros | Extremos X/Y en KiCad, mm |
|---|---|---:|---|
| W1 | DIO1 | 30,00 mm | 41,6069 / 55,2488 → 69,0342 / 67,4035 |
| W2 | DIO2 | 28,63 mm | 41,4785 / 56,9882 → 68,8852 / 65,2730 |

Conductor **aislado de 0,35–0,45 mm**; taladros 0,6 mm. Cortar inicialmente unos 50 mm por cable y ajustar con holgura y patas. Doblar para pasar junto a los capacitores, sin apoyarse sobre sus cuerpos. Soldar los extremos por abajo y montar los cables antes del DevKit.

`EmisorASV_Vista_puentes.kicad_pcb` representa estos dos cables mediante F.Cu para ver recorridos y agujeros. **No fabricar F.Cu ni generar Gerbers desde esa copia.** El archivo principal contiene solo las pistas reales inferiores y las huellas de conexión de los alambres. Los taladros quedan fuera del cuerpo del LoRa con al menos 0,9 mm de separación desde su borde.

## Desacople y reserva de energía

- **C4:** 47 µF junto al 5V del ESP32.
- **C5:** 100 nF junto a entrada y GND del LD1117, ramas de aproximadamente 4 mm.
- **C6:** 22 µF junto a salida y GND del LD1117, ramas de aproximadamente 9 mm.
- **C7:** 100 nF junto a VCC del LoRa, rama de aproximadamente 4,3 mm y retorno local.
- **C8:** 10 µF junto a C7, reserva local durante transmisión.

Los recorridos locales de estos capacitores se fijaron antes del ruteo y se comprobaron después. Ninguno depende de puentes de alambre. El plano GND inferior y las pistas de masa conectan todas las tierras sin islas eléctricamente separadas.

USB del DevKit es la única alimentación de uso. El celular debe actuar como host OTG y suministrar energía suficiente: falta ensayarlo con su teléfono/cable reales. U2 recibe SYS_5V y entrega LORA_3V3 exclusivamente al radio. No unir LORA_3V3 al 3V3 del DevKit. No aplicar 12 V.

J4 y JP2 sin montar para la antena de resorte. ANT pad 16 no va a GND. Para futuro SMA, quitar el resorte, montar J4/JP2 y validar RF antes de usarlo.

## Archivos y comprobaciones

El PDF `PCB_Impresion_1a1.pdf` incluye guía superior con taladros y cobre normal/espejado. Imprimir al 100 %, sin ajuste; comprobar regla de 100 mm. La orientación para transferencia depende del proceso empleado.

ERC: 0 errores y 0 advertencias. DRC: 0 violaciones, 0 conexiones pendientes, 0 diferencias con el esquema. El verificador también comprueba el pinout contra el receptor, las conexiones por cables sin etiquetas, montaje THT/SMD, huella original ESP32 y pistas locales de capacitores.

El hardware aún debe ensayarse: cortos, 5V/3V3, arranque desde USB OTG y transmisión LoRa. Los scripts de generación sobrescriben el diseño; no ejecutarlos sobre modificaciones manuales sin respaldo.
