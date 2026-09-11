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
 ("Prise alimentation DIN puissance 4 contacts, coudée BLINDÉE","KPJX-4S-S","Kycon","Photo ext.","https://www.mouser.com/en/ProductDetail/Kycon/KPJX-4S-S?qs=0QDpPFt3C4bj8uE5yBzCJQ%3D%3D","https://www.mouser.fr/c/?q=KPJX-4S-S"),
 ("Prise alimentation DIN puissance 4 contacts, non blindée","KPJX-4S","Kycon","Variante","https://www.mouser.fr/ProductDetail/Kycon/KPJX-4S?qs=PGF6ObTbUZ1PHc9As62%2FZQ%3D%3D","https://www.mouser.fr/c/?q=KPJX-4S"),
 ("Prise alimentation, montage sur panneau","KPJX-PM-4S-S","Kycon","Variante","https://www.mouser.com/ProductDetail/Kycon/KPJX-PM-4S-S?qs=zorda86t5M9ArIfKgei5Pg%3D%3D","https://www.mouser.fr/c/?q=KPJX-PM-4S-S"),
 ("Prise alimentation DIN puissance 4 contacts — série voisine KPJ, non blindée","KPJ-4S","Kycon","À départager","https://www.mouser.com/ProductDetail/Kycon/KPJ-4S?qs=/XicOQBKAMa%252BcJ0hGGZaig%3D%3D","https://www.mouser.fr/c/?q=KPJ-4S"),
 ("Prise alimentation DIN puissance 4 contacts — série voisine KPJ, blindée","KPJ-4S-S","Kycon","À départager","https://www.mouser.com/ProductDetail/Kycon/KPJ-4S-S?qs=SrUfdAPSdgAPLkBk%2BStEGA%3D%3D","https://www.mouser.fr/c/?q=KPJ-4S-S"),
 ("Prise alimentation DIN puissance 4 contacts — version haute température","KPJXHT-4S-S","Kycon","Variante","https://www.mouser.com/ProductDetail/Kycon/KPJXHT-4S-S?qs=6olcXJbp99TwdwXWG%2BzyAQ%3D%3D","https://www.mouser.fr/c/?q=KPJXHT-4S-S"),
 ("Fiche mâle d'accouplement (réfection du cordon)","KPPX-4P","Kycon","Variante","https://www.mouser.com/ProductDetail/Kycon/KPPX-4P?qs=Y0vc5luVLxJNKFay3ZyJLw%3D%3D","https://www.mouser.fr/c/?q=KPPX-4P"),
 ("Prise jack 3,5 mm, traversante","SJ-43514","Same Sky (CUI Devices)","Documenté","https://www.mouser.com/ProductDetail/Same-Sky/SJ-43514?qs=WyjlAZoYn51bsBOfuwwiuw%3D%3D","https://www.mouser.fr/c/?q=SJ-43514"),
 ("Prise jack 3,5 mm, CMS","SJ-43514-SMT-TR","Same Sky (CUI Devices)","Documenté","https://www.mouser.com/ProductDetail/CUI-Devices/SJ-43514-SMT-TR/?qs=WyjlAZoYn528%252BiAb5RzVtg%3D%3D","https://www.mouser.fr/c/?q=SJ-43514-SMT-TR"),
 ("Micro-USB B, CMS coudée","10118193-0001LF","Amphenol FCI","Documenté","https://www.mouser.com/ProductDetail/Amphenol-FCI/10118193-0001LF?qs=Ywefl8B65e63Nsqd%2B8HZaQ%3D%3D","https://www.mouser.fr/c/?q=10118193-0001LF"),
 ("Micro-USB B, variante de montage","10118192-0001LF","Amphenol FCI","Variante","https://www.mouser.com/ProductDetail/Amphenol-FCI/10118192-0001LF?qs=Ywefl8B65e5bHFoQtIudZg%3D%3D","https://www.mouser.fr/c/?q=10118192-0001LF"),
 ("Micro-USB B, variante de montage","10118194-0001LF","Amphenol FCI","Variante","https://www.mouser.com/en/ProductDetail/Amphenol-FCI/10118194-0001LF?qs=Ywefl8B65e4FIdY8OWfRQA%3D%3D","https://www.mouser.fr/c/?q=10118194-0001LF"),
 ("Mini-USB B, 5 contacts","54819-0519","Molex","À confirmer","https://www.mouser.com/ProductDetail/Molex/54819-0519?qs=x6EjVpvqMVObi%2BAAyuuEww%3D%3D","https://www.mouser.fr/c/?q=54819-0519"),
 ("USB-C, 16 contacts, traversante","USB4085-GF-A","GCT","À confirmer","https://www.mouser.com/ProductDetail/GCT/USB4085-GF-A?qs=KUoIvG%2F9Ilba1bQOahfWjw%3D%3D","https://www.mouser.fr/c/?q=USB4085-GF-A"),
 ("Fusible réarmable PPTC, boîtier 1812","série MF-MSMF","Bourns","À confirmer","https://www.mouser.com/new/bourns/bourns-mf-msmf-series-fuses/","https://www.mouser.fr/c/?q=MF-MSMF"),
 ("Fusibles PPTC — catalogue complet","—","—","Catalogue","https://www.mouser.com/c/circuit-protection/thermistors/resettable-fuses-pptc/","https://www.mouser.fr/c/?q=fusible+PPTC+1812"),
 ("Haut-parleur Ø15 mm, 8 Ω","AS01508MR-6-R","PUI Audio","À confirmer","https://www.mouser.com/ProductDetail/PUI-Audio/AS01508MR-6-R?qs=vgjKjNJexThgIp5KgUGpgA%3D%3D","https://www.mouser.fr/c/?q=AS01508MR-6-R"),
 ("Haut-parleurs — catalogue","—","—","Catalogue","https://www.mouser.com/en/c/electromechanical/audio-devices/speakers-transducers/","https://www.mouser.fr/c/?q=haut-parleur+15mm+8+ohm"),
 ("Bouton poussoir CMS (ceux de la carte)","SKRPACE010","Alps Alpine","Vu","https://www.mouser.com/ProductDetail/Alps-Alpine/SKRPACE010?qs=dHDuPHwQO79W8iY66hDbLQ%3D%3D","https://www.mouser.fr/c/?q=SKRPACE010"),
 ("Bouton poussoir traversant 6 × 6 mm","B3F-1000","Omron","À confirmer","https://www.mouser.com/ProductDetail/Omron-Electronics/B3F-1000?qs=lK7M36XCk6JQHckSc1xIsg%3D%3D","https://www.mouser.fr/c/?q=B3F-1000"),
 ("Antenne UHF hélicoïdale CMS","ANT-868-VHETH","TE / Linx","Documenté","https://www.mouser.com/ProductDetail/TE-Connectivity-Linx-Technologies/ANT-868-VHETH?qs=pUKx8fyJudBCulCrBA9DxA%3D%3D","https://www.mouser.fr/c/?q=ANT-868-VHETH"),
 ("Antenne UHF monopole embarqué Ø7 mm","ANT-868-JJB-ST","TE / Linx","Documenté","https://www.mouser.com/ProductDetail/TE-Connectivity-Linx-Technologies/ANT-868-JJB-ST?qs=K5ta8V%2BWhtbjRn899xwLFw%3D%3D","https://www.mouser.fr/c/?q=ANT-868-JJB-ST"),
 ("Antenne UHF planaire CMS","ANT-868-SP","TE / Linx","Documenté","https://www.mouser.com/ProductDetail/Linx-Technologies/ANT-868-SP?qs=K5ta8V%2BWhtYLcp%2FwdgtLaA%3D%3D","https://www.mouser.fr/c/?q=ANT-868-SP"),
 ("Antennes 868 MHz — catalogue","—","—","Catalogue","https://www.mouser.com/c/passive-components/antennas/?center+frequency=868+MHz","https://www.mouser.fr/c/?q=antenne+868+MHz"),
 ("Inductance blindée 4,7 µH, 4×4 mm (étage boost)","SRN4018-4R7M","Bourns","Vu","https://www.mouser.com/en/ProductDetail/Bourns/SRN4018-4R7M?qs=UvjENeDOEed%2FCjy5nMh3Xg%3D%3D","https://www.mouser.fr/c/?q=SRN4018-4R7M"),
 ("Condensateurs MLCC CMS — catalogue","0603 / 0805 / 1206","Murata, Yageo, KEMET","Vu","https://www.mouser.com/c/passive-components/capacitors/ceramic-capacitors/mlccs-smd-smt/","https://www.mouser.fr/c/?q=MLCC+0805"),
 ("Kits de condensateurs","—","—","Catalogue","https://www.mouser.com/Passive-Components/Capacitors/Capacitor-Kits/_/N-2iq32","https://www.mouser.fr/c/?q=capacitor+kit"),
 ("Résistances CMS — catalogue","RC0805 / CRCW0805","Yageo, Vishay","Vu","https://www.mouser.com/c/passive-components/resistors/chip-smd-resistors/","https://www.mouser.fr/c/?q=RC0805+resistance"),
 ("Kits de résistances CMS","—","—","Catalogue","https://www.mouser.com/c/passive-components/resistors/resistor-kits/?termination+style=SMD%2FSMT","https://www.mouser.fr/c/?q=resistor+kit+0805"),
 ("Accus AA Ni-MH — la réparation la plus probable","gamme Ni-MH","Panasonic","Prioritaire","https://www.mouser.com/en/c/power/batteries/nimh-nickel-metal-hydride-battery/?m=Panasonic","https://www.mouser.fr/c/?q=Panasonic+NiMH+AA"),
 ("MCU TI MSP430FR2xxx — famille","réf. exacte à relire sur la puce","Texas Instruments","À confirmer","https://www.mouser.com/c/semiconductors/embedded-processors-controllers/microcontrollers-mcu/?q=MSP430FR2","https://www.mouser.fr/c/?q=MSP430FR2"),
]

