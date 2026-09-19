# Coller un écran tactile sur un support aluminium

Fiche de référence — choix de colle, préparation de surface et mise en œuvre
seringue / dispenser. Contexte : bâti aluminium (usiné ou profilé), écran
tactile (verre de protection + châssis plastique ou métal), usage intérieur,
petites séries.

---

## 1. Le problème physique avant le choix du produit

| Matériau | Coeff. de dilatation (µm/m·K) |
|---|---|
| Aluminium | ~23 |
| Verre (soda-lime / cover glass) | ~8–9 |
| ABS / PC (bezel) | ~65–70 |

Sur une diagonale collée de 200 mm et un écart de température de 40 °C,
l'aluminium bouge d'environ **0,12 mm de plus que le verre**. Une colle rigide
(époxy, cyano) transforme ce delta en contrainte de cisaillement dans le verre
→ micro-fissures, décollement en coin, écran qui « travaille » au tactile.

**Conséquence : sur l'interface écran ↔ aluminium, on veut un joint souple et
épais (≥ 1 mm), pas une colle structurale rigide.**
La colle rigide reste réservée à l'assemblage du support lui-même
(alu/alu, inserts, équerres).

---

## 2. Choix de colle selon l'interface

### 2.1 Écran (verre ou bezel plastique) → aluminium — **recommandé**

| Famille | Produits typiques | Pourquoi |
|---|---|---|
| **Polymère MS / SMP (silane-modifié)** ⭐ | Sika SikaFast / Sikaflex-552 AT, Bostik ISR 70-03, 3M 760 UV, Soudal Fix All | Souple (allongement 150–400 %), sans isocyanate ni solvant, adhère alu + verre + PC/ABS souvent sans primaire, ne fogge pas l'optique, cartouche 290 ml ou sachet |
| **Silicone neutre alcoxy** | Dowsil 739 / 3-1953, Loctite SI 5145, Elastosil E4x | Le plus souple, tenue thermique et UV, standard de l'industrie verre-métal |
| **Bande VHB acrylique** (pas une colle, mais souvent la meilleure solution) | 3M VHB 5952 (noir, 1,1 mm), 4941, 5925 | Épaisseur constante, absorbe le différentiel de dilatation, montage immédiat sans fixture, démontable au fil à couper |

> ⚠️ **Silicone : uniquement neutre (alcoxy ou oxime).** Jamais de silicone
> acétique (odeur vinaigre) : l'acide acétique corrode l'aluminium et attaque
> les pistes ITO / la nappe de l'écran.

### 2.2 Bezel en plastique basse énergie (PP, PE, TPE)

Acrylique structural 2K sans préparation :
**3M Scotch-Weld DP8005** ou **DP8010NS** (cartouche 38/45 ml, ratio 10:1,
work life ~3 min). Rigide → à réserver aux petites surfaces / plots localisés,
pas à un cordon périphérique complet sur verre.

### 2.3 Assemblage du support aluminium lui-même (alu/alu, inserts, équerres)

| Famille | Produits | Notes |
|---|---|---|
| **Époxy 2K** | 3M DP460 (long open time, très bonne tenue alu), DP490, Araldite 2011 / 2014-2 | Le plus résistant et durable sur métal bien préparé |
| **Acrylique structural 2K** | Loctite AA 330 + activateur SF 7386/7387, Plexus MA300 | Prise rapide, tolérant aux surfaces peu préparées |
| **Méthacrylate / freinfilet** | Loctite 638 (emmanchements), 243 (vis) | Pour ajustements cylindriques et vissage, pas pour du plan sur plan |

---

## 3. À proscrire près d'un écran

- **Cyanoacrylate (superglue)** — *blooming* : le monomère se vaporise et
  dépose un voile blanc sur le verre et le polariseur. Cassant, ne rattrape
  aucun jeu, aucune tenue au pelage.
- **Silicone acétique** — corrosion de l'alu et de l'électronique.
- **Colles à solvant / PVC / néoprène en bombe** — attaquent PC et PMMA
  (fissuration sous contrainte, *crazing*).
- **Époxy rigide en cordon périphérique plein sur le verre** — voir §1.
- **Colle chaude (hot melt)** — flue à 60 °C, l'écran descend en été.

---

## 4. Préparation de surface (80 % du résultat)

**Aluminium brut ou usiné**
1. Dégraisser à l'isopropanol (IPA) ou acétone, chiffon non pelucheux, un
   passage = un côté propre du chiffon.
