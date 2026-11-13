"""Open PolyForge. Parametric model (kit 1.9 interface, STANDARDS section 24), detail level D3.

Run from the repo root:  python .kit/cad_check.py --export
Every main dimension is in PARAMS; docs/04-calcs/sizing.py (OPF-CAL-001) and stem_check.py (OPF-STM-001) read it.

Units mm. X along the bench (0 to 2440), Y across it (-305 to 305, operator on the -Y side), Z up; floor at z = 0,
bench top at z = 900. The workbench is a context part (kind "context"): it is the maker space's own, not in the BOM.

Options (OPF-OPT-001; the recommendation is proposed, awaiting Amish):
  PF1  Screw extruder, melt pump and slot die (the Helpful Engineering proposal's main path): a desktop single-screw
       extruder feeds a 0.16 cm3/rev melt gear pump, which meters melt into a split die with 40 grooved capillaries
       (0.3 mm, 1 mm pitch). Two air knives form 0.3 mm slots 48 mm long; hot air from a diaphragm pump and a 1 kW
       inline heater attenuates the fibres onto a traversing collector drum 200 mm from the die. A corona bar over
       the drum charges the web. Die width set by the 120 V power budget (OPF-DEC-001 F1).
  PF2  Ram extruder feeding the same die: a heated vertical barrel and a ball-screw ram push one charge of melt
       through the same die, air system, drum and corona bar. Batch, no screw and no melt pump.
  PF3  Centrifugal melt spinning: a heated spinneret cup with 12 radial 0.6 mm holes spins at about 3,500 rpm inside
       a grounded collector cage; fibres form by centrifugal drawing without process air. The cut web is charged on a
       separate corona table.
"""
from __future__ import annotations

import sys
from pathlib import Path

from build123d import Box, Cylinder, Location, Plane, Polygon, Pos, Rot, extrude

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402

TITLE = "Open PolyForge"
OPTIONS = {"PF1": "Screw extruder, melt pump and slot die", "PF2": "Ram extruder feeding the same slot die",
           "PF3": "Centrifugal melt spinning (no process air)"}
PRINCIPLES = {
    "PF1": "A screw extruder and a gear melt pump meter molten polypropylene through 40 capillaries while two hot "
           "air jets draw it into fibres of a few micrometres; continuous, and the air heater sets the die width.",
    "PF2": "A heated barrel and a ball-screw ram push one charge of melt through the same die and air jets; simpler "
           "and positive displacement, but batch, with a long melt and reload cycle.",
    "PF3": "A heated cup spinning at about 3,500 rpm flings melt through radial holes; centrifugal force draws the "
           "fibres onto a cage without process air, so power is low but the web is batch and less uniform.",
}
CHOSEN = "PF1"   # carried to the drawing, BOM and build plan. Proposed, awaiting Amish (OPF-DEC-001 D1); not decided
OPTION_VIEWS = {
    "PF1": dict(el=20, az=-55, scale="person", keep_context=True, ground_z=0.0),
    "PF2": dict(el=20, az=-55, scale="person", keep_context=True, ground_z=0.0),
    "PF3": dict(el=20, az=-55, scale="person", keep_context=True, ground_z=0.0),
}
# door hinge leaves are screwed to the door and frame faces they touch; stepper and gearbox shafts sit in their bores
ALLOWED_CONTACTS = [("Door hinge", "Door"), ("Door hinge", "post")]

PARAMS = {
    # bench and frame
    "BENCH": (2440.0, 610.0, 900.0),        # 8 ft x 2 ft workbench, top at 900 mm (context)
    "RAIL": (40.0, 3.0), "RAIL_Y": 200.0, "RAIL_X": (80.0, 2360.0), "CROSS_X": (100.0, 600.0, 1240.0, 1800.0, 2340.0),
    "PLATE_T": 6.0,
    # die (PF1 and PF2)
    "AXIS_Z": 1100.0,                       # die centre line and drum axis height
    "DIE_X": (1010.0, 1070.0, 1090.0),      # rear face, start of the nose, nose tip
    "DIE_W": 90.0, "DIE_H": 40.0,           # die half width (Y) and height of each half (Z)
    "HOLES": 40, "HOLE_D": 0.27, "HOLE_PITCH": 1.0, "HOLE_L": 4.0,    # grooved capillaries, square 0.27 mm (flows as a 0.30 mm round hole)
    "AIR_GAP": 0.30, "AIR_SLOT_L": 48.0, "AIR_LAND": 5.0, "AIR_PLENUM": 2.0,    # each of two air slots: gap (mm) and length along the die (mm)
    "AIR_PLATE_T": 12.0,
    # process set points (design point after fix F1; OPF-CAL-001)
    "GHM": 0.10,                            # polymer throughput, g per hole per min
    "T_MELT": 250.0, "T_AIR": 270.0, "T_ROOM": 20.0,
    "V_AIR": 140.0,                         # air speed at the slot exit, m/s
    "DCD": 200.0,                           # die to collector distance, mm
    "BASIS_WEIGHT": 25.0,                   # target web basis weight, g/m2
    # melt pump (bought, 0.16 cm3/rev class)
    "PUMP_CC": 0.16, "PUMP": (920.0, 990.0, 50.0, 80.0),   # x0, x1, depth (Y), height (Z)
    # collector drum
    "DRUM_D": 200.0, "DRUM_L": 220.0, "DRUM_T": 3.0, "TRAVERSE": 40.0, "DRUM_RPM": 30.0,
    # corona bar
    "CORONA_GAP": 40.0, "CORONA_KV": 25.0, "CORONA_UA": 200.0, "NEEDLES": 14,
    # enclosure (forming zone)
    "ENCL_X": (900.0, 1580.0), "ENCL_Y": 290.0, "ENCL_TOP": 1460.0, "PANEL_T": 6.0, "POST": 30.0,
    # air system
    "HEATER": (32.0, 254.0, 1000.0),        # inline heater OD, length (mm) and rating (W), Omega AHPF-101 class
    "AIR_TUBE": 12.7,
    # extruder module (bought, Filabot EX2 class: 457 x 178 x 229 mm, 5/8 in screw)
    "EXTRUDER": (180.0, 637.0, 178.0, 229.0), "BARREL_OD": 40.0,
    # control panel
    "PANEL_BOX": (2050.0, 2250.0, 300.0, 400.0),
    # PF2 ram extruder
    "RAM_BORE": 30.0, "RAM_STROKE": 200.0, "RAM_BARREL": (70.0, 300.0),
    # PF3 centrifugal
    "CUP": (150.0, 45.0), "CUP_HOLES": 12, "CUP_HOLE_D": 0.6, "CAGE_D": 500.0, "CAGE_H": 200.0, "SPIN_RPM": 3500.0,
}
P = PARAMS
ZB = P["BENCH"][2]                    # bench top
ZR = ZB + P["RAIL"][0]                # top of the base frame rails
ZP = ZR + P["PLATE_T"]                # top of the mounting plates
ZA = P["AXIS_Z"]
X0, XN, XT = P["DIE_X"]

C_STEEL, C_FRAME, C_STAIN, C_AL, C_BLK = "#5B6066", "#2F5D50", "#C9CDD1", "#C4C8CC", "#141414"
C_PC, C_INS, C_ACET, C_HEAT = "#DDE6EA", "#F2F2EE", "#EDEAE0", "#B45309"


# ---------------------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------------------
def _p(name, shape, mat, kind="made", bom=None, explode=(0, 0, 0), color=None, group="shell", note=""):
    return part(name, shape, mat, kind=kind, bom=bom, group=group, explode=explode, color=color, note=note)


def B(x0, x1, y0, y1, z0, z1):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def CX(r, x0, x1, y, z):
    x0, x1 = sorted((x0, x1))
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def CY(r, y0, y1, x, z):
    y0, y1 = sorted((y0, y1))
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def CZ(r, z0, z1, x, y):
    z0, z1 = sorted((z0, z1))
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def loc(origin, x_dir, z_dir):
    return Location(Plane(origin=origin, x_dir=x_dir, z_dir=z_dir))


def bolt(d, grip, location, tag, bom=None, explode=(0, 0, 0)):
    """ISO 4017 bolt, two ISO 7089 washers, ISO 4032 nut through a joint; local +Z is the head side."""
    return [_p(f"{n}, {tag}", location * s, "zinc_plated", "fastener", bom, explode) for n, s in cp.hex_bolt_set(d, grip)]


def screw(d, length, location, tag, bom=None, explode=(0, 0, 0)):
    """Hex bolt and washer into a tapped hole (the hole is modelled at clearance); local +Z is the head side."""
    h = cp.ISO[d][4]
    return [_p(f"M{d}x{length:.0f} hex bolt (ISO 4017), {tag}", location * Pos(0, 0, h) * cp.hex_bolt(d, length), "zinc_plated", "fastener", bom, explode),
            _p(f"M{d} washer (ISO 7089), {tag}", location * cp.washer(d), "zinc_plated", "fastener", bom, explode)]


