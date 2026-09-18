# Liste Mouser complète - audioguide Tonwelt / Linkx TG-288 et sa valise de charge

Tableau unique, avec le lien Mouser en clair à côté de chaque ligne.
Consolide `mouser-tonwelt-linkx-tg288.md` et `mouser-electromecanique-tonwelt.md`.

Colonne **Statut** : `Vu` = visible sur les 15 photos macro de la carte ·
`Photo ext.` = identifié sur des photos analysées hors de ce dépôt ·
`Documenté` = attesté par la fiche produit TG-288, pas photographié ·
`À confirmer` = point de départ catalogue, une mesure reste à faire.

## Commandable chez Mouser

| Composant | Référence fabricant | Statut | Recherche Mouser |
|---|---|---|---|
| Prise alimentation DIN puissance 4 contacts, coudée **blindée** | Kycon KPJX-4S-S | Photo ext. | https://www.mouser.fr/c/?q=KPJX-4S-S |
| idem, non blindée | Kycon KPJX-4S | Variante | https://www.mouser.fr/c/?q=KPJX-4S |
| idem, montage sur panneau | Kycon KPJX-PM-4S-S | Variante | https://www.mouser.fr/c/?q=KPJX-PM-4S-S |
| Fiche mâle d'accouplement (cordon) | Kycon KPPX-4P | Variante | https://www.mouser.fr/c/?q=KPPX-4P |
| Prise jack 3,5 mm traversante | Same Sky SJ-43514 | Documenté | https://www.mouser.fr/c/?q=SJ-43514 |
| Prise jack 3,5 mm CMS | Same Sky SJ-43514-SMT-TR | Documenté | https://www.mouser.fr/c/?q=SJ-43514-SMT-TR |
| Micro-USB B, CMS coudée | Amphenol 10118193-0001LF | Documenté | https://www.mouser.fr/c/?q=10118193-0001LF |
| Micro-USB B, variante | Amphenol 10118192-0001LF | Variante | https://www.mouser.fr/c/?q=10118192-0001LF |
| Micro-USB B, variante | Amphenol 10118194-0001LF | Variante | https://www.mouser.fr/c/?q=10118194-0001LF |
| Mini-USB B 5 contacts | Molex 54819-0519 | À confirmer | https://www.mouser.fr/c/?q=54819-0519 |
| USB-C 16 contacts traversante | GCT USB4085-GF-A | À confirmer | https://www.mouser.fr/c/?q=USB4085-GF-A |
| Fusible réarmable PPTC 1812 | Bourns série MF-MSMF | À confirmer | https://www.mouser.fr/c/?q=MF-MSMF |
| Fusibles PPTC - catalogue complet | - | - | https://www.mouser.fr/c/?q=fusible%20PPTC%201812 |
| Haut-parleur Ø15 mm 8 Ω | PUI Audio AS01508MR-6-R | À confirmer | https://www.mouser.fr/c/?q=AS01508MR-6-R |
| Haut-parleurs - catalogue | - | - | https://www.mouser.fr/c/?q=haut-parleur%2015mm%208%20ohm |
| Bouton poussoir CMS (ceux de la carte) | Alps SKRPACE010 | **Vu** | https://www.mouser.fr/c/?q=SKRPACE010 |
| Bouton poussoir traversant 6 × 6 mm | Omron B3F-1000 | À confirmer | https://www.mouser.fr/c/?q=B3F-1000 |
| Antenne UHF hélicoïdale CMS | TE / Linx ANT-868-VHETH | Documenté | https://www.mouser.fr/c/?q=ANT-868-VHETH |
| Antenne UHF monopole embarqué Ø7 mm | TE / Linx ANT-868-JJB-ST | Documenté | https://www.mouser.fr/c/?q=ANT-868-JJB-ST |
| Antenne UHF planaire CMS | TE / Linx ANT-868-SP | Documenté | https://www.mouser.fr/c/?q=ANT-868-SP |
| Antennes 868 MHz - catalogue | - | - | https://www.mouser.fr/c/?q=antenne%20868%20MHz |
| Inductance blindée 4,7 µH 4×4 (étage boost) | Bourns SRN4018-4R7M | **Vu** | https://www.mouser.fr/c/?q=SRN4018-4R7M |
| Condensateurs MLCC CMS - catalogue | Murata, Yageo, KEMET | **Vu** | https://www.mouser.fr/c/?q=MLCC%200805 |
| Kits de condensateurs | - | - | https://www.mouser.fr/c/?q=capacitor%20kit |
| Résistances CMS - catalogue | Yageo RC0805, Vishay CRCW0805 | **Vu** | https://www.mouser.fr/c/?q=RC0805 |
| Kits de résistances CMS | - | - | https://www.mouser.fr/c/?q=resistor%20kit%200805 |
| Accus AA Ni-MH (**la réparation la plus probable**) | gamme Panasonic Ni-MH | - | https://www.mouser.fr/c/?q=Panasonic%20NiMH%20AA |
| MCU TI MSP430FR2xxx - famille | référence exacte à relire sur la puce | À confirmer | https://www.mouser.fr/c/?q=MSP430FR2 |

## Non distribué par Mouser

| Composant | Pourquoi | Où l'obtenir |
|---|---|---|
| SoC RF UHF `Linkx eTour-07 2003B`, QFN-32 | Puce propriétaire marquée au nom du produit | Linkx Electronics / Tonwelt (SAV) |
| Driver LCD `HOLTEK HT16C21` | Mouser ne distribue pas Holtek | TME, LCSC |
| TCXO `24.04 AK AD` (24,04 MHz) | Fréquence hors catalogue | Fabricant d'oscillateurs sur commande |
| `19AKM` (SOT-23-5, boost) | Code CMS absent des bases publiques | À identifier par brochage avant toute recherche |
| `CDV 221 A5L2` (SOP-8) | idem | idem |
| `724 2G SU` (SOP-8) | idem | idem |
| `BSG· TI 8A8 A46R` (QFN-16) | CI TI, code boîtier insuffisant | Décodage TI nécessaire |

## Mesures restantes

| Ligne | Mesure | Ce qu'elle tranche |
|---|---|---|
| Prise d'alimentation | Bague en façade : ~12,9 mm et corps ~15 × 17 mm → KPJX ; ~9,5 mm → mini-DIN (autre famille, ~1 A) | Série. Puis 4 contacts + 2 ergots + languette de masse → version blindée |
| Jack 3,5 mm | 3 ou 4 contacts, traversant ou CMS | Référence |
| Fusible | Marquage, dimensions, réarmable ou verre, courant de maintien | Famille entière |
| Haut-parleur | Diamètre, impédance (8 ou 32 Ω), épaisseur | Référence |
| Antenne | Bande réelle : 863-865 MHz (Europe) ou 902-928 MHz (US) | Une antenne hors bande dégrade fortement la portée |
| MCU | Marquage complet à la loupe | Référence - mais le MCU est programmé en usine, le remplacer ne répare rien sans le firmware |

> Prix et stocks non repris ici : ils changent, à lire sur les pages produit au moment de commander.
