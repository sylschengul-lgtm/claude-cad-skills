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
3. **Tester les liens avant de livrer** quand le réseau le permet. Dans cette session
   `www.mouser.fr` est bloqué par le proxy : le dire explicitement plutôt que d'affirmer
   que les liens fonctionnent.

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
