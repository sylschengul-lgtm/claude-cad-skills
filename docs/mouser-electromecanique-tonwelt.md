# Liste Mouser — électromécanique et passifs, audioguide Tonwelt / Linkx TG-288

Suite de `docs/mouser-tonwelt-linkx-tg288.md`, limitée aux familles demandées :
prise jack, fusible, haut-parleur, prises USB, prise d'alimentation, bouton
poussoir, antennes, condensateurs et résistances. **Mouser uniquement.**

## Statut des sources

Trois niveaux, indiqués dans la colonne « Statut » :

- **Vu** — le composant est visible sur les 15 photos macro de la carte
  (`diagnostics/talkie-surchauffe/`, branche `claude/appareil-chauffe-bloque-2aopb5`).
- **Documenté** — non photographié, mais attesté par la fiche constructeur du TG-288
  reprise dans le diagnostic (port de charge micro-USB, ressort d'antenne UHF,
  entrée micro / sortie casque selon la version émetteur ou récepteur).
- **À confirmer** — ni photographié ni documenté ici. La référence proposée est un
  point de départ catalogue, pas une pièce à commander en l'état.

---

## La liste

| # | Famille | Statut | Référence Mouser | Fabricant |
|---|---|---|---|---|
| 1 | **Prise jack 3,5 mm**, traversante | Documenté | [`SJ-43514`](https://www.mouser.com/ProductDetail/490-SJ-43514) | Same Sky (CUI Devices) |
| 1b | **Prise jack 3,5 mm**, CMS | Documenté | [`SJ-43514-SMT-TR`](https://www.mouser.com/ProductDetail/CUI-Devices/SJ-43514-SMT-TR/) | Same Sky (CUI Devices) |
| 2 | **Fusible réarmable PPTC** 1812 | À confirmer | [série `MF-MSMF`](https://www.mouser.com/new/bourns/bourns-mf-msmf-series-fuses/) · [catalogue PPTC](https://www.mouser.com/c/circuit-protection/thermistors/resettable-fuses-pptc/) | Bourns |
| 3 | **Haut-parleur** Ø15 mm, 8 Ω | À confirmer | [`AS01508MR-6-R`](https://www.mouser.com/ProductDetail/PUI-Audio/AS01508MR-6-R) · [catalogue](https://www.mouser.com/en/c/electromechanical/audio-devices/speakers-transducers/) | PUI Audio |
| 4 | **Micro-USB B**, CMS coudée | Documenté (port de charge) | [`10118193-0001LF`](https://www.mouser.com/ProductDetail/Amphenol-FCI/10118193-0001LF) · variantes [`…192`](https://www.mouser.com/ProductDetail/Amphenol-FCI/10118192-0001LF) et [`…194`](https://www.mouser.com/en/ProductDetail/Amphenol-FCI/10118194-0001LF) | Amphenol FCI |
| 5 | **Mini-USB B** 5 contacts | À confirmer | [`54819-0519`](https://mouser.com/ProductDetail/Molex/54819-0519) · [catalogue Mini-B CMS](https://www.mouser.com/en/c/connectors/usb-connectors/?product=Mini+USB+Type+B+Connectors&termination+style=SMD%2FSMT) | Molex |
| 6 | **USB-C** 16 contacts, traversante | À confirmer | [`USB4085-GF-A`](https://www.mouser.com/ProductDetail/GCT/USB4085-GF-A) (version tout-CMS : `USB4216`) | GCT |
| 7 | **Prise d'alimentation DC** 2,0 × 6,5 mm, traversante | À confirmer | [`PJ-102AH`](https://www.mouser.com/ProductDetail/Same-Sky/PJ-102AH) · [`PJ-002A`](https://www.mouser.com/en/ProductDetail/Same-Sky/PJ-002A) | Same Sky (CUI Devices) |
| 8 | **Bouton poussoir** CMS (ceux de la carte) | Vu | [`SKRPACE010`](https://www.mouser.com/ProductDetail/Alps-Alpine/SKRPACE010) | Alps Alpine |
| 8b | **Bouton poussoir** traversant 6 × 6 mm | À confirmer | [`B3F-1000`](https://www.mouser.com/ProductDetail/Omron-Electronics/B3F-1000) · [série B3F](https://www.mouser.com/c/electromechanical/switches/tactile-switches/?m=Omron&series=B3F) | Omron |
| 9 | **Antenne UHF** hélicoïdale CMS | Documenté (ressort UHF) | [`ANT-868-VHETH`](https://www.mouser.com/ProductDetail/TE-Connectivity-Linx-Technologies/ANT-868-VHETH) | TE / Linx |
| 9b | **Antenne UHF** monopole embarqué Ø7 mm | Documenté | [`ANT-868-JJB-ST`](https://www.mouser.com/ProductDetail/TE-Connectivity-Linx-Technologies/ANT-868-JJB-ST) | TE / Linx |
| 9c | **Antenne UHF** planaire CMS | Documenté | [`ANT-868-SP`](https://mouser.com/ProductDetail/Linx-Technologies/ANT-868-SP) · [toutes les 868 MHz](https://www.mouser.com/c/passive-components/antennas/?center+frequency=868+MHz) | TE / Linx |
| 10 | **Condensateurs** MLCC 0603 / 0805 / 1206 | Vu (`473` = 47 nF, MLCC de sortie boost) | [catalogue MLCC](https://www.mouser.com/c/passive-components/capacitors/ceramic-capacitors/mlccs-smd-smt/) · [kits](https://www.mouser.com/Passive-Components/Capacitors/Capacitor-Kits/_/N-2iq32) | Murata, Yageo, KEMET |
| 11 | **Résistances** 0603 / 0805 | Vu (`3R3` = 3,3 Ω en 0805) | [catalogue CMS](https://www.mouser.com/c/passive-components/resistors/chip-smd-resistors/) · [kits](https://www.mouser.com/c/passive-components/resistors/resistor-kits/?termination+style=SMD%2FSMT) | Yageo RC0805, Vishay CRCW0805 |

---

## Ce qu'il faut relever pour figer chaque référence

Une seule mesure suffit à trancher dans la plupart des cas.

| # | Mesure à faire | Pourquoi |
|---|---|---|
| 1 | **3 ou 4 contacts** (stéréo ou stéréo + micro), traversant ou CMS, hauteur du corps | Un jack 4 contacts sur une empreinte 3 contacts ne se monte pas |
| 2 | **Marquage et dimensions**, boîtier céramique/verre ou boîtier plat | Un PPTC réarmable et un fusible verre ne sont pas dans la même famille, et le courant de maintien doit être relevé |
| 3 | **Diamètre, impédance (8 Ω ou 32 Ω), épaisseur** | L'impédance conditionne l'étage de sortie audio |
| 4 | Laquelle des trois variantes Amphenol : elles diffèrent par le montage | Empreinte différente |
| 5-6 | Nombre de contacts et type de montage | — |
| 7 | **Diamètre de la broche centrale : 2,0 / 2,1 / 2,5 mm**, et diamètre extérieur | C'est le seul critère qui compte, et il ne se devine pas |
| 8 | Hauteur de l'actionneur et force de contact | Confort d'appui à l'identique |
| 9 | **La bande exacte** — le TG-288 est UHF, mais 863-865 MHz (Europe) et 902-928 MHz (US) ne prennent pas la même antenne. Lire l'étiquette de l'appareil. | Une antenne hors bande dégrade fortement la portée |
| 10-11 | Valeur, tolérance, tension de service, boîtier | — |

---

## Réserves

1. **Seuls les postes 8, 10 et 11 sont visibles sur les photos.** Le jack, le port
   micro-USB et l'antenne sont attestés par la fiche produit, pas par une photo. Le
   fusible, le haut-parleur, la prise mini-USB / USB-C et la prise d'alimentation ne
   sont ni photographiés ni documentés dans ce dépôt : ils viennent d'un relevé fait
   dans une autre session, restée locale et inaccessible depuis ici.
2. **La fréquence de l'antenne n'est pas établie.** Les références 868 MHz sont
   proposées comme bande ISM européenne la plus probable pour ce type de système —
   à vérifier sur l'étiquette avant toute commande.
3. **Ces pièces ne traitent pas la panne de surchauffe.** Le diagnostic met en tête
   la chaîne piles Ni-MH / charge, pas la connectique.