def rivnut_bolt(x, y, tag, bom=None):
    """M8 bolt and washer through a mounting plate into an M8 rivet nut set in a rail's top wall."""
    out = screw(8, 16, Location((x, y, ZP)), tag, bom)
    rn = CZ(5.5, ZR - 10.0, ZR, x, y) - CZ(4.1, ZR - 11.0, ZR + 1.0, x, y)
    out.append(_p(f"M8 rivet nut, {tag}", rn, "zinc_plated", "fastener", bom))
    return out


def ycen(shape):
    b = shape.bounding_box()
    return Pos(0, -(b.min.Y + b.max.Y) / 2, 0) * shape


def CH(shape, r=0.3):
    return cp.break_edges(shape, r)


def bead_z(x, y, z0, z1, sx, sy, leg=4.0):
    tri = Polygon((x, y), (x + sx * leg, y), (x, y + sy * leg), align=None)
    return Pos(0, 0, z0) * extrude(tri, z1 - z0)


# ---------------------------------------------------------------------------------------------------------
# bench (context), base frame and mounting plates (all options)
# ---------------------------------------------------------------------------------------------------------
def bench():
    L, D, H = P["BENCH"]
    out = [part("Workbench top, 2 ft x 8 ft (context, the maker space's own)", cp.break_edges(B(0, L, -D / 2, D / 2, H - 40, H), 3.0),
                "plywood", kind="context", group="context")]
    for i, (x, y) in enumerate(((60, -250), (60, 250), (L - 60, -250), (L - 60, 250))):
        out.append(part(f"Workbench leg {i + 1} (context)", cp.at(cp.shs(60, 3, H - 40), (x, y, 0)), "painted_steel", kind="context", group="context"))
    return out


PLATES = {   # name: x0, x1, y0, y1 ; holes over the rails at y = +-200
    "P1 extruder plate": (150.0, 880.0, -230.0, 230.0),
    "P2 melt pump and die plate": (905.0, 1100.0, -230.0, 230.0),
    "P4 collector plate": (1270.0, 1545.0, -230.0, 230.0),
    "P5 air pump plate": (1640.0, 1960.0, -230.0, 230.0),
    "P6 control panel plate": (2010.0, 2290.0, -230.0, 230.0),
}


def plate_holes(name):
    x0, x1, _, _ = PLATES[name]
    return [(x0 + 25.0, s * P["RAIL_Y"]) for s in (-1, 1)] + [(x1 - 25.0, s * P["RAIL_Y"]) for s in (-1, 1)]


def base_frame(bom_rail=1, bom_cross=1, bom_fast=34):
    a, t = P["RAIL"]
    xa, xb = P["RAIL_X"]
    out = []
    holes = [h for n in PLATES for h in plate_holes(n)]
    for s in (-1, 1):
        y = s * P["RAIL_Y"]
        r = Pos(xa, y, ZB + a / 2) * Rot(0, 90, 0) * cp.shs(a, t, xb - xa)
        for hx, hy in holes:
            if hy == y:
                r = r - CZ(5.5, ZR - t - 1, ZR + 1, hx, hy)
        for hx in (xa + 60, xb - 60):
            r = r - CZ(4.4, ZB - 1, ZR + 1, hx, y)
        out.append(_p(f"Base frame rail {'front' if s < 0 else 'rear'}, SHS 40 x 3", r, "painted_steel", "made", bom_rail, (0, s * 60, -60), C_FRAME))
    yi = P["RAIL_Y"] - a / 2
    for i, x in enumerate(P["CROSS_X"]):
        c = Pos(x, -yi, ZB + a / 2) * Rot(-90, 0, 0) * cp.shs(a, t, 2 * yi)
        out.append(_p(f"Base frame cross member {i + 1}, SHS 40 x 3", c, "painted_steel", "made", bom_cross, (0, 0, -60), C_FRAME))
        for sy in (-1, 1):
            for sx in (-1, 1):
                out.append(_p(f"Fillet weld, cross member {i + 1} {sx:+d}{sy:+d}",
                              bead_z(x + sx * a / 2, sy * yi, ZB + 2, ZR - 2, sx, -sy), "mild_steel", "weld", None, (0, 0, -60)))
    for i, (x, y) in enumerate(((xa + 60, -P["RAIL_Y"]), (xb - 60, -P["RAIL_Y"]), (xa + 60, P["RAIL_Y"]), (xb - 60, P["RAIL_Y"]))):
        cs = Location((x, y, ZR)) * cp.coach_screw(8, 80)
        out.append(_p(f"M8x80 coach screw (DIN 571) to bench, {i + 1}", cs, "zinc_plated", "fastener", bom_fast))
    return out


def plate(name, bom, extra_holes=(), cut=None):
    x0, x1, y0, y1 = PLATES[name]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    holes = [(hx - cx, hy - cy, 9.0) for hx, hy in plate_holes(name)] + [(hx - cx, hy - cy, d) for hx, hy, d in extra_holes]
    s = Pos(cx, cy, ZR) * cp.sheet(x1 - x0, y1 - y0, P["PLATE_T"], holes=holes, r_corner=4.0, edge=0.8)
    if cut is not None:
        s = s - cut
    out = [_p(f"{name}, steel plate 6 mm", s, "painted_steel", "made", bom, (0, 0, -30), C_FRAME)]
    for i, (hx, hy) in enumerate(plate_holes(name)):
        out += rivnut_bolt(hx, hy, f"{name.split()[0]} {i + 1}", 34)
    return out


# ---------------------------------------------------------------------------------------------------------
# slot die with air knives (PF1, PF2)
# ---------------------------------------------------------------------------------------------------------
HY = P["DIE_W"] / 2
DIE_BOLTS = [(1020.0, -35.0), (1020.0, 35.0), (1058.0, -35.0), (1058.0, 35.0)]
HEATER_X = 1038.0


def _die_half(upper):
    s = 1 if upper else -1
    h = P["DIE_H"]
    prof = Polygon((X0, ZA), (XT, ZA), (XN, ZA + s * h), (X0, ZA + s * h), align=None)
    body = ycen(Rot(90, 0, 0) * extrude(prof, 2 * HY))                 # XZ profile extruded along Y
    body = body - CX(3.0, X0 - 1, X0 + 32, 0, ZA)                       # melt inlet bore, 6 mm, split
    body = body - B(X0 + 28, X0 + 36, -22, 22, ZA - 3, ZA + 3)           # manifold slot, split
    if not upper:
        body = body - B(X0 + 36, XT - P["HOLE_L"], -22, 22, ZA - 0.3, ZA)   # pre-land, 0.3 mm deep
        n, pt, hd = P["HOLES"], P["HOLE_PITCH"], P["HOLE_D"]
        for i in range(n):
            y = (i - (n - 1) / 2) * pt
            body = body - B(XT - P["HOLE_L"] - 0.5, XT + 0.5, y - hd / 2, y + hd / 2, ZA - hd, ZA)
    for bx, by in DIE_BOLTS:
        body = body - CZ(3.3, ZA - h - 1, ZA + h + 1, bx, by)
    body = body - CY(3.25, -HY - 1, HY + 1, HEATER_X, ZA + s * 22)        # cartridge heater bore, 1/4 in
    for sx in (-1, 1):
        body = body - CZ(2.75, ZA + s * h - s * 12, ZA + s * h + s * 1, 1050.0 + sx * 0, sx * 18)   # air plate screws
    if upper:
        body = body - CZ(2.0, ZA + 2, ZA + h + 1, 1030.0, 0)              # air inlet port (internal drillings not shown)
    return body


def _air_plate(upper):
    """Air knife: a 12 mm plate parallel to the nose face at a 0.3 mm gap, with a flange screwed to the die half."""
    s = 1 if upper else -1
    h, g, T, L = P["DIE_H"], P["AIR_GAP"], P["AIR_PLATE_T"], P["AIR_SLOT_L"]
    dx, dz = XN - XT, s * h                       # nose face from tip (XT, ZA) to (XN, ZA + s h)
    ln = (dx ** 2 + dz ** 2) ** 0.5
    ux, uz = dx / ln, dz / ln
    nx, nz = (-uz, ux) if upper else (uz, -ux)    # normal pointing away from the die
    if nx < 0:
        nx, nz = -nx, -nz
    a0 = 1.5                                       # set-back of the knife edge from the tip, along the face
    G, Ll = P["AIR_PLENUM"], P["AIR_LAND"]         # plenum gap behind the land, land length (OPF-DEC-001 F5)
    f_top = ZA + s * h
    p0 = (XT + ux * a0 + nx * g, ZA + uz * a0 + nz * g)
    pl = (XT + ux * (a0 + Ll) + nx * g, ZA + uz * (a0 + Ll) + nz * g)
    pl2 = (XT + ux * (a0 + Ll + 1.0) + nx * G, ZA + uz * (a0 + Ll + 1.0) + nz * G)
    t = (f_top - pl2[1]) / uz                      # where the plenum face meets the die top plane
    pt_ = (pl2[0] + ux * t, f_top)
    q1 = (XN + nx * (g + T), ZA + s * h + nz * (g + T))
    q0 = (p0[0] + nx * T * 0.35, p0[1] + nz * T * 0.35)
    prof = Polygon(p0, pl, pl2, pt_, (1040.0, f_top), (1040.0, f_top + s * 10), (q1[0], f_top + s * 10), q1, q0, align=None)
    plate_ = ycen(Rot(90, 0, 0) * extrude(prof, L))
    for sx in (-1, 1):
        plate_ = plate_ - CZ(2.75, f_top - 1 if upper else f_top - 11, f_top + 11 if upper else f_top + 1, 1050.0, sx * 18)
    return cp.break_edges(plate_, 0.3)


