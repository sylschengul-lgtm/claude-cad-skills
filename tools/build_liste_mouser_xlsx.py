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
 ("Poussoir tactile CMS bas profil — série SKRW","série SKRW","Alps Alpine","Vu","https://www.mouser.fr/fr/new/alps-alpine/alps-alpine-skrw-tact-switches/"),
 ("Poussoir SKRW — variantes 50k / 500k / 1000k cycles","SKRWAEE030 · SKRWAME030 · SKRWADE030","Alps Alpine","À confirmer","https://www.mouser.fr/c/?q=SKRW"),
 ("Fusible réarmable PPTC, boîtier 1812","série MF-MSMF","Bourns","À confirmer","https://www.mouser.fr/c/?q=MF-MSMF"),
 ("Fusibles PPTC — catalogue complet","—","—","Catalogue","https://www.mouser.fr/c/?q=fusible+PPTC+1812"),
 ("Haut-parleurs — catalogue","—","—","Catalogue","https://www.mouser.fr/c/?q=haut-parleur+15mm+8+ohm"),
 ("Antenne UHF hélicoïdale CMS","ANT-868-VHETH","TE / Linx","Documenté","https://www.mouser.fr/c/?q=ANT-868-VHETH"),
 ("Antennes 868 MHz — catalogue","—","—","Catalogue","https://www.mouser.fr/c/?q=antenne+868+MHz"),
 ("Batterie lithium plate — cellule relevée n°1 (carte à ressort d'antenne)","JHY632570 · 3,7 V · 1300 mAh · 6,3×25×70 mm","JHY","Vu","https://www.mouser.fr/c/?q=3.7V+Lipo+Battery"),
 ("Batterie lithium plate — cellule relevée n°2 (carte Eco 2.0, USB-C)","sans référence · 3,87 V · 1000 mAh","—","Vu","https://www.mouser.fr/c/?q=3.8V+Lipo+Battery"),
 ("Batterie lithium plate — cellule relevée n°4","LIDIO 355485 · 3,8 V · 2500 mAh · 3,5×54×85 mm","LIDIO","Vu","https://www.mouser.fr/c/?q=3.8V+Lipo+Battery"),
 ("⚠ Aucune de ces cellules n'est distribuée par Mouser — voir docs/batteries-lithium-tonwelt.md","JHY et LIDIO = fabricants OEM","—","Hors Mouser","https://www.mouser.fr/c/?q=lithium+polymer+battery+pack"),
 ("Inductance blindée 4,7 µH, 4×4 mm (étage boost)","SRN4018-4R7M","Bourns","Vu","https://www.mouser.fr/c/?q=SRN4018-4R7M"),
 ("Condensateurs MLCC CMS — catalogue","0603 / 0805 / 1206","Murata, Yageo, KEMET","Vu","https://www.mouser.fr/c/?q=MLCC+0805"),
 ("Kits de résistances CMS","—","—","Catalogue","https://www.mouser.fr/c/?q=resistor+kit+0805"),
 ("MCU TI MSP430FR2xxx — famille","réf. exacte à relire sur la puce","Texas Instruments","À confirmer","https://www.mouser.fr/c/?q=MSP430FR2"),
]

