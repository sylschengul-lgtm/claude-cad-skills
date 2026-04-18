---
name: annotate-step
description: Create a multi-face annotated PDF from any STEP file. Extracts named faces (top, left, right, bottom, front, back) directly from the STEP via FreeCAD, classifies threaded holes by radius, and produces a clean multi-panel PDF with color-coded callouts. Use whenever the user asks to "create an annotated PDF for X.step", "annotate the holes on X", or "mark the threaded holes on X". Also handles multi-face layouts (e.g. left+right panels in top row, bottom face panel spanning full bottom row).
---

# Annotate STEP — Multi-Face Annotated PDF

Produces a color-annotated PDF from any STEP file showing selected faces with hole callouts.

**Required tool**: `mcp__freecad__execute_code`
**Required Python packages**: `matplotlib`, `reportlab`, `Pillow`

---

## Step 0 — Install dependencies

Run this first if packages may be missing:
```bash
pip3 install reportlab pillow --break-system-packages -q
```

---

## Step 1 — Confirm inputs

Ask the user (if not already provided):
1. **STEP file path** — full path to the `.step` / `.stp` file
2. **Which faces to show** — e.g. "top", "left and right", "left + right + bottom"
3. **Which threads to annotate** — per face, e.g. "left/right: M3×0.5 and M5×0.8; bottom: M3×0.5 and M4×0.7"
4. **PDF layout** — e.g. "single page, left+right panels on top row, bottom panel spanning full bottom row"

Default CAD directory: `/Users/chinnadevarapu/Documents/Antigravity/CAD/`

---

## Step 2 — Discover all faces via FreeCAD

**CRITICAL**: Never use `max(shape.Faces, key=lambda f: f.normalAt(0,0).x)` to find faces — when multiple faces share the same normal direction, `max()` picks arbitrarily and often returns a small edge face with no holes.

Instead, enumerate ALL faces, group by dominant normal axis, and pick the correct one using bounding box coordinates.

Run this discovery code first:

```python
import Part, json, math

step_path = "STEP_FILE_PATH_HERE"
shape = Part.Shape()
shape.read(step_path)

print(f"Total faces: {len(shape.Faces)}")
print()

for i, f in enumerate(shape.Faces):
    n = f.normalAt(0, 0)
    bb = f.BoundBox
    area = f.Area
    # Print faces that are planar (dominant axis > 0.9) and large enough
    dominant = max(abs(n.x), abs(n.y), abs(n.z))
    if dominant > 0.9 and area > 100:  # area in mm²
        axis = "X" if abs(n.x) > 0.9 else ("Y" if abs(n.y) > 0.9 else "Z")
        sign = "+" if (n.x if abs(n.x)>0.9 else (n.y if abs(n.y)>0.9 else n.z)) > 0 else "-"
        bb_val = bb.XMin if axis=="X" else (bb.YMin if axis=="Y" else bb.ZMin)
        print(f"Face {i:3d}: normal={sign}{axis}  area={area:.0f}mm²  "
              f"BB_{axis}={bb_val:.2f}  wires={len(f.Wires)}")

with open("/tmp/face_discovery.txt", "w") as f_out:
    f_out.write("done")
print("\nSaved marker to /tmp/face_discovery.txt")
```

Read the output:
```bash
jq -r '.result[].stdout // empty' <TOOL_RESULT_FILE> | head -80
```

**From the output, identify the correct face index for each panel:**
- Left outer face: large X-normal face with the most negative BoundBox.XMin (or XMax)
- Right outer face: large X-normal face with the most positive BoundBox.XMax
- Top face: Z-normal face with most positive ZMax
- Bottom face: Z-normal face with most negative ZMin
- Front/Back: Y-normal faces

Write down the face indices (e.g. face 52 = left outer, face 54 = right outer, face 4 = bottom).

---

## Step 3 — Extract geometry for chosen faces

**CRITICAL hole data rule**: Store **3D coordinates** (cx, cy, cz) for all holes — NOT 2D. This is required for correct projection in Step 5.

Run this extraction code with the identified face indices:

