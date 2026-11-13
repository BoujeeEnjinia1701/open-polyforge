"""Open PolyForge: sizing calculations (OPF-CAL-001), first-order, for the STEM check (OPF-STM-001).

Run from the repo root:  python docs/04-calcs/sizing.py   (writes docs/04-calcs/sizing_results.json)
Geometry and set points come from cad/src/model.py PARAMS. Sources are listed in OPF-CAL-001 with the date checked
(2026-11-12). Every assumption is labelled A1 to A16 and repeated in the calculation note. Estimates, not test results.
"""
import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
import model as M  # noqa: E402

P = M.PARAMS
R_AIR, G_AIR = 287.05, 1.4
P_ATM = 101325.0
OUT = {}

# ---- 1. circuit limits (NEC 2020: 210.19(A), 210.20(A), Table 210.21(B)(2); Article 100 continuous = 3 h or more) ----
V = 120.0
circ = {"15 A": dict(A=15, cont_W=V * 15 / 1.25, cord_A=12), "20 A": dict(A=20, cont_W=V * 20 / 1.25, cord_A=16)}
OUT["circuits"] = circ

# ---- 2. polymer stream ------------------------------------------------------------------------------------------
n, ghm = P["HOLES"], P["GHM"]
m_p_gmin = n * ghm                                  # g/min
m_p = m_p_gmin / 60 / 1000                          # kg/s
RHO_MELT = 730.0                                    # A1 assumed PP melt density near 250 C, kg/m3, to confirm
CP_SOLID = 1.8                                      # kJ/kg K, NETZSCH isotactic PP (single value)
CP_MELT_HI = 2.7                                    # A2 assumed upper melt value, to confirm against the resin
DHF_100 = 207.0                                     # J/g, melting enthalpy listed for 100 % crystalline iPP (NETZSCH 207 to 209)
XC = (0.45, 0.50)                                   # A3 crystallinity of the pellets, assumed
dT_p = P["T_MELT"] - P["T_ROOM"]
h_lo = CP_SOLID * dT_p + XC[0] * DHF_100
h_hi = CP_MELT_HI * dT_p + XC[1] * DHF_100
OUT["polymer"] = dict(g_min=m_p_gmin, kg_h=m_p * 3600, h_kJkg=[h_lo, h_hi], W=[m_p * h_lo * 1e3, m_p * h_hi * 1e3],
                      cm3_min=m_p_gmin / (RHO_MELT / 1000))

# ---- 3. process air -----------------------------------------------------------------------------------------------
T_air = P["T_AIR"] + 273.15
rho_air = P_ATM / (R_AIR * T_air)
A_slot = 2 * P["AIR_GAP"] * 1e-3 * P["AIR_SLOT_L"] * 1e-3          # m2, two slots
m_a = rho_air * P["V_AIR"] * A_slot                                # kg/s
a_sound = math.sqrt(G_AIR * R_AIR * T_air)
mach = P["V_AIR"] / a_sound
p0_over_p = (1 + (G_AIR - 1) / 2 * mach ** 2) ** (G_AIR / (G_AIR - 1))
dp_slot = (p0_over_p - 1) * P_ATM
Q_std = m_a / 1.204 * 60000                                        # L/min at 20 C, 1 atm
CP_AIR = (1.005 + 1.040) / 2                                       # kJ/kg K, mean of 300 K and 550 K (Urieli tables)
dT_pump = 15.0                                                     # A4 assumed rise through the diaphragm pump, K
ETA_HEATER = 0.95                                                  # A5 assumed heater body and fitting losses
P_heater = m_a * CP_AIR * 1e3 * (P["T_AIR"] - P["T_ROOM"] - dT_pump) / ETA_HEATER
# air-side pressure budget (laminar land, losses in dynamic heads; Sutherland viscosity) - fix F5
mu_air = 1.458e-6 * T_air ** 1.5 / (T_air + 110.4)
q_dyn = 0.5 * rho_air * P["V_AIR"] ** 2
Re_slot = rho_air * P["V_AIR"] * 2 * P["AIR_GAP"] * 1e-3 / mu_air
def slot_dp(land_mm):
    return 12 * mu_air * land_mm * 1e-3 * P["V_AIR"] / (P["AIR_GAP"] * 1e-3) ** 2 + (0.5 + 0.67 + 1.0) * q_dyn