def die(bom_half=6, bom_air=7, bom_heater=8, bom_tc=9, bom_fast=34):
    out = [_p("Die body, lower half (capillary grooves)", _die_half(False), "stainless", "made", bom_half, (0, 0, -60), C_STAIN),
           _p("Die body, upper half", _die_half(True), "stainless", "made", bom_half, (0, 0, 60), C_STAIN),
           _p("Air knife, upper", _air_plate(True), "stainless", "made", bom_air, (40, 0, 110), C_STAIN),
           _p("Air knife, lower", _air_plate(False), "stainless", "made", bom_air, (40, 0, -110), C_STAIN)]
    for s, nm in ((1, "upper"), (-1, "lower")):
        out.append(_p(f"Cartridge heater 1/4 in x 3 in, die {nm}", CH(CY(3.175, -38, 38, HEATER_X, ZA + s * 22)), "stainless", "bought", bom_heater,
                      (0, -120, s * 60), C_HEAT))
    tc = CZ(0.8, ZA - P["DIE_H"] + 6, ZA - P["DIE_H"] - 40, 1065.0, -30) if False else CY(0.8, -HY - 40, -10, 1062.0, ZA - 15)
    out.append(_p("Thermocouple, type J, die", CH(tc, 0.2), "stainless", "bought", bom_tc, (0, -80, 0)))
    h = P["DIE_H"]
    for i, (bx, by) in enumerate(DIE_BOLTS):
        out += screw(6, 70, Location((bx, by, ZA + h)), f"die clamp {i + 1}", bom_fast, (0, 0, 80))
    for s, nm in ((1, "upper"), (-1, "lower")):
        for sx in (-1, 1):
            L = loc((1050.0, sx * 18, ZA + s * (h + 10)), (1, 0, 0), (0, 0, s))
            out += screw(5, 16, L, f"air knife {nm} {sx:+d}", bom_fast, (40, 0, s * 110))
    # the die thermocouple runs through a drilled hole in the lower half
    out[0]["shape"] = out[0]["shape"] - CY(0.85, -HY - 1, -9.5, 1062.0, ZA - 15)
    # air inlet fitting on the upper half
    fit = CZ(8.0, ZA + h, ZA + h + 15, 1030.0, 0) - CZ(4.5, ZA + h - 1, ZA + h + 16, 1030.0, 0)
    out.append(_p("Air inlet fitting, 1/2 in tube to 1/4 NPT, stainless", cp.break_edges(fit, 0.5), "stainless", "bought", 13, (0, 0, 120), C_STAIN))
    return out


def die_stand(bom=10, bom_ins=11, bom_fast=34):
    """Steel stand under the die rear and the melt pump, each with a glass-mica insulator pad."""
    out = []
    zt = ZA - P["DIE_H"] - 6.0
    s1 = cp.break_edges(B(1012, 1028, -40, 40, ZP, zt), 1.0) - CZ(2.75, zt - 15, zt + 1, 1020.0, 0)
    out.append(_p("Die stand, steel block", s1, "painted_steel", "made", bom, (0, 0, -80), C_FRAME))
    out.append(_p("Insulator pad, glass-mica 6 mm, die", cp.break_edges(B(1012, 1028, -40, 40, zt, zt + 6), 0.5), "insulated_white", "bought", bom_ins, (0, 0, -40), C_INS))
    x0, x1, dd, hh = P["PUMP"]
    s2 = cp.break_edges(B(x0 + 10, x1 - 10, -20, 20, ZP, ZA - hh / 2 - 6), 1.0)
    out.append(_p("Melt pump stand, steel block", s2, "painted_steel", "made", bom, (0, 0, -80), C_FRAME))
    out.append(_p("Insulator pad, glass-mica 6 mm, melt pump", cp.break_edges(B(x0 + 10, x1 - 10, -20, 20, ZA - hh / 2 - 6, ZA - hh / 2), 0.5),
                  "insulated_white", "bought", bom_ins, (0, 0, -40), C_INS))
    return out


# ---------------------------------------------------------------------------------------------------------
# melt pump with heater plates and drive (PF1)
# ---------------------------------------------------------------------------------------------------------
def melt_pump(bom_pump=4, bom_drive=5, bom_plate=12, bom_heater=8, bom_fast=34):
    x0, x1, dd, hh = P["PUMP"]
    yb = dd / 2
    out = []
    blk = cp.break_edges(B(x0, x1, -yb, yb, ZA - hh / 2, ZA + hh / 2), 2.0)
    blk = blk - CX(3.0, x0 - 1, x1 + 1, 0, ZA)                         # inlet and outlet ports
    for sx in (-1, 1):
        for sz in (-1, 1):
            blk = blk - CY(2.75, -yb - 1, yb + 1, (x0 + x1) / 2 + sx * 22, ZA + sz * 28)
    out.append(_p("Melt gear pump, 0.16 cm3/rev (Zenith PEP-II class)", blk, "stainless", "bought", bom_pump, (0, 0, 90), C_STAIN))
    for s in (-1, 1):
        hp = B(x0, x1, s * yb, s * (yb + 12), ZA - hh / 2, ZA + hh / 2)
        hp = hp - CX(3.25, x0 - 1, x1 + 1, s * (yb + 6), ZA - 20)
        for sx in (-1, 1):
            for sz in (-1, 1):
                hp = hp - CY(2.75, -yb - 13, yb + 13, (x0 + x1) / 2 + sx * 22, ZA + sz * 28)
        if s < 0:
            hp = hp - CY(7.0, -yb - 13, -yb + 1, (x0 + x1) / 2, ZA)      # drive shaft clearance
        out.append(_p(f"Melt pump heater plate {'-Y' if s < 0 else '+Y'}, aluminium", cp.break_edges(hp, 0.8), "aluminium", "made", bom_plate,
                      (0, s * 60, 90), C_AL))
        out.append(_p(f"Cartridge heater 1/4 in x 2 in, melt pump {'-Y' if s < 0 else '+Y'}", CH(CX(3.175, x0 + 8, x0 + 58, s * (yb + 6), ZA - 20)),
                      "stainless", "bought", bom_heater, (0, s * 100, 90), C_HEAT))
    for sx in (-1, 1):
        for sz in (-1, 1):
            out += bolt(5, dd + 24, loc(((x0 + x1) / 2 + sx * 22, -yb - 12, ZA + sz * 28), (1, 0, 0), (0, -1, 0)), f"pump plates {sx:+d}{sz:+d}", bom_fast, (0, 0, 90))
    xc = (x0 + x1) / 2
    out.append(_p("Melt pump drive shaft (part of the pump)", CH(CY(5.0, -yb - 30, -yb, xc, ZA)), "stainless", "bought", bom_pump, (0, -40, 90)))
    cpl = CY(15.0, -yb - 54, -yb - 30, xc, ZA) - CY(5.0, -yb - 55, -yb - 29, xc, ZA)
    out.append(_p("Jaw coupling, 10 mm to 14 mm", cp.break_edges(cpl, 1.0), "aluminium", "bought", bom_drive, (0, -80, 90), C_AL))
    yb2 = -yb - 56.0                                                    # front face of the motor bracket
    br = B(x0 - 5, x1 + 5, yb2 - 6, yb2, ZP, ZA + 45) - CY(20.0, yb2 - 7, yb2 + 1, xc, ZA)
    br = br + B(x0 - 5, x1 + 5, yb2 - 60, yb2, ZP, ZP + 6)
    br = cp.break_edges(br, 0.8) - CZ(2.75, ZP - 1, ZP + 7, xc, yb2 - 40)
    out.append(_p("Melt pump motor bracket, steel 6 mm folded", br, "painted_steel", "made", bom_drive, (0, -100, 0), C_FRAME))
    out.append(_p("Gearbox output shaft, 14 mm", CH(CY(7.0, yb2 - 6, yb2 + 1.5, xc, ZA)), "mild_steel", "bought", bom_drive, (0, -100, 0)))
    gb = cp.break_edges(CY(28.0, yb2 - 56, yb2 - 6, xc, ZA), 1.5)
    out.append(_p("Planetary gearbox 10:1, NEMA 23", gb, "matte_black", "bought", bom_drive, (0, -140, 0), C_BLK))
    mot = cp.break_edges(B(xc - 28.5, xc + 28.5, yb2 - 132, yb2 - 56, ZA - 28.5, ZA + 28.5), 3.0)
    out.append(_p("Stepper motor NEMA 23, melt pump", mot, "matte_black", "bought", bom_drive, (0, -180, 0), C_BLK))
    out += screw(5, 16, Location((xc, yb2 - 40, ZP + 6)), "pump motor bracket", bom_fast)
    return out


