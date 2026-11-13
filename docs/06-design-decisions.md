---
doc_id: OPF-DEC-001
title: Open PolyForge design decisions register
project: Open PolyForge
doc_type: Design decisions register
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First register; D1 to D8 proposed, awaiting Amish; F1 to F10 made under the standing instruction of 2026-10-23
---

# Open PolyForge design decisions register

Every design decision for this repo, in one place. Nothing below is recorded as Amish's decision unless he made it: the open decisions are **proposed, awaiting Amish**. The STEM fixes F1 to F10 were made under his standing instruction of 2026-10-23 (STANDARDS section 20) and he can reverse them.

## Open decisions (proposed, awaiting Amish)

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| D1 | Concept choice | PF1 screw extruder, melt pump and slot die (171 of 255); PF2 ram extruder (164); PF3 centrifugal melt spinning (187) | PF3 and PF1 are within 10 %, so both come to Amish without a pick. Engineering view: PF1 meets the proposal as written and has the clearer route to filtration-grade web; PF3 is cheaper and lighter on power but its published web has a 5.5 times lower quality factor and it changes the working principle and pitch. PF1 is carried in the drawings, BOM and build plan so a constructable design exists | Everything | OPF-OPT-001, OPF-DDR-001 |
| D2 | Electrical supply and marking | (a) one 15 A circuit with the load manager, nameplate marked at the current-limited value, accepted by an electrician or the authority having jurisdiction; (b) a dedicated 20 A circuit (16 A cord limit, about 89 mm of slot); (c) 15 A plus a second 20 A circuit for the air heater (about 132 mm, two heaters, two pumps, a second disconnect); (d) hardwired supply | (a) for the prototype if it can be accepted, else (b); (c) only for a wider die later | Panel, cord, die width | OPF-CAL-001 section 5; OPF-STM-001 S1 to S3, X12 |
| D3 | Runner-up's best idea | (a) none; (b) build a PF3-style ring rig (about USD 1,000) first as a low-power bench for resin, corona charging and the NaCl test chain while the PF1 die is drawn and machined | (b) | Plan, BOM addition later | OPF-OPT-001 |
| D4 | Production mode | (a) batch sheets on the drum with doffing (as modelled, 1.9 to 2.5 m2/h); (b) a later continuous take-off with a wider die | (a) for TRL 4 | Collector, output targets (PR-007) | OPF-STM-001 S20 |
| D5 | Value-engineering target | (a) USD 10,000 per machine (proposed here; none in the proposal); (b) another figure | (a), as a hypothetical control target, not a limit | Cost reporting | OPF-MKT-001 |
| D6 | Extruder source | (a) Filabot EX2 (listed as discontinued); (b) Filabot EX3 (1,000 W total rating, raises the nameplate); (c) another 5/8 in desktop extruder; (d) PF2 ram if feeding fails | (c) or (a) used, chosen by the nameplate (D2) and a feed trial | Extruder plate, flange | OPF-STM-001 S16, S17 |
| D7 | Corona position | (a) on the drum (as modelled); (b) an off-line charging table (as PF3) so the door need not open with HV near | (a), with (b) as the fallback if spark-over or ozone tests fail | Corona bar, enclosure | OPF-STM-001 S23, S27 |
| D8 | On-product and on-machine wording | As drafted in OPF-CLM-001 | Adopt | Labels | OPF-CLM-001 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| C1 | Melt pump speed range and slip at 3.5 to 5 Pa s, and price | Metering (S15, S48); the largest cost line | BOM 4 |
| C2 | HP-200 flow at 23 to 30 kPa on 60 Hz, and its power | Air flow margin (S7, S41) | BOM 25 |
| C3 | Air heater pressure drop at 122 NL/min | Air budget (A18) | BOM 26 |
| C4 | Resin small-lot supply and data sheet window (melt temperature, residence time) | S10, S18 | PR-016 |
| C5 | Flame-retardant polycarbonate grade and its use temperature | S52 | BOM 22 |
| C6 | Ozone yield of the needle bar (or measure it) | S27 | BOM 19 |
| C7 | Freedom to operate against US 11,447,893 B2 (and, for PF3, US 8,231,378 B2 and US 8,828,294 B2) by a patent attorney | Desk reading only | OPF-FTO-001 |
| C8 | Bench load rating at about 150 kg | S36 | Maker space |

## Value engineering

Value-engineering target: USD 10,000 per machine (proposed, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 14,075.15, USD 4,075.15 over the target. Main cost drivers: the desktop extruder (USD 2,945), the melt gear pump (USD 2,500, estimate), the HV supply (USD 1,800), the die halves (USD 900) and the air heater (USD 849.89); together 64 %. Savings worth trying: a used or second-source melt pump; a lower-cost, current-limited HV module verified for 1 mA limiting; a maker-built extruder from a standard 5/8 in screw and barrel kit; the PF3 ring rig (D3) to settle charging and testing before the precision die is cut.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-11-12 | Repo shape (one public repo), licences as Helpful Water (CERN-OHL-P-2.0, Apache-2.0, CC-BY-4.0), no archive, the credits list | Amish | `project.yaml`, STANDARDS 25 |
| 2026-11-12 | F1: die width set by the power budget (40 capillaries, two 0.3 x 48 mm slots, 0.10 g/hole/min) instead of a laboratory-width die | Under Amish's standing instruction of 2026-10-23 | OPF-DDR-003 |
| 2026-11-12 | F2: load manager measuring line current, capping heater duty at 12 A, sequenced warm-up | Under the standing instruction | OPF-DDR-003 |
| 2026-11-12 | F3: HV enabled only with the door guard-locked, extraction proven and the drum turning; fixed negative, current-limited supply; ozone monitor | Under the standing instruction | OPF-DDR-003 |
| 2026-11-12 | F4: extruder branch fume hood and fixed perforated hopper lid | Under the standing instruction | OPF-DDR-003 |
| 2026-11-12 | F5: air knives with a 5 mm land at 0.3 mm and a 2 mm plenum; gaps set at temperature; 200 NL/min, 30 kPa pump class | Under the standing instruction | OPF-DDR-003 |
| 2026-11-12 | F6: grooves 0.27 mm square (0.30 mm round equivalent) | Under the standing instruction | OPF-DDR-003 |
| 2026-11-12 | F7: doffing cycle (melt pump stopped, die hot) and output reported as batch | Under the standing instruction | OPF-DDR-003 |
| 2026-11-12 | F8: heater low-flow pressure switch, check valve, pump run-on | Under the standing instruction | OPF-DDR-003 |
| 2026-11-12 | F9: heated melt tube (100 W band) | Under the standing instruction | OPF-DDR-003 |
| 2026-11-12 | F10: fire controls (insulated heater shell, cleanable duct, fly cleaning, extinguisher) | Under the standing instruction | OPF-DDR-003 |
| 2026-11-12 | Design for construction of PF1 (split grooved die, rivet-nut plates, insulator pads, belt-driven drum motor, interior interlock switch, narrowed enclosure) | Under STANDARDS section 18 (Amish, 2026-09-30) | OPF-DDR-002 |

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
