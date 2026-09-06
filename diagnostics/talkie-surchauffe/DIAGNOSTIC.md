# Diagnostic — Linkx TG-288 / eTour : l'appareil chauffe et se bloque

**Dernière révision :** 2026-09-06 (révision 2 — corrige la révision 1)
**Symptôme :** l'appareil chauffe puis se bloque.
**Base :** 15 photos macro de la carte + 2 relevés IR + zooms traités + recherche constructeur.
**Atout :** un exemplaire neuf de référence est disponible.

> ⚠️ **Sécurité — à lire avant toute manipulation**
> Retirez les piles et ne remettez pas l'appareil en valise de charge tant que le diagnostic
> n'est pas fait. **65 °C est déjà dans la zone de destruction d'un accu Ni-MH** : la
> littérature situe les dommages (perte de capacité, fuite d'électrolyte, dégazage) **dès 60 °C**,
> la plage sûre étant 30–40 °C. Un accu Ni-MH en surcharge peut **fuir de la potasse (KOH)**,
> produit corrosif et irritant. Gants + lunettes si vous ouvrez le compartiment pile.

---

## 0. Ce qui a changé depuis la révision 1

Trois corrections importantes. Je les mets en tête parce qu'elles changent où il faut chercher.

| Point | Révision 1 (erronée ou trop confiante) | Révision 2 (après recherche + zooms) |
|---|---|---|
| **Nature de l'appareil** | « talkie-walkie » | **Linkx TG-288 / eTour — audioguide UHF numérique**, alimenté par **2 × AA Ni-MH (2,4 V)** |
| **La tache noire** | « carbonisation par arc électrique, carbon tracking » | **Ce n'est pas un cratère d'arc.** Résidu liquide qui a coulé et bruni + corrosion du cuivre. Probablement une **conséquence**, pas la cause — et peut-être électriquement inoffensive |
| **Puissance dissipée** | « 1,5 à 3 W » | **Estimation retirée** : elle supposait une dissipation répartie sur tout le boîtier. Le chiffre réel dépend entièrement de l'endroit visé, que je ne connais pas |

Et une hypothèse monte au premier rang : **la chaîne pile Ni-MH / charge**, qui n'était que n°5.

---

## 1. Identification de l'appareil — confirmée

Le marquage `Linkx / eTour-07 / 2003B` du QFN-32 n'est pas une référence de transceiver du
commerce : c'est une **puce marquée au nom du produit** par le fabricant.

**Linkx Electronics (Taïwan)** commercialise la gamme **TG-288 / TG-288D / eTour** :
*Digital UHF Tour Guide System* — audioguide numérique UHF pour visites de musées, sites
historiques, usines, interprétation simultanée, assistance auditive.

Tout concorde avec les photos :
- LCD à segments avec **CH**, **cadenas**, **batterie**, **bargraphe de volume** → l'écran
  produit du constructeur affiche exactement « battery power, channel, volume » ;
- 100 canaux indépendants → cohérent avec `CH 03` ;
- ressort d'antenne UHF ;
- micro intégré, entrée micro externe / sortie casque selon version émetteur ou récepteur.

### ⚡ La donnée décisive : l'alimentation

> **TG-288 : alimentation par 2 × piles AA Ni-MH rechargeables 1,2 V** (2,4 V nominal),
> charge par **port micro-USB** ou par **valise de charge 2 / 12 / 35 emplacements**,
> autonomie annoncée 12–14 h.

Deux conséquences majeures, développées au §4 :

1. **2,4 V → 3,3 V exige un convertisseur élévateur (boost).** C'est ce que montrent les
   photos : deux inductances blindées + `19AKM` (SOT-23-5, boost) + `CDV 221 A5L2`.
   Un boost est une **charge à puissance constante** : quand la pile faiblit, il tire *plus*
   de courant. C'est un mécanisme à contre-réaction positive.
2. **Ces appareils passent leur vie en valise de charge.** Le Ni-MH est la chimie la plus
   intolérante à la surcharge : une fois plein, **100 % de l'énergie de charge part en chaleur**.

---

## 2. Nomenclature relevée

| Photo | Marquage | Fonction | Boîtier |
|---|---|---|---|
| 07–10 | `ti MSP430…30TM FR20xx 8CCH T B` | MCU principal TI MSP430FR (FRAM) | TSSOP-48 |
| 07–09 | `HOLTEK HT16C21 C029K00D2G2` | Driver LCD I²C/SPI | SOP-16 |
| 05, 11, 12 | `Linkx eTour-07 2003B` | **SoC RF UHF propriétaire Linkx** (marquage produit) | QFN-32 |
| 04, 06, 12 | `24.04 AK AD` | TCXO 24,04 MHz — référence RF | SMD 4 pads |
| 04, 06, 12 | `724 2G SU` | Régulateur / audio | SOP-8 |
| 07, 10 | `BSG· TI 8A8 A46R` | CI TI — ampli audio ou régulateur | QFN-16 |
| 06, 07 | `EAMC` | Résonateur / filtre céramique | SMD 3 br. |
| 01, 14 | `CDV 221 A5L2` | Convertisseur / contrôleur d'alimentation | SOP-8 |
| 03, 15 | `19AKM` | **Convertisseur élévateur (boost)** — voisin immédiat d'une inductance | SOT-23-5 |
| 03, 13, 15 | 2 inductances blindées | **2 étages à découpage** | 4×4 mm |
| 15 | `4R7` (4,7 µH), `18C`, `473` (47 nF) | Passifs de l'étage boost | 0603 |
| 07, 10 | `3R3` ×2 | 3,3 Ω — filtrage d'alim ou shunts | 0805 |
| 10, 12 | Trimmer métallique | Accord RF d'usine — **ne pas y toucher** | — |

Le marquage `19AKM` n'apparaît dans aucune base publique de codes SMD : c'est un boîtier
SOT-23-5 générique de fabricant asiatique. Son rôle se déduit sans ambiguïté de la topologie
(entrée pile / inductance / diode ou redressement synchrone / sortie filtrée) : **boost**.

---

## 3. Relecture des anomalies — avec les zooms

Les zooms ×3 traités sont dans `zooms/`.

### 3.1 La tache noire : ma première lecture était fausse

**Ce que montre le zoom** (`zooms/burn_05_x3.jpg`, `zooms/burn_11_x3.jpg`, deux angles) :

- la matière est **lisse, brillante, translucide brun sur les bords, opaque au centre** ;
- elle a manifestement **coulé** : bord supérieur festonné, lobes arrondis, elle a mouillé la
  surface puis s'est arrêtée ;
- elle **contourne** deux vias, autour desquels apparaît un **halo orangé-rouge** ;
- **il n'y a ni cratère, ni pastille arrachée, ni vernis soulevé, ni fibres de verre calcinées** ;
- les vias concernés sont **intacts et toujours étamés** (on voit le reflet métallique).

Une carbonisation par arc électrique, ce n'est pas ça : c'est **mat, croûteux, creusé**, avec
de la matière manquante. Ici c'est un **liquide qui a coulé, séché et bruni**, avec **oxydation
du cuivre** (le halo rouge = oxyde cuivreux Cu₂O, signature d'une attaque chimique ou thermique).

**Candidats, du plus au moins probable :**

1. **Électrolyte d'accu (KOH) ayant fui puis attaqué le cuivre et le vernis**, brunissant à la
   chaleur. Cohérent avec un Ni-MH surchauffé qui a dégazé — et cohérent avec 65 °C.
2. **Flux de brasage résiduel surchauffé** qui a coulé et bruni.
3. **Adhésif / mousse double-face liquéfié par la chaleur** — on voit justement des bandes de
   mousse blanche au bord de carte sur les photos 08, 11, 13.

### 3.2 ⚠️ Et surtout : cette tache est peut-être électriquement sans effet

Regardez le contexte (`zooms/grid_05.jpg`) : ces trous forment une **matrice régulière,
régulièrement espacée, sur une grande surface, tous étamés, sans piste individuelle visible**.
C'est la signature d'un **champ de vias de couture de masse** (*ground stitching*), typique
autour d'un bloc RF pour le blindage et l'évacuation thermique.

**Si tous ces vias sont sur le même net (la masse), un résidu qui les relie ne court-circuite
rien du tout.** La tache serait alors un **témoin** d'un événement thermique — utile comme
indice — mais **pas la cause de la panne**.

C'est vérifiable en 30 secondes (§6.3). Tant que ce n'est pas vérifié, **ne grattez rien** :
la révision 1 vous conseillait de décaper mécaniquement, c'était prématuré.

### 3.3 Encrassement autour des interrupteurs (photos 01, 02, 13, 14)

Dépôts sombres et fibres autour des pattes des poussoirs. **Mais je dégrade fortement cette
piste** : sur un audioguide il n'y a **pas de PTT** — l'émetteur émet en continu par conception,
le récepteur n'émet pas du tout. Un bouton collé ne peut donc pas provoquer une émission
permanente. Reste un rôle mineur : un bouton collé peut empêcher la mise en veille et maintenir
le rétroéclairage / le CPU actif.

### 3.4 Résidus de flux généralisés

Voile blanchâtre autour de nombreuses soudures, notamment sur l'étage boost
(`zooms/alim3_x3.jpg` : traces vertes-sombres aux bords des pastilles du `19AKM`). Hygroscopique,
facilite les fuites. À nettoyer, mais rarement fatal seul.

### 3.5 Non-anomalies

- Marques vert/jaune fluo sur le MSP430 : **feutre de contrôle qualité usine**. Normal.
- Pastilles « QC PASS » : étiquettes de production. Normal.

---

## 4. Le mécanisme le plus probable : la chaîne Ni-MH → boost

Trois effets physiques se combinent, et ils expliquent **précisément** l'enchaînement
« ça chauffe **puis** ça se bloque ».

### 4.1 La surcharge Ni-MH transforme toute l'énergie en chaleur

Le Ni-MH est la chimie la plus intolérante à la surcharge. Une fois l'accu plein, l'énergie
injectée ne peut plus être stockée : **elle est intégralement dissipée en chaleur**.

Le problème est que **la détection de fin de charge du Ni-MH est difficile** : la méthode
−ΔV ne produit qu'une **chute d'environ 5 mV**, très délicate à détecter de façon fiable — les
chargeurs la ratent couramment et poursuivent la charge. Le courant d'entretien doit rester
sous **0,05 C**. Une élévation de **1 °C/minute** signale la fin de charge.

**Ordre de grandeur pour votre appareil :** une valise de charge délivrant ~300 mA sur 2 cellules
à ~2,9 V injecte ≈ **0,9 W**. En surcharge, ces 0,9 W partent **entièrement en chaleur**, dans un
compartiment pile confiné, sans ventilation. **C'est largement suffisant pour atteindre 60–70 °C.**
Vos 65,9 °C sont parfaitement cohérents avec ce scénario.

### 4.2 Un accu vieilli fait s'emballer le boost (charge à puissance constante)

Un accu Ni-MH neuf a une résistance interne **< 50 mΩ**. En fin de vie, **elle grimpe fortement**,
et la tension de crête chute (de ~1,47 V à ~1,42 V par élément sur des cellules vieillies).

Un convertisseur boost régule sa **sortie**, donc il absorbe une **puissance d'entrée quasi
constante**. D'où la boucle :

```
accu vieilli → résistance interne ↑
      ↓
tension sous charge ↓
      ↓
le boost compense : courant d'entrée ↑   (I = P / V)
      ↓
échauffement I²R dans l'accu ↑↑  (au carré du courant)  + pertes ↑ dans l'inductance et le MOSFET
      ↓
température ↑ → l'accu se dégrade encore → tension ↓
      ↓
… jusqu'au seuil de verrouillage basse tension (UVLO) du boost
      ↓
le rail 3,3 V s'effondre → brown-out du MSP430 → ⛔ APPAREIL BLOQUÉ
```

**C'est exactement votre symptôme : ça chauffe d'abord, ça se bloque ensuite.** Le blocage n'est
pas un bug logiciel, c'est une **coupure d'alimentation** provoquée par l'échauffement.

Certains convertisseurs placent leur UVLO **au-dessus de 1,25 V/élément** : sur un pack vieilli,
le seuil est atteint alors qu'il reste de la capacité — l'appareil « se bloque » en paraissant
encore chargé.

### 4.3 Le piège des piles alcalines — à vérifier en priorité

Le TG-288 accepte « plusieurs options de batterie », **rechargeables ou jetables**.

**Si des piles alcalines jetables se retrouvent dans un appareil placé en valise de charge, elles
sont soumises à un courant de charge qu'elles ne peuvent pas accepter.** Elles s'échauffent
violemment, dégagent de l'hydrogène et **fuient de la potasse**.

Sur un parc d'audioguides manipulé par plusieurs personnes, le mélange de chimies est une erreur
fréquente. **Et ce scénario expliquerait d'un seul coup les 65 °C ET le liquide bruni qui a coulé
sur la carte (§3.1).**

👉 **Vérifiez immédiatement quelles piles sont dans l'appareil défectueux** : elles doivent porter
la mention **Ni-MH / rechargeable**. Si ce sont des alcalines (Duracell, Energizer non
rechargeables…), vous tenez très probablement la cause racine.

---

## 5. ⚠️ Deux failles méthodologiques dans la comparaison IR

Vos deux relevés sont précieux, mais avant d'en tirer une conclusion il faut écarter deux pièges.
Sans quoi le Δ36 °C peut être en partie une illusion.

### 5.1 Émetteur ou récepteur ?

Le TG-288 existe en version **émetteur** (le guide parle) et **récepteur** (les visiteurs
écoutent). L'émetteur **émet en permanence** et consomme structurellement bien plus qu'un
récepteur, qui ne fait que recevoir.

**Comparer un émetteur usagé à un récepteur neuf n'a aucune valeur diagnostique.**
→ Vérifiez les références sur les étiquettes des deux appareils. Elles doivent être identiques.

### 5.2 Le neuf était-il seulement allumé ?

23 °C, c'est **la température ambiante**. Un appareil réellement en fonctionnement est
toujours un peu au-dessus. 23 °C suggère un appareil **éteint**, ou allumé depuis très peu de temps.

→ Refaites la mesure avec les **deux appareils allumés, dans le même mode, depuis au moins
30 minutes, côte à côte, dans la même pièce**, et visez **le même point** sur les deux boîtiers.

### 5.3 Où avez-vous visé ?

C'est la question qui manque pour interpréter les 65 °C. Le compartiment pile ? Le dos du
boîtier ? La carte nue ? L'accu lui-même ? La réponse oriente tout :
- **compartiment pile chaud** → chimie / charge (§4.1, §4.3) ;
- **zone des inductances chaude** → convertisseur (§4.2) ;
- **zone RF / bloc Linkx chaude** → étage radio.

Et rappel de la révision 1, toujours valable : **ε = 0,96 est juste sur le plastique et l'époxy,
faux sur les métaux brillants** (jaquette d'accu, blindages, inductances, soudures : ε réel
0,05–0,3). Sur ces surfaces le thermomètre **sous-estime largement** — l'accu peut être bien
plus chaud que ce que vous lisez. Collez un ruban adhésif mat noir pour mesurer juste.
Rappelons aussi que **le cœur d'une cellule est nettement plus chaud que son enveloppe**.

---

## 6. Protocole — réordonné par rentabilité

### 6.0 Sécurité
Piles retirées pour toute mesure de résistance. Bracelet antistatique (MSP430 et SoC RF
sensibles ESD). Ne jamais faire fonctionner l'émetteur sans antenne.

### 6.1 ⭐ Inspection des piles et du compartiment — 2 minutes, coût nul

**C'est par là qu'il faut commencer.**

| À vérifier | Signification |
|---|---|
| Mention **Ni-MH / rechargeable** sur les deux piles | Si alcalines → **cause racine probable (§4.3)** |
| Les deux piles sont-elles de même marque, même capacité, même âge ? | Un pack dépareillé s'inverse en décharge et chauffe |
| Traces blanches/croûteuses, cristaux, verdissement sur les **contacts à ressort** | Fuite d'électrolyte confirmée |
| Déformation, gonflement, jaquette percée ou brunie | Cellule dégazée |
| Odeur ammoniacale à l'ouverture | Fuite de KOH |

### 6.2 ⭐ Test croisé des piles — 20 minutes, coût nul

Le test le plus rentable de toute la liste.

Mettez **les piles du neuf** dans l'appareil défectueux, et **celles de l'usagé** dans le neuf.
Laissez tourner 20–30 min dans le même mode.

- La chauffe **suit les piles** → **c'est la chimie, pas la carte.** Remplacez le pack, terminé.
- La chauffe **reste sur l'appareil défectueux** → le défaut est électronique. Continuez.

*Ce seul test départage les hypothèses §4.1/§4.3 des hypothèses §4.2/§6.5.*

### 6.3 ⭐ Statut électrique de la tache noire — 30 secondes

**Avant de gratter quoi que ce soit.** Ohmmètre / mode continuité, piles retirées :

1. Testez la continuité entre **chacun des vias recouverts par la tache** et la **masse**
   (blindage, tresse, borne − du compartiment pile).
2. **Tous continus avec la masse → la tache est cosmétique, oubliez-la** (c'est un témoin
   thermique, pas la panne). Nettoyage à l'IPA pour l'esthétique, rien de plus.
3. **Des vias sur des nets différents avec une résistance < 1 MΩ entre eux → là seulement**
   c'est une fuite : nettoyage IPA d'abord, et décapage mécanique uniquement si le noir résiste
   au solvant.

**Test discriminant matière :** un coton-tige d'alcool isopropylique ≥ 99 %.
- Ça part, ça teinte le coton → **résidu** (flux, adhésif, électrolyte séché) → nettoyable.
- Ça ne bouge pas, c'est imprégné dans l'époxy → **carbonisation** → décapage nécessaire.

### 6.4 ⭐ Mesure de courant comparative — le juge de paix

Multimètre **en série** sur le + pile (calibre 10 A d'abord, puis mA). Toujours en A/B.

| État | Neuf | Usagé | Lecture |
|---|---|---|---|
| Éteint | | | > 10 mA = fuite permanente |
| Allumé, veille | | | Rapport usagé/neuf > 2 = anormal |
| En fonctionnement (mode nominal) | | | |
| **En charge, pile pleine** | | | **Le courant doit chuter ou passer en entretien (≤ 0,05 C). S'il reste au courant plein → surcharge = §4.1 confirmé** |

### 6.5 Mesure de tension sous charge — révèle l'accu vieilli

Appareil allumé, en fonctionnement :

| Point | Attendu | Usagé | Diagnostic |
|---|---|---|---|
| Tension pack à vide | 2,6–2,9 V (chargé) | | |
| Tension pack **en fonctionnement** | doit rester > 2,2 V | | **Chute > 0,4 V entre à vide et en charge = résistance interne élevée = accu HS (§4.2)** |
| Sortie boost (rail 3,3 V) | 3,3 V ± 0,1 | | |
| VCC MSP430 | 3,3 V stable | | |
| Ondulation rail 3,3 V (oscillo) | < 50 mV crête-crête | | |

**Le test qui signe le blocage :** gardez le voltmètre sur le rail 3,3 V et **attendez que
l'appareil se bloque**. Si le rail s'effondre au moment exact du blocage → **brown-out confirmé**,
et la cause est en amont (accu ou boost), pas dans le logiciel.

### 6.6 Thermique localisée — trouver LE point chaud

Appareil ouvert, en fonctionnement, sans toucher :
- **Test alcool isopropylique** : un film mince d'IPA au pinceau sur la carte. **Il s'évapore
  en premier sur le point chaud.** Redoutablement efficace et gratuit.
- Ou ruban adhésif mat noir sur les zones métalliques + thermomètre IR.
- Ou caméra thermique si vous en avez une.

Candidats à surveiller : les **2 inductances**, le `19AKM`, le `CDV 221`, le QFN `BSG A46R`,
le SoC `Linkx`, et **les cellules elles-mêmes**.

### 6.7 Nettoyage et inspection finale
IPA ≥ 99 % sur les deux faces, brosse antistatique, séchage complet. Loupe ×10 : pattes du QFN
Linkx, soudures des inductances, contacts pile, port micro-USB (corrosion fréquente sur du
matériel de location).

---

## 7. Fiche de relevés

| Mesure | Neuf | Usagé | Conclusion |
|---|---|---|---|
| Référence exacte sur l'étiquette (émetteur ? récepteur ?) | | | ⚠️ doivent être identiques |
| Les deux appareils étaient-ils allumés, même mode, ≥ 30 min ? | | | ⚠️ prérequis |
| Point visé au thermomètre IR | | | ⚠️ à documenter |
| Chimie des piles (Ni-MH ou alcaline) | | | |
| Traces de fuite au compartiment pile | | | |
| T° surface après 30 min, même point | | | |
| Courant éteint | | | |
| Courant en veille | | | |
| Courant en fonctionnement | | | |
| Courant en charge, pile pleine | | | |
| U pack à vide | | | |
| U pack en fonctionnement | | | |
| Chute de tension (à vide − en charge) | | | > 0,4 V = accu HS |
| Rail 3,3 V | | | |
| Rail 3,3 V **à l'instant du blocage** | | | effondrement = brown-out |
| Vias de la tache : continus avec la masse ? | — | | oui = tache inoffensive |
| Point chaud localisé (nom du composant) | — | | |

---

## 8. Hypothèses classées — révision 2

| # | Hypothèse | Probabilité | Test |
|---|---|---|---|
| **H1** | **Piles alcalines dans un appareil mis en charge** | **Élevée** | §6.1 — 2 minutes |
| **H2** | **Surcharge Ni-MH** (fin de charge non détectée, valise ou circuit de charge) | **Élevée** | §6.1, §6.2, §6.4 dernière ligne |
| **H3** | **Accu vieilli → emballement du boost → UVLO → brown-out** | **Élevée** | §6.2, §6.5 |
| H4 | Convertisseur boost en défaut (`19AKM` / `CDV 221`, condensateur de sortie fissuré) | Moyenne | §6.5, §6.6 |
| H5 | Fuite par résidu conducteur (la tache, **si** vias sur nets différents) | Faible-moyenne | §6.3 |
| H6 | Étage RF en défaut (SoC Linkx, antenne, ROS) | Faible | §6.6 |
| H7 | Bouton collé empêchant la veille | Faible | continuité des switches au repos |

**H1, H2 et H3 se testent toutes les trois avec le §6.1 + §6.2, en une demi-heure et sans
outillage.** Commencez par là.

---

## 9. Réparations, par coût croissant

1. **Remplacer le pack par 2 AA Ni-MH neuves, appairées, de même marque et capacité** — quelques
   euros. Si H1/H2/H3, c'est terminé ici.
2. **Nettoyage IPA + séchage** du compartiment pile et de la carte (obligatoire s'il y a eu fuite :
   le KOH continue de corroder tant qu'il est présent).
3. **Nettoyage / remplacement des contacts à ressort** corrodés du compartiment pile.
4. **Vérifier la valise de charge elle-même** — si elle surcharge, elle détruira aussi les
   appareils sains. **Testez les autres appareils du parc.**
5. Remplacement des condensateurs de sortie du boost si l'ondulation est hors spec.
6. Remplacement du convertisseur (`19AKM` / `CDV 221`) — air chaud requis.
7. Carte complète si le SoC Linkx ou le MSP430 sont en cause (MCU programmé en usine,
   non remplaçable sans le firmware).

> 💡 **Pensez « parc », pas « appareil ».** Sur un ensemble d'audioguides, une valise de charge
> défaillante ou une procédure de charge inadaptée abîme les appareils **un par un**. Si vous
> avez d'autres unités, mesurez-en deux ou trois autres : si plusieurs chauffent, le problème
> est dans la **charge**, pas dans cet exemplaire.

---

## 10. À retenir

1. **L'appareil est un Linkx TG-288 / eTour, audioguide UHF, sur 2 × AA Ni-MH.** Cette seule
   information réoriente tout le diagnostic vers la **chaîne pile / charge**.
2. **La tache noire n'est pas un arc électrique.** C'est un liquide qui a coulé et bruni.
   Elle est probablement un **témoin** thermique, et possiblement sans effet électrique si les
   vias qu'elle recouvre sont tous à la masse. **Ne la grattez pas avant de l'avoir vérifiée.**
3. **Le Ni-MH transforme toute surcharge en chaleur**, et sa fin de charge est notoirement
   difficile à détecter (−ΔV ≈ 5 mV). 65,9 °C est la signature classique.
4. **Un boost sur un accu vieilli est une boucle à contre-réaction positive** qui finit par
   déclencher l'UVLO — d'où « ça chauffe, **puis** ça se bloque ». Le blocage est une coupure
   d'alimentation, pas un bug.
5. **Avant de conclure quoi que ce soit du Δ36 °C**, assurez-vous de comparer deux appareils de
   même type, allumés, dans le même mode, depuis le même temps, visés au même endroit.
6. **Le test croisé des piles (§6.2) coûte 20 minutes et zéro euro**, et il départage la moitié
   des hypothèses. Faites-le en premier.

---

## Sources

- [Linkx Electronics — TG-288 / TG-288D, Tour Guide System](http://www.linkx.com.tw/tg-288_tg-288d.html)
- [Linkx — eTour (linkxcorp)](http://www.linkxcorp.ru/en/products/tour-guide-system/etour.html)
- [SoundFields — eTour, Digital UHF Tour Guide System](http://www.soundfields.co.uk/eTour.asp)
- [GMGA — Digital UHF guide system Linkx TG-288](https://gmga.vn/en/digital-uhf-guide-system-linkx-tg-288/)
- [Battery University — BU-408: Charging Nickel-metal-hydride](https://www.batteryuniversity.com/article/bu-408-charging-nickel-metal-hydride/)
- [Electronics Notes — NiMH Battery Charging](https://www.electronics-notes.com/articles/electronic_components/battery-technology/nimh-nickel-metal-hydride-charging.php)
- [Energizer — Nickel Metal Hydride (NiMH) Handbook and Application Manual](https://data.energizer.com/pdfs/nickelmetalhydride_appman.pdf)
- [Industrial Monitor Direct — NiCd/NiMH charging current and termination methods](https://industrialmonitordirect.com/blogs/knowledgebase/nicad-vs-nimh-battery-charging-current-rate-and-termination-methods)
- [SkyRC — Temperature rise when charging AA/AAA NiMH at high current](https://blog.skyrc.com/what-you-need-to-know-about-temperature-rise-when-charging-aa-aaa-nimh-batteries-at-very-high-current-3a/)

---

## Annexe A — Index des photos

| Fichier | Contenu |
|---|---|
| `01_boutons_cdv221_qcpass.jpg` | Poussoirs, `CDV 221 A5L2`, étiquette QC |
| `02_alim_diodes_ye_br_boutons.jpg` | Section alim, diodes `YE`/`BR` |
| `03_alim_19akm_2inductances_qfn.jpg` | `19AKM`, 2 inductances blindées |
| `04_rf_724-2gsu_trimmer_tcxo.jpg` | `724 2G SU`, trimmer RF, TCXO 24,04 MHz |
| `05_ANOMALIE_point_brule_via.jpg` | Tache sombre en bordure de carte |
| `06_vue_large_msp430_linkx.jpg` | Vue d'ensemble MCU + RF |
| `07_msp430fr2_ht16c21_bsg_a46r.jpg` | MSP430FR, HT16C21, QFN `BSG A46R` |
| `08_msp430_ht16c21_bord_carte.jpg` | MCU + driver LCD, bord de carte |
| `09_lcd_ch03_ht16c21.jpg` | LCD `CH 03`, pictos cadenas/batterie/volume |
| `10_msp430_bsg_trimmer.jpg` | MCU, QFN TI, trimmer, `3R3` |
| `11_ANOMALIE_point_brule_zoom_linkx.jpg` | Tache, second angle + SoC Linkx |
| `12_linkx_etour07_msp430_724.jpg` | `Linkx eTour-07 2003B`, TCXO |
| `13_face_alim_boutons_inductances.jpg` | Face alimentation complète |
| `14_boutons_cdv221_vue2.jpg` | Poussoirs, `CDV 221 A5L2` |
| `15_alim_zoom_4r7_18c_473_19akm.jpg` | Étage boost : `4R7`, `18C`, `473`, `19AKM` |
| `16_IR_appareil_UTILISE_57C_max659.jpg` | Relevé IR **usagé** : 57 °C / max 65,9 °C |
| `17_IR_appareil_NEUF_23C_max297.jpg` | Relevé IR **neuf** : 23 °C / max 29,7 °C |

## Annexe B — Zooms traités

| Fichier | Contenu |
|---|---|
| `zooms/grid_05.jpg` | Photo 05 avec grille de coordonnées — montre la **matrice de vias** |
| `zooms/burn_05_x3.jpg` | Tache ×3 — matière lisse, coulée, halos de cuivre oxydé |
| `zooms/burn_11_x3.jpg` | Tache ×3, second angle — confirme : pas de cratère |
| `zooms/alim3_x3.jpg` | Étage boost ×3 — `19AKM` + inductance + capas de sortie |