# ---------------------------------------------------------------------------------------------------------
# desktop screw extruder module and melt tubes (PF1)
# ---------------------------------------------------------------------------------------------------------
def extruder(bom_ex=2, bom_tube=3, bom_fast=34):
    xa, xb, w, h = P["EXTRUDER"]
    out = []
    body = cp.break_edges(B(xa, xb, -w / 2, w / 2, ZP, ZP + h), 6.0) - B(xa + 2, xb - 2, -w / 2 + 2, w / 2 - 2, ZP + 2, ZP + h - 2)
    out.append(_p("Desktop single-screw extruder, 5/8 in screw (bought module)", body, "painted_steel", "bought", bom_ex, (0, 0, 60), "#1F4E79"))
    hop = B(250, 370, -55, 55, ZP + h, ZP + h + 120) - B(254, 366, -51, 51, ZP + h + 4, ZP + h + 121)
    out.append(_p("Extruder feed hopper (part of the module)", cp.break_edges(hop, 0.6), "stainless", "bought", bom_ex, (0, 0, 140), C_STAIN))
    bar = CX(P["BARREL_OD"] / 2, xb, 860, 0, ZA) - CX(8.0, xb - 1, 861, 0, ZA)
    out.append(_p("Extruder barrel (part of the module)", bar, "stainless", "bought", bom_ex, (0, 0, 60), C_STAIN))
    out.append(_p("Extruder screw, 5/8 in (part of the module)", CH(CX(7.9, xb + 5, 855, 0, ZA)), "stainless", "bought", bom_ex, (0, 0, 60)))
    bh = CX(26.0, 700, 790, 0, ZA) - CX(P["BARREL_OD"] / 2 + 0.1, 699, 791, 0, ZA)
    out.append(_p("Extruder band heater (part of the module)", cp.break_edges(bh, 1.0), "stainless", "bought", bom_ex, (0, 0, 60), C_HEAT))
    fl = CX(50.0, 860, 875, 0, ZA) - CX(3.0, 859, 876, 0, ZA)
    for k in range(4):
        fl = fl - CX(3.3, 859, 876, 40 * (1 if k % 2 else -1) * (k < 2), ZA + 40 * (1 if k % 2 else -1) * (k >= 2))
    out.append(_p("Extruder outlet flange (part of the module)", cp.break_edges(fl, 0.8), "stainless", "bought", bom_ex, (40, 0, 60), C_STAIN))
    tube = CX(12.5, 875, P["PUMP"][0], 0, ZA) - CX(3.0, 874, P["PUMP"][0] + 1, 0, ZA)
    tube = tube + CX(50.0, 875, 887, 0, ZA) - CX(3.0, 874, 888, 0, ZA)
    for k in range(4):
        yy = 40 * (1 if k % 2 else -1) * (k < 2)
        zz = ZA + 40 * (1 if k % 2 else -1) * (k >= 2)
        tube = tube - CX(3.3, 874, 888, yy, zz)
    out.append(_p("Melt tube, extruder to melt pump, 303 stainless", cp.break_edges(tube, 0.6), "stainless", "made", bom_tube, (60, 0, 60), C_STAIN))
    for k in range(4):
        yy = 40 * (1 if k % 2 else -1) * (k < 2)
        zz = ZA + 40 * (1 if k % 2 else -1) * (k >= 2)
        out += bolt(6, 27, loc((887.0, yy, zz), (0, 1, 0), (1, 0, 0)), f"outlet flange {k + 1}", bom_fast, (60, 0, 60))
    mbh = CX(19.0, 901, 918, 0, ZA) - CX(12.55, 900, 919, 0, ZA)
    out.append(_p("Melt tube band heater, 1 in bore, 100 W", cp.break_edges(mbh, 0.8), "stainless", "bought", 38, (60, 0, 100), C_HEAT))
    lid = Pos(310, 0, ZP + h + 120) * cp.sheet(124, 114, 2.0, holes=[(x, y, 8.0) for x in (-40, -20, 0, 20, 40) for y in (-35, -17, 0, 17, 35)], r_corner=2, edge=0.3)
    out.append(_p("Hopper lid with feed grille, perforated steel 2 mm", lid, "galvanised", "made", 24, (0, 0, 200)))
    fh = B(645, 894, -60, 60, ZA + 55, ZA + 115) - B(649, 890, -56, 56, ZA + 54, ZA + 111)
    fh = fh - CZ(30.0, ZA + 110, ZA + 116, 760, 0)
    out.append(_p("Extruder fume hood, galvanised steel 1 mm, branch to the exhaust", cp.break_edges(fh, 0.4), "galvanised", "made", 24, (0, 0, 120)))
    fs = CZ(30.0, ZA + 115, ZA + 200, 760, 0) - CZ(29.0, ZA + 114, ZA + 201, 760, 0)
    out.append(_p("Extruder fume hood spigot, 60 mm", fs, "galvanised", "bought", 24, (0, 0, 160)))
    ad = CX(15.0, P["PUMP"][1], X0, 0, ZA) - CX(3.0, P["PUMP"][1] - 1, X0 + 1, 0, ZA)
    out.append(_p("Melt adapter, melt pump to die, 303 stainless", cp.break_edges(ad, 0.6), "stainless", "made", bom_tube, (0, 0, 90), C_STAIN))
    sup = B(805, 845, -30, 30, ZP, ZA - P["BARREL_OD"] / 2 - 6) - CZ(2.75, ZP - 1, ZP + 14, 825, 0)
    sup = cp.break_edges(sup, 1.0)
    out.append(_p("Barrel support, steel block", sup, "painted_steel", "made", 10, (0, 0, -40), C_FRAME))
    out.append(_p("Insulator pad, glass-mica 6 mm, barrel", cp.break_edges(B(805, 845, -30, 30, ZA - P["BARREL_OD"] / 2 - 6, ZA - P["BARREL_OD"] / 2 - 0.0), 0.5)
                  - CX(P["BARREL_OD"] / 2, 800, 850, 0, ZA), "insulated_white", "bought", 11, (0, 0, -20), C_INS))
    return out


# ---------------------------------------------------------------------------------------------------------
# collector drum, traverse and corona bar (PF1, PF2)
# ---------------------------------------------------------------------------------------------------------
XD = XT + P["DCD"] + P["DRUM_D"] / 2            # drum axis x
ZRL = ZP + 18.0                                  # top of the linear rails
ZC0, ZC1 = ZRL + 16.0, ZRL + 26.0                # carriage plate
YS = P["DRUM_L"] / 2 + 55.0                      # shaft end beyond the drum
YPB = P["DRUM_L"] / 2 + 30.0                     # pillow block centre


