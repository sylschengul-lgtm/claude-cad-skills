# Règles de travail sur ce dépôt

## Langue
Répondre en français.

## Liens distributeurs (Mouser, RS, Farnell…) - règle née d'un échec
**Ne jamais fabriquer une URL `ProductDetail` à la main.** Chez Mouser, une adresse
du type `mouser.fr/ProductDetail/<Fabricant>/<Référence>` **renvoie une page 404** :
la fiche produit exige un jeton `?qs=…` qui ne se devine pas.

À faire systématiquement, pour chaque ligne d'une liste d'achat :

1. **Coller l'URL produit exactement telle que la recherche l'a renvoyée**, jeton `?qs=` compris.
   Ne jamais la « nettoyer », ne jamais en retirer la partie après le `?`.
2. **Ajouter en plus une URL de recherche par référence**, qui ne dépend d'aucun jeton :
   `https://www.mouser.fr/c/?q=<RÉFÉRENCE>`. C'est le lien de secours si le premier ne répond pas.
3. **La seule forme de lien à utiliser est `https://www.mouser.fr/c/?q=<RÉFÉRENCE>`.**
   Confirmée fonctionnelle par l'utilisateur le 12/09/2026. Elle ne dépend d'aucun jeton
   et ne subit aucune redirection. Ne plus livrer d'URL `ProductDetail` du tout.
4. **Un renvoi `mouser.com` vers `mouser.fr` perd la chaîne de requête.** Constaté :
   `mouser.com/ProductDetail/Kycon/KPJX-PM-4S-S?qs=…` arrive sur
   `mouser.fr/fr/ProductDetail/Kycon/KPJX-PM-4S-S` **sans le jeton**, donc en 404.
   Donner directement des URL `www.mouser.fr` plutôt que `www.mouser.com`.
5. **La référence fabricant est l'identifiant durable, pas l'URL.** Elle doit figurer en
   clair dans toute liste : collée dans le champ de recherche du distributeur, elle
   fonctionne quand tous les liens ont changé.
6. **Tester les liens avant de livrer** quand le réseau le permet. Vérifié le 2026-09-12 :
   `www.mouser.fr` **et** `www.mouser.com` renvoient un **403 sur le tunnel CONNECT** du
   proxy d'egress - refus de politique de l'organisation, à signaler sans le contourner.
   Donc dans cet environnement, **aucun lien Mouser n'est vérifiable** : le dire au lieu
   d'affirmer que les liens fonctionnent.

## Typographie des livrables - un livrable reste un document

- **Aucun cadratin ni demi-cadratin** (les caractères `-` et `-`) dans un fichier livré :
  ni dans un classeur Excel, ni dans un document, ni dans un script. Utiliser un
  **tiret simple**, un deux-points, une virgule ou des parenthèses selon le sens.
- **Aucun symbole décoratif** (pictogrammes, émojis) dans un fichier livré. Écrire
  « Attention : », « Sécurité : » en toutes lettres.
- Une cellule sans valeur porte `n/a`, jamais un tiret décoratif.
- Ces règles valent pour les **fichiers produits**. Elles ne s'appliquent pas aux réponses
  dans la conversation.

## Fichiers Excel
- **Pas de formule si elle n'est pas indispensable.** Le recalcul LibreOffice ne
  fonctionne pas dans cet environnement (dépassement de délai au-delà de 9 minutes),
  et une formule non recalculée s'affiche **vide** dans la plupart des visionneuses.
  Une colonne `=HYPERLINK(...)` a déjà été supprimée pour cette raison.
- **Liens dans un classeur** : hyperlien natif sur la cellule **et** URL lisible en
  texte dans la cellule, pour rester copiable-collable partout.
- Police Arial, en-tête figé, filtre automatique, colonnes à remplir sur fond jaune
  avec une légende qui les nomme.
- Le classeur doit être **régénérable par script** (`tools/build_*.py`), jamais édité
  à la main, pour pouvoir être reconstruit quand une ligne se ferme.

## Nomenclatures et listes d'achat
- **Chaque ligne porte son statut de source** : `Vu` (constaté sur photo ou sur le
  fichier), `Documenté` (attesté par une fiche constructeur), `Photo ext.` (identifié
  hors dépôt, non vérifié ici), `À confirmer` (point de départ catalogue).
- **Ne jamais inventer une référence.** Si un code CMS n'est pas résolu, l'écrire :
  un composant non identifié ne se commande pas.
- **Ne pas recopier prix ni stocks** : ils changent. Renvoyer à la page produit.
- Indiquer, pour chaque ligne ouverte, **la mesure qui la referme** (diamètre, nombre
  de contacts, impédance, bande de fréquence…).