```python
import Part, json, math

step_path = "STEP_FILE_PATH_HERE"
shape = Part.Shape()
shape.read(step_path)

def get_outer_pts(face):
    """Discretize outer wire boundary (wire index 0). Returns list of [x, y, z]."""
    pts = []
    for e in face.Wires[0].Edges:
        pts.extend([[p.x, p.y, p.z] for p in e.discretize(20)])
    return pts

def get_holes(face):
    """Extract all hole circles from wires 1..N. Returns list of dicts with cx,cy,cz,r."""
    holes = []
    for i, w in enumerate(face.Wires[1:], 1):
        edges = w.Edges
        # Prefer single-edge arc (clean circle from CAD)
        if len(edges) == 1:
            try:
                curve = edges[0].Curve
                c = curve.Center
                holes.append({"idx": i, "cx": c.x, "cy": c.y, "cz": c.z, "r": curve.Radius})
                continue
            except:
                pass
        # Fallback: discretize and compute centroid + mean radius
        all_pts = []
        for e in edges:
            all_pts.extend([[p.x, p.y, p.z] for p in e.discretize(16)])
        xs = [p[0] for p in all_pts]
        ys = [p[1] for p in all_pts]
        zs = [p[2] for p in all_pts]
        cx = sum(xs)/len(xs); cy = sum(ys)/len(ys); cz = sum(zs)/len(zs)
        r = sum(math.sqrt((x-cx)**2+(y-cy)**2+(z-cz)**2)
                for x,y,z in zip(xs,ys,zs)) / len(xs)
        holes.append({"idx": i, "cx": cx, "cy": cy, "cz": cz, "r": r})
    return holes

# Replace face indices with values from Step 2
faces = shape.Faces
out = {
    "left":   {"outer": get_outer_pts(faces[52]), "holes": get_holes(faces[52])},
    "right":  {"outer": get_outer_pts(faces[54]), "holes": get_holes(faces[54])},
    "bottom": {"outer": get_outer_pts(faces[4]),  "holes": get_holes(faces[4])},
}

with open("/tmp/PART_NAME_faces.json", "w") as f:
    json.dump(out, f)

# Print hole summary for verification
for name, fdata in out.items():
    print(f"\n{name}: {len(fdata['holes'])} holes")
    for h in sorted(fdata["holes"], key=lambda h: h["r"]):
        print(f"  r={h['r']:.3f}  cx={h['cx']:.2f}  cy={h['cy']:.2f}  cz={h['cz']:.2f}")

print("\nSaved to /tmp/PART_NAME_faces.json")
```

Read hole summary:
```bash
jq -r '.result[].stdout // empty' <TOOL_RESULT_FILE> | head -80
```

**Verify the printed hole table matches the thread sizes the user specified.** If radii don't match expectations, re-examine the face discovery output and try different face indices.

---

## Step 4 — Classify holes by radius

Use these radius ranges. Adjust if the user specifies different thread sizes:

| Thread | Nominal dia | Radius range | Color (default) | Notes |
|--------|-------------|--------------|-----------------|-------|
| M2×0.4 | 2.0 mm | 0.85–1.05 mm | — | tap drill ~1.6 mm |
| M2.5×0.45 | 2.5 mm | 1.10–1.30 mm | — | tap drill ~2.05 mm |
| M3×0.5 | 3.0 mm | 1.40–1.65 mm | Blue `#1565C0` | clearance r≈1.6, tap r≈1.25 |
| M3.5×0.5 | 3.5 mm | 1.65–1.85 mm | — | nominal r=1.75 |
| M4×0.7 | 4.0 mm | 1.85–2.20 mm | Orange `#E65100` | tap drill ~3.3 mm |
| M5×0.8 | 5.0 mm | 2.30–2.60 mm | Green `#2E7D32` | tap drill ~4.2 mm |
| M6×1.0 | 6.0 mm | 2.75–3.10 mm | — | tap drill ~5.0 mm |

**Key rule**: holes modeled at nominal diameter sit near the top of the range; holes modeled at tap-drill diameter sit near the bottom. If a hole falls between two ranges, report the ambiguity and ask the user.

**User preference**: only annotate holes that matter for assembly. Do not label every hole type unless explicitly asked.

---

## Step 5 — Generate annotated PDF

### 2D projection rules (CRITICAL)

Each face is a plane — to plot it correctly, drop the axis that is constant (the normal axis):

| Face normal | Normal axis | 2D axes to use | Code |
|-------------|-------------|----------------|------|
| ±X (left/right) | X | Y and Z | `(p[1], p[2])` for outer pts; `(h["cy"], h["cz"])` for holes |
| ±Y (front/back) | Y | X and Z | `(p[0], p[2])` for outer pts; `(h["cx"], h["cz"])` for holes |
| ±Z (top/bottom) | Z | X and Y | `(p[0], p[1])` for outer pts; `(h["cx"], h["cy"])` for holes |

### Layout

Use `matplotlib.gridspec.GridSpec` for multi-panel layouts:

```python
# Example: 2 rows — top has left+right panels, bottom has bottom face
import matplotlib.gridspec as gridspec
fig = plt.figure(figsize=(18, 12))
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)
ax_left   = fig.add_subplot(gs[0, 0])
ax_right  = fig.add_subplot(gs[0, 1])
ax_bottom = fig.add_subplot(gs[1, :])   # gs[1, :] spans full bottom row
```

For 3 equal panels side by side: `fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 8))`

### Complete draw function

