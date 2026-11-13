"""Open PolyForge: concept media from the TRL 3 model (option PF1, carried; choice awaiting Amish).

Run from the repo root, one picture per process on a small machine:
    python cad/src/concept_media.py hero | cutaway | exploded | flow | web | blueprint
Geometry comes from cad/src/model.py; numbers come from OPF-CAL-001 (docs/04-calcs/sizing_results.json) and are
estimates. Uses the pieces of .kit/concept.py render_all one at a time, with a 1.75 m person for scale.
CONCEPT, NOT FOR FABRICATION.
"""
import csv
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
import model as M  # noqa: E402

PROJECT, TITLE, DWG, DATE = "Open PolyForge", "Bench melt-blown PP media machine (option PF1, carried)", "OPF-DWG-010", "2026-11-12"
MD = ROOT / "media"
RES = ROOT / "docs/04-calcs/sizing_results.json"
SMALL = ("bolt", "washer", "nut", "rivet", "screw (DIN", "weld", "needle", "thermocouple", "foot")


def parts(context=True, small=False, clear=0.3):
    out = []
    for q in M.components(M.CHOSEN):
        if q["kind"] == "context" and not context:
            continue
        if not small and (q["kind"] in ("fastener", "weld") or any(s in q["name"].lower() for s in SMALL)):
            continue
        a = clear if q["material_name"] == "polycarbonate" else 1.0
        out.append(Part(q["name"], q["shape"], q["color"], q["bom"], tuple(q["explode"]), a))
    return out


def hero():
    ps = K.with_scale_figure([p for p in parts(context=True) if not p.name.startswith("Door -Y")])
    return K._render(ps, MD / "hero.png", title=PROJECT, size=(10, 6.5), elev=18, azim=-60,
                     note="Option PF1 (carried; choice awaiting Amish). Seen from the operator side, front left and above, 18 deg "
                          "elevation. Grey: a 1.75 m person and the maker space's 2 ft x 8 ft bench. Extruder, melt pump and die "
                          "feed a traversing drum inside a clear, exhausted, interlocked enclosure (door hidden to show the inside); 2,360 mm long on the bench. "
                          "CONCEPT, NOT FOR FABRICATION")


def cutaway():
    from build123d import Box, Pos
    cutter = Pos(1250, 400, 1200) * Box(900, 800, 1000)        # keeps y > 0: the near half is removed
    ps = []
    for p in parts(context=False):
        bb = p.shape.bounding_box()
        if p.alpha < 1.0 or bb.min.X < 860 or bb.max.X > 1600 or "Enclosure" in p.name or "Base frame" in p.name:
            continue
        try:
            h = p.shape & cutter
            if h.volume > 1e-3:
                ps.append(Part(p.name, h, p.color, p.bom))
        except Exception:
            pass
    return K._render(ps, MD / "cutaway.png", azim=-90, elev=12, size=(10, 6.5),
                     title=f"{PROJECT}: cutaway of the forming zone",
                     note="Near half removed, seen from the operator side at 12 deg elevation. Melt pump, split die with its two air "
                          "knives, the 200 mm collector drum 200 mm from the die tip, and the corona bar 40 mm above the drum; "
                          "enclosure panels hidden. CONCEPT, NOT FOR FABRICATION")


def bom_names():
    out = {}
    for r in csv.DictReader((ROOT / "bom/bom.csv").open()):
        n, _, rest = r["item"].partition(" ")
        out[int(n)] = rest.split(",")[0]
    return out


def exploded():
    names = bom_names()
    ps, seen = [], set()
    for p in parts(context=False):
        if p.bom is None or p.alpha < 1.0:
            continue
        label = names.get(p.bom, p.name)
        ps.append(Part(label if p.bom not in seen else "", p.shape, p.color, p.bom if p.bom not in seen else None, p.explode))
        seen.add(p.bom)
    return K._render(ps, MD / "exploded.png", offsets=True, labels=True, size=(12, 8), elev=24, azim=-58,
                     title=f"{PROJECT}: exploded view",
                     note="Seen from the front left and above, 24 deg elevation; numbers match bom/bom.csv. Clear enclosure panels "
                          "not shown. Modules lifted from the base frame in the order they are built")


