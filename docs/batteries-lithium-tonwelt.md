# Batteries lithium du parc - relevé sur photos

**Date du relevé :** 2026-09-12, d'après quatre photos fournies en session.
Elles remplacent définitivement l'hypothèse « 2 × AA Ni-MH » qui venait de la fiche
produit du TG-288.

## Les cellules relevées

Le code à six chiffres des cellules LiPo se lit **TTWWLL** : épaisseur en dixièmes de
millimètre, largeur en millimètres, longueur en millimètres. Convention très répandue
mais non normalisée - à recouper avec une mesure au pied à coulisse.

| # | Marquage | Tension nom. | Capacité | Énergie | Dimensions décodées | Où |
|---|---|---|---|---|---|---|
| 1 | `JHY632570` | **3,7 V** | 1300 mAh | 4,81 Wh | 6,3 × 25 × 70 mm | Carte verte à ressort d'antenne + micro-USB. Cellule fabriquée le 2024.07.27, étiquette de pose « 2024/12 » |
| 2 | *aucune référence visible* | **3,87 V** | 1000 mAh | - | - | Carte **« Eco 2.0 »**, connecteur **USB-C**, nappe FPC - appareil différent des deux précédents |
| 3 | *illisible sur la photo* | 3,8 V (à confirmer) | - | - | - | Cellule dans un boîtier noir, marquage CE |
| 4 | `LIDIO 355485` | **3,8 V** | 2500 mAh | 9,5 Wh | 3,5 × 54 × 85 mm | Lot `202010 01892` |

Toutes portent un **circuit de protection intégré** sous le kapton jaune et sortent sur un
**connecteur JST 2 points**, fil rouge et noir.

---

## Attention : Le point important : deux chimies différentes dans le même parc

| Type | Tension nominale | Tension de charge | Cellules concernées |
|---|---|---|---|
| LiPo standard | 3,7 V | **4,20 V** | n° 1 |
| LiPo haute tension (LiHV) | 3,8 - 3,87 V | **4,35 V** | n° 2, 4, probablement 3 |

Ce n'est pas un détail de catalogue, c'est un mécanisme de panne :

- **Une cellule 3,7 V dans un appareil dont le chargeur vise 4,35 V est en surcharge
  permanente.** Elle chauffe, gonfle, vieillit vite, et le circuit de protection finit par
  couper. C'est exactement le scénario « mauvaise pile mise en charge » qui était
  l'hypothèse n° 1 du diagnostic Ni-MH - transposé au lithium, où les conséquences sont
  plus graves.
- **Une cellule 3,8 V dans un chargeur 4,20 V** ne se remplit qu'à ~80 % : autonomie en
  baisse, sans danger.

**À vérifier en priorité sur les appareils qui chauffent : la tension nominale inscrite
sur la cellule correspond-elle à celle d'origine ?** Un lot de rechange acheté sans
regarder ce chiffre suffit à expliquer la panne.

Second signe à chercher : **une cellule gonflée**. Sur une poche lithium c'est visible et
palpable, et cela impose le remplacement immédiat - pas de diagnostic supplémentaire.

---

## Approvisionnement

**Ni JHY ni LIDIO ne sont distribués par Mouser** - ce sont des fabricants de cellules
poche chinois, vendus au fabricant d'équipement, pas au détail par un distributeur
généraliste.

Deux voies réalistes :

1. **Le SAV Tonwelt / Linkx** - la seule qui garantit la bonne tension, le bon connecteur
   et la bonne polarité.
2. **Une cellule équivalente**, à condition de respecter **cinq critères, sans exception** :
   - épaisseur × largeur × longueur (mesurées, pas seulement décodées du code) ;
   - capacité en mAh ;
   - **tension nominale - 3,7 V et 3,8 V ne sont pas interchangeables** ;
   - circuit de protection intégré ;
   - connecteur et **polarité**. La polarité des connecteurs JST sur cellules chinoises
     n'est pas normalisée : à vérifier au voltmètre avant de brancher, sous peine de
     détruire la carte.

Recherche Mouser par gabarit, à titre indicatif seulement :
`https://www.mouser.fr/c/?q=3.7V+Lipo+Battery`

---

## Ce que ces photos apprennent aussi

Le parc comporte **au moins trois cartes différentes**, et non une :

- `TG-288 / eTour` - la carte du diagnostic de surchauffe ;
- `TG-108_RX R.0.2` - micro-USB et jack 3,5 mm ;
- **`Eco 2.0`** - USB-C, nappe FPC, cellule 3,87 V, portant la mention `(c) Felix Bäsecke`.

Une nomenclature ne se transpose donc pas d'un appareil à l'autre. C'est la raison de
fond pour laquelle la première liste ne correspondait pas.
