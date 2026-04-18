---
name: annotate-step
description: Create an annotated top-face PDF from any STEP file. Extracts the outer profile and holes directly from the STEP top face via FreeCAD, classifies threaded holes by radius, and produces a clean PDF with color-coded callouts. Use whenever the user asks to "create an annotated PDF for X.step", "annotate the top face of X", or "mark the threaded holes on X". Also handles custom thread specs (M3, M3.5, M4, etc.) when specified.
---

# Annotate STEP — Top Face PDF

Produces a color-annotated top-view PDF from any STEP file.
Holes annotated are specified by the user (e.g. M3×0.5, M3.5×0.5).
All other geometry is drawn plain black.

**Required tool**: `mcp__freecad__execute_code`
**Required Python packages**: `matplotlib`, `reportlab`, `Pillow`

---

## Step 1 — Confirm inputs

Ask the user (if not already provided):
1. **STEP file path** — full path to the `.step` / `.stp` file
2. **Which threads to annotate** — e.g. "M3×0.5 and M3.5×0.5" (default: M3×0.5 only)

Default CAD directory: `/Users/chinnadevarapu/Documents/Antigravity/CAD/`

---

## Step 2 — Extract top face geometry via FreeCAD

Run this code. **IMPORTANT**: FreeCAD MCP output is large — always save to `/tmp` and read back with Bash.

```python
import Part, json, math

step_path = "STEP_FILE_PATH_HERE"
shape = Part.Shape()
shape.read(step_path)

# Find the face whose normal points most toward +Z
top_face = max(shape.Faces, key=lambda f: f.normalAt(0, 0).z)
print(f"Top face normal z: {top_face.normalAt(0,0).z:.4f}")
print(f"Number of wires: {len(top_face.Wires)}")

# Wire 0 = outer boundary; wires 1..N = holes
outer_wire = top_face.Wires[0]
pts = []
for e in outer_wire.Edges:
    pts.extend([(p.x, p.y) for p in e.discretize(20)])

holes = []
for i, w in enumerate(top_face.Wires[1:], 1):
    edges = w.Edges
    # Try single-edge arc (clean circle)
    if len(edges) == 1:
        try:
            curve = edges[0].Curve
            cx, cy, r = curve.Center.x, curve.Center.y, curve.Radius
            holes.append({"idx": i, "cx": cx, "cy": cy, "r": r})
            continue
        except:
            pass
    # Fallback: discretize and compute centroid + mean radius
    all_pts = []
    for e in edges:
        all_pts.extend([(p.x, p.y) for p in e.discretize(16)])
    xs2 = [p[0] for p in all_pts]; ys2 = [p[1] for p in all_pts]
    cx2 = sum(xs2)/len(xs2); cy2 = sum(ys2)/len(ys2)
    r2 = sum(math.sqrt((x-cx2)**2+(y-cy2)**2) for x,y in zip(xs2,ys2))/len(xs2)
    holes.append({"idx": i, "cx": cx2, "cy": cy2, "r": r2})

print(f"\nHoles found: {len(holes)}")
for h in holes:
    print(f"  Wire {h['idx']}: cx={h['cx']:.3f}  cy={h['cy']:.3f}  r={h['r']:.3f} mm  d={h['r']*2:.3f} mm")

out = "/tmp/PART_NAME_top_face.json"
with open(out, "w") as f:
    json.dump({"outer": pts, "holes": holes}, f)
print(f"\nSaved to {out}")
```

