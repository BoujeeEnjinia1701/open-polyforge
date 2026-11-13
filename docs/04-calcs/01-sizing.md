---
doc_id: OPF-CAL-001
title: Open PolyForge sizing and power budget
project: Open PolyForge
doc_type: Calculation note
version: "0.2"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First sizing note for PF1 with the 120 V power budget, the die width fix (OPF-DEC-001 F1) and first-order numbers for PF2 and PF3
  - version: "0.2"
    date: 2026-11-12
    author: Amish Chadha
    change: After the independent review, air-side pressure budget and knife land (F5), nameplate rating, warm-up, capture and doffing, square grooves, HP-200 pump, melt tube heater, PF3 on the 150 mm ring
---

# Open PolyForge sizing and power budget

Result: on one 120 V, 15 A circuit (1,440 W continuous) the machine can heat the process air for an air slot about 60 mm long, not a laboratory-width die. At the same slot design a 150 mm die would draw about **3,061 W (25.5 A)**, of which the air heater alone is 2,071 W; that fails both a 15 A and a 20 A circuit. The carried design (PF1) therefore uses **40 capillaries and two 0.3 x 48 mm air slots** (fix F1): it draws about **1,331 W (11.1 A)** steady at the nominal assumptions and about 1,643 W (13.7 A) if every assumption takes its upper value, which a load manager trims to 12 A (fix F2). Its nameplate sum, 2,480 W (20.7 A), is above a 15 A cord limit, so its marking is a decision for Amish with an electrician (OPF-DEC-001 D2). It lays about **4 g/min of polymer, 9.6 m2/h of 25 g/m2 web** at full capture, 6.7 to 8.6 m2/h deposited, and **1.9 to 2.5 m2/h of 140 mm wide sheets** once doffing is counted. The air, not the polymer, sets the power: melting 4 g/min takes 34 to 48 W, heating 2.62 g/s of air to 270 C takes 663 W. Script: `docs/04-calcs/sizing.py`; results: `sizing_results.json`. Estimates, not test results. CONCEPT, NOT FOR FABRICATION.

## 1. Assumptions

| # | Assumption | Value | Basis |
| --- | --- | --- | --- |
| A1 | PP melt density near 250 C | 730 kg/m3 | Assumed, to confirm with the resin supplier |
| A2 | Specific heat of the melt (upper value) | 2.7 kJ/kg K | Assumed; NETZSCH gives 1.8 kJ/kg K for iPP as a single value |
| A3 | Crystallinity of the pellets | 0.45 to 0.50 | Assumed; NETZSCH measured 94 to 112 J/g melting against 207 J/g for 100 % |
| A4 | Air temperature rise through the diaphragm pump | 15 K | Assumed (compression heat), to measure |
| A5 | Air heater body and fitting efficiency | 0.95 (0.85 pessimistic) | Assumed |
| A6 | Insulation | 25 mm mineral wool, k = 0.05 W/m K | Assumed at a 150 C mean |
| A7 | Exposed die nose | 36 cm2 at h = 45 W/m2 K | Assumed (30 convection, 15 radiation) |
| A8 | Extruder barrel loss at a quarter of rated output | 120 W (200 W) | Assumed; the EX2-class module is rated 500 W in all |
| A9 | Extruder drive at low output | 60 W (100 W) | Assumed |
| A10 | Three steppers | 45 W (60 W) | Assumed |
| A11 | Corona supply input | 15 W (30 W) | Assumed: 5 W output, about a third efficient |
| A12 | Controls, PID, sensors, power supply | 30 W (40 W) | Assumed |
| A13 | Reference die width | 150 mm (6 in) | A common laboratory die width (assumed for the reference case) |
| A14 | Warm-up heater ratings | Barrel 400 W, die 2 x 150 W, pump 2 x 100 W | Assumed for the bought module; cartridge ratings from the BOM |
| A17 | Melt tube heater and barrel nose loss | 25 W (40 W) | Assumed |
| A18 | Heater and die air passage pressure drops | 3 to 5 kPa and 2 to 4 kPa | Assumed, to measure |
| A19 | Specific heat of the steel parts | 0.5 kJ/kg K | Assumed |
| A20 | Lay-down efficiency on the drum | 70 to 90 % | Assumed (fly loss 10 to 30 %) |
| A21 | Doff time per sheet | 1.5 to 2 min | Assumed |
| A22 | HV capacitance | 2 m of cable at about 100 pF/m plus 1 nF | Assumed |
| A23 | Pellet bulk density (PF2 charge) | 550 kg/m3 | Assumed |
| A15 | Melt density for the MFR conversion | 739 kg/m3 at 230 C | Assumed |
| A16 | Shear thinning between the MFR and capillary shear rates | up to 3 times the MFR apparent viscosity | Assumed |

