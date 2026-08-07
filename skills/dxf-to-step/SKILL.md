---
name: dxf-to-step
description: >
  Extrudes a 2D DXF profile into a 3D STEP solid using FreeCAD's Python API
  (run through FreeCAD's bundled interpreter — no MCP server needed). Use this
  skill whenever the user wants to convert a DXF file to STEP, extrude a 2D
  drawing into a 3D part, or re-extrude after editing a DXF. Accepts a DXF path,
  STEP output path, and optional thickness (default 0.25 in = 6.35 mm). Also use
  when the user says things like "extrude this DXF", "regenerate the STEP file",
  "turn the DXF into a solid", or "update the STEP after changing the DXF".
---

# DXF → STEP Extrusion via FreeCAD

## Overview

This skill converts a 2D DXF (outer polyline boundary + circle holes) into
an extruded 3D STEP solid using FreeCAD's Python API.

## How to run FreeCAD code (Windows, no MCP)

There is **no FreeCAD MCP server** on this machine. Drive FreeCAD through its
bundled Python interpreter instead:

```
%LOCALAPPDATA%\Programs\FreeCAD 1.1\bin\python.exe
```

Procedure:

1. Write the script to the session scratchpad directory with the Write tool
   (e.g. `<scratchpad>\fc_extrude.py`).
2. Run it from PowerShell:
   ```
   & "%LOCALAPPDATA%\Programs\FreeCAD 1.1\bin\python.exe" "<scratchpad>\fc_extrude.py"
   ```
3. `print()` output comes straight back on stdout. The `/tmp` debug-file
   round-trip the MCP version needed is **no longer necessary** — print directly.

That interpreter (Python 3.11) already provides `FreeCAD`, `Part`, `Import`,
`Draft`, `ezdxf`, `matplotlib`, `reportlab` and `Pillow`. No
`sys.path.append` is required. Do **not** use the Windows `python` (3.13) —
it cannot import FreeCAD.

Windows path rules: always use raw strings (`r"C:\..."`). Accented paths such as
`...\Mon Bureau privé\...` work fine with FreeCAD.

## ⚠ Read the DXF with ezdxf, never with FreeCAD's importer

FreeCAD 1.1.3's DXF importers do **not** work on this machine:

- The C++ importer (`importDXF.insert()` and `Import.readDXF()`) silently
  creates **zero** objects. `freecadcmd` reveals the reason in its import
  summary: *"DXF file didn't load"*, with a blank DXF version — it fails
  before parsing entities, even on a well-formed AC1014 file.
- The legacy importer requires downloading `dxfLibrary.py` from the internet
  (`dxfAllowDownload`), which is not enabled.

Use **ezdxf** instead. It is installed in FreeCAD's interpreter and reads these
files correctly.

**Never compute bulge arcs by hand.** An LWPOLYLINE stores curved segments as a
`bulge` value per vertex; a hand-rolled sagitta formula is easy to get
backwards, which curves arcs inward and silently produces a profile that is too
small (observed: 66.83 × 71.04 mm instead of the correct 92.00 × 74.05 mm, with
holes falling outside the boundary). Always expand polylines with
`entity.virtual_entities()`, which resolves bulges into exact LINE and ARC
segments.

## Inputs to collect

| Parameter | Default | Notes |
|-----------|---------|-------|
| `dxf_path` | — | Absolute path to the source DXF file |
| `step_path` | — | Absolute path for the output STEP file |
| `thickness_mm` | `6.35` (= 0.25 in) | Extrusion depth in mm |
| `doc_name` | `"ExtrudedPart"` | Internal FreeCAD document name (must be unique per run) |

If any are missing, ask the user before proceeding.

## The proven workflow

Validated on `examples/carriage_brass_nut.dxf`: reproduces the reference
`carriage_brass_nut.step` exactly — 92.00 × 74.05 × 6.35 mm, 23415.92 mm³,
45 faces, 0.000 % volume deviation.

```python
import math
import ezdxf
import FreeCAD, Part, Import

dxf_path     = r"C:\absolute\path\to\file.dxf"
step_path    = r"C:\absolute\path\to\output.step"
thickness_mm = 6.35            # 0.25 in; adjust as needed
doc_name     = "ExtrudedPart"

V = FreeCAD.Vector
NORMAL = V(0, 0, 1)


def edges_from_entity(e):
    """LINE / ARC / CIRCLE / LWPOLYLINE / POLYLINE -> list of Part edges at z=0."""
    t = e.dxftype()
    if t == "LINE":
        a, b = e.dxf.start, e.dxf.end
        return [Part.LineSegment(V(a.x, a.y, 0), V(b.x, b.y, 0)).toShape()]
    if t == "ARC":
        c = e.dxf.center
        circ = Part.Circle(V(c.x, c.y, 0), NORMAL, e.dxf.radius)
        a0 = math.radians(e.dxf.start_angle)
        a1 = math.radians(e.dxf.end_angle)
        if a1 <= a0:
            a1 += 2 * math.pi          # ezdxf arcs always run counter-clockwise
        return [Part.ArcOfCircle(circ, a0, a1).toShape()]
    if t == "CIRCLE":
        c = e.dxf.center
        return [Part.Circle(V(c.x, c.y, 0), NORMAL, e.dxf.radius).toShape()]
    if t in ("LWPOLYLINE", "POLYLINE"):
        out = []
        for sub in e.virtual_entities():   # resolves bulges into exact LINE/ARC
            out.extend(edges_from_entity(sub))
        return out
    return []


doc = FreeCAD.newDocument(doc_name)

# Step 1 – Read the DXF with ezdxf and build Part edges
dxf = ezdxf.readfile(dxf_path)
edges = []
for e in dxf.modelspace():
    edges.extend(edges_from_entity(e))

# Step 2 – Group edges into closed wires; largest bbox area = outer boundary
wires = [Part.Wire(g) for g in Part.sortEdges(edges)]
info = sorted(
    [(w.BoundBox.XLength * w.BoundBox.YLength, w) for w in wires],
    key=lambda x: -x[0],
)
outer_wire  = info[0][1]
inner_wires = [w for _, w in info[1:]]

# Step 3 – Face → extrude → add to document
face  = Part.Face([outer_wire] + inner_wires)
solid = face.extrude(V(0, 0, thickness_mm))

feat = doc.addObject("Part::Feature", "ExtrudedPart")
feat.Shape = solid
doc.recompute()

# Step 4 – Export  ⚠️ MUST use Import.export on doc objects, NOT Part.export
# Part.export([solid], path) silently produces an empty STEP — always wrong.
objs = [o for o in doc.Objects if hasattr(o, 'Shape') and o.Shape.Volume > 0]
Import.export(objs, step_path)

# Step 5 – Verify by re-reading the exported STEP (see note below)
check = Part.Shape(); check.read(step_path)
bb = check.BoundBox
print(f"edges: {len(edges)}")
print(f"wires: {len(wires)}, inner: {len(inner_wires)}")
print(f"contour: {outer_wire.BoundBox.XLength:.2f} x {outer_wire.BoundBox.YLength:.2f} mm, "
      f"closed={outer_wire.isClosed()}")
print(f"STEP: {bb.XLength:.2f} x {bb.YLength:.2f} x {bb.ZLength:.2f} mm | "
      f"volume {check.Volume:.2f} mm3 | faces {len(check.Faces)} | valid {check.isValid()}")
```

## Verification steps

**Verify from the re-read STEP, never from the in-memory solid.** A `Part.Face`
built with hole wires reports an inflated `Volume` and `isValid() == False`
before export — the export/read cycle normalises the shape. In the validated
run the in-memory solid reported 30935.04 mm³ and *invalid*, while the exported
STEP read back as 23415.92 mm³ and *valid*. Only the second number is
meaningful.

Checks to run:

1. `outer_wire.isClosed()` must be `True`.
2. The contour bounding box must match the expected part outline. If it looks
   too small, suspect polyline bulge handling — re-check that
   `virtual_entities()` is being used.
3. The re-read STEP must report `valid True` and a plausible volume.
4. `wires` count = expected holes + 1 (the outer boundary).
5. Confirm the file from PowerShell:
   ```
   Get-Item "<step_path>" | Select-Object Name, Length, LastWriteTime
   ```
   A valid STEP is typically > 10 KB.

Report the contour size, volume, face count, and file size to the user.

## Common pitfalls

| Pitfall | Fix |
|---------|-----|
| `importDXF.insert()` / `Import.readDXF()` yield 0 objects | FreeCAD's DXF importers are broken here — read the DXF with `ezdxf` |
| Hand-rolled bulge arcs curve the wrong way → contour too small, holes outside it | Expand polylines with `entity.virtual_entities()`; never compute sagitta by hand |
| In-memory `solid.Volume` inflated and `isValid()` False | Normal for a face with holes — verify by re-reading the exported STEP |
| `Part.export([solid], path)` → empty STEP | Always use `Import.export(objs, path)` where `objs` comes from `doc.Objects` |
| `FreeCAD.newDocument()` name clash if run twice in one script | Use a unique `doc_name`, or `FreeCAD.closeDocument(doc_name)` in a `try/except` first |
| `ModuleNotFoundError: Part` | Import `FreeCAD` **before** `Part` — `Part` is not importable on its own |
| Using the wrong interpreter | The Windows `python` (3.13) cannot import FreeCAD — always call FreeCAD's bundled `python.exe` |
| Backslashes eaten in paths | Use raw strings: `r"C:\path\to\file.dxf"` |
| DXF units mismatch | Confirm the DXF header before converting thickness (`$INSUNITS = 4` means mm) |

## Unit notes

- The upstream project DXFs are in **millimetres** (`$INSUNITS = 4` in DXF HEADER)
- Default thickness is **0.25 in = 6.35 mm** (standard aluminium plate)
- If the user specifies thickness in inches, multiply by 25.4

## Sample files

The upstream repository ships examples at:
`<your-projects-dir>\claude-cad-skills\examples\`
(`carriage_brass_nut.dxf`, `frame_250108.dxf` and their STEP counterparts).