```python
import json, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.units import mm
from PIL import Image as PILImage

JSON_PATH  = "/tmp/PART_NAME_faces.json"
OUT_PDF    = "/path/to/output/PART_NAME_annotated.pdf"
PART_LABEL = "PART_NAME"

# Define thread classes per face group: label → (r_min, r_max, hex_color)
LR_CLASSES = {
    "M3\u00d70.5": (1.40, 1.65, "#1565C0"),   # blue
    "M5\u00d70.8": (2.30, 2.60, "#2E7D32"),   # green
}
BOT_CLASSES = {
    "M3\u00d70.5": (1.40, 1.65, "#1565C0"),   # blue
    "M4\u00d70.7": (1.85, 2.20, "#E65100"),   # orange
}

with open(JSON_PATH) as f:
    data = json.load(f)

def classify(r, classes):
    for label, (rmin, rmax, color) in classes.items():
        if rmin <= r <= rmax:
            return label, color
    return None, None

def leader_offset(hx, hy, cx_part, cy_part, dist=14):
    dx = hx - cx_part; dy = hy - cy_part
    mag = math.sqrt(dx*dx + dy*dy) or 1
    return hx + dx/mag * dist, hy + dy/mag * dist

def draw_panel(ax, outer_pts_2d, holes_2d, classes, title):
    """
    outer_pts_2d: list of (x2d, y2d) — the outer boundary
    holes_2d:     list of (x2d, y2d, r) — holes
    classes:      dict of label → (rmin, rmax, color)
    """
    xs = [p[0] for p in outer_pts_2d]
    ys = [p[1] for p in outer_pts_2d]
    ax.set_aspect('equal')
    ax.axis('off')
    ax.fill(xs, ys, color='#f5f5f5', zorder=0)
    ax.plot(xs + [xs[0]], ys + [ys[0]], 'k-', linewidth=1.0, zorder=1)

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    cx_p = (x_min + x_max) / 2
    cy_p = (y_min + y_max) / 2

    # Draw unclassified holes plain black
    for (hx, hy, r) in holes_2d:
        lbl, _ = classify(r, classes)
        if lbl is None:
            ax.add_patch(plt.Circle((hx, hy), r, color='k',
                                    fill=False, linewidth=0.7, zorder=2))

    # Draw classified holes + leader annotations
    counts = {lbl: 0 for lbl in classes}
    for (hx, hy, r) in holes_2d:
        lbl, color = classify(r, classes)
        if lbl is None:
            continue
        ax.add_patch(plt.Circle((hx, hy), r, color=color,
                                fill=False, linewidth=1.5, zorder=3))
        counts[lbl] += 1
        lx, ly = leader_offset(hx, hy, cx_p, cy_p, dist=14)
        angle = math.atan2(ly - hy, lx - hx)
        tip_x = hx + r * math.cos(angle)
        tip_y = hy + r * math.sin(angle)
        ax.annotate(
            lbl,
            xy=(tip_x, tip_y), xytext=(lx, ly),
            fontsize=7.0, color=color, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=color, lw=0.8),
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color, lw=0.8),
            zorder=5, ha='center', va='center'
        )

    handles = [
        mpatches.Patch(edgecolor=classes[lbl][2], facecolor='white', linewidth=1.5,
                       label=f"{lbl}  ({counts[lbl]}\u00d7)")
        for lbl in classes if counts[lbl] > 0
    ] + [mpatches.Patch(edgecolor='black', facecolor='white', linewidth=0.7,
                        label="Other geometry")]
    ax.legend(handles=handles, loc='lower right', fontsize=7.0, framealpha=0.9)

    pad = 12
    ax.set_xlim(x_min - pad, x_max + pad)
    ax.set_ylim(y_min - pad, y_max + pad)
    ax.set_title(title, fontsize=9, fontweight='bold', pad=6)

# ── Project 3D face data → 2D panel coordinates ───────────────────────────
# X-normal faces (left/right): drop X axis → use (y, z)
left_outer_pts  = [(p[1], p[2]) for p in data["left"]["outer"]]
left_holes      = [(h["cy"], h["cz"], h["r"]) for h in data["left"]["holes"]]

right_outer_pts = [(p[1], p[2]) for p in data["right"]["outer"]]
right_holes     = [(h["cy"], h["cz"], h["r"]) for h in data["right"]["holes"]]

# Z-normal faces (top/bottom): drop Z axis → use (x, y)
bot_outer_pts   = [(p[0], p[1]) for p in data["bottom"]["outer"]]
bot_holes       = [(h["cx"], h["cy"], h["r"]) for h in data["bottom"]["holes"]]

# ── Layout ─────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 12))
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)
ax_left   = fig.add_subplot(gs[0, 0])
ax_right  = fig.add_subplot(gs[0, 1])
ax_bottom = fig.add_subplot(gs[1, :])

draw_panel(ax_left,   left_outer_pts,  left_holes,  LR_CLASSES,
           "Left Face (\u2212X view)")
draw_panel(ax_right,  right_outer_pts, right_holes, LR_CLASSES,
           "Right Face (+X view)")
draw_panel(ax_bottom, bot_outer_pts,   bot_holes,   BOT_CLASSES,
           "Bottom Face (\u2212Z view)")

fig.suptitle(f"{PART_LABEL} \u2014 Annotated Hole Views",
             fontsize=13, fontweight='bold', y=0.98)

img_path = "/tmp/annotated_preview.png"
plt.savefig(img_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"PNG saved: {img_path}")

# ── Build PDF ──────────────────────────────────────────────────────────────
img = PILImage.open(img_path)
iw, ih = img.size
page_w, page_h = landscape(A4)
margin = 10 * mm
avail_w = page_w - 2 * margin
avail_h = page_h - 2 * margin - 18 * mm
scale = min(avail_w / iw, avail_h / ih)
draw_w, draw_h = iw * scale, ih * scale
draw_x = (page_w - draw_w) / 2
draw_y = margin

c = rl_canvas.Canvas(OUT_PDF, pagesize=landscape(A4))
c.setFont("Helvetica-Bold", 12)
c.drawCentredString(page_w/2, page_h - 12*mm,
                    f"{PART_LABEL} \u2014 Annotated Hole Views")
c.setFont("Helvetica", 8)
c.drawCentredString(page_w/2, page_h - 19*mm,
    "M3\u00d70.5 (blue) | M4\u00d70.7 (orange) | M5\u00d70.8 (green) | Black = other geometry")
c.drawImage(img_path, draw_x, draw_y, width=draw_w, height=draw_h)
c.setFont("Helvetica", 7)
c.setFillColorRGB(0.5, 0.5, 0.5)
c.drawCentredString(page_w/2, 6*mm,
                    "Generated from STEP via FreeCAD | All dimensions in mm")
c.save()
print(f"PDF saved: {OUT_PDF}")
```

