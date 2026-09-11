# Nomenclature (BOM) — composants identifiés sur les plaques et où les acheter

**Projet** : pousse-seringue *Antigravity* (dépôt `claude-cad-skills`)
**Base d'analyse** : uniquement les 4 fichiers CAO présents dans `examples/` —
`carriage_brass_nut.dxf/.step`, `carriage_brass_nut_a.dxf/.step`,
`frame_250108.dxf/.step`, `face_x72_right_outer.step`.
**Méthode** : extraction automatique des cercles DXF et des `CYLINDRICAL_SURFACE`
STEP (diamètre + position + axe), puis rapprochement avec les standards
mécaniques du commerce.
**Date** : 2026-09-11

> ⚠️ Il n'y a **aucune carte électronique** dans ce dépôt. « Les cartes » sont ici
> les deux **plaques/tôles** mécaniques : le chariot (*carriage*, alu 6,35 mm =
> 1/4") et le châssis plié (*frame*, tôle 3,175 mm = 1/8"). La liste ci-dessous
> est déduite de la géométrie — elle n'est pas une nomenclature officielle du
> projet. Les niveaux de confiance sont indiqués.

---

## 1. Géométrie relevée (faits mesurés)

### 1.1 Chariot — `carriage_brass_nut(.a)` — 78,2 × 76,1 × **6,35 mm** (plaque 1/4")

| Perçage | Qté | Position (x, y) mm | Lecture |
|---|---|---|---|
| Ø10,5 central + 4 × Ø3,5 sur cercle Ø16 | 1 + 4 | centre (−7,56 ; 27,18) | Bride d'écrou T8 standard |
| idem, mais 4 × Ø2,4 (taraudage M3) | 4 | même centre | variante `_a` (montage vissé M3) |
| Ø15,1 | 2 | (−37,56 ; 27,17) et (22,44 ; 27,18) — **entraxe 60 mm** | Douilles linéaires LM8UU (Ø ext. 15) |
| Ø32 (lamage) | 2 | mêmes centres que Ø15,1 | logement/appui des douilles |
| Ø6 | 8 | dont (−23,06 ; 11,67/42,67) et (7,94 ; 11,67/42,67) | passage de **têtes de vis M3 CHC** (Ø tête 5,5) |
| Ø3,2 + lamage Ø10 | 2 | (−26,56 ; 63,22) et (11,44 ; 63,23) — entraxe 38 mm | fixation M3 de la bride de seringue |
| Ø2,4 (taraudage M3) | 8 | pourtour | fixations M3 |
| Poches Ø20 / Ø24 / Ø31 / Ø37 | 2/2/1/1 | axe seringue y≈63,2 et y≈23,2 | dégagements corps de seringue |

### 1.2 Châssis — `frame_250108` — 143,7 × 88,2 × 76 mm, tôle **3,175 mm** (1/8"), développé 317,9 × 96,1 mm

| Perçage | Qté | Position | Lecture |
|---|---|---|---|
| Ø22,5 + 4 × Ø3,2 en carré **31 × 31 mm** | 1 + 4 | centre (−7,56 ; 27,18), flanc | **Interface moteur NEMA 17** (pilote Ø22, vis M3) |
| Ø14 + lamage Ø26,1 | 1 | même axe, flanc opposé | Palier d'extrémité de la vis (le README parle du **KFL08**) |
| Taraudages M3 (Ø2,4) | 2 + 2 | à ±14 mm **et** ±20 mm de l'axe | **deux entraxes de fixation** du palier (2 options de montage) |
| Ø12,45 + lamage Ø18 | 2 | (−37,56 ; 27,17) et (22,44 ; 27,17) — entraxe 60 mm | Appuis d'extrémité des axes de guidage (bague à collerette) |
| Ø7,8 | 2 | z = 63,23, entraxe 57 mm | Emmanchement d'**axe rectifié Ø8** (guidage haut) |
| Ø30,1 | 1 | axe seringue (−7,56 ; 63,23) | Passage du corps de seringue |
| Ø5 | 2 | z = 64,63, entraxe 35,1 mm | Passage vis M5 |
| Ø6,35 (1/4") + lamage Ø12,7 (1/2") | 4 | base, axes X et Y | Vis **1/4"-20 CHC chambrées** (fixation sur embase) |
| Ø3,175 (1/8") | 6 | base, trame 25 / 45 mm | Fixation embase (vis #6-32 ou pions 1/8") |
| Ø2 (M2) | 12 | flancs, paires à 8 mm (trous oblongs) | Capteurs / butées de fin de course |
| Ø2 (M2) en carré 5 × 5 mm | 2 × 4 | base, gauche et droite | Petit support / PCB / capteur |
| Ø12 sur axes inclinés à ~38° | 4 | 4 coins | Entretoises ou pieds inclinés |

---

## 2. Composants du commerce à acheter

### 2.1 Confiance élevée — le motif de perçage correspond exactement au standard

