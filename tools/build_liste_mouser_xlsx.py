from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

F = "Arial"
HDR_FILL = PatternFill("solid", fgColor="1F3864")
HDR_FONT = Font(name=F, size=10, bold=True, color="FFFFFF")
TITLE = Font(name=F, size=14, bold=True, color="1F3864")
SUB = Font(name=F, size=9, italic=True, color="555555")
BODY = Font(name=F, size=10)
BOLD = Font(name=F, size=10, bold=True)
LINK = Font(name=F, size=9, color="0563C1", underline="single")
INPUT_FILL = PatternFill("solid", fgColor="FFFF00")
ALT = PatternFill("solid", fgColor="F2F5FA")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

wb = Workbook()

# ─────────────────────────── Feuille 1 : liste Mouser ───────────────────────────
ws = wb.active
ws.title = "Liste Mouser"

rows = [
 ("Prise alimentation DIN puissance 4 contacts, coudée BLINDÉE","KPJX-4S-S","Kycon","Photo ext.","https://www.mouser.fr/c/?q=KPJX-4S-S"),
 ("Fiche mâle d'accouplement (réfection du cordon)","KPPX-4P","Kycon","Variante","https://www.mouser.fr/c/?q=KPPX-4P"),
 ("Prise jack 3,5 mm, CMS","SJ-43514-SMT-TR","Same Sky (CUI Devices)","Documenté","https://www.mouser.fr/c/?q=SJ-43514-SMT-TR"),
 ("Micro-USB B, CMS coudée","10118193-0001LF","Amphenol FCI","Documenté","https://www.mouser.fr/c/?q=10118193-0001LF"),
 ("Micro-USB B, variante de montage","10118192-0001LF","Amphenol FCI","Variante","https://www.mouser.fr/c/?q=10118192-0001LF"),
 ("Micro-USB B, variante de montage","10118194-0001LF","Amphenol FCI","Variante","https://www.mouser.fr/c/?q=10118194-0001LF"),
 ("Mini-USB B, 5 contacts","54819-0519","Molex","À confirmer","https://www.mouser.fr/c/?q=54819-0519"),
 ("Poussoir tactile CMS bas profil - série SKRW","série SKRW","Alps Alpine","Vu","https://www.mouser.fr/fr/new/alps-alpine/alps-alpine-skrw-tact-switches/"),
 ("Poussoir SKRW - variantes 50k / 500k / 1000k cycles","SKRWAEE030 · SKRWAME030 · SKRWADE030","Alps Alpine","À confirmer","https://www.mouser.fr/c/?q=SKRW"),
 ("Fusible réarmable PPTC, boîtier 1812","série MF-MSMF","Bourns","À confirmer","https://www.mouser.fr/c/?q=MF-MSMF"),
 ("Fusibles PPTC - catalogue complet","n/a","n/a","Catalogue","https://www.mouser.fr/c/?q=fusible+PPTC+1812"),
 ("Haut-parleurs - catalogue","n/a","n/a","Catalogue","https://www.mouser.fr/c/?q=haut-parleur+15mm+8+ohm"),
 ("Antenne UHF hélicoïdale CMS","ANT-868-VHETH","TE / Linx","Documenté","https://www.mouser.fr/c/?q=ANT-868-VHETH"),
 ("Antennes 868 MHz - catalogue","n/a","n/a","Catalogue","https://www.mouser.fr/c/?q=antenne+868+MHz"),
 ("Batterie lithium plate - cellule relevée n°1 (carte à ressort d'antenne)","JHY632570 · 3,7 V · 1300 mAh · 6,3×25×70 mm","JHY","Vu","https://www.mouser.fr/c/?q=3.7V+Lipo+Battery"),
 ("Batterie lithium plate - cellule relevée n°2 (carte Eco 2.0, USB-C)","sans référence · 3,87 V · 1000 mAh","n/a","Vu","https://www.mouser.fr/c/?q=3.8V+Lipo+Battery"),
 ("Batterie lithium plate - cellule relevée n°4","LIDIO 355485 · 3,8 V · 2500 mAh · 3,5×54×85 mm","LIDIO","Vu","https://www.mouser.fr/c/?q=3.8V+Lipo+Battery"),
 ("Attention : Aucune de ces cellules n'est distribuée par Mouser - voir docs/batteries-lithium-tonwelt.md","JHY et LIDIO = fabricants OEM","n/a","Hors Mouser","https://www.mouser.fr/c/?q=lithium+polymer+battery+pack"),
 ("Inductance blindée 4,7 µH, 4×4 mm (étage boost)","SRN4018-4R7M","Bourns","Vu","https://www.mouser.fr/c/?q=SRN4018-4R7M"),
 ("Condensateurs MLCC CMS - catalogue","0603 / 0805 / 1206","Murata, Yageo, KEMET","Vu","https://www.mouser.fr/c/?q=MLCC+0805"),
 ("Kits de résistances CMS","n/a","n/a","Catalogue","https://www.mouser.fr/c/?q=resistor+kit+0805"),
 ("MCU TI MSP430FR2xxx - famille","réf. exacte à relire sur la puce","Texas Instruments","À confirmer","https://www.mouser.fr/c/?q=MSP430FR2"),
]

