"""Open PolyForge: drawing set and STL export for option PF1 (carried in the drawing set; choice awaiting Amish).

Run from the repo root:  python cad/src/sheets.py [ga|section|stl]   (no argument: all three)
    cad/drawings/OPF-DWG-001   general arrangement of the PF1 machine on its bench (enclosure panels left off)
    cad/drawings/OPF-DWG-002   half section of the forming zone: melt pump, die, air knives, drum, corona bar
    cad/stl/*.stl              the forming-zone assembly and each made part, for viewing
Making sketches for each made part (OPF-DWG-101 onward) are drawn by cad/src/build_plan_media.py.
Sheets are generated from cad/src/model.py and never edited by hand; figures come from OPF-CAL-001.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
from build123d import Box, Compound, Pos, export_stl  # noqa: E402
from drawing import Sheet, project_views  # noqa: E402
import model as M  # noqa: E402

P = M.PARAMS
DATE = "2026-11-12"
DWG = ROOT / "cad/drawings"
R = json.loads((ROOT / "docs/04-calcs/sizing_results.json").read_text())
PROJECT = "Open PolyForge"
MAT = "Steel SHS frame and plates; stainless die, knives and melt parts; aluminium drum; acetal; polycarbonate. See bom/bom.csv"


def body_parts(panels=False, small=False):
    out = []
    for q in M.components("PF1"):
        if q["kind"] == "context" or q["kind"] == "weld":
            continue
        if not panels and q["material_name"] == "polycarbonate":
            continue
        if not small and q["kind"] == "fastener":
            continue
        out.append(q)
    return out


def ga():
    parts = body_parts()
    work = DWG / "_views_ga"
    views = project_views(Compound(children=[q["shape"] for q in parts]), work)
    s = Sheet(project=PROJECT, title="PF1 machine: general arrangement",
              dwg_no="OPF-DWG-001", rev="P1", author="Amish Chadha", date=DATE, concept=True, scale=None, material=MAT,
              revisions=[("P1", "Preliminary GA from the TRL 3 model (OPF-CAL-001)", DATE, "AC")])
    s.add_ortho(views, ["front", "top", "right"])
    s.add_svg(views["iso"], 276, 32, 140, 70, label="Isometric view", sublabel="Not to scale; enclosure panels and fasteners not shown")
    e = R["envelope_mm"]
    s.add_notes("Key dimensions (mm) and data", [
        f"Overall {e['length']:.0f} long, {e['depth']:.0f} deep, {e['height']:.0f} above the bench",
        "Base frame SHS 40 x 3, rails at +-200; plates 6 mm on M8 rivet nuts",
        f"Die: 40 grooves {P['HOLE_D']:.2f} mm square at {P['HOLE_PITCH']:.0f} mm pitch; nose at x {M.XT:.0f}",
        f"Air knives: 0.30 mm land 5 long, 2 mm plenum, slots {P['AIR_SLOT_L']:.0f} long",
        f"Drum {P['DRUM_D']:.0f} dia x {P['DRUM_L']:.0f}, {P['DCD']:.0f} from the die tip, traverse +-{P['TRAVERSE']:.0f}",
        f"Corona needles {P['CORONA_GAP']:.0f} above the drum, -{P['CORONA_KV']:.0f} kV",
        f"Enclosure x {P['ENCL_X'][0]:.0f} to {P['ENCL_X'][1]:.0f}, exhaust 0.10 m3/s",
        f"Steady {R['total_W'][0]:,.0f} W ({R['current_A'][0]:.1f} A), cap 12 A",
        f"Polymer {R['polymer']['g_min']:.1f} g/min; web 140 wide at 25 g/m2",
        f"Mass about {R['mass_kg']['PF1']:.0f} kg; parts USD {R['bom_total']:,.2f}",
        "PRELIMINARY, NOT FOR FABRICATION",
    ], x=276, y=118, width=140)
    s.save(DWG / "OPF-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote cad/drawings/OPF-DWG-001.svg, .pdf, .png")


def forming_zone(cut=True):
    keep = []
    cutter = Pos(1250, 400, 1200) * Box(900, 800, 1000)
    for q in body_parts(small=True):
        bb = q["shape"].bounding_box()
        if bb.min.X < 880 or bb.max.X > 1560 or "Enclosure" in q["name"] or "Base frame" in q["name"] or "Exhaust" in q["name"]:
            continue
        if bb.min.Z < M.ZP - 1:
            continue
        if cut:
            try:
                h = q["shape"] & cutter
                if h.volume > 1e-3:
                    keep.append(h)
            except Exception:
                pass
        else:
            keep.append(q["shape"])
    return keep


def section():
    parts = forming_zone()
    work = DWG / "_views_sec"
    views = project_views(Compound(children=parts), work, center_lines=False)
    s = Sheet(project=PROJECT, title="PF1 forming zone: half section, pump to drum",
              dwg_no="OPF-DWG-002", rev="P1", author="Amish Chadha", date=DATE, concept=True, scale=None, material=MAT,
              revisions=[("P1", "Preliminary half section from the TRL 3 model", DATE, "AC")])
    s.add_ortho(views, ["front", "top", "right"], dims=True)
    s.add_svg(views["iso"], 276, 32, 140, 70, label="Isometric view", sublabel="Near half removed; not to scale")
    a = R["air"]
    s.add_notes("Melt, air and charge path", [
        f"Melt pump 0.16 cm3/rev at {R['die']['pump_rpm']:.0f} rpm, 250 C",
        "Melt adapter 6 bore into the split die; manifold slot, 0.3 pre-land",
        f"40 grooves {P['HOLE_D']:.2f} sq, 4 long; {R['die']['dp_hole_MPa'][0]:.2f} to {R['die']['dp_hole_MPa'][1]:.2f} MPa",
        f"Air {a['Q_std_Lmin'] * 1.204 / 1.293:.0f} NL/min at 270 C through two 0.30 x 48 slots",
        f"Air side {R['air_pressure']['total_kPa'][0]:.0f} to {R['air_pressure']['total_kPa'][1]:.0f} kPa at the pump (estimate)",
        f"Die tip to drum {P['DCD']:.0f}; drum 200 dia, 30 rpm",
        "Corona needles 40 above the drum, -25 kV, 1 mA limit",
        "Cartridge heaters: die 2 x 150 W, pump 2 x 100 W",
        "Insulator pads under the die and pump stands",
        "PRELIMINARY, NOT FOR FABRICATION",
    ], x=276, y=118, width=140)
    s.save(DWG / "OPF-DWG-002")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote cad/drawings/OPF-DWG-002.svg, .pdf, .png")


def stl():
    out = ROOT / "cad/stl"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.stl"):
        old.unlink()
    export_stl(Compound(children=forming_zone(cut=False)), str(out / "opf-pf1-forming-zone.stl"), tolerance=0.2, angular_tolerance=0.3)
    seen = set()
    for q in body_parts():
        if q["kind"] != "made":
            continue
        base = q["name"].split(",")[0].lower().replace(" ", "-")
        base = "".join(ch for ch in base if ch.isalnum() or ch == "-").strip("-")
        if base in seen or "rail" in base or "post" in base:
            continue
        seen.add(base)
        export_stl(q["shape"], str(out / f"opf-{base}.stl"), tolerance=0.1, angular_tolerance=0.2)
    print("wrote", len(list(out.glob("*.stl"))), "STL files to cad/stl/")


if __name__ == "__main__":
    fns = {"ga": ga, "section": section, "stl": stl}
    for w in sys.argv[1:] or list(fns):
        fns[w]()