2. Abraser : Scotch-Brite rouge ou abrasif P240–P320, en croisé, jusqu'à mat
   uniforme (on retire la couche d'oxyde faible et on augmente la surface).
3. Souffler / dépoussiérer, **re-dégraisser à l'IPA**.
4. Coller dans les **30 à 60 min** (l'oxyde se reforme).

**Aluminium anodisé** — bonne surface de collage telle quelle, dégraissage
IPA + abrasion très légère suffisent (ne pas percer l'anodisation).

**Verre de l'écran** — IPA uniquement. Pour un SMP/silicone sur verre en
usage exigeant : primaire silane (Sika Aktivator-205 puis Primer-206 G+P).

**PC / ABS** — IPA seulement (l'acétone fissure le PC). Pour PP/PE : DP8005
sans primaire, ou traitement flamme/plasma.

**VHB** — surface > 15 °C à la pose, primaire 3M Primer 94 sur alu poudré ou
plastique difficile, pression de pose **≥ 15 N/cm²** (rouleau), tenue finale
à 72 h.

---

## 5. Mise en œuvre à la seringue / au dispenser

### 5.1 Mono-composant (MS polymer, silicone) — seringue ou cartouche

| Paramètre | Valeur conseillée | Source |
|---|---|---|
| Conditionnement | seringue Luer-Lock — les tailles standard du marché sont **3 / 5 / 10 / 30 / 55 / 70 cc** ; ou cartouche 290 ml + pistolet | [Nordson EFD — Syringe barrel selection](https://www.nordson.com/en/about-us/nordson-blog/efd-blogs/022520-fluid-dispensing-101---syringe-barrel-selection) |
| Corps de seringue | **transparent** (on voit le niveau et les bulles) ; ambré pour les colles UV, noir pour les produits photosensibles | idem |
| Remplissage | incliner le corps, **ne pas dépasser les 2/3** — au-delà on emprisonne de l'air | [Nordson EFD — How to prevent air bubbles](https://www.nordson.com/en/about-us/nordson-blog/efd-blogs/how-to-prevent-air-bubbles-in-syringe-barrel-dispensing) |
| Purge avant la 1re pose | retourner la seringue **luer vers le haut**, tapoter le flanc pour faire monter les bulles, retirer le bouchon, pousser le piston lentement. Produit très visqueux : passage en centrifugeuse | [Nordson EFD — How do you purge air from a syringe barrel](https://www.nordson.com/en/divisions/efd/resources/frequently-asked-questions/how-do-you-purge-air-from-a-syringe-barrel) · [FAQ bulles](https://www.nordson.com/en/divisions/efd/resources/frequently-asked-questions/why-do-i-keep-getting-air-bubbles-in-my-syringe) |
| Aiguille / buse | tapered tip **14G (Ø int. ≈ 1,55 mm)** ou **16G (Ø int. 1,2 mm)** ; 18G = 0,86 mm, trop fin pour une pâte thixotrope. Buse conique pour un cordon de 3 mm | [Nordson EFD — Optimum dispense tips](https://www.nordson.com/en/products/efd-products/dispense-tips-and-needles) · [table des gauges](https://blog.darwin-microfluidics.com/syringe-needle-gauge-table/) |
| Dispenser pneumatique | Nordson EFD **Ultimus V** ou **Performus** — plage machine 0–7 bar (modèles basse pression 0–1 bar). **Régler à 0,5–2,5 bar** pour un MS/silicone en 14-16G et monter progressivement | [Ultimus V](https://www.nordson.com/en/products/efd-products/ultimus-v-dispensers) · [Performus](https://www.nordson.com/en/products/efd-products/performus-series-dispensers) · [UltimusPlus — manuel (PDF)](https://www.jacrawfordco.com/wp-content/uploads/2023/10/Nordson-EFD-UltimusPlus-Series-Operating-Manual-2023.pdf) |
| Cordon | Ø 3–5 mm, **discontinu** (plots ou segments de 20–30 mm espacés de 20 mm) | voir encadré ci-dessous |
| Épaisseur de joint | **1–3 mm** — c'est elle qui absorbe la dilatation | §1 |
| Contrôle d'épaisseur | cales, billes de verre calibrées 1 mm, ou plots imprimés 3D dans le support | — |
| Formation de peau | **~30 min** pour un Sikaflex-552 AT (5–40 °C) | [Sikaflex-552 AT — PDS (PDF)](https://industry.sika.com/content/dam/dms/dk01/x/sikaflex_-552_at.pdf) |
| Vitesse de cure | **2–4 mm / 24 h** à 20 °C / 50 % HR pour un MS polymer. Plus lent si l'air est froid ou sec | [MS polymer — cure times](https://qinanxgroup.com/blog/ms-polymer-sealant-curing-time-and-working-properties/) · [Méthodes de réticulation](https://bopinchem.com/sealant-curing-methods-explained-moisture-cure-reactive-uv-cure-and-more/) |

> **Pourquoi le cordon discontinu.** Ces colles réticulent par l'humidité de
> l'air, de l'extérieur vers l'intérieur. Un joint complètement confiné entre
> **deux surfaces non poreuses** — verre et métal, exactement notre cas — est
> un mode de défaillance connu : sans vapeur d'eau disponible, le cœur du
> cordon ne durcit jamais. La peau formée en surface ralentit en plus la
> diffusion vers le matériau situé dessous. D'où : segments courts, chemins
> d'air ouverts, et surtout **pas de cordon périphérique fermé**.
> Sources : [Does silicone need air to cure — INCURE](https://incurelab.com/wp/does-silicone-need-air-to-cure) ·
> [Condensation cure silicone — ScienceDirect](https://www.sciencedirect.com/topics/engineering/condensation-cure-silicone) ·
> [Température et humidité sur la cure d'un élastomère silicone — ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0142941820321966) ·
> [Kinetics of moisture cure of silicone sealants — J. Adhesion](https://www.tandfonline.com/doi/abs/10.1080/00218469808009970)

> **Note de vérification.** Les valeurs ci-dessus proviennent des extraits
> indexés de ces pages ; le proxy réseau de la session bloque l'accès direct
> à nordson.com, sika.com et à la plupart des PDF de fiches techniques.
> Recouper avec la fiche technique du lot réellement acheté avant mise en
> production.

### 5.2 Bi-composant (époxy DP460, acrylique DP8005 / AA 330)

| Paramètre | Valeur conseillée |
|---|---|
| Conditionnement | cartouche **Duo-Pak 38–50 ml**, ratio 1:1, 2:1 ou 10:1 selon produit |
| Matériel | pistolet applicateur 3M EPX (ou équivalent) + **mélangeur statique** correspondant au ratio |
| Purge | jeter les **3 à 5 premiers cm** de mélange (ratio non établi dans les premières spires) |
| Work life | DP8005 ≈ 3 min · AA 330 + activateur ≈ 3–5 min · DP460 ≈ 60 min |
| Épaisseur de joint | **0,1–0,5 mm** (colle structurale : joint fin = joint fort) |
| Maintien | brider ou scotcher jusqu'au *handling strength*, puis 24 h avant charge |
| Après usage | laisser le mélangeur en place sur la cartouche : il fait bouchon |

Températures : en dessous de 15 °C les cinétiques s'effondrent (époxy 2K
peut ne jamais atteindre sa dureté finale). Chauffer la pièce, pas la colle.

---

## 6. Règles de conception du support (ce qui compte plus que la colle)

- **Jamais la colle seule en pelage.** Prévoir une **lèvre / rebord de
  retenue** sur le support alu : la colle travaille en cisaillement, la
  géométrie encaisse le pelage et le poids.
- **Surface de collage** : viser 200–400 mm² par 100 g d'écran pour un SMP
  (contrainte de service très basse, ~0,1 MPa) — largement dimensionné.
- Cordon sur le **châssis / bezel** de l'écran plutôt que sur le verre actif
  quand c'est possible.
- Prévoir un **accès de démontage** (jeu de fil à couper, ou plots
  localisés) : un écran, ça se remplace.
- Ne pas coller par-dessus la nappe / le connecteur FPC.

---

## 7. Recette par défaut (si on ne veut pas réfléchir)

1. Support alu : dégraissage IPA → abrasion P320 → IPA.
2. **3M VHB 5952** (bandes de 12 mm, 1,1 mm d'épaisseur) sur les zones de
   contact, primaire 3M Primer 94 si l'alu est peint/poudré.
3. Complément : plots de **MS polymer** (Sikaflex-552 AT) à la seringue 14G
   dans les angles, pour l'étanchéité et la reprise d'effort.
4. Rebord de retenue mécanique en bas du support pour le poids.
5. 24 h avant manipulation, 72 h avant charge complète.

---

## 8. Cordon plat périphérique à la buse ovale — le cas « écran dans support alu »

C'est la géométrie réelle du montage d'un écran dans un cadre aluminium :
un **ruban plat continu** sur tout le pourtour du bezel.

### 8.1 Le conflit à résoudre en premier

Une buse ovale sert précisément à poser un **ruban continu**. Or (voir §5.1)
un cordon **mono-composant** réticulant à l'humidité, enfermé en boucle
fermée entre **deux surfaces non poreuses** (verre + aluminium), ne durcit
jamais à cœur. **Buse ovale + cordon fermé ⇒ il faut changer de chimie**, ou
renoncer au cordon continu.

Trois sorties possibles :

| Sortie | Chimie | Conséquence |
|---|---|---|
| **A — garder le 1K MS/silicone** | Sikaflex-552 AT, Dowsil neutre | Ruban **segmenté** (20–30 mm, espacés de 20 mm) posé à la buse ovale. Le moins cher, pas d'étanchéité périphérique |
| **B — passer en 2K** ⭐ | **Silicone 2K** ou MS/PU 2K, cartouche bi-composant + mélangeur statique + **buse plate en sortie de mélangeur** | Ruban **continu** possible, réticulation indifférente au confinement, souplesse conservée. C'est la bonne réponse si on veut à la fois le ruban plat et l'étanchéité |
| **C — UV / dual-cure** | Acrylique UV + cure humidité (type Dymax Multi-Cure) | Ruban continu, prise en secondes sous UV à travers le verre, cure « dans l'ombre » pour les zones masquées. Cycle le plus rapide, matériel le plus cher |

Mention pour mémoire : en production série, l'industrie de l'affichage
utilise massivement soit le **PUR hot-melt réactif** (Technomelt — tenue
immédiate au refroidissement puis cure humidité en 24–48 h, appliqué chaud
à la buse plate, donc sur le boîtier et non sur la dalle), soit la **mousse
adhésive prédécoupée** (3M VHB, tesa). Ni l'un ni l'autre ne se fait avec un
dispenser pneumatique de paillasse.

### 8.2 Choix de la buse ovale

Les Optimum Oval Tips sont faites pour « appliquer des rubans plats de
fluides épais — pâtes, mastics, époxy — de façon précise et constante », et
sont dimensionnées pour le débit élevé / haute viscosité.

| Gauge ovale | Largeur de ruban visée | Repère |
|---|---|---|
| 18 GA (vert) | ~1,5–2 mm | ruban fin, petits bezels |
| 14 GA (olive) | ~3 mm | cas courant écran/cadre |
| 10 GA | ≥ 4 mm | gros cadres, forte reprise de jeu |

Longueurs standard **6,35 mm (0,25")** pour le point-à-point rapide et
**12,7 mm (0,5")** pour la précision générale ; longueurs sur mesure et
versions coudées disponibles. Références types : `7024653` (ovale 18 GA
vert 0,5"), `7018036` (14 GA olive 1,5").

Règles de pose :
- **Grand axe de l'ovale perpendiculaire au sens d'avance** — sinon on pose
  un boudin, pas un ruban.
- **Face plate parallèle au substrat**, distance de travail constante
  ≈ la moitié de la hauteur de ruban visée.
- Vitesse d'avance constante : c'est elle, pas la pression, qui fixe la
  section du ruban une fois la pression réglée.
- Le hub SafetyLok se visse à fond sur le corps de seringue ; le raccord est
  affleurant côté fluide pour ne pas piéger d'air.
- ⚠ Les **couleurs de hub ne sont pas normalisées** entre fabricants : se
  fier au gauge marqué.

### 8.3 Choix du dispenser

| Appareil | Plage | Pour quoi |
|---|---|---|
| **Performus** | 0–7 bar (modèles 0–1 bar) | Prototypage, petites séries, réglage manuel |
| **Ultimus V** | 0–7 bar, haute précision, profils programmables | Plusieurs tailles d'écran / plusieurs recettes mémorisées |
| **UltimusPlus I-II** ⭐ | 0–7 bar, régulation en boucle fermée | Production répétable : la pression est tenue malgré la vidange du corps de seringue — c'est ce qui garde une section de ruban constante sur tout le tour |

Réglage de départ pour un MS/silicone en buse ovale 14 GA : **1,5–3 bar**,
monter progressivement jusqu'à obtenir la section visée à vitesse d'avance
constante. Si 7 bar ne suffisent pas (pâte > ~300 000 mPa·s à travers une
fente ovale), ne pas forcer : passer d'une seringue 30–55 cc à un **système
à cartouche / réservoir** ou à une **pompe volumétrique** (cavité
progressive). Le pneumatique sur seringue a une limite physique ici.

### 8.4 Buse ovale **sur seringue** — ce que ça impose

Configuration retenue : **Optimum Oval Tip inox, hub SafetyLok, vissée sur un
corps de seringue Luer**, alimentée par un dispenser pneumatique.

Conséquence directe : **une seringue ne contient qu'un produit déjà prêt.**
Il n'y a pas de mélangeur statique dans la chaîne. Donc l'option B de §8.1
(2K en cartouche bi-composant) **n'est pas accessible avec ce matériel**, sauf
à pré-mélanger le 2K dans la seringue — possible, mais on travaille alors
contre la pot life et il faut dégazer en centrifugeuse avant de poser.

Le tableau se réduit donc à ceci :

| Produit en seringue | Ruban continu fermé ? | Verdict |
|---|---|---|
| **1K MS / silicone neutre** | **Non** — réticule par l'humidité, cœur jamais durci en boucle fermée (§5.1) | Ruban **segmenté** obligatoire |
| **1K acrylique UV / dual-cure** (type Dymax Multi-Cure) | **Oui** | ⭐ **La seule chimie qui fait un tour complet avec ce matériel.** Prise sous UV à travers le verre, cure « dans l'ombre » pour les zones masquées par le cadre alu |
| 2K pré-mélangé en seringue | Oui | Dépannage / petites séries. Dégazage centrifugeuse + surveiller la pot life |

⚠️ Avec un produit UV : **corps de seringue ambré obligatoire** (il bloque
les UV et laisse passer moins de 12 % de lumière visible sous 550 nm), sinon
le produit réticule dans la seringue. Corps noir pour les produits totalement
photosensibles.

### 8.5 Liste de matériel et mise en route

**Matériel**
- Corps de seringue **30 cc** — transparent pour un MS/silicone, **ambré**
  pour un UV. Piston assorti.
- **Optimum Oval Tip 14 GA**, longueur 0,5" (réf. type `7018036` en 14 GA
  olive ; `7024653` en 18 GA vert pour un ruban plus fin).
- Dispenser **UltimusPlus I-II** (régulation en boucle fermée — c'est elle
  qui garde la section constante sur tout le tour).
- Bouchons de seringue, clé de serrage douce, coupons alu de réglage.

**Mise en route, dans l'ordre**
1. Remplir le corps **incliné, aux 2/3 maximum**.
2. Purger : **luer vers le haut**, tapoter le flanc, retirer le bouchon,
   pousser le piston lentement. Produit épais : centrifugeuse.
3. Visser la buse ovale à fond (SafetyLok), **grand axe perpendiculaire au
   sens d'avance**.
4. Démarrer à **1,5 bar**. Régler le *vacuum / suck-back* du dispenser pour
   éviter la goutte en fin de course — indispensable sur un parcours fermé.
5. Poser 100 mm d'essai sur un **coupon alu**, couper le ruban en travers,
   mesurer largeur et hauteur au pied à coulisse.
6. Corriger par pas de **0,3 bar** et ajuster la vitesse d'avance jusqu'à la
   section visée. À pression figée, **c'est la vitesse qui fixe la section.**
7. Consigner : pression, vitesse, gauge, température ambiante. Reprendre ces
   valeurs à chaque lot — et les revalider si le lot de colle change.

### 8.4 Note sur les écrans tonwelt

tonwelt (Berlin) fournit des solutions de médiation : guides audio et
multimédia, dont le **supraGuide TOUCH** — un appareil **portatif** à écran
tactile — ainsi que des stations fixes. Les deux cas ne sollicitent pas le
collage de la même façon :

- **Appareil portatif** → la charge dimensionnante est le **choc de chute**,
  pas la dilatation (un écran de 4–5" ne génère qu'un différentiel
  négligeable). Privilégier un joint **souple et amortissant** sur tout le
  pourtour (2K silicone, ou mousse adhésive) et une retenue mécanique.
- **Station fixe / grand écran** → la dilatation différentielle redevient
  dimensionnante (§1), joint souple **1–3 mm** obligatoire.

Demander à tonwelt la **matière exacte du pourtour** de la dalle (verre nu,
bezel PC/ABS, cadre métal) : c'est elle qui décide du primaire, pas
l'aluminium.

---

## 9. Ruban continu sous cadre opaque — la solution retenue

Choix arrêté : **ruban périphérique continu**, buse ovale sur seringue.
Le cordon est donc enfermé entre le verre et un **cadre aluminium opaque**.
Deux mécanismes de réticulation sont alors hors-jeu :

- **l'humidité** (1K MS, silicone) — pas de vapeur d'eau au cœur (§5.1) ;
- **les UV seuls** — la lumière n'atteint pas la zone masquée par le cadre.

Y compris les **dual-cure à seconde cure humidité** : leur mécanisme de
secours est justement celui qui échoue en joint confiné. Le « dual-cure »
n'est pas une réponse automatique ici.

### 9.1 La réponse : époxy cationique à pré-activation

**DELO KATIOBOND** — époxy à polymérisation **cationique**. Une fois
amorcée par la lumière, la réaction se poursuit seule à température
ambiante, **sans nouvel apport de lumière ni d'humidité**. C'est le seul
mécanisme des quatre qui traverse un joint totalement confiné.

**Procédé de pré-activation** (« polymérisation vivante ») — c'est lui qui
règle le problème des pièces opaques :

1. Poser le ruban continu à la buse ovale sur le cadre alu.
2. **Pré-activer** le cordon à la lampe, **avant assemblage** — ordre de
   grandeur : **2 s à 1 000 mW/cm²**.
3. Pendant le *temps ouvert*, la colle reste fluide : on présente et on
   positionne l'écran tranquillement.
4. Assembler, puis **post-illumination ~5 s à 5 000 mW/cm²** (sur la tranche
   accessible) pour la tenue à la manipulation.
5. **Cure complète à température ambiante**, sans rien d'autre.

Tenue en température jusqu'à 180 °C, faible retrait.

### 9.2 La limite à vérifier avant de commander : la taille de l'écran

Un époxy cationique est **rigide**. On retombe donc sur §1. Le
déplacement différentiel à l'extrémité du collage vaut
`δ = Δα × (L/2) × ΔT`, avec `Δα ≈ 14 µm/m·K` (alu − verre) ; la déformation
de cisaillement dans le joint vaut `γ = δ / e`, `e` = épaisseur de colle.

| Diagonale L | δ à ΔT = 40 °C | γ avec e = 0,2 mm | Verdict |
|---|---|---|---|
| 100 mm | 0,028 mm | ~14 % | Acceptable |
| 150 mm | 0,042 mm | ~21 % | Limite |
| 300 mm | 0,084 mm | ~42 % | **Non** — le verre casse |

> **Règle :** ruban continu **rigide** acceptable jusqu'à ~**150 mm de
> diagonale**. Au-delà, il faut rester souple.

### 9.3 Et si l'écran est grand ?

« Continu **+** souple **+** durcit à l'ombre » n'existe pas en 1K seringue.
Il faut alors sortir de ce matériel :

- **Mousse adhésive prédécoupée** (3M VHB, tesa) — continue, souple,
  **aucune réticulation à attendre**. C'est la réponse propre au grand écran.
- **Silicone 2K** en cartouche + mélangeur statique — souple et insensible
  au confinement, mais demande un pistolet 2K, pas une seringue.

### 9.4 Produit écarté, et pourquoi

**Dymax Dual-Cure 3401** revient souvent dans les recherches (UV + humidité,
dispo en seringue 30 ml). Il ne convient pas ici, pour deux raisons
indépendantes :

- **Viscosité nominale 150 cP** — c'est quasiment de l'eau. Impossible de
  tenir un ruban de 3 mm à la buse ovale : ça coule avant la pré-activation.
- **Dureté Shore D 55-75, allongement à la rupture 13 %** — rigide et peu
  déformable, donc soumis à la même limite de diagonale que le Katiobond,
  sans son avantage de cure à l'ombre.

### 9.5 Matériel à ajouter

- Corps de seringue **ambré** — obligatoire pour un produit photosensible,
  sinon il réticule dans la seringue.
- **Lampe de pré-activation** (~1 000 mW/cm²) + **lampe de
  post-illumination** (~5 000 mW/cm²), à la longueur d'onde du grade retenu.
- Grade **thixotrope** impératif — demander le grade « tenue de cordon » à
  DELO, un grade fluide ne fera pas de ruban.
- Pression de départ en 14 GA ovale : commencer à **1,5 bar** et régler
  par la méthode du coupon (§8.5). La viscosité varie beaucoup d'un grade à
  l'autre, il n'y a pas de valeur universelle à recopier.

## 10. Solution retenue : bande VHB — liste d'achat

Décision : **bande adhésive double face**, pas de colle liquide. Tout le
problème de réticulation (§5.1, §9) disparaît — une bande n'a rien à faire
durcir. Elle est **continue**, **souple** (elle encaisse la dilatation
différentielle à n'importe quelle diagonale) et **immédiate**.

### 10.1 Consommables

| Article | Référence | Pour quoi |
|---|---|---|
| **Ruban VHB** | **3M VHB 5952**, noir, **1,1 mm**, largeur 12 mm, rouleau 33 m | Le cœur du montage. Mousse acrylique conformable, formulée métaux / plastiques / peintures poudrées |
| Variante plus épaisse | 3M VHB **5962F**, 1,6 mm | Si l'écran est grand ou le support peu plan : plus d'épaisseur = plus de souplesse |
| **Primaire** | **3M Primer 94**, flacon 236 ml (ou ampoules 0,66 ml) | **Seulement** si l'alu est peint ou poudré, ou sur plastique difficile. Sèche en moins d'une minute |
| Dégraissant | Isopropanol (IPA) + chiffons non pelucheux | Avant et après abrasion |
| Abrasif | Scotch-Brite rouge ou abrasif P320 | Retirer l'oxyde faible de l'alu |
| Rouleau applicateur | Rouleau caoutchouc dur | Appliquer les 15 N/cm² de pression de pose |
| Démontage | Fil à couper (nylon ou acier fin) | Un écran, ça se remplace |

**Quantité** : le périmètre d'un écran ~10" (220 × 130 mm) fait environ
700 mm. Un rouleau de 33 m couvre donc une cinquantaine d'écrans — un seul
rouleau suffit largement pour un prototype et une petite série.

### 10.1 bis — Largeur de bande : ne pas confondre avec l'épaisseur

Deux dimensions distinctes, et c'est la source d'erreur classique :

- **Épaisseur = 1,1 mm** — fixée par la référence (5952). C'est elle qui
  donne la souplesse et absorbe la dilatation. On n'y touche pas.
- **Largeur = 6 / 9 / 12 / 19 mm** — c'est la bande posée à plat le long du
  cadre. Elle se choisit sur la **largeur de portée réelle du bezel**.

**La largeur n'est pas un problème de tenue.** Sur un périmètre de 700 mm,
même une bande de 3 mm donne 2 100 mm² de surface collée — plusieurs
centaines de newtons de résistance au cisaillement, pour un écran qui pèse
quelques newtons. Le choix de largeur est une question de **portée
disponible sur le cadre** et de **facilité de pose**, pas de résistance.

| Largeur de portée du cadre | Solution |
|---|---|
| ≥ 12 mm | Rouleau 12 mm — le plus simple |
| 6–10 mm | Rouleau **6 mm** ou 9 mm |
| 3–5 mm | Découpe sur mesure (refente) chez un converter |
| < 3 mm | **Joint cadre découpé d'une seule pièce** — impossible à poser en rouleau à la main, et c'est de toute façon la solution des fabricants d'écrans : un cadre prédécoupé se pose aligné du premier coup |

Le 5952 est d'ailleurs référencé par 3M pour l'*electronic screen bonding*
et le *frame panel bonding* — c'est son emploi d'origine. Il est disponible
en rouleaux standard et sur mesure, et « en formes et tailles illimitées »
via le réseau de converters 3M. Compter une tolérance de 1 à 2 mm sur le
premier rouleau d'une refente sur mesure.

### 10.2 Où acheter (France)

- **[Farnell FR — VHB 5952 noir, 33 m × 12 mm](https://fr.farnell.com/3m/5952-black-33m-x-12mm/ruban-double-face-33m-x-12mm-noir/dp/3935789)** — exactement la référence visée
- [RS France — VHB 5952F, 11 m × 19 mm × 1,1 mm](https://fr.rs-online.com/web/p/rubans-mousse/1634731) · [VHB 5962F, 33 m × 12 mm × 1,6 mm](https://fr.rs-online.com/web/p/rubans-mousse/1747320)
- [Rubix — Ruban 3M VHB 5952](https://fr.rubix.com/fr/ruban-5952-3m-vhb/p-G5015002667)
- [Strong Adhésifs — VHB 5952, découpe **sur mesure**](https://www.strongadhesifs.com/608-ruban-adhesif-double-face-3m-vhb-5952.html) — utile pour des bandes prédécoupées à la largeur du bezel
- [Comptoir des Pros — VHB 5952F](https://www.comptoirdespros.com/ruban-adhesif-double-face-3mtm-vhbtm-5952f-noir.html)
- [3M France — fiche produit 5952](https://www.3mfrance.fr/3M/fr_FR/p/d/b40065688/) · [fiche technique FR (PDF)](https://multimedia.3m.com/mws/media/692359O/mousse-double-face-vhb-5952.pdf) · [TDS 3M (PDF)](https://multimedia.3m.com/mws/media/2528070O/3m-vhb-tape-5952.pdf?fn=3M-VHB-Tape-5952.pdf)
- **Rouleau étroit** : [SKS — 5952F noir, **6 mm** × 33 m](https://www.shop-sks.com/fr/3M-VHB-ruban-adhesif-5952F-noir-6-mm-x-33-m-1-1-mm) · [12 mm × 33 m](https://www.shop-sks.com/fr/3M-VHB-Ruban-adhesif-5952F-noir-12-mm-x-33-m-1-1-mm)

Primer 94 : [3M — fiche produit](https://www.3m.com/3M/en_US/p/d/b40065491/) ·
[FXbrands (UE), flacon 236 ml](https://www.fxbrands.eu/3mtm-94-primer-for-vhbtm-tape-236-ml.html) ·
[ampoules 0,66 ml](https://www.fxbrands.eu/3mtm-94-primer-for-vhb-tape-ampoule-066-ml.html)

### 10.3 Procédure de pose

1. Alu : **IPA → abrasion P320 → IPA**. Primer 94 seulement si peint/poudré,
   laisser sécher < 1 min.
2. Surface et pièces à **plus de 15 °C**.
3. Poser la bande sur le **support alu** d'abord, liner encore en place.
4. Retirer le liner, présenter l'écran, **presser au rouleau à 15 N/cm²
   minimum** — c'est la pression qui fait l'adhérence, pas le temps d'attente.
5. Tenue immédiate à la manipulation ; **résistance finale à 72 h**.
6. **Rebord de retenue mécanique** en bas du support : la bande travaille en
   cisaillement, jamais en pelage.

## Sources

- [Permabond — Bonding glass to metal](https://permabond.com/bonding-glass-to-metal/)
- [Permabond — How to prepare & bond glass](https://permabond.com/resource-center/prepare-bond-glass-industrial-adhesive)
- [3M — Acrylic structural adhesives, features and advancements (PDF)](https://multimedia.3m.com/mws/media/1586274O/iatd-structural-acrylic-features-recent-advancements-wp.pdf)
- [3M Scotch-Weld DP8005 — fiche produit](https://www.3m.com/3M/en_US/p/d/b40066451/)
- [3M Scotch-Weld DP460 — Technical Data Sheet (PDF)](https://multimedia.3m.com/mws/media/2365880O/3m-scotch-weld-epoxy-adhesive-dp460-off-white.pdf)
- [3M — Structural adhesives / acrylic adhesives](https://www.3m.com/3M/en_US/bonding-and-assembly-us/structural-adhesives/acrylic-adhesives/)
- [US 11604491 — Display cover glass/cell attachment to frame](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11604491) (bracket collé au cover glass via adhésif mousse, pour absorber les concentrations de contrainte et le différentiel de dilatation)

### Buses ovales et dispensers (§8)

- [Nordson EFD — Optimum Oval Tips](https://www.nordson.com/en/products/efd-products/optimum-oval-tips)
- [Nordson EFD — Dispense Tips and Needles](https://www.nordson.com/en/products/efd-products/dispense-tips-and-needles)
- [Nordson EFD — Optimum Angled Tips](https://www.nordson.com/en/products/efd-products/optimum-angled-tips)
- [Nordson EFD — Optimum Components brochure (PDF)](https://www.jacrawfordco.com/wp-content/uploads/2019/09/Nordson-EFD-Optimum-Component-Brochure-1.pdf)
- [Nordson EFD — catalogue Dispensing Tips (DirectIndustry)](https://pdf.directindustry.com/pdf/nordson-efd/dispensing-tips/35688-146801.html)
- [Référence ovale 18 GA vert 0,5\" — 7024653](https://www.testequity.com/product/10161845-7024653)
- [Nordson EFD — UltimusPlus I-II](https://www.nordson.com/en/products/efd-products/ultimusplus-i-ii-dispensers)
- [Nordson EFD — Ultimus V](https://www.nordson.com/en/products/efd-products/ultimus-v-dispensers)
- [Nordson EFD — Performus Series](https://www.nordson.com/en/products/efd-products/performus-series-dispensers)
- [Component Supply — les couleurs de hub ne sont pas normalisées](https://www.componentsupplycompany.com/needle-hub-colors-and-gauge-sizes-component-supplys-guide/)

### Ruban continu, cure à l'ombre (§9)

- [DELO KATIOBOND — page produit](https://www.delo-adhesives.com/us/adhesives/delo-katiobond-uv-adhesive/)
- [Inseto — DELO KATIOBOND, époxy cationique UV et à activation lumineuse](https://www.inseto.com/adhesives/uv-cured-and-light-activated-epoxies-delo-katiobond/)
- [Inseto — colles à activation lumineuse (pré-activation, temps ouvert)](https://www.inseto.com/adhesives/light-activated-adhesives/)
- [Inseto — DELO DUALBOND, dual-cure](https://www.inseto.com/adhesives/dual-curing-adhesives-delo-dualbond/)
- [Supratec Syneo — DELO KATIOBOND](https://www.supratec-syneo.com/en/technical-adhesives/uv-photosensibles/epoxy/)
- [Dymax — Dual-Cure Technology](https://dymax.com/about-dymax/working-with-dymax/innovations/dual-cure-technology)
- [Dymax 3401 — PDS (PDF)](https://dymax.com/content/download/3763/file/3401%20PDS.pdf) · [fiche Gluespec (viscosité 150 cP, Shore D 55-75, allongement 13 %)](https://www.gluespec.com/Materials/adhesive/dymax/dual-cure-3401)
- [Dymax 9702 — colle optique pour afficheurs plats](https://dymax.com/products/formulations/light-curable-materials/bonding/dissimilar-substrate-bonding/9702)

### PUR hot-melt réactif et écrans tonwelt (§8)

- [3M — PUR adhesives (polyuréthane réactif)](https://www.3m.com/3M/en_US/bonding-and-assembly-us/structural-adhesives/pur-adhesives/)
- [Henkel Technomelt PUR — guide produit](https://www.hotmelt.com/blogs/blog/complete-product-guide-to-henkel-loctite-technomelt-pur-polyurethane-adhesives)
- [tonwelt — site produits](https://tonwelt.com/)
- [tonwelt — supraGuide TOUCH](https://tonwelt.com/produkte/audio-und-multimediaguides/supraguide-touch/)
