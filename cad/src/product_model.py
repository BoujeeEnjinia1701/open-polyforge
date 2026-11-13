"""Open PolyForge: product appearance model (kit 1.9), TRL 3, option PF1 (carried; choice awaiting Amish).

Built from components("PF1") in cad/src/model.py with every part used as it is, so every main dimension comes from
the model. Only scale context is added: a standing 1.75 m mannequin from .kit/context_parts.py on the floor (z = 0) at
the operator side of the bench, and a half-cut copy of the forming zone for the cutaway render. The workbench is the
maker space's own and is shown as context. APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.
Groups: "shell" (outside), "internal" (inside the enclosure), "context" (bench, person), "cut" (half section),
"open" (everything except the door, so the forming zone shows).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Pos, Rot  # noqa: E402
import model as M  # noqa: E402

TITLE = "Open PolyForge: bench melt-blown polypropylene media machine"
PERSON = (1250.0, -M.P["BENCH"][1] / 2 - 420.0)
X0, X1 = M.P["ENCL_X"]

RENDER_VIEWS = [
    {"name": "hero", "groups": ["open", "context"], "explode": False, "el": 16, "az": -55, "args": ["--lens=40"],
     "note": "On a 2 ft x 8 ft maker-space bench beside a 1.75 m operator, seen from the operator side, front left and slightly above "
             "(about 16 deg elevation); door hidden to show the die, drum and corona bar; machine 2,288 mm long"},
    {"name": "studio", "groups": ["shell", "internal"], "explode": False, "el": 22, "az": -55, "args": [],
     "note": "Studio view from the front left and above (about 22 deg elevation): extruder, guard-locked clear enclosure with its "
             "exhaust hood, air pump and control panel on the welded base frame"},
    {"name": "cutaway", "groups": ["cut"], "explode": False, "el": 10, "az": -90, "args": [],
     "note": "Half section of the forming zone seen from the operator side (about 10 deg elevation): melt pump, split die with air "
             "knives, collector drum 200 mm from the die tip and the corona bar 40 mm above it"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 24, "az": -58, "args": [],
     "note": "Exploded view from the front left and above (about 24 deg elevation): modules lifted off the base frame in build order"},
]


def product_parts():
    import context_parts
    out = []
    cutter = Pos(1250, 400, 1200) * Box(900, 800, 1000)
    for q in M.components("PF1"):
        d = dict(q)
        bb = q["shape"].bounding_box()
        inside = bb.min.X >= X0 - 10 and bb.max.X <= X1 + 10 and q["material_name"] != "polycarbonate" and "Enclosure" not in q["name"]
        if q["kind"] == "context":
            d["group"] = "context"
        else:
            d["group"] = "internal" if inside else "shell"
        out.append(d)
        if q["kind"] != "context" and not q["name"].startswith("Door -Y"):
            o = dict(q)
            o["group"] = "open"
            out.append(o)
        if inside and q["kind"] != "weld":
            try:
                h = q["shape"] & cutter
                if h.volume > 1e-3:
                    c = dict(q)
                    c["shape"], c["group"], c["name"] = h, "cut", q["name"] + " (section)"
                    out.append(c)
            except Exception:
                pass
    man = Pos(PERSON[0], PERSON[1], 0) * Rot(0, 0, 160) * context_parts.mannequin(1750.0, "stand")
    out.append(dict(name="Operator (scale)", shape=man, material="clay", material_name="skin", color="#9C9C9E", kind="context",
                    bom=None, group="context", explode=(0, 0, 0), note=""))
    return out


if __name__ == "__main__":
    from collections import Counter
    print(Counter(p["group"] for p in product_parts()))