dp_land_fixed = slot_dp(P["AIR_LAND"])
dp_land_long = slot_dp(43.0)                                       # the knife parallel to the whole 43 mm face (before F5)
Q_hot = m_a / rho_air
v_line = Q_hot / (math.pi / 4 * 0.0109 ** 2)
Re_line = rho_air * v_line * 0.0109 / mu_air
f_line = 0.316 / Re_line ** 0.25
dp_line = (f_line * 0.45 / 0.0109 + 4 * 0.3) * 0.5 * rho_air * v_line ** 2
DP_HEATER, DP_DIE = (3000.0, 5000.0), (2000.0, 4000.0)            # A18 heater and die passage drops, assumed, to measure
dp_total = [dp_land_fixed + dp_line + 0.5e3 + DP_HEATER[0] + DP_DIE[0], dp_land_fixed + dp_line + 0.5e3 + DP_HEATER[1] + DP_DIE[1]]
dp_before = [dp_land_long + dp_line + 0.5e3 + DP_HEATER[0] + DP_DIE[0], dp_land_long + dp_line + 0.5e3 + DP_HEATER[1] + DP_DIE[1]]
Q_norm = m_a / 1.293 * 60000                                       # NL/min at 0 C (pump rating basis)
OUT["air_pressure"] = dict(mu=mu_air, Re_slot=Re_slot, q_dyn_kPa=q_dyn / 1000, slot_kPa=dp_land_fixed / 1000, slot_long_kPa=dp_land_long / 1000,
                           line_kPa=dp_line / 1000, v_line=v_line, total_kPa=[x / 1000 for x in dp_total], before_kPa=[x / 1000 for x in dp_before],
                           Q_norm=Q_norm, pump_max_kPa=30.0, pump_rated_NLmin=200.0)
OUT["air"] = dict(rho=rho_air, slot_area_mm2=A_slot * 1e6, m_kg_s=m_a, Q_std_Lmin=Q_std, mach=mach, dp_slot_kPa=dp_slot / 1000,
                  ratio=m_a / m_p, heater_W=P_heater, heater_duty=P_heater / P["HEATER"][2], per_mm_W=P_heater / P["AIR_SLOT_L"],
                  pump_rated_Lmin=200.0, pump_rated_kPa=20.0)

# ---- 4. heat losses (A6: mineral wool k = 0.05 W/m K at about 150 C mean, 25 mm thick, assumed) -------------------
K_INS, T_INS = 0.05, 0.025
dT_hot = P["T_MELT"] - P["T_ROOM"]
A_die = 2 * (0.08 * 0.09 + 0.08 * 0.08 + 0.09 * 0.08)              # die halves and knives, insulated faces, m2
A_pump = 2 * (0.07 * 0.074 + 0.07 * 0.08 + 0.074 * 0.08)
q_die = K_INS * A_die * dT_hot / T_INS
q_nose = 0.0036 * (30 + 15) * dT_hot                               # A7 exposed nose 36 cm2, h = 30 convection + 15 radiation
q_pump = K_INS * A_pump * dT_hot / T_INS
L_line, r1, r2 = 0.35, 0.00635, 0.00635 + T_INS
q_line = 2 * math.pi * K_INS * L_line * (P["T_AIR"] - P["T_ROOM"]) / math.log(r2 / r1)
OUT["losses_W"] = dict(die=q_die, nose=q_nose, pump=q_pump, hot_line=q_line)

# ---- 5. power budget ----------------------------------------------------------------------------------------------
def budget(scale=1.0, pess=False):
    """Steady-state electrical demand, W. scale multiplies the die width (air and polymer); pess uses upper values."""
    pw = OUT["polymer"]["W"][1 if pess else 0] * scale
    air = P_heater * scale * ((ETA_HEATER / 0.85) if pess else 1.0)
    items = {
        "Process air heater": air,
        "Hot air line loss (made up by the heater)": q_line * (1.5 if pess else 1.0),
        "Extruder barrel heaters (loss plus melt enthalpy)": (200.0 if pess else 120.0) + pw,    # A8 barrel loss 120 to 200 W
        "Extruder drive motor": 100.0 if pess else 60.0,                                          # A9 60 to 100 W at low output
        "Melt pump and die heaters (losses)": (q_die + q_nose + q_pump) * (1.5 if pess else 1.0),
        "Air pump (rated input)": 250.0,                                                          # Hiblow HP-200, 250 W
        "Melt tube heater and barrel nose loss": 40.0 if pess else 25.0,                          # A17
        "Steppers: melt pump, drum, traverse": 60.0 if pess else 45.0,                           # A10
        "Corona supply input": 30.0 if pess else 15.0,                                            # A11
        "Controls, PID, sensors, PSU": 40.0 if pess else 30.0,                                    # A12
    }
    return items, sum(items.values())


