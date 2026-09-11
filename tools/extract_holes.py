#!/usr/bin/env python3
"""Inventaire des perçages d'un DXF ou d'un STEP, sans dépendance externe.

Usage:
    python3 tools/extract_holes.py examples/frame_250108.step examples/*.dxf

DXF : lit les entités CIRCLE (codes 10/20 = centre, 40 = rayon).
STEP: lit les CYLINDRICAL_SURFACE et remonte leur AXIS2_PLACEMENT_3D pour
      obtenir le diamètre, la position et la direction de l'axe. Les trous
      dédoublés (une surface par demi-cylindre) sont fusionnés sur leur axe.

Sert à retrouver la quincaillerie du commerce à partir de la seule géométrie :
un carré de 31 mm en M3 autour d'un Ø22 = NEMA 17, 4 trous sur un cercle Ø16
autour d'un Ø10,5 = écrou à bride T8, un Ø15,1 = LM8UU, etc.
"""
import collections
import re
import sys


def dxf_circles(path):
    """-> [(diametre, x, y)] pour chaque entité CIRCLE du DXF."""
    toks = [l.strip() for l in open(path, errors="ignore")]
    out, i = [], 0
    while i < len(toks) - 1:
        if toks[i] == "0" and toks[i + 1] == "CIRCLE":
            data, j = {}, i + 2
            while j < len(toks) - 1 and toks[j] != "0":
                data.setdefault(toks[j], []).append(toks[j + 1])
                j += 2
            out.append((round(2 * float(data["40"][0]), 3),
                        float(data["10"][0]), float(data["20"][0])))
            i = j
        else:
            i += 1
    return out


def _split_args(s):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            depth += {"(": 1, ")": -1}.get(ch, 0)
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def step_holes(path):
    """-> [(diametre, (x,y,z), (dx,dy,dz))] pour chaque surface cylindrique."""
    txt = re.sub(r"\s+", " ", open(path, errors="ignore").read())
    ents = {int(m.group(1)): (m.group(2), m.group(3))
            for m in re.finditer(r"#(\d+)\s*=\s*([A-Z_0-9]+)\s*\((.*?)\)\s*;", txt)}

    def triple(ref):
        return tuple(float(v) for v in
                     _split_args(ents[ref][1])[1].strip("() ").split(","))

    out = []
    for typ, argstr in ents.values():
        if typ != "CYLINDRICAL_SURFACE":
            continue
        a = _split_args(argstr)
        placement = _split_args(ents[int(a[1][1:])][1])
        out.append((round(2 * float(a[2]), 3),
                    triple(int(placement[1][1:])),
                    triple(int(placement[2][1:]))))
    return out


def axis_name(d):
    for i, name in enumerate("XYZ"):
        if abs(d[i]) > 0.9:
            return name
    return f"({d[0]:.2f},{d[1]:.2f},{d[2]:.2f})"


def report(path):
    print(f"\n=== {path} ===")
    if path.lower().endswith(".dxf"):
        circles = dxf_circles(path)
        groups = collections.defaultdict(list)
        for dia, x, y in circles:
            groups[dia].append((round(x, 2), round(y, 2)))
        for dia in sorted(groups):
            print(f"  Ø{dia:8.3f} ×{len(groups[dia]):3d}  {sorted(groups[dia])}")
        return

    # STEP : fusionne les surfaces partageant diamètre + droite d'axe
    uniq = {}
    for dia, loc, direction in step_holes(path):
        ax = axis_name(direction)
        drop = {"X": (1, 2), "Y": (0, 2), "Z": (0, 1)}.get(ax)
        pos = (round(loc[drop[0]], 2), round(loc[drop[1]], 2)) if drop else \
              tuple(round(v, 2) for v in loc)
        uniq[(dia, ax, pos)] = True
    groups = collections.defaultdict(list)
    for dia, ax, pos in uniq:
        groups[(dia, ax)].append(pos)
    for dia, ax in sorted(groups):
        pos = sorted(groups[(dia, ax)])
        print(f"  Ø{dia:8.3f}  axe {ax:>3}  ×{len(pos):3d}  {pos}")


if __name__ == "__main__":
    paths = sys.argv[1:]
    if not paths:
        sys.exit(__doc__)
    for p in paths:
        report(p)
