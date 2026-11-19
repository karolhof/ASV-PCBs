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
- ZIP del ESP32 y fotos del módulo aportados por el usuario; huella LoRa confirmada en esta conversación.

Las comprobaciones de software no sustituyen las mediciones de 5 V/3,3 V y el ensayo de transmisión del prototipo. Los scripts de generación sobrescriben colocación y esquema; conservar el diseño final antes de ejecutarlos.

## Revisión del 17/11/2026: alimentación directa de 3V3

**U2, C5 y C6 retirados del esquema y de la PCB.** El pin 3V3 de U3 (pad 1) alimenta LORA_3V3: LoRa y pull-ups. C7 de 100 nF y C8 de 10 µF siguen junto al LoRa con conexiones cortas de alimentación y retorno. C4 permanece junto a 5V del ESP32.

No se modifican los GPIO, borneras ni antena. El emisor sigue alimentándose por USB; el receptor conserva entrada de batería, buck de 5V y JP1. Retirar JP1 antes de USB en el receptor. La capacidad de corriente del regulador del DevKit real debe comprobarse durante transmisión; el hardware todavía no fue ensayado.

Los scripts de ruteo intermedio y reportes de revisiones con regulador están archivados en `referencias/proceso_con_U2/`. El archivo principal `.kicad_pcb` es la PCB vigente.
