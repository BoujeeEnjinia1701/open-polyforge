---
doc_id: OPF-FEA-001
title: Open PolyForge feasibility assessment
project: Open PolyForge
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First feasibility assessment of PF1 by aspect
---

# Open PolyForge feasibility assessment

PF1 is feasible on paper at a small scale. Power and the air supply are the tight aspects; everything else uses established melt-blowing practice at a lower throughput per hole.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Melt blowing at 0.10 g/hole/min, 270 C air at 140 m/s, 200 mm to the drum, within published practice | Medium | Fibre diameter not predicted, only targeted | OPF-STM-001 S8 to S13, S19 |
| Power | 1,331 W nominal on one 15 A circuit; 1,643 W pessimistic capped at 12 A; nameplate 2,480 W | Low | Marking and acceptance to resolve (D2) | OPF-CAL-001 section 5; S1 to S3 |
| Air supply | 122 NL/min at 23 to 27 kPa against a 30 kPa pump maximum | Medium | Little margin; heater drop to confirm (C3) | S7, S41 |
| Materials | Stainless die, aluminium drum, acetal insulators, polycarbonate enclosure | Medium | Polycarbonate temperature and fire grade (S52) | S49, S52 |
| Manufacturing and assembly | Two precision parts (die halves, knives) on a 3-axis mill; the rest maker-space work | Medium | Groove sealing flatness (S46) | OPF-BLD-001; OPF-DDR-002 |
| Controls | Four PID zones, three steppers, interlocks and a load manager | Medium | Firmware is TRL 4 work | PR-002, PR-019 |
| Supply | Extruder discontinued (EX2); melt pump price to obtain; resin small lots | Medium | D6, C1, C4 | OPF-MKT-001 |
| Output | 1.9 to 2.5 m2/h of sheets with doffing | Medium | Below the 9.6 m2/h laid rate | S20 |
| Regulatory | Machine standards as practice; no product approval for the machine | Medium | Electrical inspection | OPF-REG-001 |
| Freedom to operate | Core die and charging patents expired; one active die-tip patent to compare | Medium | Attorney opinion (C7) | OPF-FTO-001 |

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
