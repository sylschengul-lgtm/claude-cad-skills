# Batteries lithium du parc, releve sur photos

Derniere mise a jour : 2026-09-19. Cinq cellules relevees, dont quatre avec un
marquage entierement lisible. Ce releve remplace definitivement l'hypothese
« 2 x AA Ni-MH » qui venait de la fiche produit Linkx du TG-288.

## Les cellules relevees

Le code a six chiffres des cellules LiPo se lit TTWWLL : epaisseur en dixiemes de
millimetre, largeur en millimetres, longueur en millimetres. Convention tres repandue
mais non normalisee, a recouper avec une mesure au pied a coulisse.

| Marquage | Tension | Capacite | Energie | Dimensions decodees | Date | Protection |
|---|---|---|---|---|---|---|
| `GM 303556` | 3,7 V | 650 mAh | n/a | 3,0 x 35 x 56 mm | 2024-03-22 | Oui, visible |
| `JHY632570` | 3,7 V | 1300 mAh | 4,81 Wh | 6,3 x 25 x 70 mm | 2023-01-03, pose 2023/07 | Oui |
| `SL5022243`, lot 01536 | 3,7 V | 450 mAh | n/a | Code non decodable avec certitude | n/a | A verifier |
| `LIDIO 355485` | **3,8 V** | 2500 mAh | 9,5 Wh | 3,5 x 54 x 85 mm | 2020-10 | Oui |
| Sans reference, carte Eco 2.0 | **3,87 V** | 1000 mAh | n/a | A mesurer | n/a | Oui |

Toutes sortent sur un **connecteur JST 2 points**, fil rouge et noir, avec un circuit
de protection sous le kapton jaune.

Note : un second exemplaire de la `JHY632570` avait ete photographie le 12/09, fabrique
le 2024-07-27 et pose en 2024/12. Le parc comporte donc **plusieurs lots de fabrication**
d'une meme reference, ce qui est normal mais complique le suivi.

## Le point critique : deux chimies dans le meme parc

| Type | Tension nominale | Tension de charge | Cellules concernees |
|---|---|---|---|
| LiPo standard | 3,7 V | **4,20 V** | `GM 303556`, `JHY632570`, `SL5022243` |
| LiPo haute tension | 3,8 a 3,87 V | **4,35 V** | `LIDIO 355485`, cellule de la carte Eco 2.0 |

Trois cellules sur cinq sont en 3,7 V, deux en haute tension. Ce n'est pas un detail de
catalogue, c'est un mecanisme de panne :

- **Une cellule 3,7 V dans un appareil dont le chargeur vise 4,35 V est en surcharge
  permanente.** Elle chauffe, gonfle, vieillit vite, et le circuit de protection finit
  par couper. C'est le scenario « mauvaise pile mise en charge » transpose au lithium,
  ou les consequences sont plus graves.
- **Une cellule 3,8 V dans un chargeur 4,20 V** ne se remplit qu'a 80 % environ :
  autonomie en baisse, sans danger.

A verifier en priorite sur les appareils qui chauffent : la tension nominale inscrite sur
la cellule correspond-elle a celle d'origine ? Second signe a chercher : une cellule
gonflee, visible et palpable, qui impose le remplacement immediat sans autre diagnostic.

## Approvisionnement

Aucune de ces cellules n'est distribuee par un distributeur generaliste. `JHY`, `LIDIO`
et `GM` sont des fabricants de cellules poche chinois qui vendent au fabricant
d'equipement.

### La methode qui marche : chercher par code de taille

Les fabricants de cellules poche indexent leur catalogue par le code a six chiffres.
C'est donc ce code, et non un nom de marque, qu'il faut coller dans un moteur de
recherche ou sur le site d'un fabricant.

| Source | Ce qu'elle apporte |
|---|---|
| EEMB, boutique en ligne et Amazon | Nomme ses cellules `LP` + code de taille (exemple reel : `LP553450`, 3,7 V 650 mAh). Livrees avec connecteur JST et circuit de protection. Vendu au detail en Europe |
| DNK Power, lipolbattery, PKCELL | Fabricants chinois dont les catalogues sont indexes par code de taille. Devis direct |
| Jauch Quartz, via DigiKey | Le seul equivalent proprement industriel, meme convention de code (`LP` + TTWWLL), avec circuit de protection et fils. Limite au 3,7 V |
| TYVA Energie, France | Fabrication sur mesure, pour les formats ou les tensions introuvables |
| Mouser | Packs LiPo 3,7 V generiques, sans recherche par code de taille |

### Conclusion sur les cellules haute tension

Ni Mouser, ni Jauch, ni le catalogue standard EEMB ne proposent de cellules a 3,8 ou
3,87 V. **Les deux cellules haute tension du parc restent donc a commander en OEM ou en
fabrication sur mesure.** Seules les trois cellules 3,7 V ont un equivalent catalogue
realiste.

### Les cinq criteres d'un equivalent, aucun n'est facultatif

1. **Dimensions** mesurees au pied a coulisse, pas seulement decodees du code.
2. **Capacite** en mAh.
3. **Tension nominale.** 3,7 V et 3,8 V ne sont pas interchangeables.
4. **Circuit de protection** integre.
5. **Connecteur et polarite.** La polarite des JST sur cellules chinoises n'est pas
   normalisee : verifier au voltmetre avant de brancher, sous peine de detruire la carte.

Securite : une poche lithium gonflee ou en surchauffe est un risque d'incendie. Ne pas la
percer, ne pas la plier, ne pas continuer a la charger, ne pas la laisser en valise. La
sortir de l'appareil, la placer dans un contenant ininflammable, la faire reprendre en
dechet.

## Ce que ces photos apprennent aussi

Le parc comporte au moins trois cartes differentes : `TG-288 / eTour` (carte du diagnostic
de surchauffe), `TG-108_RX R.0.2`, et `Eco 2.0`. Une nomenclature ne se transpose pas d'un
appareil a l'autre.
