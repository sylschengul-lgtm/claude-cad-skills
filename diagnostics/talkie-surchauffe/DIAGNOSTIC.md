# Diagnostic — Appareil qui chauffe et se bloque

**Date d'analyse :** 2026-09-03
**Symptôme rapporté :** l'appareil chauffe puis se bloque (figeage / plus de réponse aux commandes).
**Base d'analyse :** 15 photos macro de la carte + 2 relevés au thermomètre infrarouge.
**Atout majeur :** un **exemplaire neuf de référence** est disponible → diagnostic comparatif A/B possible.

> ⚠️ **Avant tout : arrêtez d'utiliser l'appareil et retirez la batterie.**
> 65 °C en surface de coque signifie que le point chaud interne est bien plus élevé
> (typiquement +20 à +40 °C sur le composant fautif, soit 85–105 °C).
> Sur un appareil à batterie Li-ion, un défaut qui dissipe en continu est un risque
> de brûlure et, en cas d'emballement, d'incendie. Ne pas laisser en charge sans surveillance.

---

## 1. Identification du matériel

La carte correspond à un **émetteur-récepteur portatif (talkie-walkie / radio VHF-UHF)** :

- ressort d'antenne soudé en haut de carte,
- afficheur LCD segments avec pictogrammes **CH**, **cadenas (key lock)**, **batterie**, **bargraphe volume**,
- LCD affichant `CH 03` (photo 09).

### Composants identifiés

| Repère photo | Marquage | Fonction probable | Boîtier |
|---|---|---|---|
| 07, 08, 09, 10 | `ti MSP430…30TM FR20xx 8CCH T B` | **MCU principal** Texas Instruments MSP430FR (FRAM) — logique, IHM, gestion clavier | TSSOP-48 |
| 07, 08, 09 | `HOLTEK HT16C21 C029K00D2G2` | **Driver LCD** I²C/SPI (20×4 segments) | SOP-16 |
| 05, 11, 12 | `Linkx eTour-07 2003B` | **SoC RF émetteur-récepteur** (transceiver bande radio) | QFN-32 |
| 04, 06, 12 | `24.04 AK AD` | **TCXO 24,04 MHz** — horloge de référence RF | SMD 4 pads |
| 04, 06, 12 | `724 2G SU` | Régulateur / driver audio (ligne RF) | SOP-8 |
| 07, 10, 13 | `BSG· TI 8A8 A46R` | CI Texas Instruments — **régulateur ou ampli audio** | QFN-16 |
| 06, 07, 12 | `EAMC` | **Résonateur / filtre céramique** (FI ou audio) | SMD 3 broches |
| 01, 14 | `CDV 221 A5L2` | **Convertisseur DC-DC** (contrôleur à découpage) | SOP-8 / QFN-8 |
| 03, 15 | `19AKM` | Convertisseur DC-DC / chargeur | SOT-23-5 |
| 03, 13, 15 | 2 inductances blindées | **2 étages d'alimentation à découpage** (buck et/ou boost) | 4×4 mm |
| 15 | `4R7` (4,7 µH), `18C`, `473` (47 nF) | Passifs de l'étage d'alimentation | 0603 |
| 02, 13 | `YE`, `BR` | Diodes SOT-23 (protection / redressement) | SOT-23 |
| 07, 10 | `3R3` ×2 | Résistances 3,3 Ω — **shunts de mesure de courant** ou filtrage d'alim | 0805 |
| 10, 12 | Trimmer métallique | **Ajustage RF** (capa variable / accord) — ne pas y toucher | — |

**Deux sous-ensembles** apparaissent : une **section logique/RF** (MSP430 + HT16C21 + Linkx + TCXO)
et une **section alimentation/clavier** (2 inductances, 19AKM, CDV 221, boutons tactiles).

---

## 2. Relevés thermiques

Thermomètre IR, émissivité réglée **ε = 0,96**.

| | Appareil **utilisé** (photo 16) | Appareil **neuf** (photo 17) | Écart |
|---|---|---|---|
| Lecture instantanée | ≈ **57 °C** | ≈ **23 °C** | +34 °C |
| MAX mémorisé | ≈ **65,9 °C** | ≈ **29,7 °C** | +36 °C |

### Interprétation

