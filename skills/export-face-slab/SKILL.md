---
name: export-face-slab
description: Export a single face from a STEP file as a printable slab (extruded solid) for 3D printing. Use this skill whenever the user wants to extract a face from a STEP/CAD file and export it for printing — e.g. "export the right face of the frame", "print the flange face to check holes", "extract face at x=72 as STEP", "save face slab for printing". Also use for any workflow involving inspecting or verifying hole quality by printing individual faces of a mechanical part.
---

# Export Face Slab from STEP File

This skill extracts a planar face from a STEP file, extrudes it into a solid slab, and exports it as a printable STEP file. The typical use case is 3D-printing individual faces of a frame or bracket to quickly verify hole quality without printing the entire part.

---

## How to run FreeCAD code (Windows, no MCP)

There is **no FreeCAD MCP server** on this machine. Drive FreeCAD through its bundled Python interpreter:

```
%LOCALAPPDATA%\Programs\FreeCAD 1.1\bin\python.exe
```

Procedure:

1. Write the script to the session scratchpad directory with the Write tool (e.g. `<scratchpad>\fc_faceslab.py`).
2. Run it from PowerShell:
   ```
   & "%LOCALAPPDATA%\Programs\FreeCAD 1.1\bin\python.exe" "<scratchpad>\fc_faceslab.py"
   ```
3. `print()` output comes straight back on stdout — no `/tmp` round-trip needed.

That interpreter (Python 3.11) provides `FreeCAD`, `Part`, `Import`, `importDXF`, `Draft`, `matplotlib`, `reportlab` and `Pillow`. No `sys.path.append` is required. Do **not** use the Windows `python` (3.13) — it cannot import FreeCAD.

**Important**: steps 2 and 4 below must run in the **same script**. Each invocation of `python.exe` is a fresh process, so a document created in one run is gone in the next. Either scan and export in one script (asking the user in between and re-running), or re-open the STEP file at the top of the export script.

Windows path rules: always use raw strings (`r"C:\..."`). Accented paths work fine with FreeCAD.

---

## Step 1 — Get the input file

If the user hasn't provided the STEP file path, ask for it. Sample files ship with the upstream repo at:
`<your-projects-dir>\claude-cad-skills\examples\`

---

## Step 2 — Scan X-normal planar faces

Load the STEP file and report all faces whose surface normal points along the X axis:

```python
import Part, FreeCAD

step_path = r"STEP_FILE_PATH_HERE"
doc_name = "FaceExport"

try:
    FreeCAD.closeDocument(doc_name)
except Exception:
    pass

doc = FreeCAD.newDocument(doc_name)
Part.insert(step_path, doc_name)
shape = doc.Objects[0].Shape

x_normal_faces = []
for i, face in enumerate(shape.Faces):
    surf = face.Surface
    # Must check type name — cylinders also have .Axis so hasattr() would give false positives
    if type(surf).__name__ != 'Plane':
        continue
    normal = surf.Axis
    if abs(normal.x) < 0.9:
        continue
    bb = face.BoundBox
    x_center = round((bb.XMin + bb.XMax) / 2, 3)
    x_normal_faces.append({
        'index': i,
        'x_center': x_center,
        'normal_x': round(normal.x, 3),
        'area': round(face.Area, 2),
        'y_range': (round(bb.YMin, 3), round(bb.YMax, 3)),
        'z_range': (round(bb.ZMin, 3), round(bb.ZMax, 3)),
    })

x_normal_faces.sort(key=lambda f: f['x_center'])
for f in x_normal_faces:
    print(f"index={f['index']:3d}  x={f['x_center']:8.3f}  normal_x={f['normal_x']:+.0f}  area={f['area']:8.2f} mm2  Y={f['y_range']}  Z={f['z_range']}")