ws["A1"] = "Liste Mouser — audioguide Tonwelt / Linkx et sa valise de charge"
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
        cell.font = BOLD if (c == 2 and ref != "—") else BODY
        cell.alignment = Alignment(vertical="top", wrap_text=(c == 1))
        if i % 2: cell.fill = ALT
    ws.cell(row=r, column=5).fill = INPUT_FILL
    ws.cell(row=r, column=5).alignment = Alignment(horizontal="center", vertical="top")
    link = ws.cell(row=r, column=6)
    link.hyperlink = lien; link.font = LINK
    link.alignment = Alignment(vertical="top")
    # Colonne G : formule HYPERLINK — cliquable dans Excel, LibreOffice et Google Sheets,
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
 ("TCXO « 24.04 AK AD » — 24,04 MHz","Fréquence hors catalogue","Fabricant d'oscillateurs, sur commande"),
 ("« 19AKM » — SOT-23-5, convertisseur boost","Code CMS absent des bases publiques","À identifier par brochage avant toute recherche"),
 ("« CDV 221 A5L2 » — SOP-8","Code CMS non résolu","idem"),
 ("« 724 2G SU » — SOP-8","Code CMS non résolu","idem"),
 ("« BSG· TI 8A8 A46R » — QFN-16","CI Texas Instruments, code boîtier insuffisant","Décodage TI nécessaire"),
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
 ("Prise d'alimentation","Plan de perçage constructeur à comparer trou par trou : https://www.mouser.com/datasheet/3/166/1/KPJX.pdf  —  Diamètre extérieur de la bague en façade : ~12,9 mm avec corps ~15 × 17 mm → série KPJX ; ~9,5 mm → mini-DIN, autre famille limitée à ~1 A. Puis compter les trous côté cuivre : 4 contacts + 2 ergots + languette de masse → version blindée.","Tranche entre KPJX-4S-S et KPJX-4S"),
 ("Prise jack 3,5 mm","3 ou 4 contacts (stéréo, ou stéréo + micro) ; traversant ou CMS ; hauteur du corps.","Un jack 4 contacts ne se monte pas sur une empreinte 3 contacts"),
 ("Fusible","Marquage, dimensions, réarmable (PPTC) ou verre, et courant de maintien.","Détermine la famille entière"),
 ("Haut-parleur","Diamètre, impédance (8 Ω ou 32 Ω), épaisseur.","L'impédance conditionne l'étage de sortie audio"),
 ("Micro-USB B","Laquelle des trois variantes Amphenol : elles diffèrent par le montage.","Empreinte différente"),
 ("Antenne UHF","La bande réelle : 863–865 MHz (Europe) ou 902–928 MHz (US). Elle est sur l'étiquette de l'appareil.","Une antenne hors bande dégrade fortement la portée"),
 ("Bouton poussoir SKRW","Force d'actionnement et durée de vie visée (50k / 500k / 1000k cycles) — c'est le suffixe de la référence. Boîtier 3,7 × 3,7 mm, course 0,35 mm.","Le suffixe exact de la référence SKRW"),
 ("Batterie lithium plate","Longueur × largeur × épaisseur, capacité en mAh, tension nominale, type de connecteur, et présence ou non du circuit de protection intégré.","Sans ces cinq valeurs aucune cellule n'est commandable : une LiPo ne se substitue pas au jugé"),
 ("Condensateurs / résistances","Valeur, tolérance, tension de service, boîtier.","—"),
 ("Écran LCD","Relever : nombre exact de broches, pas entre broches, dimensions du verre, et photo du verre allumé segment par segment. Le HT16C21 pilote au plus 20 segments × 4 communs — c'est la limite du plan à refaire.","Dossier de refabrication sur mesure, si le SAV ne fournit plus la pièce"),
 ("MCU MSP430FR2xxx","Relire le marquage complet à la loupe. ⚠ Le MCU est programmé en usine : le remplacer ne remet pas l'appareil en service sans le firmware Linkx.","Référence exacte"),
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
 ("À confirmer","Ni photographié ni documenté ici. La référence est un point de départ catalogue — voir l'onglet « Mesures restantes »."),
 ("Variante","Autre version du même composant (montage, blindage, accouplement)."),
 ("Catalogue","Lien vers une famille Mouser, pas vers une référence unique."),
 ("Prioritaire","⚠ OBSOLÈTE pour les appareils à batterie lithium plate. Le diagnostic de surchauffe repose sur la chimie Ni-MH (surcharge, absence de détection de fin de charge) : ces hypothèses H1, H2 et H3 ne s'appliquent PAS à une cellule lithium, dont la surchauffe relève du circuit de charge, du circuit de protection ou du gonflement de la cellule."),
 ("",""),
 ("Rapprochement à faire","L'alimentation associée à la prise Kycon est donnée pour 5 V / 10 A / 50 W : c'est le format d'une valise de charge multi-emplacements, pas d'un audioguide qui se charge en micro-USB sur 2 × AA Ni-MH. Or le diagnostic désigne la valise de charge comme suspect à tester. Si cette prise est celle de la valise, les deux sujets n'en font qu'un — et changer le connecteur ne réglera pas la surchauffe."),
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

out = "exports/Liste-Mouser-Tonwelt-TG288.xlsx"
wb.save(out)
print("écrit:", out)
