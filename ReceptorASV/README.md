# Receptor ASV - revisión E: LoRa SMD y resto THT

Actualizado el 05/10/2026 para KiCad 10. El esquema conserva **cables continuos** entre la alimentación, el ESP32, el LoRa y los dos conectores UART. Un punto marca una unión; un cruce sin punto no conecta.

## Montaje definido

**U4 (módulo LoRa) es el único componente que se suelda SMD a esta PCB.** Las otras referencias, incluido el SMA y JP2 opcionales, son THT. El DevKit, el buck y el LoRa son módulos completos; sus componentes internos ya vienen montados.

- **U3:** se importó sin cambios geométricos la huella `ESPRESSIF_ESP32-DEVKITC-32UE.kicad_mod` del ZIP del usuario. Se cotejaron los 38 nombres/números de pines con el símbolo suministrado. Paso 2,54 mm; distancia entre hileras 25,4 mm. No se usa la antigua huella aproximada.
- **U4:** huella local `XL1278_SMT_16P_16.5x17mm_P1.27mm`, solo SMD, 16 contactos, paso principal 1,27 mm. Se entrega un plano con escala 1:1. Las posiciones finas siguen basadas en la referencia XL1278-SMT y deben cotejarse con el módulo real.

## Abrir y consultar

- `ReceptorASV.kicad_pro`: proyecto.
- `ReceptorASV.kicad_sch`: esquema conectado, revisión E.
- `ReceptorASV.pdf`: esquema A3.
- `ASV_Receptor.pretty/`: huellas locales del ESP32 y del LoRa.
- `ASV_Receptor.kicad_sym`, `sym-lib-table`, `fp-lib-table`: biblioteca de símbolos y configuración local.
- `documentacion/Lista_de_materiales.md`: lista agrupada por cantidades, actualizada a THT.
- `documentacion/BOM.md`: correspondencia entre referencia, valor y huella.
- `documentacion/Huella_LoRa_XL1278_SMD.pdf`: plano ampliado, numeración y comprobación a escala 1:1.
- `documentacion/huellas/`: vistas SVG exportadas por KiCad.
- `documentacion/ERC.rpt`, `validacion_netlist.txt`, `Verificacion_montaje.md`: comprobaciones.
- `referencias/ESP32-DEVKITC-32UE/`: originales del ZIP (símbolo, huella y STEP). El STEP se conserva como referencia; no se asignó una transformación 3D no verificada.

La PCB está colocada y ruteada: **120 × 90 mm, cobre solo B.Cu, señales de 0,5 mm y cuatro puentes aislados por arriba**. Se conserva el esquema y su pinout. Los capacitores de desacople tienen conexiones locales cortas a alimentación y masa. El hardware aún requiere pruebas del prototipo.

- `ReceptorASV.kicad_pcb`: diseño principal para fabricar.
- `ReceptorASV_Vista_puentes.kicad_pcb`: guía visual con alambres representados en F.Cu; no fabricar esa capa.
- `documentacion/Montaje_PCB.md` y `PCB_Receptor_montaje.pdf`: montaje y posición de capacitores.
- `documentacion/PCB_Impresion_1a1.pdf`: agujeros, guía de puentes y cobre a escala real.
- `documentacion/DRC.json`, `verificar_pcb.py`: comprobaciones de conexiones, anchos, montaje y capacitores.
- `fabricacion/Gerber/`: fabricación de una cara; no hay F.Cu.

## Alimentación

J1 recibe la batería AGM TAIYO TYD12-33, 12 V / 33 Ah. Pin 1 positivo, pin 2 negativo/GND. Entrada prevista 10,5–14,7 V.

1. F1: cartucho 5 × 20 mm de 1 A, nominal DC >=32 V, en portafusible Schurter 0031.8201 THT. Añadir un fusible de cable junto al positivo de batería; el fusible de PCB no protege el cable anterior a ella. Validar curva frente al arranque.
2. D1: 1N5822 axial, protección de polaridad; D2: P6KE18A unidireccional, cátodo a VIN_PROT y ánodo a GND. El P6KE18A tiene tensión de trabajo 15,3 V y limitación especificada 25,2 V en las condiciones de su ficha; verificar transitorios reales. No equivale a P6KE16A.
3. U1: buck RECOM R-78E5.0-1.0, 5 V/1 A, entrada 8–28 V. Su huella THT usa el cuerpo/paso compatibles de la familia R-78E. Reservar unos 0,7 A a 5 V para ESP32 y radio, y medir consumo real. Un 7805 lineal no es sustituto validado.
4. JP1 une BUCK_5V a SYS_5V.
5. U2: **LD1117V33 en TO-220**, conectado 1 GND, 2 OUT y 3 IN. La aleta metálica también es OUT (3,3 V), no GND. Recibe SYS_5V y alimenta únicamente el LoRa.
6. C5: 100 nF cerámico THT junto a entrada U2. C6: 22 µF/25 V electrolítico junto a su salida, con margen sobre los 10 µF mínimos indicados por ST. C7/C8: 100 nF y 10 µF junto al radio.

A 140 mA de radio, la disipación aproximada de U2 es (5–3,3) × 0,14 = 0,24 W más su consumo propio; verificar temperatura del prototipo. No se alimentan las STM32 desde esta placa. No unir la salida LORA_3V3 al 3V3 del DevKit.

