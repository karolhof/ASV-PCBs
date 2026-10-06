# Lista de materiales - emisor ASV

Para una placa. Solo U4 LoRa se suelda SMD; todo lo demás es THT. Los módulos completos traen sus componentes internos montados.

| Cant. | Material | Montaje / dimensiones | Referencias |
|---:|---|---|---|
| 1 | ESP32-DEVKITC-32UE | DevKit de 38 pines; huella del ZIP aportado | U3 |
| 1 | Módulo completo XL1278-SMT / SX1278, 433 MHz | SMD; cuerpo 16,5 × 17 mm; paso 1,27 mm | U4 |
| 1 | ST LD1117V33, salida 3,3 V | TO-220-3 vertical, THT | U2 |
| 1 | Electrolítico 47 µF / 25 V | Radial Ø5 mm, paso 2 mm | C4 |
| 1 | Electrolítico 22 µF / 25 V | Radial Ø5 mm, paso 2 mm | C6 |
| 1 | Electrolítico 10 µF / 25 V | Radial Ø5 mm, paso 2 mm | C8 |
| 2 | Cerámico con patas 100 nF / 50 V | Disco Ø≤5 mm, espesor ≤2,5 mm, paso 5 mm | C5, C7 |
| 2 | Resistencia 10 kΩ, ¼ W | Axial DIN0207, paso 7,62 mm | R1, R2 |
| 2 | Zócalo hembra 1×19 | Paso 2,54 mm, altura ≥8 mm | Montaje U3 |
| 1 | Antena de resorte 433 MHz | La incluida con el módulo, si corresponde | U4 ANT |
| 1 | Adaptador USB OTG y cable al DevKit | Compatibles con celular y conector real del DevKit | Externo |
| 1 | PCB de una cara | 95 × 80 mm, cobre inferior | — |
| 4 | Tornillos y separadores M3 | Opcionales; agujeros de 3,2 mm | H1–H4 |

Puentes de alambre: ver `Montaje_PCB.md`; usar conductor aislado 0,35–0,45 mm y dejar margen para las patas.

## No comprar/montar por ahora

J4 (SMA Amphenol 132134 vertical THT) y JP2 (tira de dos pines a 2,54 mm con shunt): reservados para futura antena externa. Con el resorte, ambos sin montar y JP2 abierto. ANT no se conecta a GND. Antes de usar SMA, retirar el resorte y validar RF.

No lleva batería, convertidor 12→5 V, fusible, borneras UART ni conectores STM32. El regulador U2 recibe 5 V del USB del DevKit y alimenta solo el LoRa. No conectar su salida al pin 3V3 del DevKit. C6 de aluminio de 22 µF, respetando polaridad; verificar estabilidad del prototipo y no sustituir automáticamente por cerámico de ESR muy baja.

El celular debe suministrar energía como host USB OTG; se debe probar su capacidad de alimentar el conjunto real. No se verificó un modelo de celular concreto ni disponibilidad comercial de piezas.