Values in brackets are the pessimistic case.

## 2. Polymer stream

40 capillaries x 0.10 g/hole/min = **4.0 g/min (0.24 kg/h)**, 5.5 cm3/min of melt. Enthalpy from 20 to 250 C: h = cp dT + Xc dHf = 1.8 x 230 + 0.45 x 207 = 507 kJ/kg, up to 2.7 x 230 + 0.50 x 207 = 725 kJ/kg; **34 to 48 W**. The desktop extruder rated just over 0.91 kg/h on filament resins runs at about a quarter of that (PR-007). Resin: ExxonMobil Exceed Flow PP6936G2, MFR 1,550 g/10 min at 230 C and 2.16 kg (PR-016).

## 3. Process air

Two slots, each 0.30 x 48 mm: 28.8 mm2. At 270 C and 1 atm the air density is 0.650 kg/m3 (ideal gas). At 140 m/s, within the 130 to 160 m/s measured near a 260 C die (Wu et al. 2024): **2.62 g/s, 122 NL/min** (the pump's normal-litre basis), Mach 0.30. Air-to-polymer mass ratio **39**. The slot is laminar (Re 1,933). Its loss is 12 mu L v / g2 over the land plus entry (0.5), developing-flow (0.67) and exit (1.0) dynamic heads of 6.4 kPa each: with a knife parallel to the whole 43 mm nose face that is 36.5 kPa and the air side 43 to 47 kPa, beyond a diaphragm pump. With a 5 mm land and a 2 mm plenum (fix F5) the slot needs 16.5 kPa; with the hot line (1.5 kPa at 43 m/s), the cold line (0.5 kPa) and assumed heater and die passages (A18) the pump must deliver **23 to 27 kPa**, inside the 30 kPa maximum of a 200 NL/min, 250 W linear pump (Hiblow HP-200) with little margin. A bleed valve trims excess flow; a pressure switch cuts the heater on low flow (F8; PR-025). Heater: Q = m cp dT / eta = 2.62 g/s x 1.02 kJ/kg K x 235 K / 0.95 = **663 W**, 66 % of a 1,000 W, 120 V, 430 C inline heater (Omega AHPF-101). cp is the mean of 1.005 kJ/kg K at 300 K and 1.040 at 550 K (Urieli air tables). The air needs **13.8 W per mm of slot**: this is the number that sets the die width (PR-006).

## 4. Heat losses

Die halves and knives, 0.0435 m2 under 25 mm of insulation: 19 W. Exposed nose: 37 W. Melt pump with plates: 15 W. Hot air line, 0.35 m of insulated 1/2 in tube: 17 W. The die and pump cartridges (2 x 150 W and 2 x 100 W) are sized by warm-up, not by steady loss.

## 5. Power budget against the supply

Table 1. Steady electrical demand, W (NEC 2020: continuous load at 125 %; 12 A cord-and-plug limit on a 15 A receptacle).

| Load | Nominal | Pessimistic |
| --- | --- | --- |
| Process air heater | 663 | 741 |
| Hot air line loss | 17 | 26 |
| Extruder barrel heaters (loss plus melt) | 154 | 248 |
| Extruder drive motor | 60 | 100 |
| Melt pump and die heaters | 72 | 108 |
| Air pump | 250 | 250 |
| Melt tube heater and barrel nose | 25 | 40 |
| Steppers (pump, drum, traverse) | 45 | 60 |
| Corona supply | 15 | 30 |
| Controls | 30 | 40 |
| **Total** | **1,331 (11.1 A)** | **1,643 (13.7 A)** |
| Against 1,440 W (15 A) | 109 under | 203 over |

The nominal case meets PR-001; the pessimistic case does not, so the load manager (PR-002, fix F2) measures line current and caps the summed heater duty at 12 A. At the pessimistic case that would cool the air by about 64 K, to about 206 C, below the usual 230 C floor; the throughput set point is then lowered instead until the losses are measured (V1). The nameplate sum of every load at its rating is 2,480 W (20.7 A): cord-and-plug equipment is usually judged on its marked rating, so whether a current-limited machine may be marked at 12 A is to assess with an electrician or the authority having jurisdiction (OPF-DEC-001 D2). Warm-up is sequenced: stage 1 brings barrel, pump and die up with the air off (about 975 W); stage 2 starts the air pump and heater under the same 12 A cap. The die, knives, pump and melt parts (7.8 kg in the model) take about 900 kJ to heat, about 32 min on the 500 W of cartridges, about 0.75 kWh per start with the extruder. The exhaust fan runs on its own building circuit.

Table 2. Die width the supply allows (nominal, same slot design).

| Supply | Air slot length | Note |
| --- | --- | --- |
| One 15 A circuit, 1,440 W | about 56 mm | Carried design 48 mm; the pessimistic case already needs the load manager |
| One 20 A circuit, 1,920 W | about 89 mm | Needs a 20 A receptacle (16 A cord limit) and more air |
| 15 A plus a 20 A circuit for the air heater | about 132 mm | Needs two heaters and two pumps; proposed to Amish (OPF-DEC-001 D2) |
| Reference: 150 mm die on one circuit | 3,061 W, 25.5 A (three pumps) | Fails (STM S1); fixed by F1 |

Recuperation was weighed: the process air leaves with the fibres into the enclosure and cannot be recovered; drawing the pump intake across the warm extruder body would gain tens of watts at most, not worth the ducting at TRL 3.

## 6. Die hydraulics and melt pump

The MFR test is itself a capillary viscometer: 2.16 kg on a 9.55 mm barrel is 296 kPa through a 2.095 x 8.000 mm die; 1,550 g/10 min gives an apparent viscosity of **5.0 Pa s** at about 3,900 1/s. At 250 C the viscosity is about 0.69 times that (Arrhenius with an assumed 40 kJ/mol), about 3.5 Pa s. A 0.30 mm square groove would pass 43 % more than a 0.30 mm round hole (square duct Q = 0.0351 a4 dp / (mu L)), so the grooves are 0.27 mm square, a 0.30 mm round equivalent (fix F6). Each 4 mm groove at 0.10 g/min then needs **0.17 to 0.73 MPa** (from the 250 C value up to three times the 230 C value for shear thinning; no Bagley correction), far inside the pump's 27.6 MPa differential. At 3.5 to 5 Pa s the melt is at the thin end for a gear pump, so slip is calibrated (V2). The low pressure is the risk: the split between holes depends on the manifold and the 0.3 mm pre-land, so basis-weight profile is measured (V2, PR-005). Melt pump: 5.5 cm3/min / 0.16 cm3/rev = **34 rpm** (PR-003).

## 7. Web output and collector

Area rate = 4.0 g/min / 25 g/m2 = 0.16 m2/min = **9.6 m2/h** (PR-007). The spray is about 60 mm wide at the drum; a +-40 mm traverse gives a **140 mm** web (PR-008). A 200 mm drum carries a 0.088 m2 sheet, laid in about 0.55 min at 25 g/m2; the drum turns at 30 rpm (18.8 m/min surface) so the sheet builds from many thin passes (PR-005). With 70 to 90 % capture (A20) the deposit is 6.7 to 8.6 m2/h, and with a 1.5 to 2 min doff per sheet (A21, fix F7: the melt pump stops, the die stays hot, the sheet is cut off) the output is **1.9 to 2.5 m2/h** of sheets (PR-007). Steady energy: 1.33 kW / 9.6 m2/h = **0.14 kWh/m2**, USD 0.019 per m2 at the 2026 US commercial average of 14.01 cents/kWh (EIA STEO); with capture, doffing and warm-up two to four times that. 

## 8. Corona and extraction

-25 kV across 40 mm is 0.63 kV/mm on average, a fifth of the roughly 3 kV/mm breakdown of air in a uniform field; the needle tips concentrate the field to start the corona. Negative point-to-plane gaps spark over at higher voltage than positive, so the supply is fixed negative. At 200 uA the output is 5 W, inside the 30 kV, 1 mA supply (PR-010); stored energy of cable and supply about 0.38 J (A22). No ozone yield for a DC needle corona of this geometry was found, so a bounding 50 g/kWh is assumed: 0.25 g/h, 0.35 ppm in the 0.10 m3/s exhaust duct, which is ducted outdoors. HV is enabled only with the door shut and the exhaust airflow proven, and an ozone monitor sits at the operator (PR-014, PR-015). The exhaust is 46 times the process air volume. Over-temperature cut-outs at 300 C on every zone, below the 450 to 470 C decomposition of PP (PR-011). Guarding and stops: PR-012, PR-013, PR-024. Purge and cleaning: PR-023. Controls: PR-019. Precision parts: PR-018. Documentation: PR-020. Claims: PR-021. Fibre target: PR-004. Media benchmark: PR-009.

## 9. Options PF2 and PF3

- **PF2 ram extruder.** A 30 mm bore with a 200 mm stroke holds about 78 g of pellets (bulk 550 kg/m3, A23): 19 min at 4 g/min. Melting the charge by conduction takes about 30 min or more (r2 / alpha with alpha = 1.2e-7 m2/s), so with a 10 min reload the die runs at most about 32 % of the time. At 1 MPa the ram needs 707 N, 0.62 N m at a 5 mm lead ball screw. Power as PF1 less about 80 W.
- **PF3 centrifugal melt spinning.** Molina et al. (2022) spun 24 to 26 g in about 2 min with a 15 cm aluminium ring at 3,500 rpm and 160 to 200 C through 0.6 mm holes, with mean fibres 3.4 to 5.2 um. PF3 uses the same ring: 27.5 m/s at the rim, 10,075 m/s2. About 690 to 790 W (ring heater 450 to 550 W with convection from the spinning ring, motor 150 W, controls, corona), about half the circuit. A 0.3 kg ring stores about 113 J. Their best web had a quality factor 5.5 times below the reference respirator media (STM X8).

## 10. Mass and cost

Model mass: PF1 148 kg (steel plates and frame dominate), PF2 150 kg, PF3 96 kg. Envelope of PF1 from the model: 2,288 x 600 mm on the bench, 746 mm above it (PR-017). Value-engineering target USD 10,000 (proposed, awaiting Amish). Estimated cost of the constructable design: USD 14,075.15, USD 4,075.15 over the target (PR-022; bom/bom.csv).

## Sources (checked 2026-11-12)

- NEC 2020 210.19(A), 210.20(A), Table 210.21(B)(2): [open-exam-prep guide](https://open-exam-prep.com/study-guides/ak-electrician/ch06/ch06-sec01); continuous load 3 h or more, 1,440 W on 15 A: [Industrial Monitor Direct](https://industrialmonitordirect.com/blogs/knowledgebase/nec-15a-circuit-wattage-limits-continuous-vs-non-continuous-load-calculations).
- NETZSCH polymer database, isotactic PP. [Page](https://polymers.netzsch.com/Materials/Details/11).
- Urieli, I. Air Cp and Cv tables, Ohio University. [Page](https://people.ohio.edu/urieli/thermo/property_tables/air/air_Cp_Cv.html).
- ExxonMobil PP filtration nonwovens fact sheet (Exceed Flow PP6936G2, MFR 1,550). [PDF](https://www.exxonmobilchemical.com/-/media/media-assets/media-library-assets/apr/factsheet-pp-filtration-nonwovens-factsheet-en.pdf).
- Schmidt, J., S. Shenvi Usgaonkar, S. Kumar, K. Lozano and C. J. Ellison. 2022. "Advances in Melt Blowing Process Simulations." *Industrial and Engineering Chemistry Research* 61: 65 to 85. [PDF](https://par.nsf.gov/servlets/purl/10420470).
- Wu, W., W. Han, Y. Sun, H. Yi and X. Wang. 2024. "Experimental Study of the Airflow Field and Fiber Motion in the Melt-Blowing Process." *Polymers* 16 (4): 469. [Page](https://www.mdpi.com/2073-4360/16/4/469).
- Omega AHPF inline heater data sheet. [PDF](https://assets.dwyeromega.com/pdf/process-heaters-and-coolers/duct-heaters/AHPF_HEATER.pdf). Hiblow HP-150 and HP-200 specifications (flow in normal litres per minute). [PDF](https://cdn.shopify.com/s/files/1/0259/5028/9980/files/HP-150-200-Specs.pdf).
- CIRCOR Zenith PEP-II gear pumps. [PDF](https://www.circor.com/sites/pumps/files/2023-10/zenith_pep_ii_gear_pumps.pdf). Filabot EX2. [Page](https://www.filabot.com/products/filabot-original-ex2).
- Sisco melt flow rate tester specifications (die 2.095 x 8.000 mm, barrel 9.550 mm). [PDF](https://www.sisco.com/images/uploaded/sisco-melt-flow-rate-tester-technical-specifications.pdf).
- OSHA ozone chemical data. [Page](https://www.osha.gov/chemicaldata/9). CCOHS, Industrial ventilation: hoods. [Page](https://www.ccohs.ca/oshanswers/prevention/ventilation/hoods.html).
- EIA Short-Term Energy Outlook, Table 7c. [PDF](https://www.eia.gov/outlooks/steo/tables/pdf/7ctab.pdf).
- Molina, A., et al. 2022. "Low Cost Centrifugal Melt Spinning for Distributed Manufacturing of Non-Woven Media." *PLOS ONE* 17 (4): e0264933. [PDF](https://rcastoragev2.blob.core.windows.net/f7a4c484a3a6a85ae30da4d11485fa82/PMC9017944.pdf).

> **Safety:** These numbers describe a machine with mains wiring, heaters up to 430 C, molten polymer at 250 C, high voltage to 30 kV and moving parts. Nothing here is a build record; see OPF-BLD-001 for the safety stops and OPF-CLM-001 for the release limitation: no media from a prototype machine is used in a mask or respirator until its efficiency, pressure drop and charge decay are measured by a qualified laboratory and the finished product is certified to its own standard.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