C3 y C4 aportan 57 µF en SYS_5V; con el DevKit, mantener la carga capacitiva dentro de los 220 µF especificados por RECOM. C1/C2 son ahora electrolíticos radiales; el convertidor tiene filtrado interno. Verificar arranque, rizado y transitorios con el cable/batería reales; RECOM recomienda arranque suave. El circuito no carga la batería ni tiene corte automático por descarga profunda.

### USB

**Retirar JP1 antes de conectar USB al DevKit.** Con JP1 abierto, USB puede alimentar SYS_5V a través del DevKit y el regulador LoRa. No conectar USB con JP1 puesto; no hay selección automática de fuentes.

## Señales ESP32 y LoRa

El módulo de la última foto es SX1278 de 433 MHz. El patrón de referencia es XL1278-SMT; no confundir con Ra-02, DRF1278F u otros módulos que usan el mismo chip con otro pinout.

| Señal | GPIO ESP32 | Pad LoRa |
|---|---:|---:|
| SCK | 18 | 8 |
| MOSI | 23 | 7 |
| MISO | 19 | 6 |
| NSS / CS | 27 | 9 |
| RESET | 14 | 11 |
| DIO0 | 26 | 10 |
| DIO1 | 25 | 2 |
| DIO2 | 33 | 3 |
| VCC | LORA_3V3 | 5 |
| GND | GND | 1, 12, 15 |
| Antena | RF_433 | 16 |
| DIO3 / DIO4 / DIO5 | Sin conectar | 4 / 13 / 14 |

El antiguo símbolo del emisor asigna ANT al 12. No usar esa asignación para este módulo de referencia: 12 es GND y 16 es ANT. El emisor no se modificó.

Los pines del ESP32 están agrupados funcionalmente en el dibujo para mantener cables legibles; la numeración física se conserva y coincide con la huella aportada. UART0 queda disponible para USB/programación.

## Dos STM32

| Conector | Pin 1 | Pin 2 | Pin 3 | GPIO del ESP32 |
|---|---|---|---|---|
| J2 | GND | TX ESP → RX STM32 1 | RX ESP ← TX STM32 1 | TX 21, RX 22 (UART1) |
| J3 | GND | TX ESP → RX STM32 2 | RX ESP ← TX STM32 2 | TX 17, RX 16 (UART2) |

Se prevén UART directas de 3,3 V, alimentación propia de cada STM32 y GND común. Falta el modelo exacto de ambas placas para confirmar sus conectores/niveles. UART conectado directamente, sin resistencias serie (R3–R6 retiradas en revisión D). R1 y R2 de 10 kΩ son pull-ups de NSS y RESET del LoRa. No conectar RS-232, RS-485 o señales de 5 V directamente.

## Huella LoRa y antena

La huella tiene pads SMD de 2,4 × 0,9 mm en F.Cu/F.Paste/F.Mask, margen de máscara 0,05 mm, marca de pin 1, contorno de cuerpo en F.Fab y área de montaje en F.CrtYd. No tiene taladros. El espacio mínimo de cobre entre pads es 0,37 mm. El plano PDF se deriva del archivo de huella real, no de un dibujo independiente.

Antes de fabricar, imprimir su dibujo pequeño al 100 %, comprobar la regla de 100 mm y apoyar el módulo para cotejar los 16 contactos, orientación y centros. El usuario confirmó que la huella coincide con su módulo. Respetar la orientación del pin 1 al montar.

Elegir **una sola antena**. Para resorte soldado al módulo, no montar J4 ni JP2; dejar JP2 abierto para aislar el SMA. Para antena externa, retirar el resorte y montar **SMA Amphenol 132134 vertical THT** (J4). Cerrar JP2 únicamente después de retirar el resorte. La ruta SMA queda reservada, pero su impedancia y desempeño RF requieren validación antes de usarla.

## Reproducción y archivos anteriores

`generar_receptor.py` regenera esquema/biblioteca/BOM y copia la huella ESP32 original local. No ejecutarlo sobre modificaciones manuales sin guardarlas primero. `documentacion/verificar_revision_C.py` comprueba netlist, montaje de cada pad, correspondencia de pines y conexiones sin etiquetas. `documentacion/generar_plano_lora.py` regenera el plano PDF con ReportLab.

Las revisiones previas están respaldadas en `documentacion/revision_A_etiquetas.zip` y `revision_B_antes_THT.zip`; las huellas aproximadas anteriores se trasladaron a `referencias/huellas_obsoletas/` y no forman parte de la biblioteca activa.

## Fuentes

- ZIP y capturas aportados por el usuario.
- Espressif DevKitC V4: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html
- RECOM R-78E-1.0: https://recom-power.com/pdf/Innoline/R-78E-1.0.pdf
- ST LD1117: https://www.st.com/resource/en/datasheet/ld1117.pdf
- Vishay 1N5822: https://www.vishay.com/docs/88526/1n5820.pdf
- Vishay P6KE18A: https://www.vishay.com/docs/88369/p6ke.pdf
- Referencia de pinout/geometría LoRa del autor del breakout: https://github.com/matburnham/kicad-libs y https://github.com/matburnham/lora-breakout . No es certificación del fabricante de la unidad del usuario.
- Huellas estándar: bibliotecas instaladas de KiCad.
