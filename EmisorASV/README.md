# Emisor ASV - ESP32 DevKit y LoRa

Esquema con cables continuos y PCB de una cara. El ESP32 se conecta al LoRa por SPI y control; no hay conexiones UART a STM32. Alimentación por USB del DevKit desde el celular en modo host OTG.

## Archivos

- `EmisorASV.kicad_pro`: proyecto KiCad 10.
- `EmisorASV.kicad_sch`: esquema conectado.
- `EmisorASV.kicad_pcb`: PCB principal, cobre solo B.Cu.
- `EmisorASV_Vista_puentes.kicad_pcb`: copia para mostrar alambres en F.Cu; no fabricar esa cara.
- `documentacion/EmisorASV.pdf`: esquema.
- `documentacion/PCB_Emisor_montaje.pdf`: guía de montaje.
- `documentacion/PCB_Impresion_1a1.pdf`: cobre y puentes a escala real, con agujeros.
- `documentacion/Lista_de_materiales.md`: materiales y dimensiones.
- `documentacion/ERC.rpt`, `DRC.json`, `verificar_diseno.py`: verificaciones.
- `fabricacion/Gerber/`: fabricación de una cara; no contiene F.Cu.

## Alimentación y montaje

USB alimenta el ESP32; su pin 5V lleva esa alimentación a U2, LD1117V33 TO-220, que genera 3,3 V exclusivamente para el LoRa. Pinout U2: 1 GND, 2 OUT, 3 IN; la aleta es OUT. No conectar el 3V3 del DevKit a LORA_3V3. No conectar batería de 12 V a este emisor.

C4 47 µF junto al pin 5V del ESP32. C5 100 nF junto a IN/GND de U2. C6 22 µF junto a OUT/GND de U2. C7 100 nF y C8 10 µF junto al LoRa, con pistas y retornos locales cortos. Todo THT salvo el módulo LoRa, montado por debajo.

Antena actual de resorte: J4 y JP2 sin montar. ANT del módulo es pad 16, separado de GND. La ruta SMA es una reserva que requiere validación RF antes de usar antena externa.

El celular debe tener modo host USB OTG y suministrar corriente suficiente. Compatibilidad y autonomía dependen del teléfono/cable y se comprueban en el prototipo. El diseño no incluye firmware ni aplicación del celular.

## Mapa de conexiones, igual al receptor

| Señal | GPIO ESP32 | Pad LoRa |
|---|---:|---:|
| SCK | 18 | 8 |
| MOSI | 23 | 7 |
| MISO | 19 | 6 |
| NSS | 27 | 9 |
| RESET | 14 | 11 |
| DIO0 | 26 | 10 |
| DIO1 | 25 | 2 |
| DIO2 | 33 | 3 |
| VCC | LORA_3V3 | 5 |
| GND | GND | 1, 12, 15 |
| ANT | RF_433 | 16 |

R1/R2 de 10 kΩ mantienen NSS/RESET en alto al arrancar. Los pads LoRa 4, 13, 14 quedan sin conectar. GPIO restantes del ESP32 quedan libres. La huella del ESP32 es la suministrada; la LoRa corresponde a la ya confirmada por el usuario para el receptor. Se respaldaron los archivos anteriores en `documentacion/Emisor_antes_de_actualizar.zip`.

## Fuentes

- [Espressif DevKitC V4: USB, alimentación y pines](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html).
- [ST LD1117: pinout y capacitor de estabilidad](https://www.st.com/resource/en/datasheet/ld1117.pdf).
- ZIP del ESP32 y fotos del módulo aportados por el usuario; huella LoRa confirmada en esta conversación.

Las comprobaciones de software no sustituyen las mediciones de 5 V/3,3 V y el ensayo de transmisión del prototipo. Los scripts de generación sobrescriben colocación y esquema; conservar el diseño final antes de ejecutarlos.
