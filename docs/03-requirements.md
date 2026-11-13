---
doc_id: OPF-PRS-001
title: Open PolyForge product requirements and specifications
project: Open PolyForge
doc_type: Product requirements
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First product requirements for the carried option PF1, traced to OPF-URS-001, with targets, tolerances and planned verification
---

# Open PolyForge product requirements and specifications

Requirements for the carried option PF1 (screw extruder, melt pump and slot die); the choice between PF1, PF2 and PF3 is awaiting Amish (OPF-DEC-001 D1). "Met on paper" means OPF-CAL-001 or a cited source shows it; nothing is tested at TRL 3. Verification families are in OPF-VER-001.

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-003 | Deployment and assembly | Steady power | Steady line current at the design point shall not exceed the cord-and-plug limit of a 15 A circuit | 12 | maximum | A | Analysis OPF-CAL-001 section 5; measurement V1 at TRL 4 | At risk (11.1 A nominal, 13.7 A pessimistic; load manager caps at 12 A; nameplate 20.7 A to resolve, OPF-DEC-001 D2) |
| PR-002 | UR-003, UR-008 | Safety | Load manager | A supervisory controller shall sequence warm-up and cap summed heater duty so the line current stays at or under the target | 12 | maximum | A | Demonstration V1 | Met by design (firmware to write at TRL 4) |
| PR-003 | UR-001, UR-005 | Performance | Die | The die shall have 40 square grooves of 0.27 mm (0.30 mm round equivalent) at 1.0 mm pitch and two 0.30 mm x 48 mm air slots on a 5 mm land | 0.27 | +-0.01 | mm | Inspection with pin gauges and an optical comparator | Met by design |
| PR-004 | UR-001 | Performance | Fibre diameter | Mean fibre diameter of the web shall fall within the target range | 1 to 5 | mean | um | SEM image analysis V3 | To verify at TRL 4 |
| PR-005 | UR-006, UR-012 | Performance | Basis weight | The web shall be made at the target basis weight with a coefficient of variation no more than 10 % over the central 100 mm | 25 | +-2.5 | g/m2 | Weighing of 100 cm2 discs V2 | To verify at TRL 4 |
| PR-006 | UR-001, UR-006 | Performance | Process window | Melt shall be held at 250 C, air at 270 C, air at 140 m/s at the slot and die-to-collector distance at 200 mm, each adjustable | 250, 270, 140, 200 | +-5 C, +-10 m/s, 150 to 300 mm | C, m/s, mm | Inspection and measurement V2 | Met by design |
| PR-007 | UR-007 | Performance | Output | The machine shall make sheets of web at the target area rate, doffing included | 2 | minimum | m2/h | Analysis OPF-CAL-001 section 7; timed run V2 | At risk (1.9 to 2.5 on paper; 9.6 laid at full capture) |
| PR-008 | UR-012 | Performance | Test samples | Each run shall yield flat web at least 140 mm wide for 100 cm2 test discs | 140 | minimum | mm | Inspection | Met on paper (140 mm web) |
| PR-009 | UR-001, UR-012 | Performance | Media benchmark | Charged web shall reach the target NaCl efficiency at about 0.3 um with pressure drop under 10 mm H2O at the lab's flat-sheet flow (media benchmark only) | 90 | minimum | % | Test V5 at a laboratory (42 CFR 84.181 aerosol as the benchmark method) | To verify at TRL 4 |
| PR-010 | UR-002 | Performance | Corona charging | The corona bar shall run at up to -30 kV, current-limited to 1 mA, with 30 to 50 mm needle-to-drum gap | 25 | 10 to 30 | kV | Inspection; V4 | Met by design |
| PR-011 | UR-008 | Safety | Over-temperature | Every heater zone shall have an independent over-temperature cut-out that removes heater power | 300 | maximum | C | Inspection; demonstration V7 | Met by design |
| PR-012 | UR-008 | Safety | Interlocked enclosure | Die, drum, traverse and corona bar shall run only with the enclosure door shut and guard-locked; opening stops motion and removes HV | 0 | none | exposed hazards | Inspection; demonstration V7 | Met by design |
| PR-013 | UR-008 | Safety | Emergency stop | Two emergency stop stations (ISO 13850) shall remove heater, motor and HV power | 2 | minimum | stations | Inspection; demonstration V7 | Met by design |
| PR-014 | UR-009 | Safety | Extraction | The enclosure shall be exhausted to outdoors at the target flow, and HV shall be enabled only with airflow proven | 0.10 | minimum | m3/s | Measurement V6 | Met by design |
| PR-015 | UR-009 | Safety | Ozone at the operator | Ozone at the operator position shall stay below the workplace limit | 0.1 | maximum | ppm | Monitor and measurement V6 | To verify at TRL 4 |
| PR-016 | UR-016 | Logistics | Resin | The machine shall run on a commercial melt-blown PP grade of MFR 1,200 to 1,800 g/10 min (230 C, 2.16 kg) | 1550 | 1200 to 1800 | g/10 min | Inspection of the resin data sheet | Met by design |
| PR-017 | UR-004 | Deployment and assembly | Footprint | The machine shall fit a 610 x 2,440 mm bench | 2440 | maximum | mm | Analysis (model) | Met on paper (2,360 mm) |
| PR-018 | UR-005 | Deployment and assembly | Buildability | Only the die body and air knives shall need precision CNC work; every other part is bought or made with maker-space tools | 2 | maximum | precision parts | Inspection of the build plan | Met by design |
| PR-019 | UR-010 | Usability | Controls | Heater zones on PID controllers with thermocouples; steppers for pump, drum and traverse | 4 | minimum | PID zones | Inspection | Met by design |
| PR-020 | UR-011 | Usability | Documentation | Build plan, operating and purge procedure and maintenance schedule shall be published with the design | 3 | minimum | documents | Inspection; independent build V8 | At risk (build plan done; operating manual at TRL 4) |
| PR-021 | UR-013 | Regulatory | Claims | All wording shall follow OPF-CLM-001 | 0 | none | banned claims | Inspection; render.py --check | Met by design |
| PR-022 | UR-014 | Cost | Machine cost | Parts at prototype quantities shall be reported against the value-engineering target | 10000 | target | USD | BOM | Over target (USD 14,075.15) |
| PR-023 | UR-015 | Maintenance | Purge and clean | The melt path shall be purgeable with a low-MFR PP and the die split for cleaning without removing the melt pump | 1 | maximum | hours to clean | Demonstration V2 | Met by design |
| PR-025 | UR-003, UR-008 | Safety | Air supply | The air pump shall deliver the design flow at the measured air-side pressure; a pressure switch shall remove heater power on low flow | 122 | minimum | NL/min | Analysis OPF-CAL-001 section 3; measurement V1 | At risk (23 to 27 kPa needed, pump maximum 30 kPa) |
| PR-024 | UR-008 | Safety | Hot surfaces | No surface the operator can touch outside the enclosure in normal use shall exceed the target | 60 | maximum | C | IR survey V7 | To verify at TRL 4 |

## Assumptions

Assumptions A1 to A16 are listed in OPF-CAL-001 section 1. Targets remain proposals for review with the project team and a test laboratory.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