ws["A1"] = "Liste Mouser — audioguide Tonwelt / Linkx TG-288 et sa valise de charge"
ws["A1"].font = TITLE
ws["A2"] = ("Prix et stocks volontairement absents : ils changent — à lire sur la page produit au moment de commander.  "
            "Colonne E (Qté) en jaune : à compléter, nombre entier, ex. 2.  Colonne F : adresse en clair, à copier-coller.  Colonne G : cliquer sur « Ouvrir ».")
ws["A2"].font = SUB
ws.merge_cells("A1:G1"); ws.merge_cells("A2:G2")

hdr = ["Composant", "Référence fabricant", "Fabricant", "Statut", "Qté", "Lien produit Mouser", "Recherche par référence"]
HR = 4
for c, h in enumerate(hdr, 1):
    cell = ws.cell(row=HR, column=c, value=h)
    cell.font = HDR_FONT; cell.fill = HDR_FILL; cell.border = BORDER
    cell.alignment = Alignment(vertical="center", horizontal="center")
ws.row_dimensions[HR].height = 22

for i, (comp, ref, fab, stat, url, rech) in enumerate(rows):
    r = HR + 1 + i
    vals = [comp, ref, fab, stat, None, url, rech]
    for c, v in enumerate(vals, 1):
        cell = ws.cell(row=r, column=c, value=v)
        cell.border = BORDER
        cell.font = BOLD if (c == 2 and ref != "—") else BODY
        cell.alignment = Alignment(vertical="top", wrap_text=(c == 1))
        if i % 2: cell.fill = ALT
    ws.cell(row=r, column=5).fill = INPUT_FILL
    ws.cell(row=r, column=5).alignment = Alignment(horizontal="center", vertical="top")
    link = ws.cell(row=r, column=6)
    link.hyperlink = url; link.font = LINK
    link.alignment = Alignment(vertical="top")
    # Colonne G : formule HYPERLINK — cliquable dans Excel, LibreOffice et Google Sheets,
    # y compris là où les liens natifs ne sont pas activés (mode protégé, visionneuse mobile).
    rlink = ws.cell(row=r, column=7)
    rlink.hyperlink = rech; rlink.font = LINK
    rlink.alignment = Alignment(vertical="top")
    if i % 2: rlink.fill = ALT
    rlink.border = BORDER


last = HR + len(rows)
ws.auto_filter.ref = f"A{HR}:G{last}"
ws.freeze_panes = f"A{HR+1}"
for col, w in zip("ABCDEFG", [46, 24, 22, 13, 7, 62, 44]):
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
 ("Bouton poussoir","Hauteur de l'actionneur et force de contact.","Retrouver le même confort d'appui"),
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
 ("Prioritaire","Le diagnostic de surchauffe place la chaîne piles Ni-MH / charge en tête des causes (hypothèses H1, H2 et H3)."),
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
