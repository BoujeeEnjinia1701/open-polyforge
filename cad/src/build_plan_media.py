"""Open PolyForge: prototype build plan pictures (OPF-BLD-001, STANDARDS section 18), option PF1.

Run from the repo root, one picture group per process on a small machine:
    python cad/src/build_plan_media.py overview
    python cad/src/build_plan_media.py sheets [101 102 ...]
    python cad/src/build_plan_media.py joints [1 2 ...]
    python cad/src/build_plan_media.py steps [1 2 ...]
Every picture is drawn from cad/src/model.py components("PF1"), so pictures and model never disagree:
    docs/05-build-plan/overview.png        every component group pulled apart, numbered in build order
    cad/drawings/OPF-DWG-101 to 110        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import functools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from build123d import Box, Compound, Pos  # noqa: E402
import model as M  # noqa: E402

OUT = ROOT / "docs/05-build-plan"
DWG = ROOT / "cad/drawings"
DATE = "2026-11-12"
PROJECT = "Open PolyForge"


@functools.lru_cache(None)
def raw():
    return [q for q in M.components("PF1") if q["kind"] != "weld"]


def grp(label, keys, color=None, explode=(0, 0, 0), fasteners=False, exclude=()):
    """One picture item from every part whose name contains any of keys."""
    sh = [q["shape"] for q in raw() if any(k in q["name"] for k in keys) and not any(e in q["name"] for e in exclude)
          and (fasteners or q["kind"] != "fastener") and q["kind"] != "context"]
    first = next(q for q in raw() if any(k in q["name"] for k in keys) and not any(e in q["name"] for e in exclude))
    return Part(label, Compound(children=sh), color or first["color"], first["bom"], tuple(explode))


def bench():
    return Part("Workbench (the maker space's own)", Compound(children=[q["shape"] for q in raw() if q["kind"] == "context"]), "#E5E7EB")


G = {
    "frame": (("Base frame",), {}),
    "plates": (("steel plate 6 mm",), {}),
    "extruder": (("Desktop single-screw", "Extruder ", "Hopper lid"), dict(exclude=("fume",))),
    "barrel_sup": (("Barrel support", "glass-mica 6 mm, barrel"), {}),
    "pump": (("Melt gear pump", "Melt pump heater plate", "Cartridge heater 1/4 in x 2 in", "Melt pump drive shaft", "Jaw coupling, 10",
              "Melt pump motor bracket", "Gearbox output", "Planetary gearbox", "Stepper motor NEMA 23, melt pump", "Melt pump stand",
              "glass-mica 6 mm, melt pump"), {}),
    "melt_tube": (("Melt tube,", "Melt adapter", "Melt tube band heater"), {}),
    "die": (("Die body", "Air knife", "Cartridge heater 1/4 in x 3 in", "Thermocouple, type J", "Air inlet fitting", "Die stand", "glass-mica 6 mm, die"), {}),
    "collector": (("Collector drum", "Pillow block", "Bearing riser", "Timing", "Drum motor bracket", "Stepper shaft, 8 mm, drum", "Stepper motor NEMA 23, drum",
                   "Drum carriage", "Linear rail", "Linear bearing", "Traverse", "Lead screw end", "Stepper motor NEMA 17"), {}),
    "encl": (("Enclosure post", "Enclosure rail", "Enclosure top cross"), {}),
    "panels": (("Enclosure panel", "Enclosure roof", "Door", "interlock switch"), {}),
    "corona": (("Corona", "Insulator hanger", "HV lead clip"), {}),
    "air": (("Linear diaphragm air pump", "Air pump rubber", "Inline air heater", "Thermocouple, type K", "air line", "Rotameter"), {}),
    "panel": (("Control panel enclosure", "Emergency stop", "Panel indicator"), {}),
    "hoods": (("Exhaust hood", "Exhaust duct spigot", "Extruder fume hood"), {}),
}
LABEL = {"frame": "Base frame, welded SHS", "plates": "Mounting plates (5)", "extruder": "Desktop extruder with hopper lid",
         "barrel_sup": "Barrel support and pad", "pump": "Melt pump, heater plates and drive", "melt_tube": "Melt tube, heater and adapter",
         "die": "Split die, air knives and stand", "collector": "Collector drum, belt drive and traverse", "encl": "Enclosure frame",
         "panels": "Enclosure panels and interlocked door", "corona": "Corona bar and hangers", "air": "Air pump, heater and lines",
         "panel": "Control panel and emergency stops", "hoods": "Exhaust hoods"}
ORDER = ["frame", "plates", "extruder", "barrel_sup", "pump", "melt_tube", "die", "collector", "encl", "corona", "air", "panel", "panels", "hoods"]
EXPL = {"frame": (0, 0, -250), "plates": (0, 0, -150), "extruder": (0, -350, 0), "barrel_sup": (0, -250, -100), "pump": (0, -350, 150),
        "melt_tube": (0, 0, 250), "die": (0, 0, 350), "collector": (0, -400, 0), "encl": (0, 0, 0), "corona": (0, 0, 550),
        "air": (0, 350, 0), "panel": (0, -300, 0), "panels": (0, 900, 700), "hoods": (0, 0, 1200)}


def g(key, explode=None, label=None):
    keys, kw = G[key]
    return grp(LABEL[key] if label is None else label, keys, explode=explode if explode is not None else (0, 0, 0), **kw)


def overview():
    ps = [g(k, EXPL[k]) for k in ORDER]
    return bv.overview(ps, OUT / "overview.png", title=f"{PROJECT}: PF1 components in build order",
                       subtitle="Every component group pulled apart and numbered in build order; bench not shown; plan, not yet built",
                       size=(12, 8), key=True, elev=24, azim=-58)


def P_(name, color=None):
    q = next(q for q in raw() if q["name"] == name)
    return Part(name, q["shape"], color or q["color"], q["bom"])


SHEETS = {
    101: (["Base frame rail front, SHS 40 x 3", "Base frame rail rear, SHS 40 x 3"] + [f"Base frame cross member {i}, SHS 40 x 3" for i in range(1, 6)],
          "Base frame: making sketch", "SHS 40 x 40 x 3 steel, about 6.4 m; cut, drilled, welded, painted",
          ["Two rails 2,280 long at 400 centres; five cross members 360 long",
           "Cross members at 100, 600, 1,240, 1,800 and 2,340 from the left end",
           "Fillet weld each cross member to the rails, 4 mm, both sides",
           "Drill 11 mm holes in the rail tops for the M8 rivet nuts (plate corners)",
           "Drill 8.8 mm through both walls 60 mm from each end for the coach screws",
           "Fits: stands on the bench, coach-screwed through at four points",
           "Check: frame flat on the bench within 1 mm; diagonals equal"]),
    102: (["P2 melt pump and die plate, steel plate 6 mm"], "Pump and die plate (one of five): making sketch", "6 mm steel plate, laser or band-saw cut, drilled",
          ["195 x 460 mm; corner holes 9 mm, 25 in from the ends, on the rail lines",
           "M5 tapping holes for the die stand and the pump motor bracket",
           "The other four plates follow the same pattern (sizes on DWG-001)",
           "Fits: on the rails, M8 bolts into rivet nuts set in the rail tops",
           "Check: the plate sits flat with all four bolts tight"]),
    103: (["Die body, lower half (capillary grooves)", "Die body, upper half"], "Split die body: making sketch",
          "17-4PH or 303 stainless, two blocks 80 x 90 x 40 mm; precision CNC, lapped",
          ["Nose 20 mm long from the 1,070 line to the tip; faces lapped flat to a few micrometres",
           "6 mm melt inlet and 8 mm manifold slot split between the halves",
           "Lower half: 0.3 mm deep pre-land and 40 grooves 0.27 x 0.27 mm at 1.0 mm pitch, 4 mm long",
           "Four 6.6 mm clamp holes; 6.5 mm cartridge heater bore across each half",
           "Upper half: 4 mm air inlet port; internal drillings to both knives",
           "Check: blue the faces, then check every groove with a 0.25 mm pin gauge"]),
    104: (["Air knife, upper", "Air knife, lower"], "Air knives: making sketch", "12 mm stainless plate of the die alloy; CNC, land lapped",
          ["Inner face parallel to the nose face; 5 mm land set 0.30 mm from it",
           "2 mm plenum behind the land; 48 mm slot length",
           "Flange 10 mm screwed to the die half with two M5 screws",
           "Set the gap with 0.30 mm shims at running temperature",
           "Check: equal back pressure on both knives at the design air flow"]),
    105: (["Melt tube, extruder to melt pump, 303 stainless", "Melt adapter, melt pump to die, 303 stainless"], "Melt tube and adapter: making sketch",
          "303 stainless bar, 25 and 30 mm; turned and drilled",
          ["Melt tube 25 mm OD, 6 mm bore, 100 mm flange with four 6.6 mm holes on 80 mm",
           "Adapter 30 mm OD, 6 mm bore, 20 mm long between pump and die",
           "Faces square and smooth for a metal-to-metal seal",
           "Fits: tube to the extruder flange (four M6), adapter between pump and die faces",
           "Check: no leak at 1 MPa on first heat (pressure gauge)"]),
    106: (["Collector drum shell, aluminium tube 200 x 3", "Collector drum end disc -Y, aluminium 10 mm", "Collector drum end disc +Y, aluminium 10 mm",
           "Collector drum shaft, 20 mm steel"], "Collector drum: making sketch", "Aluminium tube 200 x 3, 10 mm plate discs, 20 mm steel shaft",
          ["Shell 220 long, ends deburred and rounded (no sharp edge facing the corona)",
           "Discs pressed or bonded in, four 30 mm lightening holes, 20 mm bore",
           "Shaft 375 long: 155 to the left of the drum centre, 220 to the right",
           "Balance the drum; run-out under 0.2 mm",
           "Check: the shaft is grounded through the bearings and belt side"]),
    107: (["Drum carriage plate, aluminium 10 mm", "Bearing riser -Y, aluminium block", "Drum motor bracket, aluminium 6 mm"], "Drum carriage and brackets: making sketch",
          "10 mm aluminium plate and blocks, 6 mm folded bracket",
          ["Carriage plate 330 x 405 mm on four linear bearing blocks",
           "Two risers bring the pillow blocks to the die line (1,100 above the floor)",
           "Motor bracket holds the NEMA 23 beside the drum for the belt",
           "Fits: risers and bracket bolted through the carriage with M8",
           "Check: drum axis level and square to the die within 0.5 mm"]),
    108: (["Corona bar body, acetal 30 x 30"], "Corona bar: making sketch", "Acetal bar 30 x 30 x 300 mm, 14 stainless needles",
          ["14 holes 1.1 mm, 20 mm pitch, 12 deep, along the underside centre line",
           "Needles pressed in, tips 40 mm above the drum top",
           "Two 20 mm holes on top for the acetal hangers, 200 mm apart",
           "Brass HV clip at the +Y end",
           "Check: needle tips in a line within 0.5 mm"]),
    109: (["Enclosure post 1, aluminium SHS 30 x 2", "Enclosure rail top -Y, aluminium SHS 30 x 2", "Enclosure panel -X end, polycarbonate 6 mm"],
          "Enclosure frame and panels: making sketch", "Aluminium SHS 30 x 2; 6 mm polycarbonate (flame-retardant grade asked)",
          ["Frame 680 x 580 x 560 mm; screwed corner brackets",
           "End panels notched round the base rails; 30 mm hole for the melt tube, 18 mm for the air line",
           "Door on the operator side on two hinges, guard-locked switch inside",
           "Roof with a 200 mm opening under the hood",
           "Check: door closes and locks; gaps under 3 mm all round"]),
    110: (["Exhaust hood, galvanised steel 1 mm folded", "Extruder fume hood, galvanised steel 1 mm, branch to the exhaust"],
          "Exhaust hoods: making sketch", "1 mm galvanised sheet, folded and riveted",
          ["Roof hood 260 x 260 x 80 with a 100 mm spigot",
           "Branch hood 245 x 120 x 60 over the extruder outlet, 60 mm spigot",
           "Both ducted to one inline fan to outdoors (own circuit)",
           "Check: smoke drawn in at every opening with the fan on"]),
}


def sheets(which=None):
    for no, (names, title, mat, notes) in SHEETS.items():
        if which and str(no) not in which:
            continue
        sh = [q["shape"] for q in raw() if q["name"] in names]
        first = next(q for q in raw() if q["name"] in names)
        part = Part(title.split(":")[0], Compound(children=sh), first["color"], first["bom"])
        nb = [g(k) for k in ("frame", "plates", "die", "collector")]
        print(bv.component_sheet(part, nb, PROJECT, f"OPF-DWG-{no}", title, mat, notes, DATE))


def _window(items, lo, hi):
    win = Pos(*[(a + b) / 2 for a, b in zip(lo, hi)]) * Box(*[b - a for a, b in zip(lo, hi)])
    out = []
    for p in items:
        try:
            s = p.shape & win
            if s.volume > 1e-3:
                out.append(Part(p.name, s, p.color, p.bom))
        except Exception:
            pass
    return out


def named(keys, label, fasteners=True):
    sh = [q["shape"] for q in raw() if any(k in q["name"] for k in keys) and (fasteners or q["kind"] != "fastener")]
    first = next(q for q in raw() if any(k in q["name"] for k in keys))
    return Part(label, Compound(children=sh), first["color"], first["bom"])


def joints(which=None):
    J = {
        1: ("Joint 1: split die, groove face, air knives and clamp screws (cut open)",
            [named(["Die body, lower"], "Die lower half (grooves)"), named(["Die body, upper"], "Die upper half"),
             named(["Air knife, upper"], "Air knife, upper"), named(["Air knife, lower"], "Air knife, lower"),
             named(["die clamp"], "M6 clamp screws"), named(["Cartridge heater 1/4 in x 3"], "Cartridge heaters")],
            (1005, 0, 1045), (1100, 50, 1160), "+Y"),
        2: ("Joint 2: mounting plate on the base rail, M8 bolt into a rivet nut (cut open)",
            [named(["Base frame rail front"], "Base rail, SHS 40 x 3"), named(["P2 melt pump and die plate"], "Mounting plate, 6 mm"),
             named(["P2 1"], "M8 bolt, washer and rivet nut")], (905, -225, 895), (960, -175, 970), "+Y"),
        3: ("Joint 3: drum shaft in its pillow block, timing belt to the drum motor",
            [named(["Collector drum shell"], "Drum"), named(["Collector drum shaft"], "Drum shaft"), named(["Pillow block bearing, 20 mm +Y"], "Pillow block"),
             named(["Timing pulley"], "Timing pulleys"), named(["Timing belt"], "Timing belt"), named(["Stepper motor NEMA 23, drum"], "Drum motor"),
             named(["Drum motor bracket"], "Motor bracket")], (1190, 100, 960), (1450, 215, 1140), None),
        4: ("Joint 4: corona bar on its acetal hangers over the drum",
            [named(["Corona bar body"], "Corona bar, acetal"), named(["Corona needle"], "Needles, 40 mm above the drum"),
             named(["Insulator hanger"], "Acetal hangers"), named(["Enclosure top cross rail, corona"], "Top cross rail"),
             named(["Collector drum shell"], "Drum (grounded)")], (1300, -160, 1150), (1480, 170, 1460), None),
    }
    for k, (title, ps, lo, hi, cut) in J.items():
        if which and str(k) not in which:
            continue
        print(bv.joint(_window(ps, lo, hi), OUT / f"joint-{k:02d}.png", title,
                       subtitle="Close-up from the model; parts named", cut=cut, elev=22, azim=-55))


def steps(which=None):
    S = [
        ("Step 1: set the base frame on the bench and coach-screw it down", [], [bench()], ["frame"]),
        ("Step 2: bolt the five mounting plates onto the rails (M8 into rivet nuts)", ["frame"], [bench()], ["plates"]),
        ("Step 3: fit the extruder, its barrel support and the hopper lid", ["frame", "plates"], [], ["extruder", "barrel_sup"]),
        ("Step 4: fit the melt pump stand, pump, heater plates and drive", ["frame", "plates", "extruder", "barrel_sup"], [], ["pump"]),
        ("Step 5: fit the melt tube and adapter, then the die stand and the split die with its knives", ["frame", "plates", "extruder", "barrel_sup", "pump"], [], ["melt_tube", "die"]),
        ("Step 6: fit the traverse rails, carriage, drum and belt drive", ["frame", "plates", "extruder", "pump", "melt_tube", "die"], [], ["collector"]),
        ("Step 7: build the enclosure frame round the forming zone", ["frame", "plates", "extruder", "pump", "melt_tube", "die", "collector"], [], ["encl"]),
        ("Step 8: hang the corona bar on its acetal hangers, 40 mm above the drum", ["frame", "plates", "pump", "die", "collector", "encl"], [], ["corona"]),
        ("Step 9: fit the air pump, heater and air lines", ["frame", "plates", "die", "collector", "encl", "corona"], [], ["air"]),
        ("Step 10: fit the control panel and the two emergency stops; wire it", ["frame", "plates", "extruder", "die", "collector", "encl", "air"], [], ["panel"]),
        ("Step 11: fit the panels, the interlocked door and the exhaust hoods", ["frame", "plates", "extruder", "pump", "die", "collector", "encl", "corona", "air", "panel"], [], ["panels", "hoods"]),
    ]
    for k, (title, done, ctx, new) in enumerate(S, 1):
        if which and str(k) not in which:
            continue
        print(bv.step([g(d) for d in done], [g(n, (0, -150, 200) if n not in ("frame", "plates") else (0, 0, 200)) for n in new],
                      OUT / f"step-{k:02d}.png", title, context=ctx, size=(9, 6.5), elev=24, azim=-58, label_done=False))


if __name__ == "__main__":
    cmd, args = (sys.argv[1] if len(sys.argv) > 1 else "all"), sys.argv[2:]
    if cmd in ("overview", "all"):
        print(overview())
    if cmd in ("sheets", "all"):
        sheets(args)
    if cmd in ("joints", "all"):
        joints(args)
    if cmd in ("steps", "all"):
        steps(args)
