# Auditoría de montaje - revisión E

| Referencia | Componente | Montaje |
|---|---|---|
| J1 | BATERIA 12 V / 33 Ah | THT |
| F1 | 1 A / 5x20 mm | THT |
| D1 | 1N5822 | THT |
| D2 | P6KE18A | THT |
| C1 | 47u / 50 V | THT |
| C2 | 10u / 50 V | THT |
| U1 | 12 V a 5 V / R-78E5.0-1.0 | THT |
| JP1 | PUENTE | THT |
| C3 | 10u / 25 V | THT |
| C4 | 47u / 25 V | THT |
| C5 | 100n / 50 V | THT |
| U2 | 5 V a 3,3 V / LD1117V33 | THT |
| C6 | 22u / 25 V | THT |
| U3 | ESP32-DEVKITC-32UE | THT |
| U4 | LoRa SX1278 / 433 MHz | SMD |
| R1 | 10k | THT |
| R2 | 10k | THT |
| J4 | ANTENA 433 MHz | THT |
| JP2 | RF: ABIERTO con resorte | THT |
| C7 | 100n / 50 V | THT |
| C8 | 10u / 25 V | THT |
| J2 | STM32 1 | THT |
| J3 | STM32 2 | THT |

Revision E - KiCad 10.0.6
ERC: 0 errores, 0 advertencias (ver ERC.rpt).
75 conexiones verificadas en netlist; todas siguen conectadas al eliminar etiquetas.
23 referencias fisicas: U4 SMD y las otras 22 THT. UART directos, sin R3-R6.
Huella ESP32 identica byte a byte a la provista en ZIP; 38 nombres/numeros de pin cotejados.
LD1117V33: 1 GND, 2 OUT, 3 IN.
LoRa: 16 pads SMD; paso principal 1,27 mm; sin solapes; separacion minima de cobre 0.37 mm.
La comprobacion geometrica no valida el ajuste contra el modulo fisico.