def collector(bom_drum=14, bom_brg=15, bom_motor=16, bom_trav=17, bom_carr=18, bom_fast=34):
    R, L, t = P["DRUM_D"] / 2, P["DRUM_L"], P["DRUM_T"]
    out = []
    shell = CY(R, -L / 2, L / 2, XD, ZA) - CY(R - t, -L / 2 - 1, L / 2 + 1, XD, ZA)
    out.append(_p("Collector drum shell, aluminium tube 200 x 3", shell, "aluminium", "made", bom_drum, (0, 0, 120), C_AL))
    for s in (-1, 1):
        disc = CY(R - t, s * (L / 2 - 10), s * L / 2, XD, ZA) - CY(10.0, -L, L, XD, ZA)
        for k in range(4):
            disc = disc - CY(15.0, -L, L, XD + 55 * (1 if k % 2 else -1) * (k < 2), ZA + 55 * (1 if k % 2 else -1) * (k >= 2))
        out.append(_p(f"Collector drum end disc {'-Y' if s < 0 else '+Y'}, aluminium 10 mm", cp.break_edges(disc, 0.6), "aluminium", "made", bom_drum,
                      (0, s * 60, 120), C_AL))
    out.append(_p("Collector drum shaft, 20 mm steel", cp.round_bar(20, YS + 200.0, 0.8).moved(Location((XD, -YS, ZA), (1, 0, 0), -90)),
                  "mild_steel", "made", bom_drum, (0, 0, 120)))
    zcb = ZA - 33.3                                   # pillow block base (UCP204 class, 33.3 mm centre height)
    for s in (-1, 1):
        y = s * YPB
        pb = B(XD - 63, XD + 63, y - 19, y + 19, zcb, zcb + 14) + CY(32.0, y - 19, y + 19, XD, ZA)
        pb = pb - CY(10.0, y - 20, y + 20, XD, ZA)
        for sx in (-1, 1):
            pb = pb - CZ(5.0, zcb - 1, zcb + 15, XD + sx * 48, y)
        out.append(_p(f"Pillow block bearing, 20 mm {'-Y' if s < 0 else '+Y'}", cp.break_edges(pb, 1.0), "cast_aluminium", "bought", bom_brg, (0, 0, 120)))
        rs = B(XD - 70, XD + 70, y - 25, y + 25, ZC1, zcb)
        for sx in (-1, 1):
            rs = rs - CZ(4.25, ZC1 - 1, zcb + 1, XD + sx * 48, y)
        out.append(_p(f"Bearing riser {'-Y' if s < 0 else '+Y'}, aluminium block", cp.break_edges(rs, 1.0), "aluminium", "made", bom_carr, (0, 0, 60), C_AL))
        for sx in (-1, 1):
            out += bolt(8, zcb + 14 - ZC0, Location((XD + sx * 48, y, zcb + 14)), f"pillow block {s:+d}{sx:+d}", bom_fast, (0, 0, 120))
    # drum motor beside the drum on the carriage, timing belt to a pulley on the +Y shaft end (clears the back panel
    # at full traverse; OPF-DDR-002)
    XM, yb = XD - 140.0, 180.0
    ZM = ZC1 + 6 + 28.5 + 1.5
    yp0, yp1 = 188.0, 198.0
    pd = CY(20.0, yp0, yp1, XD, ZA) - CY(10.05, yp0 - 1, yp1 + 1, XD, ZA)
    out.append(_p("Timing pulley, 40 mm, drum shaft", cp.break_edges(pd, 0.6), "aluminium", "bought", bom_motor, (0, 100, 120), C_AL))
    pm = CY(12.0, yp0, yp1, XM, ZM) - CY(4.05, yp0 - 1, yp1 + 1, XM, ZM)
    out.append(_p("Timing pulley, 24 mm, drum motor", cp.break_edges(pm, 0.6), "aluminium", "bought", bom_motor, (0, 100, 60), C_AL))
    yc = (yp0 + yp1) / 2
    import math
    r1, r2 = 12.0 + 1.7, 20.0 + 1.7
    dx_, dz_ = XD - XM, ZA - ZM
    Ld = math.hypot(dx_, dz_)
    ux_, uz_ = dx_ / Ld, dz_ / Ld
    ct = (r1 - r2) / Ld
    st = math.sqrt(1 - ct ** 2)
    for k, sg in enumerate((1, -1)):
        nx_, nz_ = ct * ux_ - sg * st * uz_, ct * uz_ + sg * st * ux_
        belt = cp.rope([(XM + r1 * nx_, yc, ZM + r1 * nz_), (XD + r2 * nx_, yc, ZA + r2 * nz_)], 3.0)
        out.append(_p(f"Timing belt, 6 mm, run {k + 1}", belt, "rubber_belt", "bought", bom_motor, (0, 100, 90)))
    br = B(XM - 40, XM + 40, yb, yb + 6, ZC1, ZM + 40) - CY(12.0, yb - 1, yb + 7, XM, ZM)
    br = br + B(XM - 48, XM + 48, yb - 30, yb + 6, ZC1, ZC1 + 6)
    for sx in (-1, 1):
        br = br - CZ(4.25, ZC1 - 1, ZC1 + 7, XM + sx * 38, yb - 15)
    out.append(_p("Drum motor bracket, aluminium 6 mm", cp.break_edges(br, 0.8), "aluminium", "made", bom_carr, (0, 120, 60), C_AL))
    out.append(_p("Stepper shaft, 8 mm, drum motor", CH(CY(4.0, yb, yp1 + 1, XM, ZM)), "mild_steel", "bought", bom_motor, (0, 140, 60)))
    mot = cp.break_edges(B(XM - 28.5, XM + 28.5, yb - 76, yb, ZM - 28.5, ZM + 28.5), 3.0)
    out.append(_p("Stepper motor NEMA 23, drum", mot, "matte_black", "bought", bom_motor, (0, 160, 60), C_BLK))
    for sx in (-1, 1):
        out += bolt(8, ZC1 + 6 - ZC0, Location((XM + sx * 38, yb - 15, ZC1 + 6)), f"drum motor bracket {sx:+d}", bom_fast, (0, 120, 60))
    # carriage on two linear rails along Y, lead screw drive
    cx0, cx1 = XM - 55, XD + 95
    car = B(cx0, cx1, -YS - 10, yb + 10, ZC0, ZC1)
    for s in (-1, 1):
        for sx in (-1, 1):
            car = car - CZ(4.25, ZC0 - 1, ZC1 + 1, XD + sx * 48, s * YPB)
    for sx in (-1, 1):
        car = car - CZ(4.25, ZC0 - 1, ZC1 + 1, XM + sx * 38, yb - 15)
    for sx in (-1, 1):
        for sy in (-1, 1):
            car = car - CZ(2.75, ZC0 - 1, ZC1 + 1, XD + sx * 70, sy * 60)
    out.append(_p("Drum carriage plate, aluminium 10 mm", cp.break_edges(car, 0.8), "aluminium", "made", bom_carr, (0, 0, 30), C_AL))
    for sx in (-1, 1):
        rail = B(XD + sx * 70 - 10, XD + sx * 70 + 10, -200, 200, ZP, ZRL)
        for yy in (-150, -50, 50, 150):
            rail = rail - CZ(2.25, ZP - 1, ZRL + 1, XD + sx * 70, yy)
        out.append(_p(f"Linear rail, 20 mm, {'-X' if sx < 0 else '+X'}", cp.break_edges(rail, 0.8), "stainless", "bought", bom_trav, (0, 0, -20), C_STAIN))
        for sy in (-1, 1):
            blk = B(XD + sx * 70 - 17, XD + sx * 70 + 17, sy * 60 - 20, sy * 60 + 20, ZRL - 6, ZC0)
            blk = blk - B(XD + sx * 70 - 10.2, XD + sx * 70 + 10.2, sy * 60 - 21, sy * 60 + 21, ZRL - 7, ZRL)
            blk = blk - CZ(2.75, ZRL, ZC0 + 1, XD + sx * 70, sy * 60)
            out.append(_p(f"Linear bearing block {sx:+d}{sy:+d}", cp.break_edges(blk, 0.8), "stainless", "bought", bom_trav, (0, 0, 10), C_STAIN))
            out += screw(5, 16, Location((XD + sx * 70, sy * 60, ZC1)), f"bearing block {sx:+d}{sy:+d}", bom_fast, (0, 0, 30))
    zs = ZP + 25.0                                                      # lead screw axis
    out.append(_p("Traverse lead screw, 8 mm, 2 mm lead", CH(CY(4.0, -230, 200, XD, zs)), "stainless", "bought", bom_trav, (0, 0, -10)))
    nut = cp.break_edges(B(XD - 15, XD + 15, -12, 12, zs - 10, ZC0), 1.0) - CY(4.1, -13, 13, XD, zs)
    out.append(_p("Traverse nut block, brass nut in aluminium", nut, "brass", "bought", bom_trav, (0, 0, 10)))
    mb = B(XD - 25, XD + 25, -240, -234, ZP, zs + 21) - CY(11.0, -241, -233, XD, zs) + B(XD - 25, XD + 25, -260, -234, ZP, ZP + 4)
    out.append(_p("Traverse motor bracket, aluminium", cp.break_edges(mb, 0.6), "aluminium", "made", bom_carr, (0, -60, 0), C_AL))
    m17 = cp.break_edges(B(XD - 21, XD + 21, -288, -240, zs - 21, zs + 21), 2.0)
    out.append(_p("Stepper motor NEMA 17, traverse", m17, "matte_black", "bought", bom_trav, (0, -100, 0), C_BLK))
    out[-1]["shape"] = out[-1]["shape"]
    sb = cp.break_edges(B(XD - 20, XD + 20, 200, 216, ZP, zs + 8), 0.8) - CY(4.1, 199, 217, XD, zs)
    out.append(_p("Lead screw end bearing block", sb, "aluminium", "bought", bom_trav, (0, 60, 0), C_AL))
    out[-4]["shape"] = out[-4]["shape"] - CY(4.0, -241, -233, XD, zs)
    return out


def corona(bom_bar=19, bom_ins=20):
    zt = ZA + P["DRUM_D"] / 2 + P["CORONA_GAP"]       # needle tips
    out = []
    bar = B(XD - 15, XD + 15, -150, 150, zt + 5, zt + 35)
    n = P["NEEDLES"]
    ys = [(-130 + i * 260 / (n - 1)) for i in range(n)]
    for y in ys:
        bar = bar - CZ(0.55, zt + 4, zt + 16, XD, y)
    for s in (-1, 1):
        bar = bar - CZ(10.1, zt + 30, zt + 36, XD, s * 100)
    out.append(_p("Corona bar body, acetal 30 x 30", cp.break_edges(bar, 1.0), "hdpe_natural", "made", bom_bar, (0, 0, 120), C_ACET))
    for i, y in enumerate(ys):
        out.append(_p(f"Corona needle {i + 1}, stainless 1 mm", CH(CZ(0.5, zt, zt + 15, XD, y), 0.15), "stainless", "bought", bom_bar, (0, 0, 120)))
    zb = P["ENCL_TOP"] - P["POST"]
    for s in (-1, 1):
        out.append(_p(f"Insulator hanger {'-Y' if s < 0 else '+Y'}, acetal rod 20 mm", CH(CZ(10.0, zt + 30, zb, XD, s * 100), 0.8), "hdpe_natural", "made", bom_ins,
                      (0, 0, 160), C_ACET))
    out.append(_p("HV lead clip, brass", cp.break_edges(B(XD - 8, XD + 8, 150, 162, zt + 12, zt + 28), 0.8), "brass", "bought", bom_bar, (0, 40, 120)))
    return out