ws["A1"] = "Liste Mouser - audioguide Tonwelt / Linkx et sa valise de charge"
ws["A1"].font = TITLE
ws["A2"] = ("Liste arrêtée par l'utilisateur (16 lignes retenues sur 31), plus les poussoirs SKRW et la batterie lithium.  Prix et stocks absents : ils changent.  "
            "Colonne E (Qté) en jaune : à compléter, nombre entier, ex. 2.  Colonne F : adresse en clair, à copier-coller.  Colonne G : cliquer sur « Ouvrir ».")
ws["A2"].font = SUB
ws.merge_cells("A1:F1"); ws.merge_cells("A2:F2")

hdr = ["Composant", "Référence fabricant", "Fabricant", "Statut", "Qté", "Lien Mouser (recherche par référence)"]
HR = 4
for c, h in enumerate(hdr, 1):
    cell = ws.cell(row=HR, column=c, value=h)
    cell.font = HDR_FONT; cell.fill = HDR_FILL; cell.border = BORDER
    cell.alignment = Alignment(vertical="center", horizontal="center")
ws.row_dimensions[HR].height = 22

for i, (comp, ref, fab, stat, lien) in enumerate(rows):
    r = HR + 1 + i
    vals = [comp, ref, fab, stat, None, lien]
    for c, v in enumerate(vals, 1):
        cell = ws.cell(row=r, column=c, value=v)
        cell.border = BORDER
        cell.font = BOLD if (c == 2 and ref != "n/a") else BODY
        cell.alignment = Alignment(vertical="top", wrap_text=(c == 1))
        if i % 2: cell.fill = ALT
    ws.cell(row=r, column=5).fill = INPUT_FILL
    ws.cell(row=r, column=5).alignment = Alignment(horizontal="center", vertical="top")
    link = ws.cell(row=r, column=6)
    link.hyperlink = lien; link.font = LINK
    link.alignment = Alignment(vertical="top")
    # Colonne G : formule HYPERLINK - cliquable dans Excel, LibreOffice et Google Sheets,
    # y compris là où les liens natifs ne sont pas activés (mode protégé, visionneuse mobile).


last = HR + len(rows)
ws.auto_filter.ref = f"A{HR}:F{last}"
ws.freeze_panes = f"A{HR+1}"
for col, w in zip("ABCDEF", [46, 26, 22, 13, 7, 48]):
    ws.column_dimensions[col].width = w

# ─────────────────────────── Feuille 2 : hors Mouser ───────────────────────────
ws2 = wb.create_sheet("Hors Mouser")
ws2["A1"] = "Composants non distribués par Mouser"
ws2["A1"].font = TITLE
ws2.merge_cells("A1:C1")
hors = [
 ("Écran LCD à segments, ~19 broches soudées en ligne","Verre SUR MESURE : pictogrammes propres au produit (cadenas, pile, CH, 2 digits 7 segments, haut-parleur + bargraphe 4 barres). Aucun équivalent catalogue, chez Mouser ni ailleurs.","Linkx / Tonwelt (SAV), ou refabrication sur plan par un fabricant de LCD sur mesure"),
 ("SoC RF UHF « Linkx eTour-07 2003B », QFN-32","Puce propriétaire marquée au nom du produit","Linkx Electronics / Tonwelt (SAV)"),
 ("Driver LCD « HOLTEK HT16C21 », SOP","Mouser ne distribue pas Holtek","TME, LCSC"),
 ("TCXO « 24.04 AK AD » - 24,04 MHz","Fréquence hors catalogue","Fabricant d'oscillateurs, sur commande"),
 ("« 19AKM » - SOT-23-5, convertisseur boost","Code CMS absent des bases publiques","À identifier par brochage avant toute recherche"),
 ("« CDV 221 A5L2 » - SOP-8","Code CMS non résolu","idem"),
 ("« 724 2G SU » - SOP-8","Code CMS non résolu","idem"),
 ("« BSG· TI 8A8 A46R » - QFN-16","CI Texas Instruments, code boîtier insuffisant","Décodage TI nécessaire"),
]
for c, h in enumerate(["Composant", "Pourquoi", "Où l'obtenir"], 1):
    cell = ws2.cell(row=3, column=c, value=h)
    cell.font = HDR_FONT; cell.fill = HDR_FILL; cell.border = BORDER
    cell.alignment = Alignment(vertical="center", horizontal="center")
