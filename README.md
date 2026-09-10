# Claude CAD Skills

Three Claude Code skills developed during the Antigravity syringe pump project. They automate the DXF → STEP → annotated PDF pipeline using FreeCAD via MCP.

---

## Skills

| Skill | What it does |
|---|---|
| [`/dxf-to-step`](skills/dxf-to-step/SKILL.md) | Extrudes a 2D DXF profile into a 3D STEP solid |
| [`/annotate-step`](skills/annotate-step/SKILL.md) | Creates an annotated top-face PDF from a STEP file |
| [`/export-face-slab`](skills/export-face-slab/SKILL.md) | Extracts a single face from a STEP and exports it as a printable slab |

---

## Requirements

- [Claude Code](https://claude.ai/code) with FreeCAD MCP server (`mcp__freecad__execute_code`)
- FreeCAD installed (the MCP server connects to it)
- Python packages: `matplotlib`, `reportlab`, `Pillow` (for annotate-step)

Install skills by copying each folder into `~/.claude/skills/`.

---

## Example Prompts

### `/dxf-to-step` — DXF to STEP extrusion

**Basic use:**
```
/dxf-to-step
DXF: /path/to/carriage_brass_nut.dxf
Output: /path/to/carriage_brass_nut.step
Thickness: 6.35mm
```

**Natural language triggers:**
```
Convert carriage_brass_nut.dxf to a STEP file, 6.35mm thick.
```
```
I updated the hole positions in frame_250108.dxf — regenerate the STEP.
```
```
Extrude this DXF into a solid at 0.25 inches thick.
```

**Example files:**
- Input DXF: [`examples/carriage_brass_nut.dxf`](examples/carriage_brass_nut.dxf)
- Output STEP: [`examples/carriage_brass_nut.step`](examples/carriage_brass_nut.step)

---

### `/annotate-step` — Annotated top-face PDF

**Basic use:**
```
/annotate-step
STEP: /path/to/carriage_brass_nut.step
Annotate: M3×0.5 threaded holes
```

**Natural language triggers:**
```
Create an annotated PDF for carriage_brass_nut.step — mark the M3×0.5 holes.
```
```
Annotate the top face of frame_250108_M4holes_flange.step — mark M4 and M5 holes.
```
```
Generate a PDF with callouts for all threaded holes in the carriage plate.
```

**Customizing which holes to annotate:**
```
Annotate frame_250108.step — show M3×0.5 in blue and M4×0.7 in red.
```

**Example files:**
- Input STEP: [`examples/carriage_brass_nut.step`](examples/carriage_brass_nut.step)
- Output PDF: [`examples/carriage_brass_nut_a_annotated.pdf`](examples/carriage_brass_nut_a_annotated.pdf)
- Input STEP (frame): [`examples/frame_250108.step`](examples/frame_250108.step)
- Output PDF (frame): [`examples/frame_250108_M4holes_flange_annotated.pdf`](examples/frame_250108_M4holes_flange_annotated.pdf)

---

### `/export-face-slab` — Extract printable face slab

**Basic use:**
```
/export-face-slab
STEP: /path/to/frame_250108_M4holes_flange.step
Face: right outer face (x ≈ 72mm)
Thickness: 3.175mm
Output: face_x72_right_outer.step
```

**Natural language triggers:**
```
Export the right face of the frame as a printable slab so I can verify the KFL08 holes.
```
```
Extract the flange face at x=72 from frame_250108_M4holes_flange.step — 3mm wall.
```
```
I want to 3D print just the side face to check hole quality before printing the full frame.
```

**Example files:**
- Input STEP: [`examples/frame_250108.step`](examples/frame_250108.step)
- Output slab STEP: [`examples/face_x72_right_outer.step`](examples/face_x72_right_outer.step)

---

## Typical workflow

```
DXF (2D drawing)
    │
    │  /dxf-to-step
    ▼
STEP (3D solid)
    │
    ├──  /annotate-step  ──► Annotated PDF (for documentation / fabrication)
    │
    └──  /export-face-slab  ──► Face slab STEP (for 3D printing hole verification)
```

---

## References

| Document | Sujet |
|---|---|
| [`references/adhesif-support-aluminium-ecran-tactile.md`](references/adhesif-support-aluminium-ecran-tactile.md) | Choix de colle, préparation de surface et mise en œuvre seringue/dispenser pour coller un écran tactile sur un support aluminium |

---

## Background

These skills were developed while building an Antigravity syringe pump — specifically a carriage plate that needed to be compatible with both v4 and v3 brass nut hole patterns. The FreeCAD MCP approach (running FreeCAD Python API headlessly) turned out to be the most reliable way to automate the DXF → STEP → PDF pipeline without a GUI.

Key lessons encoded in the skills:
- Use `Import.export()` not `Part.export()` — `Part.export()` silently produces empty STEP files
- Always extract geometry from the STEP top face (`normalAt z=+1`), never from the full 3D shape
- FreeCAD MCP output exceeds token limits — always write to `/tmp` and read back with Bash
- Hole classification uses radius ranges to handle both nominal-diameter and tap-drill-diameter models
