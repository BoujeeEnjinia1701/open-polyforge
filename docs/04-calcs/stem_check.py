"""Open PolyForge: STEM check calculations (OPF-STM-001, STANDARDS sections 20 and 25.6a, machines).

Run from the repo root:  python docs/04-calcs/sizing.py      (writes sizing_results.json)
                         python docs/04-calcs/stem_check.py  (writes stem_results.csv, stem_results_options.csv and
                                                              refreshes the two tables in docs/01b-stem-check.md)
Rows S1 to S55 check the carried option PF1 (screw extruder, melt pump and slot die), including the power budget of a
full-width die that failed and was fixed under Amish's standing instruction of 2026-10-23 (OPF-DEC-001 F1 to F10); S41 to S55 were added after the independent review.
Rows X1 to X12 check PF2 (ram extruder) and PF3 (centrifugal melt spinning). Sources and dates checked (2026-11-12) are
listed in OPF-STM-001 and OPF-CAL-001.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
from stem_check import Check, WITHIN, PLAUSIBLE, FIX, FAILS  # noqa: E402,F401
import model as M  # noqa: E402

P = M.PARAMS
R = json.loads((ROOT / "docs/04-calcs/sizing_results.json").read_text())
CAL = "OPF-CAL-001"
REV = "independent review 2026-11-12"
c = Check(ROOT / "docs/04-calcs/stem_results.csv")
x = Check(ROOT / "docs/04-calcs/stem_results_options.csv")
A, PO, D, W, CO = R["air"], R["polymer"], R["die"], R["web"], R["corona"]
tot, tot_p = R["total_W"]
ref = R["reference_150mm"]
lim15 = R["circuits"]["15 A"]["cont_W"]

# ---- Engineering: power budget against the supply (STANDARDS 25.6a, the critical check) --------------------------
AP, NP = R["air_pressure"], R["nameplate_W"]
WU = R["warmup"]

# ---- Engineering: power budget against the supply (STANDARDS 25.6a, the critical check) --------------------------
c.cited("S1", f"The proposal's slot die and hot air fit one 120 V, 15 to 20 A circuit (team target); a 150 mm laboratory-width die at the "
        f"same air design needs about {ref['total_W']:,.0f} W ({ref['current_A']:.1f} A)", "Engineering and technology", "Power and link budgets",
        "NEC 2020 210.19(A), 210.20(A) and Table 210.21(B)(2): continuous load (3 h or more) at 125 %, cord-and-plug load 12 A on a 15 A and "
        "16 A on a 20 A receptacle; 1,440 W and 1,920 W continuous",
        f"{ref['total_W']:,.0f} W (air heater alone {ref['heater_W']:,.0f} W, and two more air pumps) against 1,440 W and 1,920 W: fails at both. "
        f"Fixed: the die is set to a 48 mm air slot with 40 capillaries at 0.10 g/hole/min (nominal electrical limit {R['max_slot_mm']['15 A']:.0f} mm "
        f"on 15 A); the air pump and the pessimistic case (S3) leave no room for more ({REV}: S1 weak, pump scaling added, 'with margin' "
        "withdrawn)", WITHIN, closed_by="OPF-DEC-001 F1 (standing instruction, 2026-10-23)")
c.cited("S2", f"The fixed design draws about {tot:,.0f} W ({R['current_A'][0]:.1f} A) steady, within one 15 A circuit's 1,440 W continuous",
        "Engineering and technology", "Power and link budgets", "Sum of the steady loads in OPF-CAL-001 section 5 against the NEC 125 % rule; "
        "cord-and-plug equipment is usually judged on its marked (nameplate) rating",
        f"Steady {tot:,.0f} W meets 1,440 W, but the nameplate sum is {NP:,.0f} W ({R['nameplate_A']:.1f} A). Only a load-limiting means that "
        f"an inspector accepts makes a 12 A marking valid; power factor of the pump and supplies raises the current above W / 120 ({REV}: S2 "
        "weak). Load manager now mandatory (F2); marking and acceptance to assess with an electrician (OPF-DEC-001 D2)", PLAUSIBLE)
c.cited("S3", f"With the upper value of every assumption the steady draw is {tot_p:,.0f} W ({R['current_A'][1]:.1f} A), {tot_p - lim15:.0f} W over 1,440 W",
        "Engineering and technology", "Power and link budgets", "Upper bounds A5 to A12 and A17 (heater 85 % efficient, barrel loss 200 W, die "
        "losses x 1.5, melt enthalpy at the upper value)",
        f"The load manager caps summed heater duty at 12 A; at the pessimistic case it trims the air heater by {tot_p - lim15:.0f} W, about "
        f"{R['trim_K']:.0f} K, so the air would fall to about {P['T_AIR'] - R['trim_K']:.0f} C, below the 230 C bottom of the cited range, which would "
        "coarsen the fibres; then the throughput set point is lowered instead ({REV}: corrected from 20 to 30 K). Heater lag about 2 min limits how fast it can trim (S43). Line current to measure (V1)", PLAUSIBLE)
c.claim("S4", f"The process air heater needs about {A['heater_W']:.0f} W, {A['heater_duty']:.0%} of a 1,000 W, 120 V inline heater",
        "Physics", "Thermodynamics", f"Q = m cp dT / eta: {A['m_kg_s'] * 1e3:.2f} g/s x 1.02 kJ/kg K (Urieli air tables, 1.005 at 300 K, "
        "1.040 at 550 K) x (270 - 20 - 15) K / 0.95; Omega AHPF-101 1,000 W, 203 mm heated, 254 mm long, 430 C max; heater body insulated "
        "(an uninsulated shell would lose 60 to 100 W)", round(A["heater_W"]), 1000.0, "W", closed_by=f"{CAL} section 3")
c.cited("S5", f"Melting the polymer takes only {PO['W'][0]:.0f} to {PO['W'][1]:.0f} W at {PO['g_min']:.1f} g/min; the air, not the melt, sets the power",
        "Physics", "Thermodynamics", "h = cp dT + Xc dHf: cp 1.8 kJ/kg K (NETZSCH iPP) to 2.7 (melt, assumed A2), melting enthalpy 207 J/g "
        "for 100 % crystalline iPP (NETZSCH lists 207 to 209), Xc 0.45 to 0.50 assumed",
        f"{PO['h_kJkg'][0]:.0f} to {PO['h_kJkg'][1]:.0f} kJ/kg; air heater {A['heater_W']:.0f} W is {A['heater_W'] / PO['W'][1]:.0f} to "
        f"{A['heater_W'] / PO['W'][0]:.0f} times the melt heat (air-to-polymer ratio {A['ratio']:.0f})", WITHIN, closed_by=f"{CAL} section 2")
L = R["losses_W"]
c.cited("S6", f"Die and melt pump heaters (2 x 150 W and 2 x 100 W rated) cover their steady losses of about {L['die'] + L['nose'] + L['pump']:.0f} W",
        "Physics", "Heat transfer", "Conduction through 25 mm mineral wool (k 0.05 W/m K assumed, A6); exposed nose 36 cm2 at h = 45 W/m2 K (A7)",
        f"Die {L['die']:.0f} W, nose {L['nose']:.0f} W, pump {L['pump']:.0f} W against 500 W rated: ample, so warm-up sets the heater size (S44)", PLAUSIBLE)
c.cited("S7", f"A 200 NL/min, 20 kPa (30 kPa maximum) diaphragm pump supplies the {AP['Q_norm']:.0f} NL/min that two 0.3 x 48 mm slots pass at "
        f"{P['V_AIR']:.0f} m/s and 270 C", "Physics", "Fluid mechanics",
        f"m = rho v A: rho {A['rho']:.3f} kg/m3 (ideal gas, 270 C), A {A['slot_area_mm2']:.1f} mm2; Hiblow HP-200 200 L/min (normal) at 20 kPa, "
        "30 kPa maximum continuous, 250 W",
        f"Flow is inside the rating, but the circuit needs {AP['total_kPa'][0]:.0f} to {AP['total_kPa'][1]:.0f} kPa (S41), near the 30 kPa "
        f"maximum; the pump curve at that pressure is to read from the maker and measure ({REV}: S7 weak, pressure not checked; pump raised "
        "from HP-150 to HP-200 class)", PLAUSIBLE)
c.cited("S8", f"An air-to-polymer mass ratio of about {A['ratio']:.0f} and 140 m/s at the slot attenuate PP 1,550 MFR melt to 1 to 5 um fibres",
        "Physics", "Fluid mechanics", "Commercial melt-blown fibres average 1 to 5 um at 0.3 to 3 g/hole/min, air near or below sonic at "
        "230 to 360 C (Schmidt et al. 2022); measured peak 130 to 160 m/s near a die at 260 C (Wu et al. 2024); a higher air-to-polymer "
        "ratio gives finer fibres (Milligan and Haynes, in Kara and Molnar 2022)",
        "No validated correlation for this die is available, so the diameter is a target, measured by SEM at TRL 4 (V3)", PLAUSIBLE)
c.cited("S9", "Target fibre diameter 1 to 5 um (mean about 2 um) for filtration-grade web", "Physics", "Fluid mechanics",
        "Larsen et al. 2021 (ORNL): charged melt-blown filter fibres typically 1 to 4 um, average near 2 um; Schmidt et al. 2022: commercial "
        "means 1 to 5 um", "Set as a requirement (PR-004) and measured (V3)", WITHIN, closed_by="PR-004")
c.cited("S10", "A metallocene melt-blown grade of MFR 1,550 g/10 min (230 C, 2.16 kg) is the resin", "Chemistry", "Materials and polymer chemistry",
        "ExxonMobil filtration fact sheet: Exceed Flow PP6936G2 (legacy Achieve Advanced PP6936G2) MFR 1,550; Molina et al. 2022 also used "
        "PP6936G2 at 1,550; Drabek and Zatloukal 2019: 1,500 to 1,800 for Hills nanowebs; Schmidt et al. 2022: commercial grades up to 1,500",
        f"At the upper edge of common practice; small-lot supply to confirm ({REV}: S10 weak, sources added)", WITHIN, closed_by="PR-016")
c.cited("S11", f"Melt at {P['T_MELT']:.0f} C and air at {P['T_AIR']:.0f} C are within melt-blowing practice", "Physics", "Thermodynamics",
        "Air 230 to 360 C (Schmidt et al. 2022; Textile Learner); die 215 to 340 C (Textile Learner); a 260 C die and air used by Wu et al. 2024",
        "Inside the ranges; the resin data sheet sets the final window", WITHIN, closed_by=f"{CAL} section 1")
c.cited("S12", f"Capillaries of 0.30 mm round equivalent at {P['HOLE_PITCH']:.1f} mm pitch ({D['holes_per_inch']:.1f} per inch), 40 across 39 mm, are within melt-blown practice",
        "Engineering and technology", "Manufacturing tolerances", "Hole 250 to 500 um at 1 to 4 per mm (Schmidt et al. 2022); 0.4 mm typical "
        "(Textile Learner); square duct Q = 0.0351 a4 dp / (mu L) against pi d4 / 128 for a round hole",
        f"Grooves cut in the lower half of a split die (OPF-DDR-002). A 0.30 mm square groove would pass 43 % more than a 0.30 mm hole, so the "
        f"groove is {P['HOLE_D']:.2f} mm square, which flows as a {D['round_equiv_mm']:.2f} mm hole ({REV}: area mismatch found; fixed F6)", WITHIN,
        closed_by="OPF-DEC-001 F6; OPF-DDR-002")
c.cited("S13", f"{P['GHM']:.2f} g/hole/min ({PO['g_min']:.1f} g/min) is a workable throughput, three times below the 0.3 to 3 of commercial lines",
        "Engineering and technology", "Control", "Schmidt et al. 2022 range 0.3 to 3 g/hole/min; reduced here to fit the power budget (F1)",
        "Low throughput per hole raises the air-to-polymer ratio; flow uniformity across 40 holes at low pressure to check (S14, V2)", PLAUSIBLE)
c.cited("S14", f"Each groove needs {D['dp_hole_MPa'][0]:.2f} to {D['dp_hole_MPa'][1]:.2f} MPa, well within the pump's 27.6 MPa differential",
        "Physics", "Fluid mechanics", f"Square-duct Poiseuille with an apparent viscosity of {D['mu_app_Pas']:.1f} Pa s from the MFR test geometry "
        f"(die 2.095 x 8.000 mm, barrel 9.55 mm, 2.16 kg; Sisco), times {D['f_T']:.2f} for 250 C (Arrhenius, Ea about 40 kJ/mol, assumed) up to "
        "3 times for shear thinning (A16); no Bagley correction; Zenith PEP-II to 4,000 psi differential",
        "Low die pressure makes the hole-to-hole split depend on the manifold and the pre-land; basis-weight profile to measure (V2)", PLAUSIBLE)
c.cited("S15", f"A 0.16 cm3/rev melt pump at {D['pump_rpm']:.0f} rpm meters {PO['cm3_min']:.1f} cm3/min", "Mathematics", "Units and dimensional analysis",
        "Displacement x speed; melt density 0.73 g/cm3 assumed (A1); smallest Zenith PEP-II sizes 0.16 and 0.3 cm3/rev",
        "Speed range of this size to confirm with the maker; at about 3.5 to 5 Pa s the melt is at the thin end for a gear pump, so slip and "
        "metering accuracy depend on pressure (S48)", PLAUSIBLE)
c.cited("S16", "The desktop extruder supplies the 0.24 kg/h the die needs", "Engineering and technology", "Power and link budgets",
        "Filabot EX2: just over 2 lb/h (0.91 kg/h) on filament resins, 5/8 in screw, L/D 12, 500 W; listed as discontinued, EX3 (1,000 W, "
        "200 W brushless motor) announced",
        f"Throughput is well inside, but the rating is for filament resins and the screw builds little pressure with a 5 Pa s melt (S17); the "
        f"EX3 would raise the nameplate ({REV}: S16 weak)", PLAUSIBLE)
c.cited("S17", "A filament-type screw extruder feeds a 1,550 MFR melt steadily into the melt pump inlet", "Chemistry", "Materials and polymer chemistry",
        "Very low melt viscosity (about 5 Pa s) gives back-flow over the flights and a short melt seal; the melt pump decouples the die "
        "from screw pulsation", "Screw speed under inlet-pressure control (melt pressure transducer at the pump inlet); to test V2. A ram (PF2) is "
        "the fallback if feeding fails", PLAUSIBLE)
c.cited("S18", "Melt hold-up of about 13 cm3 gives a residence time near 2.4 min at 250 C, short enough to limit degradation",
        "Chemistry", "Materials and polymer chemistry", "Hold-up estimate (screw channel about 10 cm3, pump and die about 3 cm3) over "
        f"{PO['cm3_min']:.1f} cm3/min; Borealis: higher processing temperature degrades PP more",
        "Purge with a low-MFR PP at shutdown; residence time and die build-up to observe (V2)", PLAUSIBLE)
c.cited("S19", f"Die-to-collector distance {P['DCD']:.0f} mm (adjustable 150 to 300) is within melt-blowing practice", "Engineering and technology",
        "Manufacturing tolerances", "Typical DCD 50 to 500 mm (Kara and Molnar 2022); 10 to 50 cm (Schmidt et al. 2022); 25 cm (Wu et al. 2024)",
        "Longer DCD gives a softer, bulkier web; set by test", WITHIN, closed_by="PR-006")
c.cited("S20", f"Output: {W['area_m2_h']:.1f} m2/h of {P['BASIS_WEIGHT']:.0f} g/m2 web laid at 100 % capture, {W['deposited_m2_h'][0]:.1f} to "
        f"{W['deposited_m2_h'][1]:.1f} m2/h deposited, and {W['batch_m2_h'][0]:.1f} to {W['batch_m2_h'][1]:.1f} m2/h of sheets with doffing",
        "Mathematics", "Units and dimensional analysis", "Mass balance: area = mass rate / basis weight; lay-down 70 to 90 % assumed (A20); "
        f"a {W['sheet_m2']:.3f} m2 sheet every {W['min_per_sheet']:.2f} min plus a 1.5 to 2 min doff (A21)",
        f"Batch doffing is the limit: the melt pump stops, the die stays hot, the sheet is cut off and the run restarts (F7). PR-007 restated "
        f"({REV}: S20 weak, capture and doffing added)", WITHIN, closed_by=f"{CAL} section 7; OPF-DEC-001 F7; PR-007")
c.cited("S21", f"{P['BASIS_WEIGHT']:.0f} g/m2 is a realistic basis weight for one filter layer", "Engineering and technology", "Standards practice",
        "ExxonMobil filtration fabrics tested at 25 gsm (TSI 8130, NaCl, 32 L/min); ORNL web about 30 g/m2, two plies of 30 to 35 g/m2 in a "
        "finished respirator (Larsen et al. 2021)", "Matches", WITHIN, closed_by="PR-005")
c.cited("S22", f"Traversing the drum {2 * P['TRAVERSE']:.0f} mm under the spray gives a {W['web_width_mm']:.0f} mm web of even basis weight",
        "Engineering and technology", "Control", "Lay-down geometry: a 48 mm slot spreads to about 60 mm at 200 mm (assumed)",
        "Edges thinner than the middle; even zone and CV of basis weight to measure (V2); large enough for 100 cm2 test discs", PLAUSIBLE)

# ---- Electromagnetism: corona (STANDARDS 25.6a) -----------------------------------------------------------------
c.cited("S23", f"A -{P['CORONA_KV']:.0f} kV needle bar {P['CORONA_GAP']:.0f} mm above the grounded drum makes a corona without sparking to the drum",
        "Physics", "Electromagnetism and circuits", "Melt-blown corona charging at 5 to 25 kV (Wadsworth and Hersh, US 4,375,718), 15 to 35 kV "
        "(Shim et al. 2008), 30 to 60 kV (Larsen et al. 2021), up to 50 kV per bar (NC State Nonwovens Institute line); air breaks down near "
        "3 kV/mm in a uniform field", f"Average field {CO['E_avg_kV_mm']:.2f} kV/mm; the needle tips start the corona. Negative point-to-plane "
        "spark-over at 40 mm is well above 25 kV, positive is lower, so the supply is fixed negative polarity and current-limited; humidity "
        f"shifts onset (S54); voltage raised in steps (V4; {REV}: polarity note added)", PLAUSIBLE)
c.claim("S24", f"Corona output at {P['CORONA_UA']:.0f} uA is about {CO['P_out_W']:.0f} W, well inside a 30 kV, 1 mA (30 W) supply",
        "Physics", "Electromagnetism and circuits", "P = V I; supply 0 to 30 kV, 1 mA", CO["P_out_W"], 30.0, "W", closed_by=f"{CAL} section 8")
c.cited("S25", "Corona charging raises the web's filtration efficiency at 0.3 um above that of the uncharged web", "Physics", "Electromagnetism and circuits",
        "Larsen et al. 2021: charging is critical to high efficiency; ExxonMobil charged 25 gsm fabrics about 98 to 99.6 % on TSI 8130 at 32 L/min; "
        "Wadsworth and Hersh patent", "Mechanism established; the gain for this web is measured before and after charging (V5)", PLAUSIBLE)
c.cited("S26", "The charge holds after heat and humidity ageing", "Physics", "Electromagnetism and circuits",
        "Larsen et al. 2021 aged media 24 h at 70 C and 85 % RH; 42 CFR 84.181 conditions filters 25 h at 38 C and 85 % RH before testing "
        "(benchmark only)", "Charge decay is a measured property; no figure is claimed until V5", PLAUSIBLE)

# ---- Chemistry: ozone and fumes ---------------------------------------------------------------------------------
c.cited("S27", "Ozone from the corona stays below the 0.1 ppm workplace limit in the room", "Chemistry", "Environmental and atmospheric chemistry",
        "OSHA PEL 0.1 ppm (8 h TWA) and NIOSH REL 0.1 ppm ceiling; no ozone yield for a negative needle corona of this geometry was found, "
        "so 50 g/kWh is assumed as a working figure, not a bound (negative corona makes more ozone than positive, and some NOx)",
        f"{CO['ozone_g_h']:.2f} g/h gives {CO['ozone_ppm_at_exhaust']:.2f} ppm in the exhaust duct, ducted outdoors. HV runs only with the door "
        "shut and extraction proven (F3); ozone monitor at the operator (BOM 35); measured in V6", PLAUSIBLE)
c.cited("S28", "Fumes from hot PP are captured by the forming enclosure exhaust and the extruder branch hood", "Chemistry", "Environmental and atmospheric chemistry",
        "Borealis (2022): PP processing emits hydrocarbons, oxygenates (formaldehyde, acetaldehyde, formic acid, acetone) and wax-like "
        "aerosol, more at higher temperature; CCOHS: capture velocity about 0.5 m/s",
        f"Exhaust {CO['exhaust_m3_s']:.2f} m3/s is {CO['exhaust_over_process_air']:.0f} times the process air; the extruder outlet and hopper, outside "
        "the enclosure, get a branch hood (F4); smoke test and aldehyde sampling (V6)", PLAUSIBLE)
c.cited("S29", "Thermo-oxidative degradation at 250 C melt and 270 C air stays low enough to run", "Chemistry", "Physical (kinetics, equilibria, thermochemistry)",
        "NETZSCH: iPP decomposition 450 to 470 C (a thermogravimetric figure, not an oxidation onset); in air PP oxidises from about 200 C, "
        "which oxidation-induction tests use; air heater maximum outlet 430 C (Omega)",
        f"Oxidation does happen at these set points (it is the source of the aldehydes in S28); independent cut-outs at 300 C on every zone "
        f"(PR-011); MFR drift and die-lip build-up to measure ({REV}: S29 refuted as worded, restated)", PLAUSIBLE)

# ---- Biology and human factors ----------------------------------------------------------------------------------
c.cited("S30", "Hot surfaces (die 250 C, air line 270 C, heater sheath up to 430 C, extruder barrel outside the enclosure) cannot be touched in normal use",
        "Biology", "Human physiology and biomechanics", "ISO 13732-1 burn thresholds for bare metal about 70 C at 1 s, 60 C at 10 s, 51 C at "
        "1 min (as summarised by Inzonex)", "Parts above 60 C inside the interlocked enclosure or under insulation; extruder barrel and melt "
        "tube insulated and guarded; hot-surface labels; IR survey at run temperature (V7)", PLAUSIBLE)
c.cited("S31", "The drum, traverse, melt pump and extruder screw cannot trap a hand while running", "Biology", "Human physiology and biomechanics",
        "NFPA 79 and IEC 60204-1 stop functions; ISO 13850 emergency stop; ISO 14119 interlocking with guard locking",
        f"Drum, traverse and pump inside the interlocked enclosure; the extruder screw (outside) is reached only through the hopper, now "
        f"under a fixed perforated lid (F4). Standards cited are requirements, not a demonstration ({REV}: S31 weak)", PLAUSIBLE)
c.cited("S32", "Mains wiring is safe for a technically capable maker to build and inspect", "Engineering and technology", "Standards practice",
        "NFPA 79 (2024), IEC 60204-1:2016+A1:2021, UL 508A practice for the panel; NEC 210.21(B)(2) 12 A on a 15 A receptacle",
        "Panel built to UL 508A practice but not listed; inspection by a qualified electrician before first power (safety stop in BLD)", PLAUSIBLE)
c.cited("S33", "The high-voltage circuit cannot shock an operator in normal use", "Engineering and technology", "Standards practice",
        "Current-limited 1 mA supply; enable through the door interlock; grounded drum and enclosure frame",
        f"Stored energy about {CO['stored_J']:.2f} J (cable and supply, A22); HV off and bar grounded by a grounding stick before the door "
        "unlocks; to verify V4", PLAUSIBLE)
c.cited("S34", "The web's efficiency and pressure drop can be measured by the standard NaCl method at about 0.3 um", "Engineering and technology",
        "Standards practice", "42 CFR 84.181: NaCl, CMD 0.075 um, 85 L/min, 38 C and 85 % RH preconditioning; TSI 8130A: NaCl CMD 0.075 um, "
        "MMD 0.26 um, 10 to 110 L/min, 0 to 2,500 Pa", "Method exists; a test laboratory or a university tester is needed (V5); a benchmark for "
        "the media only, not a respirator test", WITHIN, closed_by="PR-008")
c.cited("S35", "Target pressure drop under 10 mm H2O (98 Pa) per layer at the test flow", "Engineering and technology", "Standards practice",
        "Larsen et al. 2021: under 10 mm H2O (preferably 8) considered comfortable; the NIOSH respirator benchmark allows 25 to 35 mm H2O for a "
        "finished respirator", "Target for the media only (PR-009), measured in V5", PLAUSIBLE)
c.cited("S36", f"The machine (about {R['mass_kg']['PF1']:.0f} kg with steel plates) sits on a standard 2 ft x 8 ft workbench", "Physics",
        "Mechanics and statics", "Model mass; bench rating to assess with the maker space", "Assembled in place on the bench; heavy modules "
        "(extruder 13 kg, panel, plates) lifted by two people", PLAUSIBLE)
env = R["envelope_mm"]
c.claim("S37", f"The whole machine fits a 2 ft x 8 ft (610 x 2,440 mm) bench: depth {env['depth']:.0f} mm measured from the model",
        "Engineering and technology", "Standards practice", "Bounding box of every kit part in the model (not the bench parameter)",
        round(env["depth"]), 610.0, "mm", closed_by=f"model; length {env['length']:.0f} mm, height {env['height']:.0f} mm above the bench; "
        f"duct and cords leave from the top and the back ({REV}: S37 weak, depth was the bench value; recomputed)")
c.cited("S38", "The air jet at 140 m/s is loud; hearing protection may be needed", "Physics", "Acoustics and vibration",
        "Jet noise rises steeply with jet speed; no measured level for this die was found", "Measure dBA at the operator (V7); enclosure "
        "attenuates", PLAUSIBLE)
c.cited("S39", "The machine makes media for testing; no respirator performance follows from it", "Biology", "Epidemiology",
        "NIOSH 42 CFR Part 84, EN 149 and GB 2626 apply to finished respirators (benchmarks only, OPF-CLM-001)",
        "Claims limited to measured media properties", WITHIN, closed_by="OPF-CLM-001")
c.cited("S40", f"Steady energy use is about {W['energy_kWh_m2']:.2f} kWh per m2 at full capture, plus about {WU['kWh_start']:.1f} kWh per start-up",
        "Mathematics", "Units and dimensional analysis", "Steady draw / area rate; warm-up energy (S44); EIA STEO 14.01 cents/kWh commercial, 2026",
        f"USD {W['energy_usd_m2']:.3f} per m2 steady; with capture losses, doffing and warm-up the energy per m2 is two to four times higher "
        f"({REV}: S40 weak)", WITHIN, closed_by=f"{CAL} section 7; OPF-MKT-001")

# ---- claims added after the independent review (missed claims M1 to M27) ---------------------------------------------
c.cited("S41", f"The air side needs {AP['total_kPa'][0]:.0f} to {AP['total_kPa'][1]:.0f} kPa at the pump; a knife parallel to the whole 43 mm nose face "
        f"would need {AP['before_kPa'][0]:.0f} to {AP['before_kPa'][1]:.0f} kPa, beyond the pump", "Physics", "Fluid mechanics",
        f"Laminar slot (Re {AP['Re_slot']:.0f}): dp = 12 mu L v / g2 plus entry 0.5, developing-flow 0.67 and exit 1.0 dynamic heads "
        f"({AP['q_dyn_kPa']:.1f} kPa each); Sutherland viscosity; hot line {AP['line_kPa']:.1f} kPa (Blasius, four bends); heater 3 to 5 kPa and "
        "die passages 2 to 4 kPa assumed (A18)",
        f"Fails as first modelled; fixed by a 5 mm lapped land at 0.3 mm with a 2 mm plenum behind it (F5): slot {AP['slot_kPa']:.1f} kPa. "
        "Total within the 30 kPa pump maximum with little margin; outlet pressure measured (V1)", WITHIN,
        closed_by="OPF-DEC-001 F5 (standing instruction, 2026-10-23); margin to measure")
c.cited("S42", "The air heater cannot overheat if the air flow drops", "Engineering and technology", "Control",
        "With 1,000 W into 2.6 g/s the rise is about 370 K; at 1.8 g/s about 530 K, above the 430 C rating",
        "Pressure switch at the heater inlet removes heater power on low flow; check valve after the pump; the pump runs on 5 min after the "
        "heater stops (F8)", WITHIN, closed_by="OPF-DEC-001 F8; PR-011")
c.cited("S43", "The air temperature holds steady enough for even fibres", "Engineering and technology", "Control",
        "A 0.6 kg stainless heater body against about 2.7 W/K of air flow gives a time constant near 2 min (estimate)",
        "PID on the outlet thermocouple; load-manager trims are slow ramps; to measure (V1)", PLAUSIBLE)
c.cited("S44", f"Warm-up takes about {WU['minutes']:.0f} min for {WU['hot_mass_kg']:.1f} kg of die, knives, pump and melt parts",
        "Physics", "Heat transfer", "E = m cp dT with steel cp 0.5 kJ/kg K (A19) over 230 K; 500 W of die and pump cartridges less half the "
        "steady loss", f"{WU['energy_kJ']:.0f} kJ; heaters are sized by warm-up; plus the extruder's own warm-up", PLAUSIBLE)
c.cited("S45", "The 0.3 mm air gaps stay even at temperature", "Physics", "Strength of materials",
        "Steel expansion about 12 to 17 x 10-6 per K over 230 K grows 48 mm by about 0.13 to 0.19 mm; laminar slot flow goes as gap cubed",
        "Die and knives of the same stainless alloy, heated as one block; gaps set with shims at temperature (F5); flow split checked by "
        "measuring each knife's pressure (V1)", PLAUSIBLE)
c.cited("S46", "The split die seals the 40 grooves without melt leaking between them", "Engineering and technology", "Manufacturing tolerances",
        "Metal-to-metal seal at about 0.2 to 0.7 MPa melt pressure (S14) needs faces flat to a few micrometres",
        "Faces lapped and checked with blue before grooving; four M6 clamp screws; leakage seen as flash on the nose (V2)", PLAUSIBLE)
c.cited("S47", "The melt stays molten from extruder to pump", "Physics", "Heat transfer",
        "Short melt tube between the extruder flange and the pump", "Melt tube band heater, 100 W, on its own zone, insulated (F9; BOM 38)",
        WITHIN, closed_by="OPF-DEC-001 F9")
c.cited("S48", "The gear pump meters a 3.5 to 5 Pa s melt accurately", "Engineering and technology", "Control",
        "Gear pump slip rises as viscosity falls; this melt is at the thin end of a melt pump's range", "Calibrate output against pump speed at "
        "the run pressure (V2)", PLAUSIBLE)
c.cited("S49", "PP fibre fly and condensed wax in the enclosure and duct do not catch fire", "Chemistry", "Physical (kinetics, equilibria, thermochemistry)",
        "PP is combustible; ignition sources are the heater shell (up to 430 C), the die nose and corona sparks; autoignition values on PP safety "
        "data sheets are to confirm", "Heater shell insulated and outside the fibre stream; cleanable duct; fly cleaned each shift; "
        "extinguisher at the bench (BOM 39); over-temperature trips (F10)", PLAUSIBLE)
c.cited("S50", "Static on the charged web and sheets does not harm the operator or the web", "Physics", "Electromagnetism and circuits",
        "Charged webs carry kilovolt surface potentials and attract fly", "Drum grounded through the shaft; sheets handled with gloves on a "
        "grounded table; nuisance shocks to note (V4)", PLAUSIBLE)
c.cited("S51", "Extracting 0.10 m3/s from the room is safe", "Engineering and technology", "Standards practice",
        "0.10 m3/s (212 cfm) needs make-up air; back-draft of combustion appliances to check", "Make-up air path agreed with the maker space; "
        "no open-flue appliances in the room (safety stop)", PLAUSIBLE)
c.cited("S52", "The polycarbonate enclosure stays below its use temperature", "Chemistry", "Materials and polymer chemistry",
        "Polycarbonate softens near 145 to 150 C (glass transition); continuous use about 115 to 125 C (typical); standard grades are not flame "
        "retardant", "Die and heater insulated, panels 150 mm or more from hot parts; flame-retardant grade asked of the supplier; panel "
        "temperature in the IR survey (V7)", PLAUSIBLE)
c.cited("S53", "Hot melt does not splash the operator at start-up and purge", "Biology", "Human physiology and biomechanics",
        "A 3.5 to 5 Pa s melt at 250 C flows almost like oil", "Purge only with the door shut into a catch tray; face shield, gloves and apron "
        "(BOM 39)", WITHIN, closed_by="OPF-BLD-001 safety stops")
c.cited("S54", "Humidity does not stop charging", "Physics", "Electromagnetism and circuits",
        "Humidity changes corona onset, spark-over and charge retention", "Room RH logged with every run; charging tested at two RH levels (V4, V5)", PLAUSIBLE)
c.cited("S55", "Line current stays within the limit with the real power factor", "Engineering and technology", "Power and link budgets",
        "Linear pumps and switch-mode supplies draw current above W / 120", "The load manager measures current, not power (F2)", WITHIN,
        closed_by="OPF-DEC-001 F2; PR-002")

# ---- options PF2 and PF3 -----------------------------------------------------------------------------------------
p2, p3 = R["PF2"], R["PF3"]
x.cited("X1", f"PF2: one {p2['charge_kg'] * 1000:.0f} g pellet charge runs {p2['run_min']:.0f} min, but melting it takes about {p2['melt_min']:.0f} min or more, "
        f"so the die runs at most about {p2['duty']:.0%} of the time", "Physics", "Heat transfer", "Pellet bulk density about 550 kg/m3 (assumed); "
        "conduction time ~ r2 / alpha, alpha = k / (rho cp) with k 0.2 W/m K (NETZSCH 0.17 to 0.25), rho 900, cp 1.8; 10 min to reload",
        f"A pellet bed conducts worse than solid PP and needs latent heat, so the duty is an upper value ({REV}: X1 weak, voids added)", WITHIN)
x.claim("X2", f"PF2: a 30 mm ram at 1 MPa needs {p2['ram_force_N']:.0f} N and {p2['screw_torque_Nm']:.2f} N m at a 5 mm lead ball screw",
        "Physics", "Mechanics and statics", "F = p A; T = F l / (2 pi eta), eta 0.9; NEMA 23 with 10:1 gearbox gives several N m", round(p2["screw_torque_Nm"], 2), 2.0, "N m")
x.cited("X3", "PF2: a pellet charge melts without trapped air", "Physics", "Fluid mechanics", "Pellet beds are about 35 to 40 % voids (assumed)",
        "Air must be pressed out before the die sees melt, or fibres break; needs a vented compaction stroke", PLAUSIBLE)
x.cited("X4", f"PF2: melt held about {p2['melt_min'] + p2['run_min']:.0f} min at 250 C stays processable", "Chemistry", "Materials and polymer chemistry",
        "Borealis: degradation rises with temperature and time", "Ten times the PF1 residence time; MFR drift to measure", PLAUSIBLE)
x.cited("X5", "PF2: power fits 15 A with the same die width", "Engineering and technology", "Power and link budgets",
        "Same air system; the ram barrel heaters replace the extruder heaters", "Same die width limit (S1); no gain in output", WITHIN)
x.cited("X6", f"PF3: a heated 150 mm ring at {p3['rpm']:.0f} rpm ({p3['tip_speed_m_s']:.1f} m/s, {p3['accel_m_s2']:,.0f} m/s2 at the rim) spins PP into fibres of a few micrometres",
        "Physics", "Fluid mechanics",
        "Molina et al. 2022 (PLOS ONE): 15 cm x 4.5 cm aluminium ring at 3,500 rpm, 160 to 200 C, 8 to 24 holes of 0.41 to 0.97 mm, 24 to 26 g in "
        "about 2 min; mean fibre 3.4 to 5.2 um across MFR 12 to 1,550, wide spread (SD 3.0 to 5.2 um)",
        f"PF3 now uses the demonstrated 150 mm ring ({REV}: X6 refuted, a 60 mm cup gave 2.5 times less rim acceleration; fixed)", WITHIN,
        closed_by="Option model changed to the 150 mm ring")
x.claim("X7", f"PF3: power is about {p3['total_W'][0]:.0f} to {p3['total_W'][1]:.0f} W, well inside 1,440 W", "Engineering and technology", "Power and link budgets",
        f"Ring heater 450 to 550 W (melt {p3['melt_W']:.0f} W plus convection from the spinning ring), motor 150 W, controls and corona (estimates)",
        p3["total_W"][1], 1440.0, "W")
x.cited("X8", "PF3: the web filters comparably to melt-blown media", "Physics", "Fluid mechanics",
        "Molina et al. 2022: best 3-ply web 94.5 % at 16.3 cm H2O against a reference respirator's 97.3 % at 3.7 cm H2O (room-air and incense "
        "particles, not NaCl); quality factor -ln(1 - E) / dp",
        f"Quality factor {p3['qf_best']:.4f} against {p3['qf_ref']:.4f} per Pa: 5.5 times worse, not comparable ({REV}: should fail). Finer, more "
        "even fibres (higher speed, a different ring) might close it but are not demonstrated. Option not carried", FIX,
        closed_by="Noted in OPF-OPT-001; option not carried")
x.cited("X9", f"PF3: a burst of the spinning ring is contained", "Physics", "Mechanics and statics",
        f"Kinetic energy 0.5 m r2 w2 for a 0.3 kg ring at 75 mm and {p3['rpm']:.0f} rpm: {p3['ring_KE_J']:.0f} J",
        "Containment by the steel cage rings and a 6 mm polycarbonate enclosure is to assess; no containment criterion was found to cite", PLAUSIBLE)
x.cited("X10", "PF3: the cage gives an even web", "Engineering and technology", "Control", "Radial throw onto a 500 mm cage; Molina used a drum at -5 kV",
        "Deposit is densest at the ring height; a rotating or traversing collector needed; uniformity to measure", PLAUSIBLE)
x.cited("X11", "PF3: the pellet or flake charge is batch", "Engineering and technology", "Control", "Molina et al. 2022: about 25 g per 2 min run",
        "Continuous feed would need a melt feeder into the spinning ring (a different machine)", WITHIN)
x.cited("X12", f"PF1 on a second 20 A circuit for the air heater: slot up to about {R['max_slot_mm']['15 A plus a 20 A circuit for the air heater']:.0f} mm",
        "Engineering and technology", "Power and link budgets", "Air heater at 95 % of 1,920 W on its own circuit; rest on 15 A",
        "Needs about 1,800 W of heater (two heaters: the largest 120 V AHPF is 1,200 W), about 2.2 times the air (two pumps) and two supply "
        f"cords, which raises NFPA 79 disconnect questions ({REV}: X12 weak, hardware not scaled)", PLAUSIBLE)


def table(rows):
    out = ["| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |",
           "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in sorted(rows, key=lambda r: int(r["id"][1:])):
        out.append(f"| {r['id']} | {r['claim']} | {r['field']} | {r['branch']} | {r['law']} | {r['check']} | {r['verdict']} | {r['closed_by'] or 'Open'} |")
    return "\n".join(out)


def inject(doc, tag, text):
    s = doc.read_text(encoding="utf-8")
    a, b = f"<!-- {tag} -->", f"<!-- /{tag} -->"
    if a in s and b in s:
        i, j = s.index(a) + len(a), s.index(b)
        doc.write_text(s[:i] + "\n" + text + "\n" + s[j:], encoding="utf-8")


if __name__ == "__main__":
    state = c.write()
    x.write()
    doc = ROOT / "docs/01b-stem-check.md"
    if doc.exists():
        inject(doc, "STM_TABLE", table(c.rows))
        inject(doc, "STM_OPTIONS", table(x.rows))
        print("refreshed tables in docs/01b-stem-check.md")
    print("PF1 state:", state)