ws2.row_dimensions[3].height = 22
for i, row in enumerate(hors):
    for c, v in enumerate(row, 1):
        cell = ws2.cell(row=4+i, column=c, value=v)
        cell.font = BODY; cell.border = BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        if i % 2: cell.fill = ALT
for col, w in zip("ABC", [44, 46, 40]):
    ws2.column_dimensions[col].width = w
ws2.freeze_panes = "A4"

# ─────────────────────── Feuille 3 : mesures restantes ───────────────────────
ws3 = wb.create_sheet("Mesures restantes")
ws3["A1"] = "Mesures à faire avant de commander"
ws3["A1"].font = TITLE
ws3.merge_cells("A1:C1")
mes = [
 ("Prise d'alimentation","Plan de perçage constructeur à comparer trou par trou : https://www.mouser.com/datasheet/3/166/1/KPJX.pdf  -  Diamètre extérieur de la bague en façade : ~12,9 mm avec corps ~15 × 17 mm → série KPJX ; ~9,5 mm → mini-DIN, autre famille limitée à ~1 A. Puis compter les trous côté cuivre : 4 contacts + 2 ergots + languette de masse → version blindée.","Tranche entre KPJX-4S-S et KPJX-4S"),
 ("Prise jack 3,5 mm","3 ou 4 contacts (stéréo, ou stéréo + micro) ; traversant ou CMS ; hauteur du corps.","Un jack 4 contacts ne se monte pas sur une empreinte 3 contacts"),
 ("Fusible","Marquage, dimensions, réarmable (PPTC) ou verre, et courant de maintien.","Détermine la famille entière"),
 ("Haut-parleur","Diamètre, impédance (8 Ω ou 32 Ω), épaisseur.","L'impédance conditionne l'étage de sortie audio"),
 ("Micro-USB B","Laquelle des trois variantes Amphenol : elles diffèrent par le montage.","Empreinte différente"),
 ("Antenne UHF","La bande réelle : 863-865 MHz (Europe) ou 902-928 MHz (US). Elle est sur l'étiquette de l'appareil.","Une antenne hors bande dégrade fortement la portée"),
 ("Bouton poussoir SKRW","Force d'actionnement et durée de vie visée (50k / 500k / 1000k cycles) - c'est le suffixe de la référence. Boîtier 3,7 × 3,7 mm, course 0,35 mm.","Le suffixe exact de la référence SKRW"),
 ("Batterie lithium plate","Longueur × largeur × épaisseur, capacité en mAh, tension nominale, type de connecteur, et présence ou non du circuit de protection intégré.","Sans ces cinq valeurs aucune cellule n'est commandable : une LiPo ne se substitue pas au jugé"),
 ("Condensateurs / résistances","Valeur, tolérance, tension de service, boîtier.","n/a"),
 ("Écran LCD","Relever : nombre exact de broches, pas entre broches, dimensions du verre, et photo du verre allumé segment par segment. Le HT16C21 pilote au plus 20 segments × 4 communs - c'est la limite du plan à refaire.","Dossier de refabrication sur mesure, si le SAV ne fournit plus la pièce"),
 ("MCU MSP430FR2xxx","Relire le marquage complet à la loupe. Attention : Le MCU est programmé en usine : le remplacer ne remet pas l'appareil en service sans le firmware Linkx.","Référence exacte"),
]
for c, h in enumerate(["Ligne", "Mesure à faire", "Ce qu'elle tranche"], 1):
    cell = ws3.cell(row=3, column=c, value=h)
    cell.font = HDR_FONT; cell.fill = HDR_FILL; cell.border = BORDER
    cell.alignment = Alignment(vertical="center", horizontal="center")
