# Componentes - Receptor ASV, revision E - THT + LoRa SMD

U3 y U4 son modulos completos, no chips sueltos. J4 se monta solo para antena externa; no conectar dos antenas. Valores y encapsulados de pasivos deben respetar las tensiones indicadas.

| Referencia | Valor / componente | Huella |
|---|---|---|
| J1 | BATERIA 12 V / 33 Ah | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal |
| F1 | 1 A / 5x20 mm | Fuse:Fuseholder_Cylinder-5x20mm_Schurter_0031_8201_Horizontal_Open |
| D1 | 1N5822 | Diode_THT:D_DO-201AD_P15.24mm_Horizontal |
| D2 | P6KE18A | Diode_THT:D_DO-15_P10.16mm_Horizontal |
| C1 | 47u / 50 V | Capacitor_THT:CP_Radial_D6.3mm_P2.50mm |
| C2 | 10u / 50 V | Capacitor_THT:CP_Radial_D5.0mm_P2.00mm |
| U1 | 12 V a 5 V / R-78E5.0-1.0 | Converter_DCDC:Converter_DCDC_RECOM_R-78E-0.5_THT |
| JP1 | PUENTE | Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical |
| C3 | 10u / 25 V | Capacitor_THT:CP_Radial_D5.0mm_P2.00mm |
| C4 | 47u / 25 V | Capacitor_THT:CP_Radial_D5.0mm_P2.00mm |
| C5 | 100n / 50 V | Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm |
| U2 | 5 V a 3,3 V / LD1117V33 | Package_TO_SOT_THT:TO-220-3_Vertical |
| C6 | 22u / 25 V | Capacitor_THT:CP_Radial_D5.0mm_P2.00mm |
| U3 | ESP32-DEVKITC-32UE | ASV_Receptor:ESPRESSIF_ESP32-DEVKITC-32UE |
| U4 | LoRa SX1278 / 433 MHz | ASV_Receptor:XL1278_SMT_16P_16.5x17mm_P1.27mm |
| R1 | 10k | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal |
| R2 | 10k | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal |
| J4 | ANTENA 433 MHz | Connector_Coaxial:SMA_Amphenol_132134_Vertical |
| JP2 | RF: ABIERTO con resorte | Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical |
| C7 | 100n / 50 V | Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm |
| C8 | 10u / 25 V | Capacitor_THT:CP_Radial_D5.0mm_P2.00mm |
| J2 | STM32 1 | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-3-5.08_1x03_P5.08mm_Horizontal |
| J3 | STM32 2 | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-3-5.08_1x03_P5.08mm_Horizontal |

Fusible de cable externo junto a bateria: 1 A, DC >=32 V, con portafusible adecuado; validar frente al consumo y arranque. No alimenta las placas externas.


## Elementos del montaje de PCB

- W1–W4: cuatro alambres aislados, conductor 0,35–0,45 mm; taladro 0,6 mm.
- Dos zócalos hembra 1×19, paso 2,54 mm, altura >=8 mm para U3.
- Cuatro separadores M3, opcionales.