| # | Composant | Spécification déduite | Qté | Preuve géométrique |
|---|---|---|---|---|
| 1 | **Moteur pas à pas NEMA 17** | 42 mm, pilote Ø22, 4 × M3 à 31 × 31 mm, arbre Ø5 | 1 | Ø22,5 + carré 31,00 × 30,99 mm sur le flanc |
| 2 | **Vis trapézoïdale T8** (Tr8, Ø8) | longueur utile ≥ 150 mm ; pas selon débit visé (T8×2 = 2 mm/tour recommandé pour la précision) | 1 | Ø10,5 central + Ø14 au palier |
| 3 | **Écrou laiton à bride T8** | bride Ø22, 4 trous M3 sur cercle **Ø16**, moyeu Ø10, H 15 mm | 1 | 4 × Ø3,5 à r = 8,00 mm + Ø10,5 |
| 4 | **Douilles linéaires LM8UU** | 8 × 15 × 24 mm | 2 | Ø15,1 × 2, entraxe 60 mm |
| 5 | **Axes rectifiés Ø8 mm** (acier chromé ou inox) | Ø8 h6, L ≈ 150–170 mm (guidage bas) + 2 × L ≈ 145 mm (guidage haut, Ø7,8 = emmanché) | 2 à 4 | Ø15,1 chariot / Ø7,8 châssis |
| 6 | **Accouplement flexible 5 × 8 mm** | moteur Ø5 → vis Ø8 | 1 | implicite (moteur Ø5 + vis T8 coaxiaux) |
| 7 | **Visserie M3 CHC inox** | M3×0,5, longueurs 8 à 20 mm ; tête Ø5,5 | ~30 | Ø3,2 (passage), Ø2,4 (taraudage), Ø6 (passage de tête) |

### 2.2 Confiance moyenne — à confirmer sur la pièce réelle avant commande

| # | Composant | Spécification déduite | Qté | Réserve |
|---|---|---|---|---|
| 8 | **Palier à bride KFL08** (alésage 8 mm) | logement Ø26,1 + passage Ø14 | 1 | Le KFL08 du commerce a un **entraxe de fixation ~36 mm en Ø5 (M4/M5)** ; la tôle offre du **M3 à 28 et 40 mm**. Vérifier la référence exacte, ou prévoir un roulement 608/688 + bride imprimée. |
| 9 | **Bagues à collerette Ø8/Ø12, collerette Ø18** (type igus JFM-0812 ou bronze fritté) | logement Ø12,45 + lamage Ø18 | 2 | Le logement Ø12,45 est **large de 0,45 mm** pour une bague Ø12 : soit la bague est collée/clipsée, soit la pièce réelle est un autre support d'axe. À mesurer. |
| 10 | **Vis 1/4"-20 CHC** + rondelles | passage 1/4" (6,35), lamage 1/2" (12,7) | 4 | Fixation sur embase/table optique — confirmer la longueur. |
| 11 | **Vis #6-32 ou pions Ø1/8"** | Ø3,175 | 6 | Passage 1/8" : peut être vis **ou** pion de positionnement. |
| 12 | **Micro-interrupteur / butée de fin de course** + visserie M2 | trous Ø2 oblongs, paires à 8 mm | 1 à 2 | Fonction déduite de la position (course du chariot), pas du modèle. |
| 13 | **Vis M5** | Ø5, entraxe 35,1 mm | 2 | Fonction non déterminée (bride ? poignée ?). |
| 14 | **Seringue Luer** | corps Ø ≈ 26–30 mm → **50/60 mL** typiquement | 1 | Déduit de Ø30,1 (châssis) et Ø31 (chariot). |

### 2.3 Matière première (les « cartes » elles-mêmes)