ws3.row_dimensions[3].height = 22
for i, row in enumerate(mes):
    for c, v in enumerate(row, 1):
        cell = ws3.cell(row=4+i, column=c, value=v)
        cell.font = BOLD if c == 1 else BODY
        cell.border = BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        if i % 2: cell.fill = ALT
for col, w in zip("ABC", [26, 78, 42]):
    ws3.column_dimensions[col].width = w
ws3.freeze_panes = "A4"

# ─────────────────────────── Feuille 4 : sources ───────────────────────────
ws4 = wb.create_sheet("Sources & statuts")
ws4["A1"] = "D'où vient chaque information"
ws4["A1"].font = TITLE
ws4.merge_cells("A1:B1")
src = [
 ("Vu","Composant visible sur les 15 photos macro de la carte (dépôt claude-cad-skills, branche claude/appareil-chauffe-bloque-2aopb5, dossier diagnostics/talkie-surchauffe/)."),
 ("Photo ext.","Identifié sur des photos analysées hors de ce dépôt (clichés 1000011752/53/54.jpg, non versionnés ici). Identification rapportée, non vérifiée sur pièce."),
 ("Documenté","Attesté par la fiche produit Linkx TG-288 reprise dans le diagnostic (port de charge micro-USB, ressort d'antenne UHF, entrée micro / sortie casque), mais non photographié."),
 ("À confirmer","Ni photographié ni documenté ici. La référence est un point de départ catalogue - voir l'onglet « Mesures restantes »."),
 ("Variante","Autre version du même composant (montage, blindage, accouplement)."),
 ("Catalogue","Lien vers une famille Mouser, pas vers une référence unique."),
 ("Prioritaire","Attention : OBSOLÈTE pour les appareils à batterie lithium plate. Le diagnostic de surchauffe repose sur la chimie Ni-MH (surcharge, absence de détection de fin de charge) : ces hypothèses H1, H2 et H3 ne s'appliquent PAS à une cellule lithium, dont la surchauffe relève du circuit de charge, du circuit de protection ou du gonflement de la cellule."),
 ("",""),
 ("Rapprochement à faire","L'alimentation associée à la prise Kycon est donnée pour 5 V / 10 A / 50 W : c'est le format d'une valise de charge multi-emplacements, pas d'un audioguide qui se charge en micro-USB sur 2 × AA Ni-MH. Or le diagnostic désigne la valise de charge comme suspect à tester. Si cette prise est celle de la valise, les deux sujets n'en font qu'un - et changer le connecteur ne réglera pas la surchauffe."),
]
for c, h in enumerate(["Statut", "Signification"], 1):
    cell = ws4.cell(row=3, column=c, value=h)
    cell.font = HDR_FONT; cell.fill = HDR_FILL; cell.border = BORDER
    cell.alignment = Alignment(vertical="center", horizontal="center")
ws4.row_dimensions[3].height = 22
for i, (k, v) in enumerate(src):
    a = ws4.cell(row=4+i, column=1, value=k); b = ws4.cell(row=4+i, column=2, value=v)
    a.font = BOLD; b.font = BODY
    for cell in (a, b):
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        if k: cell.border = BORDER
ws4.column_dimensions["A"].width = 22
ws4.column_dimensions["B"].width = 104
ws4.freeze_panes = "A4"

# ─────────────────── Feuille 5 : périmètre tourGuide AIR ───────────────────
ws5 = wb.create_sheet("tourGuide AIR")
ws5["A1"] = "tourGuide AIR - le seul produit touché par la panne de surchauffe"
ws5["A1"].font = TITLE
ws5["A2"] = ("Sous-ensemble de la feuille « Liste Mouser », restreint à ce qui est constaté ou attesté "
             "sur la carte du tourGuide AIR (les 15 photos macro de diagnostics/talkie-surchauffe/). "
             "La feuille principale reste inchangée.")
ws5["A2"].font = SUB
ws5.merge_cells("A1:E1"); ws5.merge_cells("A2:E2")