---

## Step 6 — Open and verify

```bash
open /path/to/output/PART_NAME_annotated.pdf
```

Verify:
- Correct number of panels with correct face shapes
- Holes are correctly colored (not misclassified)
- Unclassified holes appear plain black with no label
- Counts in the legend match what FreeCAD reported in Step 3

---

## Critical rules and lessons learned

### Face selection
- **NEVER** use `max(shape.Faces, key=...)` to pick faces — it returns arbitrary results when multiple faces have the same normal. Always enumerate faces in Step 2 and use explicit indices.
- After finding candidate face indices, check the bounding box position (XMin/XMax) to confirm which is truly the outer vs inner face.
- A small face area with no holes is a warning sign you've selected the wrong face.

### Hole coordinate storage
- **Always store 3D coordinates** (cx, cy, cz) from FreeCAD, not 2D. Drop the correct axis in Step 5 based on the face normal. Storing 2D directly leads to projection errors.

### FreeCAD MCP output size
- FreeCAD MCP results exceed the MCP token limit for large STEP files. **Always** save geometry to `/tmp/...json` and read the stdout summary via:
  ```bash
  jq -r '.result[].stdout // empty' <TOOL_RESULT_FILE> | head -80
  ```
- Never try to return large geometry data directly from `mcp__freecad__execute_code`.

### Single-edge arc detection
- Prefer `edges[0].Curve.Center` and `.Radius` for single-edge wires — this gives exact geometry.
- Fall back to discretize + centroid only when the wire has multiple edges.

### matplotlib gridspec for complex layouts
- Use `gridspec.GridSpec(rows, cols)` for layouts where panels have different sizes.
- `gs[1, :]` spans a subplot across all columns in row 1.
- Set `hspace` and `wspace` on the GridSpec to control spacing.

### ReportLab unicode
- Use `\u00d7` for × (multiplication sign) in all canvas strings.
- For subscripts/superscripts, use `<super>`/`<sub>` tags only inside `Paragraph` objects, not raw canvas strings.
- Use `landscape(A4)` from `reportlab.lib.pagesizes` for landscape orientation.

### Hole radius classification
- Holes modeled at tap-drill diameter sit near the lower end of the range; holes at nominal diameter sit near the upper end.
- r=1.587mm is an M3 clearance hole (nominal r=1.5mm + clearance), classifies in the M3×0.5 range (1.40–1.65mm).
- r=2.250mm is an M4 clearance hole (4.5mm drill), classifies in M4×0.7 range.
- If ambiguous (between two ranges), report the specific radius to the user and ask for confirmation.

### Annotation style
- Only annotate holes critical for assembly. Do not label every feature.
- Unclassified holes (bores, counterbores, clearance holes not needed for assembly) → plain black, no label.
