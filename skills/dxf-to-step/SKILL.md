---
name: dxf-to-step
description: >
  Extrudes a 2D DXF profile into a 3D STEP solid using FreeCAD MCP
  (mcp__freecad__execute_code). Use this skill whenever the user wants to
  convert a DXF file to STEP, extrude a 2D drawing into a 3D part, or
  re-extrude after editing a DXF. Accepts a DXF path, STEP output path,
  and optional thickness (default 0.25 in = 6.35 mm). Also use when the
  user says things like "extrude this DXF", "regenerate the STEP file",
  "turn the DXF into a solid", or "update the STEP after changing the DXF".
---

# DXF → STEP Extrusion via FreeCAD

## Overview

This skill converts a 2D DXF (outer polyline boundary + circle holes) into
an extruded 3D STEP solid using FreeCAD's Python API through the
`mcp__freecad__execute_code` MCP tool.

## Inputs to collect

| Parameter | Default | Notes |
|-----------|---------|-------|
| `dxf_path` | — | Absolute path to the source DXF file |
| `step_path` | — | Absolute path for the output STEP file |
| `thickness_mm` | `6.35` (= 0.25 in) | Extrusion depth in mm |
| `doc_name` | `"ExtrudedPart"` | Internal FreeCAD document name (must be unique per session) |

If any are missing, ask the user before proceeding.

## The proven workflow

Run this as a single `mcp__freecad__execute_code` call:

```python
import FreeCAD, Part, importDXF, Import

dxf_path     = "/absolute/path/to/file.dxf"
step_path    = "/absolute/path/to/output.step"
thickness_mm = 6.35          # 0.25 in; adjust as needed
doc_name     = "ExtrudedPart"  # change if re-running in same session

# Step 1 – Load DXF and collect all edges
doc = FreeCAD.newDocument(doc_name)
importDXF.insert(dxf_path, doc_name)
doc.recompute()

edges = []
for obj in doc.Objects:
    if hasattr(obj, 'Shape'):
        edges.extend(obj.Shape.Edges)

# Step 2 – Sort edges into closed wires; largest bbox = outer boundary
sorted_edges = Part.sortEdges(edges)
wires = [Part.Wire(g) for g in sorted_edges]
wire_info = sorted(
    [(w.BoundBox.XLength * w.BoundBox.YLength, w) for w in wires],
    key=lambda x: -x[0]
)
outer_wire  = wire_info[0][1]
inner_wires = [w for _, w in wire_info[1:]]

# Step 3 – Face → extrude → add to document
face  = Part.Face([outer_wire] + inner_wires)
solid = face.extrude(FreeCAD.Vector(0, 0, thickness_mm))

feat = doc.addObject("Part::Feature", "ExtrudedPart")
feat.Shape = solid
doc.recompute()

# Step 4 – Export  ⚠️ MUST use Import.export on doc objects, NOT Part.export
# Part.export([solid], path) silently produces an empty STEP — always wrong.
objs = [o for o in doc.Objects if hasattr(o, 'Shape') and o.Shape.Volume > 0]
Import.export(objs, step_path)

# Debug output (FreeCAD MCP does not surface print() — write to a file)
with open("/tmp/dxf_to_step_debug.txt", "w") as f:
    f.write(f"edges: {len(edges)}\n")
    f.write(f"wires: {len(wires)}, inner: {len(inner_wires)}\n")
    f.write(f"volume: {solid.Volume:.2f} mm3\n")
    f.write(f"exported objs: {len(objs)}\n")
```

## Verification steps

After the `mcp__freecad__execute_code` call completes:

1. **Read the debug file** with Bash: `cat /tmp/dxf_to_step_debug.txt`
   - Check that `wires` count = expected holes + 1 (the outer boundary)
   - Check that `volume > 0`
   - Check that `exported objs >= 1`
2. **Check the STEP file** with Bash: `ls -lh <step_path>`
   - File must exist and be non-zero in size (a valid STEP is typically > 10 KB)

Report the wire count, volume, and file size to the user.

## Common pitfalls

| Pitfall | Fix |
|---------|-----|
| `Part.export([solid], path)` → empty STEP | Always use `Import.export(objs, path)` where `objs` comes from `doc.Objects` |
| `FreeCAD.newDocument()` name clash if run twice in same session | Use a unique `doc_name` each call (e.g. append a counter or timestamp) |
| `print()` output invisible in MCP result | Write debug info to `/tmp/` and read with Bash |
| DXF units mismatch | Project DXFs use mm (`$INSUNITS = 4`). Confirm before converting thickness. |

## Unit notes

- Project DXFs are in **millimetres** (`$INSUNITS = 4` in DXF HEADER)
- Default thickness is **0.25 in = 6.35 mm** (standard aluminium plate)
- If the user specifies thickness in inches, multiply by 25.4
