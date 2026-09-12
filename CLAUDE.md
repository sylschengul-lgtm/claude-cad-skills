# Règles de travail sur ce dépôt

## Langue
Répondre en français.

## Liens distributeurs (Mouser, RS, Farnell…) — règle née d'un échec
**Ne jamais fabriquer une URL `ProductDetail` à la main.** Chez Mouser, une adresse
du type `mouser.fr/ProductDetail/<Fabricant>/<Référence>` **renvoie une page 404** :
la fiche produit exige un jeton `?qs=…` qui ne se devine pas.

À faire systématiquement, pour chaque ligne d'une liste d'achat :

1. **Coller l'URL produit exactement telle que la recherche l'a renvoyée**, jeton `?qs=` compris.
   Ne jamais la « nettoyer », ne jamais en retirer la partie après le `?`.
2. **Ajouter en plus une URL de recherche par référence**, qui ne dépend d'aucun jeton :
   `https://www.mouser.fr/c/?q=<RÉFÉRENCE>`. C'est le lien de secours si le premier ne répond pas.
3. **Mettre la recherche en premier, la fiche produit en second.** La recherche est la
   seule forme qui ne dépend d'aucun jeton ; c'est elle qui doit être le lien principal.
4. **Un renvoi `mouser.com` vers `mouser.fr` perd la chaîne de requête.** Constaté :
   `mouser.com/ProductDetail/Kycon/KPJX-PM-4S-S?qs=…` arrive sur
   `mouser.fr/fr/ProductDetail/Kycon/KPJX-PM-4S-S` **sans le jeton**, donc en 404.
   Donner directement des URL `www.mouser.fr` plutôt que `www.mouser.com`.
5. **La référence fabricant est l'identifiant durable, pas l'URL.** Elle doit figurer en
   clair dans toute liste : collée dans le champ de recherche du distributeur, elle
   fonctionne quand tous les liens ont changé.
6. **Tester les liens avant de livrer** quand le réseau le permet. Vérifié le 2026-09-12 :
   `www.mouser.fr` **et** `www.mouser.com` renvoient un **403 sur le tunnel CONNECT** du
   proxy d'egress — refus de politique de l'organisation, à signaler sans le contourner.
   Donc dans cet environnement, **aucun lien Mouser n'est vérifiable** : le dire au lieu
   d'affirmer que les liens fonctionnent.

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

## Appareils du parc — ne pas confondre
- **Linkx TG-288 / eTour** : audioguide UHF, 2 × AA Ni-MH, carte analysée dans
  `diagnostics/talkie-surchauffe/` (branche `claude/appareil-chauffe-bloque-2aopb5`).
- **Linkx TG-108** : modèle distinct. Une carte marquée `TG-108_RX R.0.2` a été
  photographiée : MCU en QFP différent, micro-USB et jack 3,5 mm visibles.
  Une nomenclature établie pour le TG-288 **ne vaut pas** pour le TG-108.

## Git
Développer et pousser sur la branche désignée pour la session. Tout livrable
(document, classeur, script) est commité — rien ne reste seulement dans la conversation.