air = [
 ("Cellule lithium plate","JHY632570 · 3,7 V · 1300 mAh","Vu","Carte à ressort d'antenne + micro-USB - Attention : reste à confirmer que cette carte est bien l'AIR","https://www.mouser.fr/c/?q=3.7V+Lipo+Battery"),
 ("Port de charge micro-USB B","10118193-0001LF (+ variantes …192 / …194)","Documenté","Le diagnostic cite le port micro-USB (§6.7, corrosion fréquente en location)","https://www.mouser.fr/c/?q=10118193-0001LF"),
 ("Poussoirs tactiles CMS","série SKRW","Vu","Corrigé par l'utilisateur. Suffixe selon durée de vie visée","https://www.mouser.fr/c/?q=SKRW"),
 ("Inductance blindée 4,7 µH, 4×4 mm","SRN4018-4R7M","Vu","Deux étages à découpage sur la carte","https://www.mouser.fr/c/?q=SRN4018-4R7M"),
 ("Condensateurs MLCC 0603 / 0805","à relever","Vu","473 = 47 nF identifié sur l'étage boost","https://www.mouser.fr/c/?q=MLCC+0805"),
 ("Résistances 0805","à relever","Vu","3R3 = 3,3 Ω identifié","https://www.mouser.fr/c/?q=RC0805"),
 ("Prise jack 3,5 mm (sortie casque)","SJ-43514-SMT-TR","Documenté","Fiche Linkx : sortie casque sur la version récepteur","https://www.mouser.fr/c/?q=SJ-43514-SMT-TR"),
 ("Écran LCD à segments","SUR MESURE - hors catalogue","Vu","Pictogrammes propres au produit. SAV Linkx/Tonwelt ou refabrication sur plan","n/a"),
 ("Prise d'alimentation de la VALISE de charge","KPJX-4S-S","Photo ext.","Appartient à la valise, pas à l'appareil - mais la valise est suspecte n°4","https://www.mouser.fr/c/?q=KPJX-4S-S"),
]
exclus = [
 ("USB-C et nappe FPC","Ce sont les connecteurs de la carte « Eco 2.0 » (supraGuide ECO), pas de l'AIR"),
 ("Antennes Linx ANT-868-*","L'AIR porte un ressort d'antenne soudé sur la carte, pas une antenne de catalogue"),
 ("Prise mini-USB","Gardée par l'utilisateur, mais non constatée sur la carte de l'AIR - appartient à un autre produit"),
 ("Haut-parleur","Non constaté sur l'AIR : c'est un récepteur à écouteurs"),
 ("Fusible PPTC","Non constaté sur les photos de l'AIR"),
 ("MCU, SoC RF, driver LCD, TCXO, 4 codes CMS non résolus","Voir la feuille « Hors Mouser » : non commandables ou non identifiés"),
]

for c, h in enumerate(["Composant", "Référence", "Statut", "Pourquoi cette ligne", "Lien Mouser"], 1):
    cell = ws5.cell(row=4, column=c, value=h)
    cell.font = HDR_FONT; cell.fill = HDR_FILL; cell.border = BORDER
    cell.alignment = Alignment(vertical="center", horizontal="center")
ws5.row_dimensions[4].height = 22
r = 5
for i, row in enumerate(air):
    for c, v in enumerate(row, 1):
        cell = ws5.cell(row=r, column=c, value=v)
        cell.font = BOLD if c == 2 else BODY
        cell.border = BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=(c in (1, 4)))
        if i % 2: cell.fill = ALT
    if row[4].startswith("http"):
        ws5.cell(row=r, column=5).hyperlink = row[4]
        ws5.cell(row=r, column=5).font = LINK
    r += 1

r += 1
ws5.cell(row=r, column=1, value="Volontairement EXCLU du périmètre AIR").font = Font(name=F, size=12, bold=True, color="E65100")
r += 1
for c, h in enumerate(["Écarté", "Pourquoi"], 1):
    cell = ws5.cell(row=r, column=c, value=h)
    cell.font = HDR_FONT; cell.fill = HDR_FILL; cell.border = BORDER
    cell.alignment = Alignment(vertical="center", horizontal="center")
r += 1
for i, (k, v) in enumerate(exclus):
    for c, val in enumerate((k, v), 1):
        cell = ws5.cell(row=r, column=c, value=val)
        cell.font = BOLD if c == 1 else BODY
        cell.border = BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        if i % 2: cell.fill = ALT
    r += 1

