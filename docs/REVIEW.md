# Open PolyForge review note

**Media completed, 2026-11-12.** The Blender Cycles renders queued by this session were rendered on Amish's Mac: `media/options.png`, `media/render-hero.png`, `render-studio.png`, `render-cutaway.png` and `render-exploded.png` were composed and captioned, `media/card.png` and `media/social-preview.png` were made with `cards.py`, and `image_qc.py` passes. `render.py --check` passes. `release_gate.py` fails only on `stem_check: open` (Plausible rows wait on TRL 4 evidence; design decisions await Amish). Amish approved the repo as public on 2026-11-12.

## Session 2026-11-12: P0 to P3 (TRL 3) under kit 1.9.1-he

### What was done

- STEM check first ([docs/01b-stem-check.md](01b-stem-check.md), `docs/04-calcs/stem_check.py`, `stem_results.csv`, `stem_results_options.csv`) with the machine checks of STANDARDS 25.6a and the 120 V power budget as the controlling check; then an independent review by a separate agent (its own `claude -p` process, given only the results tables, the two scripts, their output, the design parameters and the source list).
- Three concept options at D3 in `cad/src/model.py` (PF1 315 parts, PF2 271, PF3 192; `cad/fidelity.json` passes D3, no interference, no bare primitives); STEP per part for PF1 in `cad/step/PF1/` and an assembly STEP per option (44 MB in all, largest file 14 MB).
- Pipeline documents: PRB, STM, PRC, OPT, URS, PRS, RTM (generated, 0 gaps), CAL with `sizing.py`, BLD with pictures, DEC with DDR 0001 to 0003, REG, FEA, RSK (PHA and design FMEA), MKT, PLN (Helpful Engineering process content), CLM, VER, FTO.
- Drawings OPF-DWG-001 (GA) and 002 (half section of the forming zone); making sketches OPF-DWG-101 to 110; STL in `cad/stl/`; concept media in `media/` (hero, cutaway, exploded, flow, viewer and model.glb, blueprint).
- `cad/src/product_model.py`; render queue in `/home/claude/he5/renderq/open-polyforge` (option scenes and `open-polyforge__options_jobs.json`) and `/home/claude/he5/renderq/open-polyforge/views` (`open-polyforge__jobs.json`, four views).
- `project.yaml` filled to P3, TRL 3, `stem_check: open`, `design_state: constructable`, `budget_usd: 10000` (proposed).
- No team concept renders exist for this project in `/home/claude/he5/img/`; the design follows the text proposal only.

### Key results (OPF-CAL-001)

- Air sets the power: 13.8 W per mm of air slot at 270 C and 140 m/s. A 150 mm die: about 3,061 W (25.5 A), fails 15 A and 20 A. Carried die: 40 grooves, two 0.3 x 48 mm slots (fix F1).
- Steady draw 1,331 W (11.1 A) nominal; 1,643 W (13.7 A) pessimistic, capped at 12 A by the load manager (F2), which would cool the air about 64 K (then throughput is lowered instead). Nameplate sum 2,480 W (20.7 A).
- Polymer 4.0 g/min; melt heat 34 to 48 W; air 2.62 g/s (122 NL/min), heater 663 W (66 % of 1,000 W); air-to-polymer ratio 39.
- Air side 23 to 27 kPa at the pump after the 5 mm knife land (F5); 43 to 47 kPa without it. Pump maximum 30 kPa.
- Groove pressure 0.17 to 0.73 MPa; melt pump 34 rpm; warm-up about 32 min.
- Web: 9.6 m2/h laid at full capture, 6.7 to 8.6 deposited, 1.9 to 2.5 m2/h of 140 mm sheets with doffing (F7).
- Corona -25 kV at 40 mm, 5 W; ozone 0.35 ppm in the exhaust duct at an assumed 50 g/kWh; exhaust 0.10 m3/s to outdoors.
- Footprint 2,288 x 600 mm on the bench, 746 mm high; about 148 kg.
- Value-engineering target USD 10,000 (proposed); estimated cost of the constructable design USD 14,075.15 (USD 4,075.15 over). Largest lines: extruder USD 2,945, melt pump USD 2,500 (estimate), HV supply USD 1,800, die USD 900, heater USD 849.89.

### Requirements not met or at risk

- PR-001 steady current 12 A: at risk (pessimistic 13.7 A before the cap; nameplate 20.7 A, D2).
- PR-007 output: at risk (1.9 to 2.5 m2/h of sheets against 2).
- PR-025 air supply: at risk (23 to 27 kPa against a 30 kPa pump maximum).
- PR-020 documentation: at risk (operating manual is TRL 4 work).
- PR-022 cost: over the value-engineering target by USD 4,075.15.
- PR-004, PR-005, PR-009, PR-015, PR-024: to verify at TRL 4.

