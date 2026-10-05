---
name: ezermala-ui
description: Ezermalas e-pakalpojuma lapu noteikumi. Izmanto, kad veido vai maini HTML lapas mapē ui/.
---
# Ezermalas lapas

## Valoda
- Visi teksti latviski. Uzruna "jūs".
- Statusi: RECEIVED "Saņemts", IN_PROGRESS "Izskatīšanā", FORWARDED "Pārsūtīts", ANSWERED "Atbildēts", WITHDRAWN "Atsaukts".

## Datumi
- Formāts DD.MM.GGGG. Laiku nerādi, ja tas nav vajadzīgs.

## Dati
- Nekad nerādi personas kodu, vārdu, e-pastu un iesnieguma tekstu, ja uzdevums to skaidri neprasa.
- Rādi tikai laukus, kas vajadzīgi lietotājam šajā lapā.

## Termiņi
- Nokavētu termiņu rādi sarkanā krāsā UN ar tekstu "Termiņš nokavēts".
- Citādi rādi "Atlikušas N dienas".
- Atbildētam iesniegumam termiņu kā nokavētu nerādi.

## Kļūdas
- 404: "Iesniegums ar šādu numuru nav atrasts. Pārbaudiet numuru."
- Citas kļūdas: "Neizdevās ielādēt datus. Mēģiniet vēlreiz." Kļūdas kodu un tehnisko tekstu nerādi.

## Izskats
- Viens HTML fails, bez ārējām bibliotēkām un CDN.
- Lapa lasāma 360 px platumā.
- Krāsas: tumši zila #1D3557, zaļgani zila #2A9D8F, kļūdām #E76F51, fons #F1F3F5.