| # | Pièce | Matière | Format |
|---|---|---|---|
| 15 | Chariot | Alu 6061-T6 **6,35 mm (1/4")** | découpe 78 × 77 mm + perçages/taraudages |
| 16 | Châssis | Tôle alu/acier **3,175 mm (1/8")** | développé **317,9 × 96,1 mm**, 5 pliages |

---

## 3. Où acheter

### 3.1 Europe / France

| Composant | Fournisseurs | Prix indicatif |
|---|---|---|
| NEMA 17 | [StepperOnline](https://www.omc-stepperonline.com/), [RS France](https://fr.rs-online.com/), [Gotronic](https://www.gotronic.com/), [Makershop](https://www.makershop.fr/) | 12–25 € |
| Vis T8 + écrou laiton bride | [Grossiste3D](https://www.grossiste3d.com/coupleurs-vis-trapezoidale/1879-ecrou-en-laiton-pour-vis-mere-t8-pas-2mm-avance-8mm.html), [Euro-Makers](https://euro-makers.com/fr/tiges-filetees-axes/), [Motedis](https://www.motedis.com/) | 8–20 € |
| LM8UU | [Motedis](https://www.motedis.com/), [Misumi Europe](https://uk.misumi-ec.com/), [TME](https://www.tme.eu/) | 2–5 €/pce |
| Axes rectifiés Ø8 h6 | [Misumi (réf. SFJ8/PSFJ8, coupe à la longueur)](https://uk.misumi-ec.com/), [Motedis](https://www.motedis.com/), [igus drylin](https://www.igus.fr/) | 6–15 €/axe |
| Palier KFL08 | [Motedis](https://www.motedis.com/en/Flange-Bearing-8mm-die-cast-KFL08), [Mädler](https://www.maedler.de/), [Maker Store UK](https://makerstore.co.uk/products/kfl08-pillow-block-flange-bearing) | 4–9 € |
| Bagues à collerette JFM-0812 | [igus](https://www.igus.fr/iglidur-ibh/flanged-bearings), [TME](https://www.tme.eu/en/details/jfm-0812-12/plain-bearings/igus/), [Misumi](https://uk.misumi-ec.com/vona2/detail/221000103515/) | 1–4 €/pce |
| Accouplement 5×8 | Gotronic, Makershop, Motedis, AliExpress | 4–8 € |
| Visserie M2/M3/M5 inox | [Accu](https://www.accu.co.uk/), [Bossard](https://www.bossard.com/), [Otelo](https://www.otelo.fr/), [Würth](https://www.wurth.fr/) | 10–30 € le lot |
| Micro-switch (Omron D2F / SS-5GL) | [RS](https://fr.rs-online.com/), [Farnell](https://fr.farnell.com/), [TME](https://www.tme.eu/) | 1–4 €/pce |
| Découpe des 2 plaques (laser/jet d'eau + pliage) | [Weerg](https://www.weerg.com/), [Xometry Europe](https://xometry.eu/), [Protolabs](https://www.protolabs.fr/), [John Steel](https://www.johnsteel.fr/) | 40–150 € le jeu |
| Seringue 50/60 mL Luer | VWR, Fisher Scientific, Dutscher, pharmacie | 0,5–2 €/pce |

### 3.2 États-Unis (source d'origine du projet)

| Composant | Fournisseurs |
|---|---|
| Visserie (M2/M3/M5, 1/4"-20, #6-32), pions 1/8" | [McMaster-Carr](https://www.mcmaster.com/) — la référence pour le mélange métrique/impérial de ce projet |
| Alu 1/4" et 1/8" | [OnlineMetals](https://www.onlinemetals.com/), McMaster |
| Découpe tôle + pliage | [SendCutSend](https://sendcutsend.com/), [OSHCut](https://oshcut.com/), [Xometry](https://www.xometry.com/) |
| LM8UU / T8 / NEMA 17 | [Adafruit](https://www.adafruit.com/product/1181), [ZYLtech](https://www.zyltech.com/), [VXB](https://vxb.com/), [RobotDigg](https://www.robotdigg.com/) |
| KFL08 | [VXB](https://vxb.com/products/8mm-flange-kfl08-bearing-miniature-pillow-block-mounted-bearings), [Maker Store USA](https://makerstore.cc/product/kfl08-pillow-block-flange-bearing/) |

---

## 4. À vérifier avant de commander

1. **Palier de vis (KFL08)** — entraxe M3 28/40 mm relevé dans la CAO vs. ~36 mm / Ø5 du KFL08 standard. Mesurer le palier réel ou adapter la tôle.
2. **Logements Ø12,45 + Ø18** — identifier la bague réellement montée (jeu de 0,45 mm sur un Ø12 nominal).
3. **Pas de la vis T8** — non déductible de la CAO (T8×2, ×4 ou ×8). Le pas fixe la résolution en volume : prendre **T8×2** pour un pousse-seringue.
4. **Longueur des axes Ø8 et de la vis** — dépend de la course utile, à prendre sur l'assemblage complet (absent du dépôt).
5. **Trous Ø2 (M2)** — confirmer s'il s'agit de butées de fin de course ou d'un support de capteur.
6. Cette analyse ne couvre **que** les fichiers d'exemple du dépôt. Les fichiers de référence du projet sont annoncés dans les skills sous
   `/Users/chinnadevarapu/Documents/Antigravity/CAD/` — les analyser donnerait une nomenclature complète (électronique de commande incluse, absente ici).

---

## 5. Reproduire l'analyse

Le script [`tools/extract_holes.py`](../tools/extract_holes.py) (sans dépendance,
Python 3 seul) régénère l'inventaire des perçages utilisé ci-dessus :

```bash
python3 tools/extract_holes.py examples/frame_250108.step
python3 tools/extract_holes.py examples/carriage_brass_nut.dxf
```

Il lit les entités `CIRCLE` du DXF et les `CYLINDRICAL_SURFACE` du STEP
(diamètre, position, direction d'axe), et fusionne les surfaces dédoublées.
Note : les entrées **Ø70** du châssis ne sont pas des trous mais les **congés
R35** du contour ; de même Ø12 sur axes inclinés = bossages de coin.

Le skill [`/annotate-step`](../skills/annotate-step/SKILL.md) produit la même
information sous forme de PDF annoté par face, avec classification des trous
par diamètre (M2 → M6).