# ---------------------------------------------------------------------------------------------------------
# forming enclosure, exhaust hood, air system and control panel (all options)
# ---------------------------------------------------------------------------------------------------------
def enclosure(bom_frame=21, bom_panel=22, bom_lock=23, bom_hood=24, pass_holes=((ZA, 0.0, 30.0),)):
    xa, xb = P["ENCL_X"]
    Y, top, a, pt = P["ENCL_Y"], P["ENCL_TOP"], P["POST"], P["PANEL_T"]
    out = []
    posts = [(xa, -Y), (xb - a, -Y), (xa, Y - a), (xb - a, Y - a)]
    for i, (x, y) in enumerate(posts):
        out.append(_p(f"Enclosure post {i + 1}, aluminium SHS 30 x 2", Pos(x + a / 2, y + a / 2, ZB) * cp.shs(a, 2, top - ZB), "aluminium", "made", bom_frame,
                      (0, 0, 0), C_AL))
    for s in (-1, 1):
        yy = s * (Y - a / 2)
        for z, nm in ((ZB, "bottom"), (top - a, "top")):
            r = Pos(xa + a, yy, z + a / 2) * Rot(0, 90, 0) * cp.shs(a, 2, xb - xa - 2 * a)
            if nm == "bottom":
                for x in (xa + 160, xb - 160):
                    r = r - CZ(3.3, ZB - 1, ZB + a + 1, x, yy)
            out.append(_p(f"Enclosure rail {nm} {'-Y' if s < 0 else '+Y'}, aluminium SHS 30 x 2", r, "aluminium", "made", bom_frame, (0, 0, 0), C_AL))
    for x, nm in ((xa + a / 2, "-X"), (xb - a / 2, "+X")):
        r = Pos(x, -Y + a, top - a / 2) * Rot(-90, 0, 0) * cp.shs(a, 2, 2 * Y - 2 * a)
        out.append(_p(f"Enclosure top cross rail {nm}, aluminium SHS 30 x 2", r, "aluminium", "made", bom_frame, (0, 0, 0), C_AL))
    r = Pos(XD, -Y + a, top - a / 2) * Rot(-90, 0, 0) * cp.shs(a, 2, 2 * Y - 2 * a)
    out.append(_p("Enclosure top cross rail, corona hanger", r, "aluminium", "made", bom_frame, (0, 0, 0), C_AL))
    # panels: -X end (melt or feed pass-through), +X end (air line), +Y back, -Y door, roof with the hood opening
    notch = [B(xa - pt - 1, xb + pt + 1, s_ * P["RAIL_Y"] - 21, s_ * P["RAIL_Y"] + 21, ZB - 1, ZR + 1) for s_ in (-1, 1)]
    pe = B(xa - pt, xa, -Y, Y, ZB, top) - notch[0] - notch[1]
    for z, y, d in pass_holes:
        pe = pe - CX(d / 2, xa - pt - 1, xa + 1, y, z)
    out.append(_p("Enclosure panel -X end, polycarbonate 6 mm", cp.break_edges(pe, 0.8), "polycarbonate", "made", bom_panel, (-80, 0, 0), C_PC))
    px = B(xb, xb + pt, -Y, Y, ZB, top) - notch[0] - notch[1] - CX(9.0, xb - 1, xb + pt + 1, 120.0, 1300.0)
    out.append(_p("Enclosure panel +X end, polycarbonate 6 mm", cp.break_edges(px, 0.8), "polycarbonate", "made", bom_panel, (80, 0, 0), C_PC))
    out.append(_p("Enclosure panel back +Y, polycarbonate 6 mm", cp.break_edges(B(xa, xb, Y, Y + pt, ZB, top), 0.8), "polycarbonate", "made", bom_panel, (0, 80, 0), C_PC))
    door = B(xa + 2, xb - 2, -Y - pt, -Y, ZB + 2, top - 2)
    out.append(_p("Door -Y, polycarbonate 6 mm, interlocked", cp.break_edges(door, 0.8), "polycarbonate", "made", bom_panel, (0, -120, 0), C_PC))
    hx, hw = 1240.0, 200.0
    roof = B(xa - pt, xb + pt, -Y - pt, Y + pt, top, top + pt) - B(hx - hw / 2, hx + hw / 2, -hw / 2, hw / 2, top - 1, top + pt + 1)
    out.append(_p("Enclosure roof, polycarbonate 6 mm with hood opening", cp.break_edges(roof, 0.8), "polycarbonate", "made", bom_panel, (0, 0, 120), C_PC))
    for i, z in enumerate((ZB + 120, top - 160)):
        kn = CZ(4.0, z, z + 60, xa - pt - 5, -Y - pt - 4)
        lf = B(xa - pt - 5, xa + 40, -Y - pt - 2, -Y - pt, z, z + 60)
        out.append(_p(f"Door hinge {i + 1}, stainless", cp.break_edges(kn + lf, 0.3), "stainless", "bought", bom_lock, (0, -120, 0), C_STAIN))
    sw = cp.break_edges(B(xb - 75, xb - 32, -Y + 2, -Y + 26, 1250, 1330), 2.0)
    out.append(_p("Door interlock switch with guard locking (ISO 14119 type 2)", sw, "safety_yellow", "bought", bom_lock, (0, -160, 0)))
    hd = B(hx - 130, hx + 130, -130, 130, top + pt, top + pt + 80) - B(hx - 126, hx + 126, -126, 126, top + pt - 1, top + pt + 76)
    hd = hd - CZ(50.0, top + pt + 70, top + pt + 81, hx, 0)
    out.append(_p("Exhaust hood, galvanised steel 1 mm folded", cp.break_edges(hd, 0.4), "galvanised", "made", bom_hood, (0, 0, 200)))
    sp = CZ(50.0, top + pt + 80, top + pt + 180, hx, 0) - CZ(49.0, top + pt + 79, top + pt + 181, hx, 0)
    out.append(_p("Exhaust duct spigot, 100 mm, galvanised", sp, "galvanised", "bought", bom_hood, (0, 0, 260)))
    for s_ in (-1, 1):
        for k, x in enumerate((xa + 160, xb - 160)):
            out.append(_p(f"M6x60 coach screw (DIN 571), enclosure rail {'-Y' if s_ < 0 else '+Y'} {k + 1}",
                          Location((x, s_ * (Y - a / 2), ZB + a)) * cp.coach_screw(6, 60), "zinc_plated", "fastener", 34))
    return out


def fix_foot_conflicts(parts):
    """The foot angles sit beside the posts on the bench; drop any that would collide with a post (kept simple)."""
    return parts


def air_system(bom_pump=25, bom_heater=26, bom_line=27, bom_fast=34):
    out = []
    xa = 1680.0
    pmp = cp.break_edges(B(xa, xa + 220, -35, 155, ZP + 10, ZP + 210), 8.0)
    out.append(_p("Linear diaphragm air pump, 200 NL/min at 20 kPa (Hiblow HP-200 class)", pmp, "hdpe_natural", "bought", bom_pump, (0, 0, 80), "#8FA3AD"))
    for sx in (-1, 1):
        for sy in (-1, 1):
            out.append(_p(f"Air pump rubber foot {sx:+d}{sy:+d}", CZ(10.0, ZP - 0.0, ZP + 0.0 + 0.001, xa + 110 + sx * 90, sy * 75) if False else
                          cp.break_edges(CZ(10.0, ZP, ZP + 10, xa + 110 + sx * 90, 60 + sy * 75), 1.0), "epdm", "bought", bom_pump, (0, 0, 120)))
    od, Lh, _ = P["HEATER"]
    x0h = 1040.0 + 0.0
    hz, hy = 1300.0, 120.0
    ht = cp.break_edges(CX(od / 2, x0h + 10, x0h + Lh, hy, hz), 1.0) + CX(8.0, x0h, x0h + 10, hy, hz) + CX(8.0, x0h + Lh, x0h + Lh + 12, hy, hz)
    out.append(_p("Inline air heater, 1,000 W 120 V, 430 C max (Omega AHPF-101 class)", ht, "stainless", "bought", bom_heater, (0, 0, 160), C_STAIN))
    tc = CH(CX(1.0, x0h - 40, x0h, hy + 12, hz), 0.2)
    out.append(_p("Thermocouple, type K, air outlet", tc, "stainless", "bought", 9, (0, 0, 160)))
    d = P["AIR_TUBE"]
    hot = cp.rope([(x0h, hy, hz), (1030.0, hy, hz), (1030.0, hy, 1170.0), (1030.0, 0.0, 1170.0), (1030.0, 0.0, ZA + P["DIE_H"] + 15 + d / 2 + 0.2)], d)
    out.append(_p("Hot air line, 1/2 in 316 stainless tube, insulated", hot, "stainless", "made", bom_line, (0, 0, 160), C_STAIN))
    xe = P["ENCL_X"][1]
    r_ = d / 2 + 0.3
    cold = cp.rope([(x0h + Lh + 12, hy, hz), (xa + 30, hy, hz), (xa + 30, hy, hz - 40 + r_)], d)
    out.append(_p("Cold air line, heater side, 1/2 in tube", cold, "stainless", "made", bom_line, (0, 0, 80), C_STAIN))
    cold2 = cp.rope([(xa + 30, hy, hz - 120 - r_), (xa + 30, hy, ZP + 210 + r_)], d)
    out.append(_p("Cold air line, pump side, 1/2 in tube", cold2, "stainless", "made", bom_line, (0, 0, 80), C_STAIN))
    fm = cp.break_edges(B(xa + 15, xa + 45, hy - 15, hy + 15, hz - 120, hz - 40), 2.0)
    out.append(_p("Rotameter 20 to 200 L/min with needle bleed valve", fm, "polycarbonate", "bought", bom_line, (0, 0, 80), C_PC))
    return out


