# Surchauffe — périmètre restreint au tourGuide AIR

**Établi le 14/09/2026.** La panne de surchauffe ne concerne **qu'un seul produit sur les
sept du parc : le `tourguide air`.** Les `go`, `play`, et toute la famille `supraguide`
sont hors périmètre.

Ce document remplace, pour cet appareil, les conclusions de
`diagnostics/talkie-surchauffe/DIAGNOSTIC.md` (branche `claude/appareil-chauffe-bloque-2aopb5`).

---

## 1. Ce que le resserrement apporte

L'appareil photographié dans le diagnostic de surchauffe **est** le tourGuide AIR : c'est
de lui que viennent les relevés infrarouges (57 °C, pointe à 65,9 °C sur l'usagé contre
23 °C sur le neuf). On sait donc à quoi il ressemble à l'intérieur :

- SoC RF UHF propriétaire `Linkx eTour-07 2003B` en QFN-32 ;
- MCU `TI MSP430FR2xxx` en TSSOP-48, driver LCD `Holtek HT16C21` ;
- écran à segments sur mesure (canal, cadenas, pile, bargraphe de volume) ;
- TCXO 24,04 MHz, ressort d'antenne UHF, port de charge micro-USB ;
- **deux étages à découpage** avec un convertisseur élévateur `19AKM` en SOT-23-5.

---

## 2. ⚠️ La contradiction à lever en premier

Deux informations solides ne s'accordent pas :

| Constat | Implique |
|---|---|
| La carte porte un **convertisseur élévateur** (boost) vers le 3,3 V | Une source **sous 3,3 V** : typiquement 2 × AA Ni-MH à 2,4 V |
| Les batteries du parc sont des **cellules lithium plates** (3,7 V et plus) | Une source **au-dessus de 3,3 V** : il faudrait un abaisseur ou un régulateur linéaire, pas un élévateur |

Trois explications possibles, à départager :

1. **Deux générations de tourGuide AIR coexistent** dans le parc : une ancienne à
   2 × AA Ni-MH, une récente à cellule lithium. C'est l'explication la plus simple.
2. L'élévateur alimente **un autre rail** que le 3,3 V — polarisation de l'écran LCD ou
   étage RF — et l'alimentation principale est bien lithium.
3. L'appareil photographié n'est pas de la même génération que ceux qui chauffent.

👉 **La vérification qui tranche, et elle prend une minute : ouvrir un tourGuide AIR qui
chauffe et regarder ce qui l'alimente.** Deux piles AA, ou une poche lithium collée ? Et
si c'est une poche, lire la tension inscrite dessus.

**Tant que ce point n'est pas levé, aucune hypothèse de cause n'est solide.**

---

## 3. Si l'alimentation est lithium — hypothèses révisées

Les hypothèses H1, H2 et H3 du diagnostic d'origine **tombent** : elles reposent toutes sur
la chimie Ni-MH (piles alcalines mises en charge, surcharge sans détection de fin de
charge à −ΔV, résistance interne d'accu vieilli).

| # | Hypothèse lithium | Pourquoi elle est plausible ici | Vérification |
|---|---|---|---|
| **L1** | **Cellule de mauvaise tension nominale montée à la réparation** | Le parc mélange du 3,7 V (charge 4,20 V) et du 3,8/3,87 V (charge 4,35 V). Une cellule 3,7 V dans un circuit de charge réglé pour 4,35 V est en **surcharge permanente** : elle chauffe, gonfle, vieillit vite | Lire la tension sur la cellule de l'appareil qui chauffe **et** sur celle d'un appareil sain. Elles doivent être identiques |
| **L2** | **Cellule gonflée** | Conséquence visible de L1, ou fin de vie normale | Visible et palpable. Coque qui ne ferme plus, carte bombée |
| **L3** | **Circuit de charge ou circuit de protection en défaut** | Un chargeur qui ne passe pas en fin de charge maintient le courant plein | Mesurer le courant d'entrée **cellule pleine** : il doit s'effondrer |
| **L4** | **La valise de charge elle-même** | Alimentation 5 V / 10 A sur prise Kycon : une valise qui dérive abîme les appareils **un par un** | Mesurer d'autres appareils du même lot. Si plusieurs chauffent, le problème est dans la valise, pas dans l'exemplaire |

### 🔥 Sécurité — spécifique au lithium

Une poche lithium gonflée ou en surchauffe est un **risque d'incendie**, pas seulement une
pièce usée. Ne pas la percer, ne pas la plier, ne pas continuer à la charger, ne pas la
laisser en valise. La sortir de l'appareil, la placer dans un contenant ininflammable, et
la faire reprendre en déchet. Cette précaution n'existait pas dans la version Ni-MH du
diagnostic.

---

## 4. Ce qui reste valable du diagnostic d'origine

Indépendamment de la chimie :

- **L'analyse de la tache noire** (§3.1 et 3.2) : ce n'est pas un arc électrique mais un
  liquide qui a coulé et bruni. Vérifier à l'ohmmètre si les vias qu'elle recouvre sont
  tous à la masse — si oui, elle est cosmétique. **Ne pas gratter avant.**
- **La critique de la comparaison infrarouge** (§5) : comparer deux appareils **du même
  modèle**, allumés, même mode, même durée, même point visé. Et l'émissivité 0,96 est
  fausse sur les surfaces métalliques brillantes, qui sont donc sous-estimées.
- **Le test croisé des batteries** (§6.2) : intervertir les cellules entre un appareil sain
  et un appareil qui chauffe. Si la chauffe suit la cellule, c'est la cellule. Toujours le
  test le plus rentable — et désormais à faire avec précaution, cellules lithium obligent.
- **Raisonner « parc » et non « appareil »** : tester deux ou trois autres tourGuide AIR.

---

## 5. Conséquence pour la liste d'achat

Le périmètre se réduit à un seul produit. Les lignes qui comptent pour le tourGuide AIR :

- la **cellule lithium** — tension nominale à faire correspondre exactement ;
- le **port de charge micro-USB** ;
- les **poussoirs SKRW** ;
- l'**écran à segments** (sur mesure, hors catalogue) ;
- la **prise Kycon** de la valise de charge, si c'est bien elle qui est en cause.

Tout ce qui relève des `supraguide` — USB-C, nappe FPC, écran tactile — sort du périmètre
de cette panne.
