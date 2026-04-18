---
name: export-face-slab
description: Export a single face from a STEP file as a printable slab (extruded solid) for 3D printing. Use this skill whenever the user wants to extract a face from a STEP/CAD file and export it for printing — e.g. "export the right face of the frame", "print the flange face to check holes", "extract face at x=72 as STEP", "save face slab for printing". Also use for any workflow involving inspecting or verifying hole quality by printing individual faces of a mechanical part.
---

# Export Face Slab from STEP File

This skill extracts a planar face from a STEP file, extrudes it into a solid slab, and exports it as a printable STEP file. The typical use case is 3D-printing individual faces of a frame or bracket to quickly verify hole quality without printing the entire part.

The tool used to talk to FreeCAD is `mcp__freecad__execute_code`.

---

## Step 1 — Get the input file

If the user hasn't provided the STEP file path, ask for it. Default search location: `/Users/chinnadevarapu/Documents/Antigravity/CAD/`

---

## Step 2 — Scan X-normal planar faces

Load the STEP file and report all faces whose surface normal points along the X axis. Run this code:

```python
import Part, FreeCAD

doc_name = "FaceExport"
# Close any existing document with this name to avoid conflicts
try:
    FreeCAD.closeDocument(doc_name)
except:
    pass

doc = FreeCAD.newDocument(doc_name)
Part.insert("STEP_FILE_PATH_HERE", doc_name)
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
    print(f"index={f['index']:3d}  x={f['x_center']:8.3f}  normal_x={f['normal_x']:+.0f}  area={f['area']:8.2f} mm²  Y={f['y_range']}  Z={f['z_range']}")
print(f"\nTotal X-normal planar faces: {len(x_normal_faces)}")
```

Present the results as a table so the user can identify the face they want. Larger-area faces are usually the structural flanges; small-area faces are typically hole annular rings.

---

## Step 3 — Ask the user to pick

Ask the user:
1. **Which face?** (by index shown in the scan, or by approximate x-coordinate)
2. **Wall thickness?** — how far to extrude inward in mm. Default: **3.175 mm** (this is the standard flange wall for this frame, distance between outer and inner parallel faces). The correct value = |x_outer – x_inner| for the two paired faces.
3. **Output filename?** — suggest a descriptive name like `face_x72_right_outer_KFL08.step`. Default directory: same as the input file.

---

## Step 4 — Extrude and export

Run this code (fill in the values from Step 3):

```python
import Part, FreeCAD, Import

doc = FreeCAD.getDocument("FaceExport")
shape = doc.Objects[0].Shape

face_index = FACE_INDEX_HERE
wall_thickness = WALL_THICKNESS_HERE   # mm
output_path = "OUTPUT_PATH_HERE"

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
print(f"Dimensions: Y={bb.YLength:.2f} mm × Z={bb.ZLength:.2f} mm × X={bb.XLength:.2f} mm thick")
print(f"Volume: {solid.Volume:.2f} mm³")
```

---

## Step 5 — Confirm

Report the output path and bounding box dimensions so the user can verify before slicing:
- **Y × Z** = the face footprint (should match the face bounding box from the scan)
- **X** = wall thickness (should equal the requested extrude distance)

If anything looks wrong (e.g. X ≠ wall_thickness, or the dimensions are far off), re-check the face index or wall thickness with the user.

---

## Key technical notes

- **Surface type check**: always use `type(surf).__name__ == 'Plane'` — never `hasattr(surf, 'Axis')` because cylinder surfaces also have `.Axis`
- **Export function**: always `Import.export([object], path)` — `Part.export()` does not work correctly for this workflow
- **Extrusion direction**: always inward (opposite to the face normal) so the slab captures the face geometry with its holes
- **Frame defaults** (Antigravity frame files in `/Users/chinnadevarapu/Documents/Antigravity/CAD/`):
  - Right outer face: x ≈ 72.422, wall thickness = 3.175 mm
  - Right inner face: x ≈ 69.247
  - Left outer face: x ≈ −71.228, wall thickness = 3.175 mm
  - Left inner face: x ≈ −68.053
