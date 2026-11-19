# Lista de materiales - emisor ASV

Para una placa. Solo U4 LoRa se suelda SMD; todo lo demás es THT. Los módulos completos traen sus componentes internos montados.

| Cant. | Material | Montaje / dimensiones | Referencias |
|---:|---|---|---|
| 1 | ESP32-DEVKITC-32UE | DevKit de 38 pines; huella del ZIP aportado | U3 |
| 1 | Módulo completo XL1278-SMT / SX1278, 433 MHz | SMD; cuerpo 16,5 × 17 mm; paso 1,27 mm | U4 |
| 1 | Electrolítico 47 µF / 25 V | Radial Ø5 mm, paso 2 mm | C4 |
| 1 | Electrolítico 10 µF / 25 V | Radial Ø5 mm, paso 2 mm | C8 |
| 1 | Cerámico con patas 100 nF / 50 V | Disco Ø≤5 mm, espesor ≤2,5 mm, paso 5 mm | C7 |
| 2 | Resistencia 10 kΩ, ¼ W | Axial DIN0207, paso 7,62 mm | R1, R2 |
| 2 | Zócalo hembra 1×19 | Paso 2,54 mm, altura ≥8 mm | Montaje U3 |
| 1 | Antena de resorte 433 MHz | La incluida con el módulo, si corresponde | U4 ANT |
| 1 | Adaptador USB OTG y cable al DevKit | Compatibles con celular y conector real del DevKit | Externo |
| 1 | PCB de una cara | 95 × 80 mm, cobre inferior | — |
| 4 | Tornillos y separadores M3 | Opcionales; agujeros de 3,2 mm | H1–H4 |

Puentes de alambre: ver `Montaje_PCB.md`; usar conductor aislado 0,35–0,45 mm y dejar margen para las patas.

## No comprar/montar por ahora

J4 (SMA Amphenol 132134 vertical THT) y JP2 (tira de dos pines a 2,54 mm con shunt): reservados para futura antena externa. Con el resorte, ambos sin montar y JP2 abierto. ANT no se conecta a GND. Antes de usar SMA, retirar el resorte y validar RF.


El celular debe suministrar energía como host USB OTG; se debe probar su capacidad de alimentar el conjunto real. No se verificó un modelo de celular concreto ni disponibilidad comercial de piezas.

## Alimentación actual, revisión sin U2

El LoRa recibe 3,3 V desde el pin **3V3 (pad 1) del DevKit U3**. U2, C5 y C6 se retiraron; no comprarlos. C7 de 100 nF y C8 de 10 µF se conservan junto al módulo. Verificar tensión, arranque y transmisión con el DevKit real: la corriente disponible depende de su regulador y del consumo conjunto.