for col, w in zip("ABCDE", [40, 30, 13, 56, 42]):
    ws5.column_dimensions[col].width = w
ws5.freeze_panes = "A5"

# ─────────────────── Feuille 6 : batteries lithium plates ───────────────────
ws6 = wb.create_sheet("Batteries")
ws6["A1"] = "Batteries lithium plates - recherche Mouser ciblée par cellule"
ws6["A1"].font = TITLE
ws6["A2"] = ("Codes à six chiffres = épaisseur (dixièmes de mm) · largeur · longueur. "
             "Aucune des trois cellules d'origine n'est distribuée par Mouser : ce sont des cellules OEM. "
             "Les recherches ci-dessous visent un ÉQUIVALENT, pas la référence d'origine.")
ws6["A2"].font = SUB
ws6.merge_cells("A1:E1"); ws6.merge_cells("A2:E2")

bat = [
 ("Cellule GM 303556", "GM 303556", "3,7 V | 650 mAh | 3,0 x 35 x 56 mm | 2024-03-22",
  "Chercher le code de taille 303556, ou le plus proche en 3,7 V 600 a 700 mAh, epaisseur 3 mm",
  "https://www.mouser.fr/c/?q=LiPo+650mAh+3.7V"),
 ("Cellule JHY632570, carte a ressort d'antenne", "JHY632570", "3,7 V | 1300 mAh | 4,81 Wh | 6,3 x 25 x 70 mm | 2023-01-03",
  "Chercher le code 632570, ou 1200 a 1500 mAh en 3,7 V, epaisseur 6,5 mm maximum",
  "https://www.mouser.fr/c/?q=LiPo+1300mAh+3.7V"),
 ("Cellule SL5022243", "SL5022243, lot 01536", "3,7 V | 450 mAh | code non decodable avec certitude",
  "Mesurer la cellule au pied a coulisse avant toute recherche : le marquage ne donne pas le gabarit",
  "https://www.mouser.fr/c/?q=LiPo+450mAh+3.7V"),
 ("Cellule LIDIO 355485", "LIDIO 355485", "3,8 V | 2500 mAh | 9,5 Wh | 3,5 x 54 x 85 mm | 2020-10",
  "Attention : 3,8 V est une cellule haute tension, charge 4,35 V. Introuvable en catalogue generaliste : OEM ou fabrication sur mesure",
  "n/a"),
 ("Cellule de la carte Eco 2.0", "sans reference", "3,87 V | 1000 mAh | dimensions a mesurer",
  "Attention : haute tension egalement. Meme conclusion : OEM ou fabrication sur mesure",
  "n/a"),
]

familles = [
 ("DigiKey", "Jauch Quartz, serie LP", "Le meilleur equivalent industriel. Meme convention de code a six chiffres, vendu avec circuit de protection et fils (PCM + 2 WIRES 50MM). Tension 3,7 V, charge 4,20 V. Non distribue par Mouser.", "https://www.digikey.com/en/product-highlight/j/jauch-quartz/lithium-polymer-batteries"),
 ("DigiKey", "Exemple : LP503562JU", "Format 5,0 x 35 x 62 mm, avec PCM et fils. Sert de modele pour comprendre la designation.", "https://www.digikey.com/en/products/detail/jauch-quartz/LP503562JU/9560989"),
 ("DigiKey", "Exemple : LP561836JU", "Format 5,6 x 18 x 36 mm, 350 mAh, avec PCM et fils.", "https://www.digikey.com/en/products/detail/jauch-quartz/LP561836JU-PCM-2-WIRES-50MM/9560979"),
 ("DigiKey", "Catalogue packs lithium polymere", "A filtrer par capacite et dimensions.", "https://www.digikey.com/en/products/filter/battery-packs/lithium-polymer/89"),
 ("EEMB (direct ou Amazon.fr)", "Cellules poche a code de taille", "Le plus proche de vos cellules OEM : meme logique de code (602835, 603449, 103395), livrees avec connecteur JST et circuit de protection. Fabricant chinois etabli, vendu au detail en Europe.", "https://www.eemb.com/categories-55"),
 ("TYVA Energie (France)", "Fabrication sur mesure", "Si aucun format standard ne convient, ou pour une cellule haute tension introuvable en catalogue.", "https://tyva-energie.com/en/custom-lithium-battery-manufacturer/"),
 ("Mouser", "Packs LiPo 3,7 V", "Catalogue generaliste, sans recherche par code de taille. Ne propose que du 3,7 V.", "https://www.mouser.fr/c/?q=3.7V+Lipo+Battery"),
]