## Le parc - sept produits Tonwelt, deux familles

Réponse de l'utilisateur le 14/09/2026. **Le parc n'est pas un modèle mais une gamme**,
répartie sur deux familles techniquement très différentes :

| Famille | Produits du parc | Nature |
|---|---|---|
| **tourGuide** | `tourguide air`, `tourguide go`, `tourguide play` | Guidage de groupe par radio : émetteur + récepteurs, canaux, antenne, écran à segments |
| **supraGuide** | `supraguide`, `supraguide eco`, `supraguide 2`, `supraguide touch` | Audioguides individuels : contenu embarqué, écran (tactile sur le TOUCH) |

**Une liste d'achat unique ne peut pas couvrir les deux familles.** Il faut une
nomenclature par produit.

### Rapprochement avec les cartes observées - hypothèses, pas certitudes

| Carte vue | Produit probable | Solidité |
|---|---|---|
| `Eco 2.0` - USB-C, nappe FPC, cellule 3,87 V 1000 mAh, `(c) Felix Bäsecke` | **supraGuide ECO** | **Forte** : la carte porte le nom |
| Carte à ressort d'antenne + micro-USB, cellule `JHY632570` 3,7 V 1300 mAh | un **tourGuide** (radio) | Moyenne : l'antenne impose la famille, pas le modèle |
| `TG-108_RX R.0.2` - micro-USB, jack 3,5 mm, MCU QFP | un **tourGuide**, version récepteur (`_RX`) | Moyenne |
| `TG-288 / eTour` - LCD à segments (CH, cadenas, pile, volume), SoC `Linkx eTour-07` | un **tourGuide** d'ancienne génération | Moyenne. Attention : La mention « 2 × AA Ni-MH » vient de la fiche **Linkx**, pas de l'appareil Tonwelt : à ne pas tenir pour acquise |

`TG-288` et `TG-108` sont des références **Linkx**, le fabricant d'origine ; Tonwelt les
revend sous ses propres noms. Ne pas présenter une référence Linkx comme le nom du produit.

**Le seul élément qui tranche est l'étiquette de l'appareil**, pas la carte.

Attention : **`tonwelt.com` est bloqué par le proxy d'egress** : les fiches techniques produit ne
sont pas consultables depuis cet environnement. Les demander à l'utilisateur en PDF.

### Panne de surchauffe - périmètre
**Elle ne concerne que le `tourguide air`** (établi le 14/09/2026), pas les sept produits.
L'appareil du diagnostic `diagnostics/talkie-surchauffe/` **est** ce tourGuide AIR.
Attention : Contradiction non levée : sa carte porte un convertisseur **élévateur** (donc source
sous 3,3 V, typiquement 2 × AA Ni-MH) alors que les batteries du parc sont au lithium.
Voir `docs/surchauffe-tourguide-air.md` - la vérification qui tranche est d'ouvrir un AIR
qui chauffe et de regarder ce qui l'alimente.

### Corrections apportées par l'utilisateur - priment sur toute déduction
- **Les batteries du parc sont des cellules lithium plates**, pas des accus AA Ni-MH.
  Relevées sur photo le 12/09/2026 : `JHY632570` 3,7 V 1300 mAh, une cellule 3,87 V
  1000 mAh sans référence, `LIDIO 355485` 3,8 V 2500 mAh. **Le parc mélange deux chimies**
  - 3,7 V (charge 4,20 V) et 3,8/3,87 V (charge 4,35 V) - ce qui est en soi un mécanisme
  de surchauffe si une cellule est montée dans le mauvais appareil. Détail dans
  `docs/batteries-lithium-tonwelt.md`.
  Conséquence lourde : le diagnostic de surchauffe repose sur la chimie Ni-MH
  (surcharge, fin de charge non détectée). **Ces hypothèses ne s'appliquent pas** à une
  cellule lithium - là, la surchauffe vient du circuit de charge, du circuit de
  protection ou du gonflement de la cellule. Ne pas réutiliser les conclusions Ni-MH.
- **Les poussoirs sont de la série Alps SKRW** (bas profil, 3,7 × 3,7 mm, course
  0,35 mm), pas SKRP.
- **Avertissement général** : beaucoup de composants proposés ne correspondaient pas aux
  photos fournies. Ne proposer que ce qui est constaté ; une ligne « à confirmer » doit
  rester l'exception, pas la majorité de la liste.

## Git
Développer et pousser sur la branche désignée pour la session. Tout livrable
(document, classeur, script) est commité - rien ne reste seulement dans la conversation.