def control_panel(bom_box=28, bom_estop=29, bom_fast=34):
    x0, x1, w, h = P["PANEL_BOX"]
    out = []
    bx = cp.break_edges(B(x0, x1, -w / 2, w / 2, ZP, ZP + h), 3.0)
    bx = bx - B(x0 + 2, x1 - 2, -w / 2 + 2, w / 2 - 2, ZP + 2, ZP + h - 2)
    bx = bx - CY(11.0, -w / 2 - 1, -w / 2 + 3, (x0 + x1) / 2, ZP + h - 70)
    for x, y in ((x0 + 30, -100), (x1 - 30, -100), (x0 + 30, 100), (x1 - 30, 100)):
        bx = bx - CZ(3.3, ZP - 1, ZP + 3, x, y)
    out.append(_p("Control panel enclosure, steel 400 x 300 x 200 (UL 508A practice)", bx, "painted_steel", "bought", bom_box, (0, 0, 80), "#D1D5DB"))
    es = CY(20.0, -w / 2 - 22, -w / 2 - 6, (x0 + x1) / 2, ZP + h - 70) + CY(10.5, -w / 2 - 6, -w / 2 + 2.5, (x0 + x1) / 2, ZP + h - 70)
    out.append(_p("Emergency stop push button, red mushroom (ISO 13850), panel", cp.break_edges(es, 1.0), "safety_red", "bought", bom_estop, (0, -80, 0)))
    out.append(_p("Emergency stop legend plate, yellow, panel", CY(28.0, -w / 2 - 2, -w / 2, (x0 + x1) / 2, ZP + h - 70) - CY(10.6, -w / 2 - 3, -w / 2 + 1, (x0 + x1) / 2, ZP + h - 70),
                  "safety_yellow", "bought", bom_estop, (0, -60, 0)))
    for i, z in enumerate((ZP + h - 150, ZP + h - 200)):
        for j in range(3):
            out.append(_p(f"Panel indicator or PID display {i * 3 + j + 1}", cp.break_edges(B(x0 + 30 + j * 50, x0 + 70 + j * 50, -w / 2 - 8, -w / 2, z, z + 40), 1.0) if j < 3 else None,
                          "matte_black", "bought", 30, (0, -40, 0), C_BLK))
    # second stop station at the extruder end, operator side
    st = cp.break_edges(B(700, 770, -228, -160, ZP, ZP + 70), 3.0)
    st = st - CY(11.0, -229, -225, 735, ZP + 40)
    out.append(_p("Emergency stop station box, yellow, operator side", st, "safety_yellow", "bought", bom_estop, (0, -60, 0)))
    es2 = CY(20.0, -250, -234, 735, ZP + 40) + CY(11.0, -234, -228.5, 735, ZP + 40)
    out.append(_p("Emergency stop push button, red mushroom (ISO 13850), operator side", cp.break_edges(es2, 1.0), "safety_red", "bought", bom_estop, (0, -80, 0)))
    for i, (x, y) in enumerate(((x0 + 30, -100), (x1 - 30, -100), (x0 + 30, 100), (x1 - 30, 100))):
        out += screw(6, 16, Location((x, y, ZP + 2)), f"panel box {i + 1}", bom_fast)
    return out


# ---------------------------------------------------------------------------------------------------------
# options
# ---------------------------------------------------------------------------------------------------------
def common(pass_holes=((ZA, 0.0, 30.0),)):
    out = bench() + base_frame()
    out += plate("P5 air pump plate", 33) + plate("P6 control panel plate", 33, extra_holes=[(x, y, 6.6) for x, y in ((2080, -100), (2220, -100), (2080, 100), (2220, 100))])
    out += enclosure(pass_holes=pass_holes) + control_panel()
    return out


def option_pf1():
    out = common()
    out += plate("P1 extruder plate", 33, extra_holes=[(825.0, 0.0, 5.5)])
    xc = (P["PUMP"][0] + P["PUMP"][1]) / 2
    out += plate("P2 melt pump and die plate", 33, extra_holes=[(1020.0, 0.0, 5.5), (xc, -P["PUMP"][2] / 2 - 96.0, 5.5)])
    out += plate("P4 collector plate", 33, extra_holes=[(XD + sx * 70, yy, 4.5) for sx in (-1, 1) for yy in (-150, -50, 50, 150)])
    out += extruder() + melt_pump() + die() + die_stand() + collector() + corona() + air_system()
    return out


def ram_extruder(bom_barrel=36, bom_drive=37, bom_frame=38, bom_fast=34):
    """PF2: vertical heated barrel with a ball-screw ram, outlet elbow into the same die."""
    od, Lb = P["RAM_BARREL"]
    bore = P["RAM_BORE"]
    xr = 820.0
    z0 = ZA + 30.0
    out = []
    el = cp.break_edges(B(xr - 30, xr + 30, -30, 30, ZA - 30, z0), 1.5) - CX(3.0, xr, xr + 31, 0, ZA) - CZ(3.0, ZA - 1, z0 + 1, xr, 0)
    out.append(_p("Ram outlet elbow block, 303 stainless", el, "stainless", "made", bom_barrel, (0, 0, -60), C_STAIN))
    br = CZ(od / 2, z0, z0 + Lb, xr, 0) - CZ(bore / 2, z0 - 1, z0 + Lb + 1, xr, 0)
    out.append(_p("Ram barrel, 70 x 30 bore, 17-4PH stainless", cp.break_edges(br, 1.0), "stainless", "made", bom_barrel, (0, 0, 60), C_STAIN))
    for i, z in enumerate((z0 + 40, z0 + 170)):
        bh = CZ(od / 2 + 8, z, z + 70, xr, 0) - CZ(od / 2 + 0.1, z - 1, z + 71, xr, 0)
        out.append(_p(f"Ram barrel band heater {i + 1}, 70 mm bore", cp.break_edges(bh, 1.0), "stainless", "bought", bom_barrel, (0, 0, 60), C_HEAT))
    zp = z0 + Lb - P["RAM_STROKE"] - 20
    zc = z0 + Lb + 260 - 120
    out.append(_p("Ram piston and rod, 29.9 mm, hardened steel", CH(CZ(bore / 2 - 0.05, zp, zc, xr, 0), 0.5), "stainless", "made", bom_barrel, (0, 0, 160)))
    tube = CX(12.5, xr + 30, X0, 0, ZA) - CX(3.0, xr + 29, X0 + 1, 0, ZA)
    out.append(_p("Melt tube, ram elbow to die, 303 stainless", cp.break_edges(tube, 0.6), "stainless", "made", bom_barrel, (60, 0, 0), C_STAIN))
    sup = cp.break_edges(B(xr - 30, xr + 30, -30, 30, ZP, ZA - 36), 1.0)
    out.append(_p("Ram elbow stand, steel block", sup, "painted_steel", "made", bom_frame, (0, 0, -60), C_FRAME))
    out.append(_p("Insulator pad, glass-mica 6 mm, ram elbow", cp.break_edges(B(xr - 30, xr + 30, -30, 30, ZA - 36, ZA - 30), 0.5), "insulated_white", "bought", 11, (0, 0, -30), C_INS))
    zt = z0 + Lb + 260
    for s in (-1, 1):
        out.append(_p(f"Ram frame column {'-Y' if s < 0 else '+Y'}, steel SHS 40 x 3", Pos(xr, s * 90, ZP) * cp.shs(40, 3, zt - ZP), "painted_steel", "made", bom_frame,
                      (0, s * 60, 0), C_FRAME))
    top = B(xr - 40, xr + 40, -110, 110, zt, zt + 15) - CZ(6.0, zt - 1, zt + 16, xr, 0)
    out.append(_p("Ram frame top plate, steel 15 mm", cp.break_edges(top, 1.0), "painted_steel", "made", bom_frame, (0, 0, 200), C_FRAME))
    for s in (-1, 1):
        out.append(_p(f"Fillet weld, ram column top {'-Y' if s < 0 else '+Y'}", bead_z(xr + 20, s * 90 + s * 20, zt - 30, zt - 2, 1, s), "mild_steel", "weld", None, (0, 0, 200)))
    zc = zt - 120
    cr = B(xr - 35, xr + 35, -110, 110, zc, zc + 15) - CZ(8.0, zc - 1, zc + 16, xr, 0)
    for s in (-1, 1):
        cr = cr - B(xr - 21, xr + 21, s * 90 - 21, s * 90 + 21, zc - 1, zc + 16)
    out.append(_p("Ram crosshead, steel 15 mm, guided on the columns", cp.break_edges(cr, 1.0), "painted_steel", "made", bom_frame, (0, 0, 180), C_FRAME))
    out.append(_p("Ball screw, 16 mm, 5 mm lead", CZ(8.0, zc + 15, zt, xr, 0) - CZ(6.0, zt - 1, zt + 1, xr, 0) if False else CH(CZ(5.9, zc + 15, zt + 15, xr, 0)),
                  "stainless", "bought", bom_drive, (0, 0, 190)))
    out.append(_p("Ball nut flange, 16 mm", cp.break_edges(CZ(18.0, zc + 15, zc + 40, xr, 0) - CZ(6.0, zc + 14, zc + 41, xr, 0), 1.0), "mild_steel", "bought", bom_drive, (0, 0, 180)))
    mot = cp.break_edges(B(xr - 28.5, xr + 28.5, -28.5, 28.5, zt + 15, zt + 91), 3.0)
    out.append(_p("Stepper motor NEMA 23 with 10:1 gearbox, ram", mot, "matte_black", "bought", bom_drive, (0, 0, 260), C_BLK))
    for i, (x, y) in enumerate(((xr - 25, -60), (xr + 25, -60), (xr - 25, 60), (xr + 25, 60))):
        out += screw(5, 12, Location((x, y, zt + 15 + 76 + 0.0)), f"ram motor {i + 1}", bom_fast) if False else []
    return out