After running, read the printed hole table using Bash (not by re-reading the FreeCAD result — it's too large):
```bash
jq -r '.result[].stdout // empty' <TOOL_RESULT_FILE> | head -60
```

---

## Step 3 — Classify holes by radius

Use these radius ranges (adjust if user specifies different thread sizes):

| Thread | Nominal dia | Radius range | Notes |
|--------|-------------|--------------|-------|
| M2×0.4 | 2.0 mm | 0.85–1.05 mm | tap drill ~1.6 mm |
| M2.5×0.45 | 2.5 mm | 1.10–1.30 mm | tap drill ~2.05 mm |
| M3×0.5 | 3.0 mm | 1.40–1.65 mm | clearance ~3.2 mm → r=1.6 |
| M3.5×0.5 | 3.5 mm | 1.65–1.85 mm | nominal r=1.75 |
| M4×0.7 | 4.0 mm | 1.85–2.15 mm | tap drill ~3.3 mm |
| M5×0.8 | 5.0 mm | 2.35–2.65 mm | tap drill ~4.2 mm |

**Key rule**: holes modeled at nominal diameter sit at the top of the range; holes modeled at tap-drill diameter sit at the bottom. If a hole falls between two ranges, report the ambiguity and ask the user.

---

## Step 4 — Generate annotated PDF

Install dependencies if needed:
```bash
pip3 install reportlab pillow --break-system-packages -q
```

Then run this script (fill in the variables at the top):

```python
import json, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.units import mm
from PIL import Image as PILImage

# ── CONFIG ──────────────────────────────────────────────────────────────────
JSON_PATH  = "/tmp/PART_NAME_top_face.json"
OUT_PDF    = "/path/to/output/PART_NAME_annotated.pdf"
PART_LABEL = "PART_NAME"

# Define thread classes: label → (r_min, r_max, hex_color)
THREAD_CLASSES = {
    "M3\u00d70.5":   (1.40, 1.65, "#1565C0"),   # blue
    "M3.5\u00d70.5": (1.65, 1.85, "#B71C1C"),   # red
}
# ────────────────────────────────────────────────────────────────────────────

with open(JSON_PATH) as f:
    data = json.load(f)

outer = data["outer"]
holes = data["holes"]
xs = [p[0] for p in outer]
ys = [p[1] for p in outer]

def classify(r):
    for label, (rmin, rmax, _) in THREAD_CLASSES.items():
        if rmin <= r <= rmax:
            return label
    return None

fig, ax = plt.subplots(figsize=(11, 11))
ax.set_aspect('equal')
ax.axis('off')

# Outer profile fill + border
ax.fill(xs, ys, color='#f5f5f5', zorder=0)
ax.plot(xs + [xs[0]], ys + [ys[0]], 'k-', linewidth=1.2, zorder=1)

# Part centroid (for leader direction)
x_min, x_max = min(xs), max(xs)
y_min, y_max = min(ys), max(ys)
cx_part = (x_min + x_max) / 2
cy_part = (y_min + y_max) / 2

def leader_offset(hx, hy, dist=11):
    dx = hx - cx_part; dy = hy - cy_part
    mag = math.sqrt(dx*dx + dy*dy) or 1
    return hx + dx/mag * dist, hy + dy/mag * dist

# Draw unclassified holes plain
for h in holes:
    if classify(h['r']) is None:
        ax.add_patch(plt.Circle((h['cx'], h['cy']), h['r'],
                                color='k', fill=False, linewidth=0.8, zorder=2))

# Draw classified holes + annotations
counts = {lbl: 0 for lbl in THREAD_CLASSES}
for h in holes:
    cls = classify(h['r'])
    if cls is None:
        continue
    _, _, color = THREAD_CLASSES[cls]
    ax.add_patch(plt.Circle((h['cx'], h['cy']), h['r'],
                             color=color, fill=False, linewidth=1.5, zorder=3))
    counts[cls] += 1
    lx, ly = leader_offset(h['cx'], h['cy'])
    angle = math.atan2(ly - h['cy'], lx - h['cx'])
    ax.annotate(
        cls,
        xy=(h['cx'] + h['r'] * math.cos(angle), h['cy'] + h['r'] * math.sin(angle)),
        xytext=(lx, ly),
        fontsize=7.5, color=color, fontweight='bold',
        arrowprops=dict(arrowstyle='->', color=color, lw=0.8),
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, lw=0.9),
        zorder=5, ha='center'
    )

# Legend
legend_handles = [
    mpatches.Patch(edgecolor=THREAD_CLASSES[lbl][2], facecolor='white', linewidth=1.5,
                   label=f"{lbl} threaded  ({counts[lbl]} holes)")
    for lbl in THREAD_CLASSES
] + [mpatches.Patch(edgecolor='black', facecolor='white', linewidth=0.8, label="Other geometry")]
ax.legend(handles=legend_handles, loc='lower right', fontsize=8.5, framealpha=0.9)

title_annots = "  |  ".join(
    f"{lbl} ({THREAD_CLASSES[lbl][2]})" for lbl in THREAD_CLASSES
)
ax.set_title(f"{PART_LABEL} \u2014 Top Face View\n{title_annots}",
             fontsize=11, fontweight='bold', pad=14)

pad = 8
ax.set_xlim(x_min - pad, x_max + pad)
ax.set_ylim(y_min - pad, y_max + pad)
plt.tight_layout()

img_path = "/tmp/annotated_preview.png"
plt.savefig(img_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# Build PDF
img = PILImage.open(img_path)
iw, ih = img.size
page_w, page_h = A4
margin = 18 * mm
avail_w = page_w - 2 * margin
avail_h = page_h - 2 * margin - 22 * mm
scale = min(avail_w / iw, avail_h / ih)
draw_w, draw_h = iw * scale, ih * scale
draw_x = (page_w - draw_w) / 2

c = rl_canvas.Canvas(OUT_PDF, pagesize=A4)
c.setFont("Helvetica-Bold", 13)
c.drawCentredString(page_w/2, page_h - 15*mm, f"{PART_LABEL} \u2014 Top Face Annotations")
c.setFont("Helvetica", 9)
annot_legend = "  |  ".join(
    f"{lbl}" for lbl in THREAD_CLASSES
)
c.drawCentredString(page_w/2, page_h - 22*mm, annot_legend + "  |  Black = other geometry")
c.drawImage(img_path, draw_x, 14*mm, width=draw_w, height=draw_h)
c.setFont("Helvetica", 7)
c.setFillColorRGB(0.5, 0.5, 0.5)
c.drawCentredString(page_w/2, 7*mm,
                    "Generated from STEP top face via FreeCAD | All dimensions in mm")
c.save()

print(f"PDF saved: {OUT_PDF}")
for lbl, cnt in counts.items():
    print(f"  {lbl}: {cnt} holes")
```

---

## Step 5 — Report and open

After saving the PDF:
- Report the output path as a markdown link
- Print the hole count table (thread type → count)
- Run `open <path>` to open in Preview

---

## Key technical rules

- **Always** extract geometry from the STEP top face via FreeCAD — never reuse DXF data or extract from the full 3D shape (picks up side/bottom faces).
- **Top face** = face with `normalAt(0,0).z` closest to +1.0.
- **Wire 0** = outer boundary; **wires 1..N** = holes.
- **FreeCAD result size**: output exceeds MCP token limit — always save to `/tmp` and read stdout via `jq` on the tool-result file.
- **Export**: use `Import.export()` not `Part.export()` for any STEP export tasks.
- **Subscripts in ReportLab**: use `\u00d7` for × (multiplication sign) in canvas strings; use `<super>`/`<sub>` tags only inside `Paragraph` objects.
- If `reportlab` or `Pillow` are missing: `pip3 install reportlab pillow --break-system-packages -q`