criteres = [
 ("1. Dimensions", "Épaisseur × largeur × longueur MESURÉES au pied à coulisse - le code à six chiffres est une convention, pas une garantie"),
 ("2. Capacité", "En mAh. Une capacité supérieure allonge l'autonomie mais souvent l'épaisseur aussi"),
 ("3. Tension nominale", "Attention : LE CRITÈRE CRITIQUE. 3,7 V (charge 4,20 V) et 3,8/3,87 V (charge 4,35 V) ne sont PAS interchangeables. Une 3,7 V dans un chargeur 4,35 V est en surcharge permanente : elle chauffe et gonfle"),
 ("4. Circuit de protection", "Vos cellules en ont un, visible sous le kapton jaune. Une cellule nue sans protection est dangereuse dans cet appareil"),
 ("5. Connecteur et POLARITÉ", "JST 2 points. La polarité n'est pas normalisée sur les cellules chinoises : vérifier au voltmètre AVANT de brancher, sous peine de détruire la carte"),
]

r = 4
for c, h in enumerate(["Cellule d'origine", "Marquage", "Spécification relevée", "Ce qu'il faut chercher", "Recherche Mouser"], 1):
    cell = ws6.cell(row=r, column=c, value=h)
    cell.font = HDR_FONT; cell.fill = HDR_FILL; cell.border = BORDER
    cell.alignment = Alignment(vertical="center", horizontal="center")
ws6.row_dimensions[r].height = 22
r += 1
for i, row in enumerate(bat):
    for c, v in enumerate(row, 1):
        cell = ws6.cell(row=r, column=c, value=v)
        cell.font = BOLD if c == 2 else BODY
        cell.border = BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=(c != 2))
        if i % 2: cell.fill = ALT
    if row[4].startswith("http"):
        ws6.cell(row=r, column=5).hyperlink = row[4]; ws6.cell(row=r, column=5).font = LINK
    r += 1

r += 1
ws6.cell(row=r, column=1, value="Ou chercher un equivalent, site par site").font = Font(name=F, size=12, bold=True, color="1F3864")
r += 1
for c, h in enumerate(["Site", "Quoi", "Pourquoi", "Lien"], 1):
    cell = ws6.cell(row=r, column=c, value=h)
    cell.font = HDR_FONT; cell.fill = HDR_FILL; cell.border = BORDER
    cell.alignment = Alignment(vertical="center", horizontal="center")
r += 1
for i, row in enumerate(familles):
    for c, v in enumerate(row, 1):
        cell = ws6.cell(row=r, column=c, value=v)
        cell.font = BOLD if c == 1 else BODY
        cell.border = BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        if i % 2: cell.fill = ALT
    ws6.cell(row=r, column=4).hyperlink = row[3]; ws6.cell(row=r, column=4).font = LINK
    r += 1

r += 1
ws6.cell(row=r, column=1, value="Les cinq critères d'un équivalent - aucun n'est facultatif").font = Font(name=F, size=12, bold=True, color="E65100")
r += 1
for i, (k, v) in enumerate(criteres):
    a = ws6.cell(row=r, column=1, value=k); b = ws6.cell(row=r, column=2, value=v)
    ws6.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
    a.font = BOLD; b.font = BODY
    for cell in (a, b):
        cell.border = BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        if i % 2: cell.fill = ALT
    r += 1

r += 1
ws6.cell(row=r, column=1, value=("Sécurité : Sécurité : une poche lithium gonflée ou en surchauffe est un risque d'incendie. "
                                 "Ne pas la percer, ne pas la plier, ne pas continuer à la charger. La sortir de l'appareil, "
                                 "la placer dans un contenant ininflammable, la faire reprendre en déchet."))
ws6.cell(row=r, column=1).font = Font(name=F, size=10, bold=True, color="C00000")
ws6.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
ws6.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="top")
ws6.row_dimensions[r].height = 30

for col, w in zip("ABCDE", [40, 26, 52, 44, 36]):
    ws6.column_dimensions[col].width = w
ws6.freeze_panes = "A5"

out = "exports/Liste-Mouser-Tonwelt-TG288.xlsx"
wb.save(out)
print("écrit:", out)