### STEM check

PF1: 20 within, 35 plausible (need TRL 4 evidence), no fails. Options: 6 within, 5 plausible, 1 fails with a fix noted (X8, PF3 web quality, not carried). Fixes under the standing instruction of 2026-10-23: F1 die width, F2 load manager, F3 corona interlocks, F4 extruder hood and hopper lid, F5 knife land and plenum, F6 groove size, F7 doffing cycle, F8 heater low-flow protection, F9 heated melt tube, F10 fire controls.

Independent review (2026-11-12): of 28 rows marked within known science, **14 held, 13 were weak, 1 was refuted** (X6, the PF3 cup was 60 mm against the demonstrated 150 mm ring); of the plausible rows, one should fail (X8) and one was wrongly quantified (S3); **27 missed claims**. I verified each with my own numbers: the laminar air knife pressure (confirmed, F5), the nameplate rating (confirmed, S2 now plausible, D2), the square groove area (confirmed, F6), the doffing and capture losses (confirmed, F7), the heater length (254 mm, model corrected), the PF3 ring (confirmed from Molina et al., model changed), the X8 quality factor (confirmed). The reviewer's 155 W reading of the pump at 60 Hz could not be confirmed from the sheet's text, so the conservative 250 W is carried. Missed claims were added as S41 to S55 or folded into existing rows; all recorded in OPF-STM-001.

### Decisions proposed and awaiting Amish (OPF-DEC-001)

- D1 concept: PF3 187, PF1 171, PF2 164 of 255; PF3 and PF1 within 10 %, both to Amish without a pick. PF1 carried in the drawings, BOM and build plan only so a constructable design exists. Choosing PF3 would change the working principle and pitch (centrifugal spinning, not melt blowing).
- D2 electrical supply and marking (one 15 A circuit with an accepted current limit; a 20 A circuit; a second circuit for the air heater; hardwired).
- D3 build a PF3-style ring rig first for resin, charging and NaCl testing.
- D4 batch sheets now, continuous take-off later. D5 value-engineering target USD 10,000. D6 extruder source (EX2 discontinued). D7 corona on the drum or off-line. D8 on-machine wording.

### Build plan findings (design for construction, OPF-DDR-002)

Split grooved die instead of drilled 5-axis work; knife flanges screwed to the die halves; insulator pads under hot parts; rivet-nut plates on a welded frame; the drum motor moved beside the drum on a timing belt because the shaft-end motor would hit the back panel at full traverse; interlock switch moved inside and the enclosure narrowed to keep the 600 mm depth; end panels notched round the base rails.

### Safety concerns

Electrical acceptance of a 2,480 W nameplate machine on a 15 A receptacle (D2); burns from the die, heater and melt splash at purge; high voltage and spark-over (fixed negative, current-limited, guard-locked); ozone (0.35 ppm in the duct at an assumed yield, so the corona runs only with extraction proven and a monitor at the operator); PP fumes and aldehydes; fibre fly fire; air heater overheating on low flow (pressure switch); misuse of test media in masks (release limitation on every document and the on-machine label). Top design FMEA items: uneven groove flow (RPN 180) and unequal knife gaps (150).

### Appearance model

`product_model.py` uses the PF1 parts as modelled plus a standing 1.75 m mannequin on the operator side and a half-cut copy of the forming zone; an "open" group omits the door so the forming zone shows in the hero. No appearance deviations from `model.py`. The bench is a simplified context model. Proposed, awaiting Amish: none.

### Checks that do not pass, and kit notes

- `python .kit/render.py --check` fails only on `media/options.png`, which needs the Blender renders of the exported option scenes; the storefront warning lists `media/render-hero.png`, `media/card.png` and `media/social-preview.png`, also Blender-dependent. After the Mac renders: `python .kit/options.py --compose=<dir>`, caption the views with `.kit/photo_caption.py`, then `python .kit/cards.py .` and `python .kit/image_qc.py`.
- The concept renderer ignores part transparency, so the hero hides the door to show the inside.
- The split die's internal air passages from the inlet to the two knives are noted on the drawings but not modelled.
- Several BOM prices are estimates, not quotes (marked in the BOM); the melt pump price is the largest uncertainty.

### Recommended next step

Amish decides D1 and D2. The design is ready for a TRL 4 laboratory build on paper (one machine, V1 to V8 of OPF-VER-001) once the portfolio cap allows; the cheapest first step is D3, the ring rig, to prove the resin, charging and test chain.
