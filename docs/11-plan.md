---
doc_id: OPF-PLN-001
title: Open PolyForge project plan
project: Open PolyForge
doc_type: Project plan
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First project plan with the Helpful Engineering process content (STANDARDS 25.7), stage gates and references
---

# Open PolyForge project plan

The project is at TRL 3 on paper (stage P3). The next step, when the portfolio cap allows, is a TRL 4 laboratory build of one machine and the test families of OPF-VER-001. This plan carries the Helpful Engineering process content and follows the proposal's roadmap (months 1 to 12 team and design, 12 to 30 build and test, 30 and on a publishable build and operating package).

## Purpose

Give local groups an accessible, documented way to make electrostatically charged melt-blown PP filter media when conventional supply fails, and preserve the know-how in an open package that can be found again years later (Helpful Engineering proposal v0.1).

## Kill criteria (project stop rules, not a product claim)

As OPF-PRB-001: line current not held at 12 A on 15 A and no second circuit accepted; mean fibre above 8 um after tuning; charged web below 90 % NaCl efficiency at under 10 mm H2O after charging is optimised (a media benchmark); ozone or aldehydes at the operator above limits with the exhaust running; no independent team can build the die from the drawings.

## Targets and key performance indicators

| KPI | Target | Now (paper) |
| --- | --- | --- |
| Line current, steady | 12 A or less on 15 A | 11.1 A nominal, 13.7 A pessimistic, capped |
| Mean fibre diameter | 1 to 5 um | Target only |
| Basis weight and CV | 25 g/m2, CV 10 % or less | Target only |
| Media benchmark | 90 % or more NaCl at about 0.3 um under 10 mm H2O | Target only |
| Output | 2 m2/h of sheets or more | 1.9 to 2.5 m2/h on paper |
| Machine cost | USD 10,000 value-engineering target (proposed) | USD 14,075.15 |
| Reproducibility | One independent team builds it from the package | Not started |

## Minimum viable team

| Role | From | Deliverable |
| --- | --- | --- |
| Product lead (Brian Finch) | Helpful Engineering | Technical direction, decision gates |
| Program manager (Ali Raza) | Helpful Engineering | Plan, actions, documentation |
| Project engineer (Bart Combee) | Helpful Engineering | Mechanical design and build lead |
| Polymer or melt-blowing specialist | To recruit | Process window, resin, die review |
| Electrostatics specialist | To recruit | Corona design and test |
| Machinist with precision CNC | To recruit or partner | Die halves and knives |
| Electrician | Maker space or volunteer | Panel review, acceptance (D2) |
| Community support (Amish) | Helpful Engineering and Design Molecule Labs | Recruiting, documentation standard |

## 60 to 90 day plan

| Days | Work | Output |
| --- | --- | --- |
| 1 to 15 | Amish decides D1 to D8; recruitment collateral from this repo | Decisions recorded in OPF-DEC-001 |
| 15 to 45 | Recruit the polymer, electrostatics and machining specialists; electrician view on D2; quotes for the melt pump, extruder and HV supply (C1 to C3) | Team and quotes |
| 30 to 60 | Specialist review of the die drawing and the air knife land; if D3 is accepted, build the ring rig for resin, charging and NaCl trials | Reviewed die drawing |
| 60 to 90 | Detail drawings for the die at Rev A after review; test-lab agreement for V5 | Ready for the TRL 4 build when the cap allows |

## Support needed from Helpful Engineering

- Project management: cadence (about monthly), roadmap, decisions, risks (proposal: active need).
- Recruiting: plastics and melt-blown specialist, electrostatics specialist, precision machinist (immediate).
- Technical expertise: polymer processing, die design, airflow, machine design (immediate).
- QA and regulatory: validation plan and the machine and media versus respirator boundary (later).
- Communication: recruitment collateral now; publication of the build and operating package later.
- Fundraising: prototype parts (about USD 14,000), die machining, test fees (not yet defined).

## External partners

Ann Arbor maker space and University of Michigan contacts (named in the proposal, to engage); a filtration test laboratory with a TSI 8130A-type tester (to identify); resin supplier for small lots (to identify).

## Stage gates

| Gate | Evidence | Status |
| --- | --- | --- |
| P3 (TRL 3) | This repo: STM with independent review, OPT, URS, PRS, RTM, CAL, CAD at D3, BOM, BLD, DEC, REG, FEA, RSK, MKT, CLM, VER, FTO | Done on paper, awaiting Amish's review |
| P4 (TRL 4), on hold under the cap | One machine built; V1 to V8 run in the lab | Planned |
| P5 (TRL 5), on hold | Run at a partner maker space; independent build | Planned |

## Decision request

Amish: D1 (PF1 or PF3), D2 (supply and marking), D3 (ring rig first), D5 (value-engineering target), D6 (extruder source).

## References

All sources are listed with links and the date checked (2026-11-12) in OPF-STM-001, OPF-CAL-001, OPF-REG-001, OPF-MKT-001 and OPF-FTO-001. Source proposal: Helpful Engineering, "Melt-Blown Polypropylene Machine" concept proposal, v0.1, 2026-09-15.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
