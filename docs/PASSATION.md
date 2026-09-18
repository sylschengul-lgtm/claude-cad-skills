# Passation - reprise du travail dans une nouvelle session

**Dernière mise à jour :** 2026-09-13
**Branche de travail :** `claude/composants-fournisseurs-oe9zvv`
**À lire en premier :** `CLAUDE.md` à la racine (règles de travail, chargé automatiquement).

---

## 1. En une phrase

Constitution d'une liste d'achat Mouser pour les **audioguides Tonwelt / Linkx** ;
le travail a dérivé, en cours de route, vers une découverte qui compte plus que la
liste elle-même : **le parc mélange deux chimies de batterie lithium**, ce qui est un
mécanisme de surchauffe à part entière.

---

## 2. Ce qui est acquis

### Les appareils - il y en a trois, pas un

| Carte | Signes distinctifs | Où c'est documenté |
|---|---|---|
| **Linkx TG-288 / eTour** | UHF, MSP430FR + SoC `Linkx eTour-07`, LCD à segments sur mesure | `diagnostics/talkie-surchauffe/DIAGNOSTIC.md`, branche `claude/appareil-chauffe-bloque-2aopb5` (15 photos macro) |
| **TG-108_RX R.0.2** | MCU en QFP différent, micro-USB, jack 3,5 mm | photo fournie en session, non versionnée |
| **« Eco 2.0 »** | USB-C, nappe FPC, cellule 3,87 V, mention `(c) Felix Bäsecke` | photo fournie en session, non versionnée |

Attention : **Une nomenclature établie pour l'un ne vaut pas pour les autres.** C'est la raison de
fond pour laquelle la première liste ne correspondait pas aux photos de l'utilisateur.

### Les batteries - le point le plus important

Relevé sur photo le 12/09/2026 (`docs/batteries-lithium-tonwelt.md`) :

| Marquage | Tension | Capacité | Dimensions décodées |
|---|---|---|---|
| `JHY632570` | **3,7 V** (charge 4,20 V) | 1300 mAh | 6,3 × 25 × 70 mm |
| sans référence | **3,87 V** (charge 4,35 V) | 1000 mAh | - |
| `LIDIO 355485` | **3,8 V** (charge 4,35 V) | 2500 mAh | 3,5 × 54 × 85 mm |

**Une cellule 3,7 V dans un appareil dont le chargeur vise 4,35 V est en surcharge
permanente** : elle chauffe, gonfle, et sa protection finit par couper. C'est la première
chose à vérifier sur un appareil qui chauffe - avant toute mesure électronique.

Corollaire : **le diagnostic de surchauffe du TG-288 est caduc** pour ces appareils. Il
repose sur la chimie Ni-MH (surcharge, fin de charge non détectée à −ΔV). Ne pas
réutiliser ses conclusions H1/H2/H3 sur du lithium.

### La liste d'achat

- `exports/Liste-Mouser-Tonwelt-TG288.xlsx` - **22 lignes**, 4 onglets.
- Elle est **arrêtée par l'utilisateur** : il a gardé 16 lignes sur 31, puis on a ajouté
  les poussoirs SKRW et les cellules lithium.
- Le classeur est **régénéré par `tools/build_liste_mouser_xlsx.py`**. Ne jamais l'éditer
  à la main : la reconstruction écraserait le tri de l'utilisateur.

Ce que son tri a tranché au passage : la prise d'alimentation est la **version blindée**
(`KPJX-4S-S` seule retenue), le jack est **en CMS**, il y a bien une **prise mini-USB**,
et une seule antenne - l'hélicoïdale CMS.

### Les liens Mouser - trois échecs, une règle

Les URL `ProductDetail` construites à la main renvoient 404 (jeton `?qs=` manquant), et un
renvoi `mouser.com` → `mouser.fr` perd la chaîne de requête. **Seule forme à utiliser :**
`https://www.mouser.fr/c/?q=<RÉFÉRENCE>`, confirmée par l'utilisateur le 12/09/2026.
66 liens morts ont été réécrits dans les documents. Détail dans `CLAUDE.md`.

Attention : **`www.mouser.fr` et `www.mouser.com` renvoient un 403 sur le tunnel CONNECT du proxy
d'egress.** Aucun lien Mouser n'est vérifiable depuis cet environnement : le dire, ne pas
le contourner.

---

## 3. Ce qui reste ouvert

Par ordre d'importance :

1. ~~Quel modèle équipe le parc ?~~ **Répondu le 14/09/2026** : sept produits Tonwelt sur
   deux familles - `tourguide air / go / play` (guidage de groupe par radio) et
   `supraguide / eco / 2 / touch` (audioguides individuels). Voir `CLAUDE.md`.
   **Nouvelle tâche qui en découle : éclater la liste d'achat par produit**, une famille
   ne partageant ni l'écran, ni la batterie, ni la connectique de l'autre.
2. **Les appareils qui chauffent ont-ils la bonne tension de cellule ?** C'est la
   vérification la plus rentable, et elle ne coûte qu'un coup d'œil sur l'étiquette.
3. **Le marquage de la 4ᵉ cellule** n'était pas déchiffrable sur la photo.
4. **Suffixe SKRW** - dépend de la durée de vie visée (50 k / 500 k / 1000 k cycles).
   `SKRWAME030` en 500 k est le compromis habituel, à défaut d'information.
5. **Bande de l'antenne** - 863-865 MHz (Europe) ou 902-928 MHz (US), c'est sur
   l'étiquette. La référence retenue `ANT-868-VHETH` suppose l'Europe.
6. **Écran LCD** - verre à segments sur mesure, aucun équivalent catalogue. Seules voies :
   SAV Linkx/Tonwelt, ou refabrication sur plan (relever nombre de broches, pas,
   dimensions, et photographier le verre rétroéclairé).
7. **Quatre codes CMS non résolus** (`19AKM`, `CDV 221 A5L2`, `724 2G SU`, `BSG A46R`) -
   non commandables tant qu'ils ne sont pas identifiés par brochage.

---

## 4. Fichiers produits

| Fichier | Contenu |
|---|---|
| `CLAUDE.md` | Règles de travail - **chargé automatiquement**, à lire en premier |
| `docs/batteries-lithium-tonwelt.md` | Relevé des cellules, analyse des deux chimies, critères de substitution |
| `docs/mouser-liste-complete-tonwelt.md` | Tableau consolidé des composants |
| `docs/mouser-electromecanique-tonwelt.md` | Connectique, haut-parleur, antennes, passifs |
| `docs/mouser-tonwelt-linkx-tg288.md` | Semi-conducteurs de la carte TG-288 |
| `docs/BOM-composants-fournisseurs.md` | **Sujet distinct** : nomenclature du pousse-seringue Antigravity, déduite de la CAO |
| `exports/Liste-Mouser-Tonwelt-TG288.xlsx` | Le livrable d'achat |
| `tools/build_liste_mouser_xlsx.py` | Régénère le classeur |
| `tools/extract_holes.py` | Inventaire des perçages d'un DXF/STEP (pousse-seringue) |

---

## 5. Deux choses à ne pas refaire

1. **Ne pas proposer de composants au jugé.** Sur les 31 lignes de la première liste,
   3 seulement étaient constatées sur les photos ; l'utilisateur a dû en supprimer la
   moitié. Une ligne « à confirmer » doit rester l'exception.
2. **Ne pas transposer une conclusion d'un appareil à l'autre.** Ni la nomenclature, ni
   le diagnostic de surchauffe.
