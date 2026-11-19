# Verificación de montaje - sin U2

Revision sin U2 - 17/11/2026
LoRa: U3 pad 1 (3V3) -> U4 pad 5 (VCC).
U2, C5 y C6 retirados. C7/C8 junto al radio.
ERC: 0 errores y 0 advertencias. DRC: 0 violaciones, 0 conexiones pendientes, paridad de esquema 0.
GPIO y borneras conservados. Cobre solo B.Cu, señales de 0,5 mm.
Comprobaciones de software; hardware pendiente de ensayo bajo transmision.

| Referencia | Componente | Montaje |
|---|---|---|
| U3 | ESP32-DEVKITC-32UE | THT |
| U4 | LoRa SX1278 / 433 MHz | SMD |
| C4 | 47u / 25 V | THT |
| R1 | 10k | THT |
| R2 | 10k | THT |
| J4 | SMA FUTURO - NO MONTAR | THT |
| JP2 | ABIERTO con resorte | THT |
| C7 | 100n / 50 V | THT |
| C8 | 10u / 25 V | THT |
