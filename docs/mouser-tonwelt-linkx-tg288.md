# Liste Mouser — carte audioguide Tonwelt / Linkx TG-288 (eTour)

Référence du relevé : `diagnostics/talkie-surchauffe/DIAGNOSTIC.md`
(branche `claude/appareil-chauffe-bloque-2aopb5`), 15 photos macro de la carte.

**Périmètre : Mouser uniquement.** Chaque ligne indique si la pièce est réellement
commandable chez Mouser, avec une référence fabricant vérifiée quand elle existe.

---

## A. Commandable chez Mouser — référence vérifiée

| Composant sur la carte | Réf. fabricant | Fabricant | Page Mouser | Qté carte |
|---|---|---|---|---|
| Inductance blindée 4,7 µH, boîtier 4×4 mm (étage boost) | `SRN4018-4R7M` | Bourns | [mouser](https://www.mouser.com/en/ProductDetail/Bourns/SRN4018-4R7M) | 2 |
| Poussoirs tactiles CMS | `SKRPACE010` (série SKRP) | Alps Alpine | [mouser](https://www.mouser.com/ProductDetail/Alps-Alpine/SKRPACE010) | 2 à 4 |
| Résistances 0805 `3R3` (3,3 Ω) | série CRCW0805 ou RC0805 | Vishay / Yageo | [catalogue](https://www.mouser.com/c/passive-components/resistors/chip-smd-resistors/) | 2 |
| Condensateur 0603 `473` (47 nF) | série GRM188 ou CC0603 | Murata / Yageo | [catalogue](https://www.mouser.com/c/passive-components/capacitors/ceramic-capacitors/mlccs-smd-smt/) | 1+ |
| MLCC de sortie boost (1206/0805, X5R/X7R) | à relever sur la carte | — | [catalogue](https://www.mouser.com/c/passive-components/capacitors/ceramic-capacitors/mlccs-smd-smt/) | 4+ |
| Accus 2 × AA Ni-MH appairés (**la réparation la plus probable**) | gamme Panasonic Ni-MH | Panasonic | [catalogue Ni-MH](https://www.mouser.com/en/c/power/batteries/nimh-nickel-metal-hydride-battery/?m=Panasonic) | 2 |

## B. Chez Mouser, mais la référence exacte reste à établir

| Composant | Ce qu'il faut faire | Point de départ Mouser |
|---|---|---|
| **MCU TI MSP430FR2xxx**, TSSOP-48 — marquage partiellement masqué sur la photo (`…30TM FR2 0xx 8CCH T B`) | Relire le marquage complet à la loupe, puis commander la référence exacte. ⚠️ Le MCU est **programmé en usine** : le remplacer ne remet pas l'appareil en service sans le firmware Linkx. | [famille MSP430FR2xxx](https://www.mouser.com/c/semiconductors/embedded-processors-controllers/microcontrollers-mcu/?q=MSP430FR2) |
| **Prise jack 3,5 mm** | ⚠️ Elle **n'apparaît sur aucune des 15 photos** (elles ne couvrent que la zone RF / MCU / alimentation). Il faut une photo du bord de carte. Puis choisir selon 3 ou 4 contacts et traversant ou CMS. | traversant : [`SJ-43514`](https://www.mouser.com/ProductDetail/490-SJ-43514) · CMS : [`SJ-43514-SMT-TR`](https://www.mouser.com/ProductDetail/CUI-Devices/SJ-43514-SMT-TR/) (Same Sky / CUI Devices) |
| **Fusible** | ⚠️ Non visible non plus sur les photos. Relever le marquage et les dimensions : un PPTC réarmable et un fusible verre ne se commandent pas dans la même famille. | PPTC 1812 : [série Bourns MF-MSMF](https://www.mouser.com/new/bourns/bourns-mf-msmf-series-fuses/) · [catalogue PPTC](https://www.mouser.com/c/circuit-protection/thermistors/resettable-fuses-pptc/) |

## C. Non distribué par Mouser

| Composant | Pourquoi | Où l'obtenir |
|---|---|---|
| `Linkx eTour-07 2003B` — SoC RF UHF, QFN-32 | Puce **propriétaire marquée au nom du produit**. Aucun distributeur généraliste. | Linkx Electronics / Tonwelt (SAV) |
| `HOLTEK HT16C21` — driver LCD | Mouser ne distribue pas Holtek. | TME, LCSC, ou distributeur Holtek |
| TCXO `24.04 AK AD` — 24,04 MHz | Fréquence non standard, hors catalogue. | Fabricant d'oscillateurs sur commande, ou Linkx |
| `19AKM` (SOT-23-5, boost) | Code CMS absent des bases publiques ; fabricant asiatique non identifié. | Remonter d'abord au fabricant par brochage et topologie |
| `CDV 221 A5L2` (SOP-8) | idem | idem |
| `724 2G SU` (SOP-8) | idem | idem |
| `BSG· TI 8A8 A46R` (QFN-16) | CI Texas Instruments, mais le code boîtier ne suffit pas à remonter à la référence. | Décodage TI nécessaire |

---

## Ce qu'il faut savoir avant de commander

1. **Aucune de ces pièces ne répare l'appareil à elle seule.** Le diagnostic classe en tête
   les hypothèses **H1/H2/H3** — piles alcalines mises en charge, surcharge Ni-MH, accu vieilli
   entraînant l'arrêt du boost. Le poste utile est donc la **ligne « accus AA Ni-MH »** du
   tableau A, pour quelques euros, et le test croisé des piles (§6.2 du diagnostic) qui coûte
   20 minutes et zéro euro.
2. **Les quatre codes CMS non résolus ne sont pas commandables en l'état** — ni chez Mouser,
   ni ailleurs. Il faut d'abord identifier le composant, pas chercher le code dans un catalogue.
3. **Prise jack et fusible ne figurent pas dans le relevé photo.** Les deux lignes du tableau B
   sont des points de départ, pas des références à commander en l'état.