- **Δ ≈ 36 °C** dans des conditions d'usage comparables. Ce n'est pas de la dispersion de
  fabrication : c'est un **courant de fuite ou de court-circuit permanent** quelque part.
- Un talkie en veille consomme typiquement 20–60 mA ; en réception 80–150 mA ; en émission
  0,5–2 A par impulsions. **Un appareil en veille ne doit pas dépasser l'ambiante de plus de
  5–10 °C.** Le neuf à 23–30 °C est cohérent avec l'ambiante ; l'utilisé à 57–66 °C ne l'est pas.
- Ordre de grandeur : pour un boîtier plastique de cette taille, ~36 °C d'élévation correspond
  grossièrement à **1,5 à 3 W dissipés en continu**. Sous 3,7 V, cela représente **0,4 à 0,8 A
  consommés en permanence** — beaucoup trop.

### ⚠️ Limite de la mesure IR

L'émissivité ε = 0,96 est correcte pour **plastique mat, résine époxy verte, composants noirs**.
Elle est **fausse sur les surfaces métalliques brillantes** (blindages, soudures, inductances,
capots) où ε réel ≈ 0,05–0,3 : le thermomètre y sous-estime largement la température.
→ Pour localiser le point chaud sur la carte nue, **coller un morceau de ruban adhésif mat noir**
sur les zones métalliques avant de viser, ou mieux : utiliser une **caméra thermique** ou le
**test au doigt mouillé / alcool isopropylique** (l'alcool s'évapore d'abord sur le point chaud).

---

## 3. Anomalies visibles sur les photos

### 3.1 🔴 CRITIQUE — Point brûlé / carbonisé (photos 05 et 11)

Sur la face LCD, dans la matrice de vias en bordure de carte (à droite du LCD, au-dessus du
Linkx eTour-07), on voit **une zone noire irrégulière carbonisée d'environ 3–4 mm**, centrée sur
un via dont **le cuivre est mis à nu et oxydé (rouge/cuivré)**.

C'est **la découverte la plus importante de l'analyse.** Ce n'est ni du flux, ni une trace de
marqueur, ni de la salissure : la forme, la couleur noire mate et le cuivre exposé au centre du
trou sont la signature d'un **arc électrique ou d'un point de surchauffe localisé** (le vernis
épargne a brûlé).

**Conséquence directe :** un époxy FR-4 carbonisé devient **conducteur** (carbon tracking).
Il crée une résistance parasite de quelques centaines d'ohms à quelques kΩ entre les pistes
voisines. Cela produit exactement le tableau clinique décrit :

- **fuite permanente → dissipation → l'appareil chauffe ;**
- **la fuite s'aggrave avec la température (coefficient négatif du carbone) → emballement lent ;**
- **la tension d'alimentation s'affaisse ou devient bruitée → le MSP430 part en brown-out
  ou son bus I²C/SPI vers le HT16C21 se corrompt → l'appareil se bloque.**

Le fait que le blocage arrive *après* l'échauffement, et non immédiatement, est très cohérent
avec ce mécanisme.

**Cause amont possible de cet arc :**
- infiltration d'humidité / condensation ayant amorcé entre deux vias à potentiels différents,
- inversion de polarité batterie ou pile ponctuelle,
- retour d'énergie RF (antenne mal accordée, émission sans antenne, ou antenne en court-circuit)
  — le point est situé **près du bloc RF (Linkx) et du bord de carte**, zone typique d'un retour
  d'onde stationnaire.

### 3.2 🟠 Contamination / résidus autour des interrupteurs tactiles (photos 01, 02, 13, 14)

Les boutons poussoirs présentent des **dépôts sombres et des fibres** sur et autour des pattes,
en particulier les deux switches du bas (photo 13) et celui de la photo 01. Sur l'appareil neuf
les mêmes zones seraient propres.

**Risque :** un switch encrassé ou collé — surtout **le PTT (Push-To-Talk)** — maintient
l'appareil **en émission permanente**. C'est la cause n°1 de surchauffe sur un talkie-walkie :
l'étage de puissance RF fonctionne en continu au lieu de quelques secondes.

Un PTT collé explique aussi le blocage : la logique reste bloquée dans l'état TX, l'IHM ne répond
plus, et l'appareil ne repasse jamais en veille.

### 3.3 🟡 Résidus de flux non nettoyé (généralisé)

Voile blanchâtre/collant autour de nombreuses soudures. En soi non fatal, mais **hygroscopique** :
il absorbe l'humidité et devient légèrement conducteur — c'est un facilitateur d'amorçage
(cf. §3.1) et de dérive.

### 3.4 🟢 Non-anomalies (à ne pas confondre)

- **Marques vertes/jaunes fluo sur le MSP430** (photos 07–10) : marquage **QC de production** au
  feutre. Normal.
- **Pastilles « QC PASS »** (photos 01, 04, 12, 14) : étiquettes de contrôle qualité usine. Normal.
- **Trimmer métallique** (photos 10, 12) : réglage RF d'usine. **Ne pas y toucher**, un
  déréglage nécessiterait un analyseur de spectre pour être rattrapé.

---

## 4. Hypothèses classées

| # | Hypothèse | Probabilité | Signes à l'appui | Test de confirmation |
|---|---|---|---|---|
| **H1** | **Carbon tracking** au point brûlé → fuite permanente | **Élevée** | Photos 05/11, échauffement continu, blocage différé | §5.3 — mesure de résistance autour du via |
| **H2** | **PTT (ou autre switch) collé** → émission permanente | **Élevée** | Photos 01/13, encrassement, blocage en état TX | §5.4 — continuité des switches au repos |
| **H3** | **Convertisseur DC-DC en défaut** (CDV 221 ou 19AKM) : oscillation, condensateur de sortie HS | Moyenne | 2 inductances = 2 rails ; un rail instable → brown-out MCU | §5.5 — mesure des rails + ondulation |
| **H4** | **Étage RF en défaut** (Linkx / 724) : ROS élevé, antenne HS, PA en avalanche | Moyenne | Point brûlé côté RF et bord de carte | §5.6 — test avec antenne neuve / mesure ROS |
| **H5** | **Batterie dégradée** (résistance interne élevée) : chauffe et s'effondre en charge | Faible-moyenne | Chauffe possible côté batterie, blocage sous appel de courant | §5.2 — test croisé de batteries |
| **H6** | Corrosion / infiltration d'humidité sous un composant | Faible | Résidus, oxydation au via | §5.7 — inspection loupe + nettoyage IPA |

**Scénario le plus probable (combinaison H2 → H1) :** un PTT encrassé ou collé a maintenu
l'appareil en émission prolongée → surchauffe de l'étage RF → arc / point chaud au niveau du via
en bordure de carte → carbonisation → fuite permanente qui, désormais, fait chauffer l'appareil
**même sans émission** et le fait se bloquer par effondrement d'alimentation.

---

## 5. Protocole de diagnostic (ordre à respecter)

Tout se fait **en comparant systématiquement avec l'appareil neuf**. Notez chaque valeur dans le
tableau du §6.

### 5.0 Sécurité

- Batterie retirée pour toute mesure de résistance.
- Ne jamais émettre (PTT) **sans antenne** — c'est ce qui détruit les étages de puissance.
- Travailler avec bracelet antistatique : le MSP430 et le Linkx sont sensibles ESD.

### 5.1 Mesure de courant — LE test décisif ⭐

C'est la mesure qui tranche entre toutes les hypothèses. Multimètre en **série** sur le + batterie
(calibre 10 A d'abord, puis mA).

| État | Attendu (neuf) | À mesurer (utilisé) | Verdict si écart |
|---|---|---|---|
| Éteint | < 1 mA | | > 10 mA → fuite permanente = **H1 confirmée** |
| Allumé, veille | 20–60 mA | | > 200 mA → **H1/H3** |
| Réception (squelch ouvert) | 80–150 mA | | |
| Émission (PTT, avec antenne) | 0,5–2 A | | |

**Si l'appareil consomme plusieurs centaines de mA en veille alors que le neuf en consomme 40 :
la cause est trouvée, c'est une fuite — passez au §5.3.**

### 5.2 Test croisé de batteries (5 min, sans outillage)

Mettez la batterie du neuf dans l'appareil défectueux, et inversement. Laissez 15 min.

- La chauffe **suit la batterie** → **H5**, remplacez la batterie, terminé.
- La chauffe **reste sur l'appareil** → le défaut est sur la carte. Continuez.

### 5.3 Vérification du point brûlé (photos 05/11)

1. **Nettoyage :** alcool isopropylique ≥ 99 %, brosse antistatique souple, puis séchage complet.
2. **Loupe / binoculaire ×10 :** la carbonisation part-elle au nettoyage ou est-elle
   **imprégnée dans l'époxy** ?
3. **Ohmmètre** entre le via carbonisé et chacun des vias voisins (batterie retirée) :
   - attendu : **> 20 MΩ** (ou circuit ouvert selon le schéma),
   - **< 1 MΩ = carbon tracking confirmé → H1.**
   Comparez impérativement avec les mêmes points sur l'appareil neuf.
4. Mesure en **mode diode** également : une jonction parasite se voit parfois mieux.

**Si H1 est confirmée :** il faut **gratter mécaniquement toute la zone carbonisée** (scalpel /
fraise Dremel fine) jusqu'à retrouver de l'époxy vert sain, sous loupe. Le carbone ne se nettoie
pas au solvant, il faut l'enlever. Puis remettre du vernis épargne UV. Si la carbonisation atteint
une piste ou traverse la carte, il faut reconstituer la liaison par fil isolé (wire wrap 30 AWG).

### 5.4 Test des interrupteurs (H2)

Batterie retirée, ohmmètre sur chaque switch, **au repos** :

- attendu : **circuit ouvert (> 1 MΩ)**,
- toute valeur < 100 kΩ au repos = **switch encrassé/collé → H2**.

Insistez sur le **PTT**. Un switch fautif se remplace pour quelques centimes (tact switch
6×6 mm ou 4,5×4,5 mm selon le modèle), ou se nettoie à l'IPA injecté puis actionné 30 fois.

Vérifiez aussi mécaniquement : le bouton du boîtier ne doit pas rester enfoncé par une
déformation du caoutchouc ou un corps étranger.

### 5.5 Mesure des rails d'alimentation (H3)

Batterie en place, appareil allumé, multimètre en tension continue puis oscilloscope si
disponible. Les deux inductances (photos 03, 13, 15) marquent les deux rails à découpage.

| Point de mesure | Attendu | Mesuré | Ondulation max |
|---|---|---|---|
| V batterie | 3,6–4,2 V | | — |
| Sortie inductance 1 | 3,3 V typ. | | < 50 mV crête-crête |
| Sortie inductance 2 | 5 V ou 1,8 V typ. | | < 50 mV crête-crête |
| VCC MSP430 (broche VCC) | 3,3 V stable | | < 30 mV |

Un rail qui **s'effondre au moment du blocage** = cause directe du figeage (brown-out MCU).
Cherchez alors le condensateur de sortie du convertisseur : un **condensateur céramique fissuré**
(chute mécanique) se met en court-circuit partiel → chauffe + rail effondré. Les gros condensateurs
bruns/marron des photos 03, 04, 15 sont les candidats.

### 5.6 Test de la chaîne RF (H4)

1. **Antenne :** mesurez à l'ohmmètre entre l'âme et la masse du ressort d'antenne, comparez
   avec le neuf. Un court-circuit franc ou une antenne cassée fait exploser le ROS.
2. **Test A/B :** montez l'antenne du neuf sur l'appareil défectueux. Si la chauffe diminue
   nettement en émission → antenne fautive, remplacement simple.
3. Si vous disposez d'un **ROS-mètre / wattmètre** adapté à la bande : ROS attendu < 1,5:1.
   Au-delà de 3:1 l'étage de puissance chauffe et se dégrade.
4. **Ne pas retoucher le trimmer** (photos 10, 12) sans analyseur de spectre.

### 5.7 Nettoyage général et inspection finale

- Bain / brossage IPA ≥ 99 % des deux faces, séchage 2 h ou air comprimé.
- Loupe ×10 sur : soudures des inductances, pattes du QFN Linkx et du QFN BSG, bord de carte.
- Recherche de **boules d'étain baladeuses** (courts-circuits mobiles), de pistes vertes-de-gris
  (corrosion), de condensateurs fissurés.

---

## 6. Fiche de relevés à remplir

| Mesure | Neuf (référence) | Utilisé | Écart | Conclusion |
|---|---|---|---|---|
| Courant éteint | | | | |
| Courant veille | | | | |
| Courant réception | | | | |
| Courant émission | | | | |
| Température surface après 15 min veille | ~23–30 °C | 57–66 °C | +36 °C | ⚠️ anormal |
| Point chaud localisé (nom du composant) | — | | | |
| R via carbonisé ↔ vias voisins | | | | |
| R PTT au repos | | | | |
| R autres switches au repos | | | | |
| V batterie en charge | | | | |
| Rail 1 (inductance 1) | | | | |
| Rail 2 (inductance 2) | | | | |
| VCC MSP430 | | | | |
| R antenne (âme/masse) | | | | |

---

## 7. Actions de réparation, par ordre de coût croissant

1. **Nettoyage IPA complet + séchage** — coût nul, résout souvent les fuites par flux humide.
2. **Décarbonisation mécanique de la zone brûlée + revernissage** — le geste clé si H1 confirmée.
3. **Remplacement du/des tact switches** (surtout PTT) — quelques centimes.
4. **Remplacement des condensateurs de sortie des DC-DC** si ondulation hors spec.
5. **Remplacement du convertisseur DC-DC fautif** (CDV 221 / 19AKM) — nécessite air chaud.
6. **Remplacement de l'antenne.**
7. Si le Linkx eTour-07 ou le MSP430 sont en cause : **remplacement de la carte complète**.
   Le MSP430 est programmé en usine (FRAM), il ne se remplace pas sans le firmware.

---

## 8. Ce qu'il faut retenir

1. L'écart thermique de **+36 °C** face à un appareil neuf identique est la preuve objective d'un
   défaut électrique, pas d'un usage intensif.
2. Le **point carbonisé** des photos 05 et 11 est très probablement la cause directe ou la
   conséquence visible du défaut. **C'est là qu'il faut regarder en premier.**
3. La **mesure du courant en veille**, comparée à l'appareil neuf, tranche en 5 minutes entre
   « fuite sur la carte » et « émission permanente ».
4. Le schéma **chauffe d'abord, blocage ensuite** est la signature d'un **brown-out
   thermique** : la fuite s'aggrave avec la température jusqu'à faire décrocher l'alimentation
   du MSP430.

---

## Annexe — Index des photos

| Fichier | Contenu |
|---|---|
| `01_boutons_cdv221_qcpass.jpg` | Switches tactiles, DC-DC `CDV 221 A5L2`, étiquette QC |
| `02_alim_diodes_ye_br_boutons.jpg` | Section alim, diodes `YE`/`BR`, switches |
| `03_alim_19akm_2inductances_qfn.jpg` | `19AKM` SOT-23-5, 2 inductances blindées, QFN |
| `04_rf_724-2gsu_trimmer_tcxo.jpg` | `724 2G SU`, trimmer RF, TCXO 24,04 MHz |
| `05_ANOMALIE_point_brule_via.jpg` | 🔴 **Zone carbonisée en bordure de carte** |
| `06_vue_large_msp430_linkx.jpg` | Vue d'ensemble MCU + RF |
| `07_msp430fr2_ht16c21_bsg_a46r.jpg` | MSP430FR2xx, HT16C21, QFN TI `BSG A46R` |
| `08_msp430_ht16c21_bord_carte.jpg` | MCU + driver LCD, bord de carte |
| `09_lcd_ch03_ht16c21.jpg` | LCD `CH 03`, pictos cadenas/batterie/volume |
| `10_msp430_bsg_trimmer.jpg` | MCU, QFN TI, trimmer RF, résistances `3R3` |
| `11_ANOMALIE_point_brule_zoom_linkx.jpg` | 🔴 **Zoom zone carbonisée** + Linkx eTour-07 |
| `12_linkx_etour07_msp430_724.jpg` | Linkx eTour-07, TCXO, `724 2G SU` |
| `13_face_alim_boutons_inductances.jpg` | Face alimentation complète |
| `14_boutons_cdv221_vue2.jpg` | Switches, `CDV 221 A5L2` |
| `15_alim_zoom_4r7_18c_473_19akm.jpg` | Zoom alim : `4R7`, `18C`, `473`, `19AKM` |
| `16_IR_appareil_UTILISE_57C_max659.jpg` | 🌡️ Relevé IR appareil **utilisé** : 57 °C / max 65,9 °C |
| `17_IR_appareil_NEUF_23C_max297.jpg` | 🌡️ Relevé IR appareil **neuf** : 23 °C / max 29,7 °C |
