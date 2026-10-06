# Lista de materiales - receptor ASV, revisión E

Para **una placa receptora**. **Solo el módulo LoRa se suelda SMD; todos los otros componentes son through-hole (THT).** Los componentes que ya vienen montados dentro del DevKit o de los módulos no se sueldan individualmente.

| Cant. | Componente | Montaje / dimensiones | Referencias |
|---:|---|---|---|
| 1 | ESP32-DEVKITC-32UE | THT; 38 pines, paso 2,54 mm, hileras separadas 25,4 mm; huella del ZIP aportado | U3 |
| 1 | Módulo completo XL1278-SMT / SX1278 de 433 MHz | **SMD**; 16 pads, cuerpo de referencia 16,5 × 17 mm | U4 |
| 1 | Convertidor RECOM R-78E5.0-1.0, 5 V / 1 A | THT, SIP-3, paso 2,54 mm | U1 |
| 1 | Regulador ST **LD1117V33**, 3,3 V | **TO-220 de 3 patas**; no SOT-223 | U2 |
| 1 | Diodo Schottky **1N5822** | Axial DO-201AD; paso de montaje 15,24 mm | D1 |
| 1 | TVS unidireccional **P6KE18A** | Axial DO-15; paso de montaje 10,16 mm | D2 |
| 1 | Portafusible para PCB **Schurter 0031.8201** o pieza con plano idéntico | THT, para cartucho 5 × 20 mm | F1, soporte |
| 1 | Fusible de **1 A**, nominal DC >=32 V | Cartucho 5 × 20 mm para el soporte anterior; verificar curva de apertura | F1, cartucho |
| 1 | Electrolítico **47 µF / 50 V** | Radial, diámetro 6,3 mm, paso 2,5 mm | C1 |
| 1 | Electrolítico **10 µF / 50 V** | Radial, diámetro 5 mm, paso 2 mm | C2 |
| 2 | Electrolítico **10 µF / 25 V** | Radial, diámetro 5 mm, paso 2 mm | C3, C8 |
| 1 | Electrolítico **47 µF / 25 V** | Radial, diámetro 5 mm, paso 2 mm | C4 |
| 1 | Electrolítico **22 µF / 25 V** | Radial, diámetro 5 mm, paso 2 mm; junto a salida de U2 | C6 |
| 2 | Cerámico con patas **100 nF / 50 V** | Radial/disco, diámetro máximo 5 mm, espesor máximo 2,5 mm, paso 5 mm | C5, C7 |
| 2 | Resistencia **10 kΩ, 1 %, ¼ W** | Axial DIN0207; cuerpo 6,3 × 2,5 mm; paso 7,62 mm | R1, R2 |
| 1 | Bornera de 2 posiciones, tipo Phoenix MKDS 1,5/2-5,08 | THT, paso 5,08 mm, entrada horizontal | J1 |
| 2 | Bornera de tornillo de 3 posiciones, Phoenix MKDS-1,5-3-5.08 o plano identico | THT, paso 5,08 mm; entrada horizontal | J2, J3 |
| 1 | Tira macho de 2 pines | THT, vertical, paso 2,54 mm | JP1 |
| 1 | Puente removible de 2 posiciones (shunt) | Paso 2,54 mm | JP1 |

C6 se aumentó a 22 µF para mantener margen respecto de los 10 µF mínimos indicados por ST para estabilidad. Usar electrolítico de aluminio adecuado para el regulador y verificar estabilidad en el prototipo. No reemplazar automáticamente por un cerámico de ESR muy baja. Respetar polaridad de todos los electrolíticos y verificar diámetro/paso del componente comprado.

## Antena: una sola opción

- **Resorte del módulo:** una antena de 433 MHz; si ya viene incluida no comprar otra. No montar J4 ni JP2; JP2 debe quedar abierto.
- **Antena externa:** agregar un **SMA Amphenol 132134 vertical THT** (J4) y una antena de 433 MHz/50 Ω con conector compatible. Retirar la antena de resorte y montar una tira macho THT de 2 pines con shunt en JP2; validar la ruta RF del prototipo. El antiguo SMA de borde ya no se usa.

## Fuera de la PCB

- Batería TAIYO TYD12-33 AGM de 12 V / 33 Ah indicada por el usuario.
- Portafusible en línea y fusible de 1 A, nominal DC >=32 V, cerca del positivo de batería, adicional a F1.
- Cable positivo/negativo y terminales según longitud, sección y bornes reales.
- Dos arneses UART de 3 conductores: TX, RX y GND; lado receptor con cable pelado para bornera de 5,08 mm; lado STM32 según su placa.
- Dos STM32 con alimentación propia, ya definidas por el usuario; modelos exactos pendientes.
- Una PCB receptora de una cara, 120 × 90 mm.

Agregar **dos tiras hembra THT de 19 contactos, paso 2,54 mm y altura >=8 mm**, para el ESP32. Agregar **cuatro alambres aislados** de conductor 0,35–0,45 mm: longitudes entre agujeros 45,6 / 47,0 / 46,2 / 76,0 mm más margen para las patas. Opcional: cuatro separadores y tornillos M3.

## Sustituciones frente a la lista anterior

- TLV75533PDBVR SMD → **LD1117V33 TO-220**. Cambia la numeración: 1 GND, 2 OUT, 3 IN.
- SS34 SMD → **1N5822 axial**.
- SMBJ16A SMD → **P6KE18A axial**. No sustituir por P6KE16A: su tensión de trabajo no es equivalente.
- Fusible SMD → **cartucho 5 × 20 mm y portafusible THT**.
- Resistencias y capacitores SMD → **axiales y radiales con patas**.
- SMA de borde → **SMA vertical THT**, opcional.

La huella ESP32 proviene del ZIP suministrado. La huella LoRa está creada y asignada, y el usuario confirmó que coincide con su módulo; respetar la marca de pin 1. No se verificaron precios ni disponibilidad comercial.