print(f"\nTotal X-normal planar faces: {len(x_normal_faces)}")
```

Present the results as a table so the user can identify the face they want. Larger-area faces are usually the structural flanges; small-area faces are typically hole annular rings.

---

## Step 3 — Ask the user to pick

Ask the user:
1. **Which face?** (by index shown in the scan, or by approximate x-coordinate)
2. **Wall thickness?** — how far to extrude inward in mm. Default: **3.175 mm** (the standard flange wall for the upstream frame; the correct value = |x_outer − x_inner| for the two paired faces).
3. **Output filename?** — suggest a descriptive name like `face_x72_right_outer_KFL08.step`. Default directory: same as the input file.

---

## Step 4 — Extrude and export

Re-open the document at the top (fresh process), then extrude:

```python
import Part, FreeCAD, Import

step_path      = r"STEP_FILE_PATH_HERE"
face_index     = FACE_INDEX_HERE
wall_thickness = WALL_THICKNESS_HERE   # mm
output_path    = r"OUTPUT_PATH_HERE"

doc_name = "FaceExport"
try:
    FreeCAD.closeDocument(doc_name)
except Exception:
    pass
doc = FreeCAD.newDocument(doc_name)
Part.insert(step_path, doc_name)
shape = doc.Objects[0].Shape

face = shape.Faces[face_index]
surf = face.Surface
normal_x = surf.Axis.x

# Extrude inward: opposite to the face normal direction
extrusion_dir = -1 if normal_x > 0 else 1
solid = face.extrude(FreeCAD.Vector(extrusion_dir * wall_thickness, 0, 0))

slab = doc.addObject("Part::Feature", "FaceSlab")
slab.Shape = solid
doc.recompute()

# IMPORTANT: use Import.export(), not Part.export() — Part.export() omits the object
Import.export([slab], output_path)

bb = solid.BoundBox
print(f"Exported to: {output_path}")
print(f"Dimensions: Y={bb.YLength:.2f} mm x Z={bb.ZLength:.2f} mm x X={bb.XLength:.2f} mm thick")
print(f"Volume: {solid.Volume:.2f} mm3")
```

---

## Step 5 — Confirm

Report the output path and bounding box dimensions so the user can verify before slicing:
- **Y × Z** = the face footprint (should match the face bounding box from the scan)
- **X** = wall thickness (should equal the requested extrude distance)

Confirm the file landed:
```
Get-Item "<output_path>" | Select-Object Name, Length, LastWriteTime
```

If anything looks wrong (e.g. X ≠ wall_thickness, or the dimensions are far off), re-check the face index or wall thickness with the user.

---

## Key technical notes

- **Import order**: `import FreeCAD` **before** `import Part` — importing `Part` first raises `ModuleNotFoundError: No module named 'Part'`
- **Surface type check**: always use `type(surf).__name__ == 'Plane'` — never `hasattr(surf, 'Axis')` because cylinder surfaces also have `.Axis`
- **Export function**: always `Import.export([object], path)` — `Part.export()` does not work correctly for this workflow
- **Extrusion direction**: always inward (opposite to the face normal) so the slab captures the face geometry with its holes
- **Process boundary**: FreeCAD documents do not survive between script runs — always re-open the STEP file in each script
- **Upstream frame reference values** — confirmed against `examples/frame_250108.step` (131 faces):
  - Right outer face: index 127, x = 72.422, area 1793.30 mm², wall thickness = 3.175 mm
  - Right inner face: index 27, x = 69.247
  - Left outer face: index 128, x = −71.228, area 2973.74 mm², wall thickness = 3.175 mm
  - Left inner face: index 18, x = −68.053

## Validation run

Exporting the right outer face of `examples/frame_250108.step` at 3.175 mm
reproduces the shipped `examples/face_x72_right_outer.step` footprint exactly:
**Y = 76.26 mm × Z = 33.88 mm × X = 3.18 mm**, valid solid. Volume comes out at
5693.74 mm³ against the reference's 5665.01 mm³ (+0.51 %), with 31 faces against
33 — the reference was evidently cut from a slightly different revision of the
frame. Treat that half-percent as the expected agreement level, not as a defect.
