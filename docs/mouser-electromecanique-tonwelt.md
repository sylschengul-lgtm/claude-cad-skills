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
| 1 | **Prise jack 3,5 mm**, traversante | Documenté | [`SJ-43514`](https://www.mouser.fr/c/?q=SJ-43514) | Same Sky (CUI Devices) |
| 1b | **Prise jack 3,5 mm**, CMS | Documenté | [`SJ-43514-SMT-TR`](https://www.mouser.fr/c/?q=SJ-43514-SMT-TR) | Same Sky (CUI Devices) |
| 2 | **Fusible réarmable PPTC** 1812 | À confirmer | [série `MF-MSMF`](https://www.mouser.fr/c/?q=MF-MSMF) · [catalogue PPTC](https://www.mouser.fr/c/?q=fusible%20PPTC%201812) | Bourns |
| 3 | **Haut-parleur** Ø15 mm, 8 Ω | À confirmer | [`AS01508MR-6-R`](https://www.mouser.fr/c/?q=AS01508MR-6-R) · [catalogue](https://www.mouser.fr/c/?q=haut-parleur%2015mm%208%20ohm) | PUI Audio |
| 4 | **Micro-USB B**, CMS coudée | Documenté (port de charge) | [`10118193-0001LF`](https://www.mouser.fr/c/?q=10118193-0001LF) · variantes [`…192`](https://www.mouser.fr/c/?q=10118192-0001LF) et [`…194`](https://www.mouser.fr/c/?q=10118194-0001LF) | Amphenol FCI |
| 5 | **Mini-USB B** 5 contacts | À confirmer | [`54819-0519`](https://www.mouser.fr/c/?q=54819-0519) · [catalogue Mini-B CMS](https://www.mouser.fr/c/?q=Mini%20USB%20type%20B) | Molex |
| 6 | **USB-C** 16 contacts, traversante | À confirmer | [`USB4085-GF-A`](https://www.mouser.fr/c/?q=USB4085-GF-A) (version tout-CMS : `USB4216`) | GCT |
| 7 | **Prise d'alimentation, DIN puissance 4 contacts**, coudée, blindée | Identifié sur photo (hors dépôt) | [`KPJX-4S-S`](https://www.mouser.fr/c/?q=KPJX-4S-S) | Kycon |
| 7b | idem, **non blindée** | Variante | [`KPJX-4S`](https://www.mouser.fr/c/?q=KPJX-4S) | Kycon |
| 7c | idem, **montage sur panneau** | Variante | [`KPJX-PM-4S-S`](https://www.mouser.fr/c/?q=KPJX-PM-4S-S) | Kycon |
| 7d | **Fiche mâle** correspondante (réfection du cordon) | Accouplement | [`KPPX-4P`](https://www.mouser.fr/c/?q=KPPX-4P) | Kycon |
| 8 | **Bouton poussoir** CMS (ceux de la carte) | Vu | [`SKRPACE010`](https://www.mouser.fr/c/?q=SKRPACE010) | Alps Alpine |
| 8b | **Bouton poussoir** traversant 6 × 6 mm | À confirmer | [`B3F-1000`](https://www.mouser.fr/c/?q=B3F-1000) · [série B3F](https://www.mouser.fr/c/?q=Omron%20B3F) | Omron |
| 9 | **Antenne UHF** hélicoïdale CMS | Documenté (ressort UHF) | [`ANT-868-VHETH`](https://www.mouser.fr/c/?q=ANT-868-VHETH) | TE / Linx |
| 9b | **Antenne UHF** monopole embarqué Ø7 mm | Documenté | [`ANT-868-JJB-ST`](https://www.mouser.fr/c/?q=ANT-868-JJB-ST) | TE / Linx |
| 9c | **Antenne UHF** planaire CMS | Documenté | [`ANT-868-SP`](https://www.mouser.fr/c/?q=ANT-868-SP) · [toutes les 868 MHz](https://www.mouser.fr/c/?q=antenne%20868%20MHz) | TE / Linx |
| 10 | **Condensateurs** MLCC 0603 / 0805 / 1206 | Vu (`473` = 47 nF, MLCC de sortie boost) | [catalogue MLCC](https://www.mouser.fr/c/?q=MLCC%200805) · [kits](https://www.mouser.fr/c/?q=capacitor%20kit) | Murata, Yageo, KEMET |
| 11 | **Résistances** 0603 / 0805 | Vu (`3R3` = 3,3 Ω en 0805) | [catalogue CMS](https://www.mouser.fr/c/?q=RC0805) · [kits](https://www.mouser.fr/c/?q=resistor%20kit%200805) | Yageo RC0805, Vishay CRCW0805 |

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
| 7 | **Diamètre extérieur de la bague métallique en façade** : ~12,9 mm et corps ~15 × 17 mm = série KPJX. ~9,5 mm = mini-DIN 4 broches, famille différente (et limitée à ~1 A, donc improbable ici). Puis compter les trous côté cuivre : 4 contacts + 2 ergots + la languette de masse = version **blindée**. | Ces deux relevés tranchent entre KPJX-4S-S et KPJX-4S |
| 8 | Hauteur de l'actionneur et force de contact | Confort d'appui à l'identique |
| 9 | **La bande exacte** — le TG-288 est UHF, mais 863-865 MHz (Europe) et 902-928 MHz (US) ne prennent pas la même antenne. Lire l'étiquette de l'appareil. | Une antenne hors bande dégrade fortement la portée |
| 10-11 | Valeur, tolérance, tension de service, boîtier | — |

---

## Poste 7 — la prise d'alimentation

Identifiée à partir de photos analysées **hors de ce dépôt** (trois clichés
`1000011752/53/54.jpg`, non versionnés ici) : embase circulaire de puissance à
**4 contacts femelles**, type DIN puissance, à souder, sortie coudée. Les cinq pattes
observées = les 4 contacts de puissance en carré + **1 languette de masse / blindage**
au bord de carte ; les deux petits trous non soudés sont les ergots de centrage.
Série **Kycon KPJX**, 7,5 A par contact sous 48 V continu.

Le bloc secteur associé est donné pour **5 V / 10 A / 50 W**, avec deux contacts au
même potentiel par polarité pour passer les 10 A.

⚠️ **Deux points que je n'ai pas vérifiés moi-même** (les photos n'ont pas été partagées
dans cette session, et prix et stocks bougent) :
- la référence exacte dépend des deux mesures du tableau ci-dessus ;
- Mouser distribue bien les quatre variantes ci-dessus — les prix et disponibilités
  sont à lire sur les pages produit, pas à reprendre d'un relevé daté.

> 💡 **Un rapprochement à faire.** 5 V / 10 A, c'est une alimentation de **valise de
> charge multi-emplacements**, pas d'un audioguide (qui se charge en micro-USB sur
> 2 × AA Ni-MH). Or le diagnostic de surchauffe désigne précisément la valise de charge
> comme suspect à tester (§9, point 4 : une valise qui surcharge abîme les appareils un
> par un). Si cette prise est celle de la valise, les deux sujets n'en font qu'un.

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