nom, tot = budget()
pes, tot_p = budget(pess=True)
OUT["budget_nominal"] = nom
OUT["budget_pessimistic"] = pes
OUT["total_W"] = [tot, tot_p]
OUT["current_A"] = [tot / V, tot_p / V]
OUT["margin_15A_W"] = [circ["15 A"]["cont_W"] - tot, circ["15 A"]["cont_W"] - tot_p]

# reference: the same slot design at 150 mm (6 in) of die, the smallest common laboratory die width (A13)
ref_scale = 150.0 / P["AIR_SLOT_L"]
_, tot_ref = budget(scale=ref_scale)
tot_ref += 250.0 * (math.ceil(Q_norm * ref_scale / 200.0) - 1)       # extra pumps for 3 times the air
OUT["reference_150mm"] = dict(scale=ref_scale, total_W=tot_ref, current_A=tot_ref / V, heater_W=P_heater * ref_scale)

# die width that fits each supply, nominal
fixed = tot - P_heater - OUT["polymer"]["W"][0]
per_mm = (P_heater + OUT["polymer"]["W"][0]) / P["AIR_SLOT_L"]
OUT["max_slot_mm"] = {"15 A": (circ["15 A"]["cont_W"] - fixed) / per_mm, "20 A": (circ["20 A"]["cont_W"] - fixed) / per_mm,
                      "15 A plus a 20 A circuit for the air heater": (circ["20 A"]["cont_W"] * 0.95) / (P_heater / P["AIR_SLOT_L"])}

# warm-up: barrel and die heaters at full rating with the air off, then the air heater under the load manager (A14)
warm = dict(stage1_W=400.0 + 2 * 150.0 + 2 * 100.0 + 30.0 + 45.0, stage2_cap_W=circ["15 A"]["cont_W"])
OUT["warmup"] = warm

# nameplate (marked) rating: every load at its rating, the basis on which cord-and-plug equipment is usually judged
NAMEPLATE = {"Air heater": 1000, "Extruder module (EX2 class)": 500, "Die cartridges": 300, "Pump cartridges": 200, "Melt tube band": 100,
             "Air pump": 250, "Steppers": 60, "Corona supply": 30, "Controls": 40}
OUT["nameplate_W"] = sum(NAMEPLATE.values())
OUT["nameplate_A"] = OUT["nameplate_W"] / V
OUT["trim_K"] = max(0.0, tot_p - circ["15 A"]["cont_W"]) * 0.85 / (m_a * CP_AIR * 1e3)
# warm-up of the die, pump and plates (steel cp 0.5 kJ/kg K, A19) from the model masses
import cad_parts as cp  # noqa: E402
hot = [q for q in M.components("PF1") if any(k in q["name"] for k in ("Die body", "Air knife", "Melt gear pump", "heater plate", "Melt adapter", "Melt tube,"))]
m_hot = sum(cp.mass_kg(q) for q in hot)
E_hot = m_hot * 0.5 * (P["T_MELT"] - P["T_ROOM"])
net_W = 300 + 200 - (q_die + q_nose + q_pump) / 2
OUT["warmup"].update(hot_mass_kg=m_hot, energy_kJ=E_hot, minutes=E_hot * 1e3 / net_W / 60, kWh_start=E_hot / 3600 + 1.0 * 0.5)