def flow():
    r = json.loads(RES.read_text())
    a, b = r["air"], r["budget_nominal"]
    stages = [("Wall outlet, 120 V 15 A", f"{r['total_W'][0]:,.0f} W ({r['current_A'][0]:.1f} A)"),
              ("Air pump and heater", f"{a['Q_std_Lmin']:.0f} L/min to 270 C, {b['Air pump (rated input)'] + a['heater_W']:.0f} W"),
              ("Extruder and melt pump", f"{r['polymer']['g_min']:.1f} g/min at 250 C"),
              ("Die: 40 holes, 2 air slots", f"{a['ratio']:.0f} kg air per kg PP, 140 m/s"),
              ("Drum and corona bar", f"{r['web']['area_m2_h']:.1f} m2/h web, -25 kV"),
              ("Exhaust to outdoors", "0.10 m3/s, fumes and ozone")]
    return K.flow_diagram(stages, MD / "flow.png",
                          f"{PROJECT}: power, air, polymer and web through the PF1 machine (estimates, OPF-CAL-001); the air "
                          "heater, not the melt, uses most of the circuit", "")


def web():
    ps = parts(context=False)
    return K.export_web_model(ps, "media", title=f"{PROJECT}: {TITLE}")


def blueprint():
    from build123d import Compound
    from drawing import Sheet, project_views
    r = json.loads(RES.read_text())
    ps = [p for p in parts(context=False) if p.alpha == 1.0]
    shown = K.with_scale_figure(parts(context=True))
    views = project_views(Compound(children=[p.shape for p in ps]), MD / "_views")
    views["iso"] = project_views(Compound(children=[p.shape for p in shown]), MD / "_views_fig")["iso"]
    s = Sheet(project=PROJECT, title=TITLE, dwg_no=DWG, rev="P1", author="Amish Chadha", date=DATE, theme="blueprint",
              material="Detailed TRL 3 model for concept communication",
              revisions=[("P1", "Concept sheet from the TRL 3 model", DATE, "AC")])
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 32, 140, 118, label="Isometric view", sublabel="Not to scale; grey is a 1.75 m person and the bench")
    s.add_notes("Key figures (estimates, OPF-CAL-001)", [
        f"2,360 mm long on a 610 x 2,440 mm bench; enclosure panels not drawn",
        f"Steady draw {r['total_W'][0]:,.0f} W ({r['current_A'][0]:.1f} A) on one 15 A circuit; cap 12 A",
        "Die: 40 grooves 0.3 mm at 1 mm pitch; air slots 2 x 0.3 x 48 mm",
        f"Polymer {r['polymer']['g_min']:.1f} g/min at 250 C; air {r['air']['Q_std_Lmin']:.0f} L/min at 270 C, 140 m/s",
        f"Web {r['web']['area_m2_h']:.1f} m2/h at 25 g/m2, {r['web']['web_width_mm']:.0f} mm wide",
        "Corona -25 kV, 40 mm gap, 1 mA limit; enclosure exhaust 0.10 m3/s",
        f"Parts USD {r['bom_total']:,.2f} (target USD 10,000, proposed)",
        "Makes media for testing only; no respirator claim"], x=276, y=168, width=140)
    s.save(MD / "concept-blueprint")
    shutil.rmtree(MD / "_views", ignore_errors=True)
    shutil.rmtree(MD / "_views_fig", ignore_errors=True)
    return MD / "concept-blueprint.png"


if __name__ == "__main__":
    fns = {"hero": hero, "cutaway": cutaway, "exploded": exploded, "flow": flow, "web": web, "blueprint": blueprint}
    for w_ in sys.argv[1:] or list(fns):
        print(w_, "->", fns[w_]())