def option_pf2():
    out = common()
    out += plate("P1 extruder plate", 33)
    out += plate("P2 melt pump and die plate", 33, extra_holes=[(1020.0, 0.0, 5.5)])
    out += plate("P4 collector plate", 33, extra_holes=[(XD + sx * 70, yy, 4.5) for sx in (-1, 1) for yy in (-150, -50, 50, 150)])
    rm = ram_extruder()
    # top-plate bolts pass through the column walls: cut their holes
    out += rm + die() + die_stand()[:2] + collector() + corona() + air_system()
    return out


def centrifugal(bom_cup=39, bom_motor=40, bom_cage=41, bom_table=42, bom_fast=34):
    """PF3: heated spinneret cup on a vertical motor inside a grounded rod cage; separate corona table."""
    dc, hc = P["CUP"]
    xc, yc = 1240.0, 0.0
    zc0 = 1130.0
    out = []
    cup = CZ(dc / 2, zc0, zc0 + hc, xc, yc) - CZ(dc / 2 - 4, zc0 + 4, zc0 + hc + 1, xc, yc)
    n = P["CUP_HOLES"]
    for i in range(n):
        cup = cup - (Pos(xc, yc, zc0 + 12) * Rot(0, 0, 360 * i / n) * Rot(0, 90, 0) * Pos(0, 0, dc / 2 - 2) * Cylinder(P["CUP_HOLE_D"] / 2, 6))
    cup = cup - CZ(6.0, zc0 - 1, zc0 + 5, xc, yc)
    out.append(_p("Spinneret cup, 60 mm, 12 radial 0.6 mm holes, stainless", cup, "stainless", "made", bom_cup, (0, 0, 120), C_STAIN))
    bh = CZ(dc / 2 + 6, zc0 + 20, zc0 + hc - 2, xc, yc) - CZ(dc / 2 + 0.05, zc0 + 19, zc0 + hc - 1, xc, yc)
    out.append(_p("Spinneret band heater, 300 W", cp.break_edges(bh, 1.0), "stainless", "bought", bom_cup, (0, 0, 140), C_HEAT))
    out.append(_p("Spindle shaft, 12 mm", CH(CZ(6.0, 1050.0, zc0 + 5, xc, yc)), "stainless", "made", bom_cup, (0, 0, 60)))
    out.append(_p("Slip ring, 2 circuits, 12 mm bore", cp.break_edges(CZ(16.0, 1090, 1110, xc, yc) - CZ(6.05, 1089, 1111, xc, yc), 0.8), "brass", "bought", bom_motor, (60, 0, 60)))
    mot = cp.break_edges(CZ(32.0, ZP + 10, 1048, xc, yc), 2.0)
    out.append(_p("Brushless spindle motor, 3,500 rpm class", mot, "matte_black", "bought", bom_motor, (0, 0, -40), C_BLK))
    mp = B(xc - 60, xc + 60, -60, 60, ZP, ZP + 10) - CZ(20.0, ZP - 1, ZP + 11, xc, yc)
    for sx in (-1, 1):
        for sy in (-1, 1):
            mp = mp - CZ(3.3, ZP - 1, ZP + 11, xc + sx * 45, sy * 45)
    out.append(_p("Spindle motor mount plate, aluminium 10 mm", cp.break_edges(mp, 0.8), "aluminium", "made", bom_motor, (0, 0, -60), C_AL))
    R, H = P["CAGE_D"] / 2, P["CAGE_H"]
    zr0, zr1 = 1040.0, 1040.0 + H
    for z, nm in ((zr0, "lower"), (zr1, "upper")):
        rg = CZ(R + 10, z, z + 6, xc, yc) - CZ(R - 15, z - 1, z + 7, xc, yc)
        out.append(_p(f"Collector cage ring {nm}, aluminium 6 mm", cp.break_edges(rg, 0.8), "aluminium", "made", bom_cage, (0, 0, 80 if nm == "upper" else -40), C_AL))
    for i in range(24):
        a = 360 * i / 24
        rod = Pos(xc, yc, 0) * Rot(0, 0, a) * Pos(R, 0, 0) * CH(CZ(2.0, zr0 + 6, zr1, 0, 0))
        out.append(_p(f"Collector cage rod {i + 1}, stainless 4 mm", rod, "stainless", "made", bom_cage, (0, 0, 40)))
    for i in range(4):
        a = 45 + 90 * i
        leg = Pos(xc, yc, 0) * Rot(0, 0, a) * Pos(R, 0, 0) * cp.break_edges(B(-10, 10, -10, 10, ZP, zr0), 1.0)
        out.append(_p(f"Cage leg {i + 1}, acetal insulator 20 mm", leg, "hdpe_natural", "made", bom_cage, (0, 0, -40), C_ACET))
    # corona table on P1: grounded plate, corona bar on two insulator posts, interlocked cover
    xt0, xt1 = 300.0, 560.0
    gp = cp.break_edges(B(xt0, xt1, -150, 150, ZP + 40, ZP + 46), 0.8)
    out.append(_p("Corona table ground plate, aluminium 6 mm", gp, "aluminium", "made", bom_table, (0, 0, 40), C_AL))
    for i, (x, y) in enumerate(((xt0 + 30, -120), (xt1 - 30, -120), (xt0 + 30, 120), (xt1 - 30, 120))):
        out.append(_p(f"Ground plate standoff {i + 1}, aluminium", cp.break_edges(CZ(10, ZP, ZP + 40, x, y), 0.8), "aluminium", "made", bom_table, (0, 0, 20), C_AL))
    zt = ZP + 46 + P["CORONA_GAP"]
    bar = B(xt0 - 30, xt1 + 30, -15, 15, zt + 5, zt + 35)
    for k in range(12):
        bar = bar - CZ(0.55, zt + 4, zt + 16, xt0 + 20 + k * 20, 0)
    out.append(_p("Corona bar body, acetal 30 x 30, table", cp.break_edges(bar, 1.0), "hdpe_natural", "made", 19, (0, 0, 80), C_ACET))
    for k in range(12):
        out.append(_p(f"Corona needle {k + 1}, stainless 1 mm, table", CH(CZ(0.5, zt, zt + 15, xt0 + 20 + k * 20, 0), 0.15), "stainless", "bought", 19, (0, 0, 80)))
    for s in (-1, 1):
        x0p = xt0 - 30 if s < 0 else xt1
        out.append(_p(f"Corona bar post {'-X' if s < 0 else '+X'}, acetal 30 mm", cp.break_edges(B(x0p, x0p + 30, -15, 15, ZP, zt + 5), 1.0),
                      "hdpe_natural", "made", 20, (0, 0, 40), C_ACET))
    cv = B(xt0 - 60, xt1 + 60, -190, 190, ZP, zt + 90) - B(xt0 - 54, xt1 + 54, -184, 184, ZP - 1, zt + 84)
    out.append(_p("Corona table cover, polycarbonate 6 mm, interlocked", cp.break_edges(cv, 0.8), "polycarbonate", "made", 22, (0, 0, 160), C_PC))
    for i, (x, y) in enumerate(((xc + 45, 45), (xc - 45, 45), (xc + 45, -45), (xc - 45, -45))):
        out += screw(6, 12, Location((x, y, ZP + 10)), f"motor plate {i + 1}", bom_fast)
    return out


def option_pf3():
    out = common(pass_holes=())
    out += plate("P1 extruder plate", 33)
    out += plate("P2 melt pump and die plate", 33)
    xc = 1240.0
    # spindle motor sits on its own plate between P2 and P4 on the base rails' cross member at x 1240
    out += [q for q in centrifugal()]
    return out


def components(option="PF1"):
    return {"PF1": option_pf1, "PF2": option_pf2, "PF3": option_pf3}[option]()


if __name__ == "__main__":
    for k in OPTIONS:
        ps = components(k)
        real = [q for q in ps if q["kind"] != "context"]
        m = sum(cp.mass_kg(q) for q in real)
        print(k, len(real), "parts", f"{m:.1f} kg")