# ---- 6. die hydraulics and the melt pump -------------------------------------------------------------------------
# apparent viscosity from the MFR test geometry: die 2.095 x 8.000 mm, barrel 9.55 mm, 2.16 kg at 230 C
mfr = 1550.0
q_mfr = mfr / 600 / 1000 / 739.0                    # m3/s; A15 melt density 739 kg/m3 at 230 C for the MFR conversion
dp_mfr = 2.16 * 9.80665 / (math.pi * (9.55e-3 / 2) ** 2)
mu_app = math.pi * dp_mfr * (2.095e-3) ** 4 / (128 * 8.0e-3 * q_mfr)
gam_mfr = 32 * q_mfr / (math.pi * (2.095e-3) ** 3)
q_hole = ghm / 60 / 1000 / RHO_MELT
a_g = P["HOLE_D"] * 1e-3                               # square groove side
gam_hole = 32 * q_hole / (math.pi * (0.3e-3) ** 3)     # shear rate of the equivalent 0.30 mm round hole
f_T = math.exp(40e3 / 8.314 * (1 / (P["T_MELT"] + 273.15) - 1 / 503.15))   # A16b Arrhenius, Ea about 40 kJ/mol (assumed)
mu_range = (mu_app * f_T, 3 * mu_app)                  # A16: from the 250 C value up to 3 times the 230 C MFR value (shear thinning)
dp_hole = [mu * P["HOLE_L"] * 1e-3 * q_hole / (0.0351 * a_g ** 4) for mu in mu_range]     # square duct, Q = 0.0351 a4 dp / (mu L)
round_equiv = (0.0351 / (math.pi / 128)) ** 0.25 * a_g * 1e3
OUT["die"] = dict(round_equiv_mm=round_equiv, f_T=f_T, mu_app_Pas=mu_app, gamma_mfr=gam_mfr, gamma_hole=gam_hole, dp_hole_MPa=[x / 1e6 for x in dp_hole],
                  pump_rpm=OUT["polymer"]["cm3_min"] / P["PUMP_CC"], holes_per_inch=25.4 / P["HOLE_PITCH"])

# ---- 7. web output and collector -----------------------------------------------------------------------------------
area_rate = m_p_gmin / P["BASIS_WEIGHT"]             # m2/min
web_w = (60.0 + 2 * P["TRAVERSE"]) / 1000             # A: spray about 60 mm wide plus the traverse stroke
sheet = math.pi * P["DRUM_D"] / 1000 * web_w
surf = math.pi * P["DRUM_D"] / 1000 * P["DRUM_RPM"]   # m/min
ETA_COLL = (0.70, 0.90)                                # A20 lay-down efficiency on the drum, assumed (fly loss 10 to 30 %)
T_DOFF = (1.5, 2.0)                                    # A21 minutes to stop the melt pump, open, cut off the sheet and restart
dep = [area_rate * 60 * e for e in ETA_COLL]
lay = sheet / area_rate
eff = [sheet / (lay / ETA_COLL[0] + T_DOFF[1]) * 60, sheet / (lay / ETA_COLL[1] + T_DOFF[0]) * 60]
OUT["web"] = dict(deposited_m2_h=dep, batch_m2_h=eff, area_m2_h=area_rate * 60, web_width_mm=web_w * 1000, sheet_m2=sheet, min_per_sheet=sheet / area_rate,
                  surface_m_min=surf, energy_kWh_m2=tot / 1000 / (area_rate * 60))

# ---- 8. corona -----------------------------------------------------------------------------------------------------
kv, gap, ua = P["CORONA_KV"], P["CORONA_GAP"], P["CORONA_UA"]
OUT["corona"] = dict(E_avg_kV_mm=kv / gap, uniform_breakdown_kV_mm=3.0, P_out_W=kv * 1e3 * ua * 1e-6,
                     ozone_ppm_at_exhaust=None)
Q_exh = 0.10                                          # m3/s, extraction from the enclosure (A: 0.5 m/s over the door gaps)
o3_yield_g_kWh = 50.0                                 # bounding ozone yield in air, assumed, to measure (V6)
o3_g_s = o3_yield_g_kWh * OUT["corona"]["P_out_W"] / 1000 / 3600
o3_ppm = o3_g_s / Q_exh / 2.0e-3 * 1.0                # 0.2 mg/m3 per 0.1 ppm (OSHA): 1 ppm = 2.0 mg/m3 = 2.0e-3 g/m3
OUT["corona"].update(ozone_g_h=o3_g_s * 3600, ozone_ppm_at_exhaust=o3_ppm, exhaust_m3_s=Q_exh,
                     exhaust_over_process_air=Q_exh / (m_a / 1.204))

C_HV = 2.0 * 100e-12 + 1.0e-9                         # A22 2 m of HV cable at about 100 pF/m plus 1 nF supply output, assumed
OUT["corona"]["stored_J"] = 0.5 * C_HV * (kv * 1e3) ** 2

# ---- 9. PF2 ram extruder ------------------------------------------------------------------------------------------
bore = P["RAM_BORE"] / 1000
vol = math.pi / 4 * bore ** 2 * P["RAM_STROKE"] / 1000
charge = vol * 550.0                                  # A23 pellet bulk density about 550 kg/m3 (assumed), one charge
alpha_pp = 0.2 / (900 * 1.8e3)                        # k 0.2 W/m K (NETZSCH 0.17 to 0.25), rho 900, cp 1.8: m2/s
t_melt = (bore / 2) ** 2 / alpha_pp                   # Fourier number 1, s
F = 1.0e6 * math.pi / 4 * bore ** 2                    # at 1 MPa (die plus screen, upper value)
torque = F * 0.005 / (2 * math.pi * 0.9)
OUT["PF2"] = dict(charge_kg=charge, run_min=charge * 1000 / m_p_gmin, melt_min=t_melt / 60, ram_force_N=F, screw_torque_Nm=torque,
                  ram_speed_mm_min=OUT["polymer"]["cm3_min"] / (math.pi / 4 * (bore * 100) ** 2) * 10,
                  duty=(charge * 1000 / m_p_gmin) / (charge * 1000 / m_p_gmin + t_melt / 60 + 10))

# ---- 10. PF3 centrifugal (Molina et al. 2022 as the basis) --------------------------------------------------------
pf3_poly = 12.5 / 60 / 1000 * (h_lo + h_hi) / 2 * 1e3   # 24 to 26 g in about 2 min
rim = P["CUP"][0] / 2000
w = P["SPIN_RPM"] * math.pi / 30
OUT["PF3"] = dict(gmin=12.5, melt_W=pf3_poly, heater_W=[300.0 + 150, 300.0 + 250], motor_W=150.0,
                  total_W=[300 + 150 + 150 + 45 + 15 + 30, 300 + 250 + 150 + 45 + 15 + 30],
                  rpm=P["SPIN_RPM"], tip_speed_m_s=w * rim, accel_m_s2=w ** 2 * rim, ring_KE_J=0.5 * 0.3 * rim ** 2 * w ** 2,
                  qf_best=-math.log(1 - 0.9448) / (16.28 * 98.0665), qf_ref=-math.log(1 - 0.9734) / (3.69 * 98.0665),
                  fibre_um="3.4 to 5.2 mean (Molina et al. 2022)")

# ---- 11. mass, envelope, cost -------------------------------------------------------------------------------------
mass = {}
for k in M.OPTIONS:
    ps = [q for q in M.components(k) if q["kind"] != "context"]
    mass[k] = sum(cp.mass_kg(q) for q in ps)
OUT["mass_kg"] = mass
bom = list(csv.DictReader((ROOT / "bom/bom.csv").open())) if (ROOT / "bom/bom.csv").exists() else []
OUT["bom_total"] = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in bom)
OUT["electricity_usd_kwh"] = 0.1401
OUT["web"]["energy_usd_m2"] = OUT["web"]["energy_kWh_m2"] * 0.1401
from build123d import Compound  # noqa: E402
bb = Compound(children=[q["shape"] for q in M.components("PF1") if q["kind"] != "context"]).bounding_box()
OUT["envelope_mm"] = dict(length=bb.max.X - bb.min.X, depth=bb.max.Y - bb.min.Y, height=bb.max.Z - M.ZB, x=[bb.min.X, bb.max.X], y=[bb.min.Y, bb.max.Y])

if __name__ == "__main__":
    (ROOT / "docs/04-calcs/sizing_results.json").write_text(json.dumps(OUT, indent=1))
    print(f"polymer {m_p_gmin:.1f} g/min; air {m_a * 1e3:.2f} g/s ({Q_std:.0f} L/min std), ratio {m_a / m_p:.0f}, Mach {mach:.2f}")
    print(f"heater {P_heater:.0f} W (duty {P_heater / P['HEATER'][2]:.0%}); total {tot:.0f} to {tot_p:.0f} W, {tot / V:.1f} to {tot_p / V:.1f} A")
    print(f"reference 150 mm die: {tot_ref:.0f} W, {tot_ref / V:.1f} A; max slot {OUT['max_slot_mm']}")
    print(f"die dp per hole {OUT['die']['dp_hole_MPa']}, mu {mu_app:.1f} Pa s, pump {OUT['die']['pump_rpm']:.0f} rpm")
    print(f"web {area_rate * 60:.1f} m2/h, sheet {sheet:.3f} m2 in {sheet / area_rate:.2f} min; {OUT['web']['energy_kWh_m2']:.3f} kWh/m2")
    print("corona", OUT["corona"]); print("PF2", OUT["PF2"]); print("PF3", OUT["PF3"]); print("mass", mass, "bom", OUT["bom_total"])
