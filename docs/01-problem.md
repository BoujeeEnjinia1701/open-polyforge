---
doc_id: OPF-PRB-001
title: Open PolyForge problem statement
project: Open PolyForge
doc_type: Problem statement
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First problem statement from the Helpful Engineering concept proposal "Melt-Blown Polypropylene Machine" v0.1 (2026-09-15), with cited burning platform, users, personas, constraints and kill criteria
---

# Open PolyForge problem statement

Local groups have no accessible, documented way to make electrostatically charged melt-blown polypropylene (PP) filter media when conventional supply fails. The resin is a commodity; the lines, the die-making skill and the process know-how are concentrated in a few large plants that take months to build. Open PolyForge sets out to make a bench-top, maker-space-buildable machine that produces and charges melt-blown PP web from standard resin on ordinary 120 V power, with build, operating and maintenance documentation. Masks and respirators are separate downstream projects. This statement draws on the Helpful Engineering concept proposal "Melt-Blown Polypropylene Machine" (v0.1, 2026-09-15) and is a proposal for review with the project team.

## Burning platform

- In March 2020 melt-blown fabric in China rose from under USD 6,000 per tonne to about USD 60,000, and one melt-blown line cost upward of EUR 3.8 million (USD 4.23 million) and took at least five to six months to make; melt-blown was less than 1 % of China's roughly three million tonnes a year of nonwovens ([NPR, 16 March 2020](https://www.kunc.org/npr-news/2020-03-16/covid-19-has-caused-a-shortage-of-face-masks-but-theyre-surprisingly-hard-to-make), checked 2026-11-12).
- Chinese mask makers reported melt-blown prices rising from CNY 20,000 (USD 2,864) to CNY 300,000 to 400,000 per tonne in early 2020 ([Yicai Global, 3 March 2020](https://yicaiglobal.com/news/china-mask-makers-see-raw-material-prices-soar-20-fold-on-supply-bottlenecks), checked 2026-11-12).
- Researchers estimated a conventional melt-blowing facility at USD 0.1 to 1 million and several months to deploy, against about USD 1,000 for a small centrifugal spinning set-up ([Molina et al. 2022, PLOS ONE](https://rcastoragev2.blob.core.windows.net/f7a4c484a3a6a85ae30da4d11485fa82/PMC9017944.pdf), checked 2026-11-12).
- Melt-blown filter media is a thin, charged web of fibres about 1 to 4 um across, typically near 2 um, at about 30 g/m2 ([Larsen et al. 2021, ACS Applied Polymer Materials](https://distantreader.org/stacks/cord/cord-0055970-ut1gdi9a.txt), checked 2026-11-12): small in mass, but hard to make without the right die, air system and charging.

## Users and context

Table 1. Users and needs.

| User | Context | Need | Persona |
| --- | --- | --- | --- |
| Maker-space build team | Well-equipped maker space or community fabrication lab | Build the machine from common parts, with machining only where precision is essential (the die) | U1 |
| Machinist | Local shop with CNC and lathe | A die and melt parts that can be machined and checked with shop tools | U2 |
| Operator (technically capable) | Workshop with ventilation and controlled access | Start, run, purge and stop the machine safely; know when the web is in specification | U3 |
| Test partner (university lab) | Filtration test laboratory | Flat web samples of known basis weight to measure efficiency at 0.3 um and pressure drop | U4 |
| Emergency planner (NGO or public sector) | Planning distributed capacity for a future outbreak | A documented, reproducible machine and its limits, honestly stated | U5 |

### Personas

- **U1 Dana, maker-space lead.** Runs a university-affiliated maker space; has welders, a CNC router, a small mill and lathe; two experienced volunteers. Wants a build that fits one bench and one wall outlet.
- **U2 Victor, machinist.** Owns a CNC mill with a 4-axis option; has never made a melt-blowing die. Wants drawings with tolerances he can hold and a way to check the capillaries.
- **U3 Priya, process engineer volunteer.** Polymer background, has run extruders; will be the first operator. Wants interlocks, a purge routine and a clear stop.
- **U4 Dr. Osei, filtration lab.** Has a TSI 8130A-type tester; needs 100 cm2 flat samples and their history.
- **U5 Marta, emergency logistics planner.** Needs to know what the machine can and cannot make before counting on it.

### Stakeholders

Table 2. Stakeholders.

| Stakeholder | Interest | How they shape the design |
| --- | --- | --- |
| Helpful Engineering project team (Brian Finch, product lead; Ali Raza, program manager; Bart Combee, project engineer; Amish, community support) | An open, buildable machine and its documentation | Source proposal, roadmap, decision gates |
| Design Molecule Labs | Constructable open design at TRL 3 | Kit standards, documentation |
| Ann Arbor maker-space and University of Michigan contacts (named in the proposal) | Build and test site | Workshop constraints, test access (to engage) |
| Plastics and petrochemical volunteers | Resin, melt-blowing and electrostatics know-how | Process window, die design review |
| Filtration test laboratories | Measured media data | Verification at TRL 4 (OPF-VER-001) |
| Downstream mask or respirator projects | Media of known properties | Their own certification (out of scope here) |

## Constraints

- About a 2 ft x 8 ft (0.61 x 2.44 m) bench footprint (proposal).
- Standard 120 V power, ideally below 15 to 20 A (proposal); one 15 A circuit gives 1,440 W continuous, a 20 A circuit 1,920 W (NEC 210.19, 210.20 and Table 210.21(B)(2)).
- Commonly available components where practical; 5 or 6 axis machining only where needed, the die (proposal).
- Technically capable operators, not novices (proposal).
- Controls from standard heaters, thermocouples, PID loops, steppers and embedded electronics (proposal).
- Value-engineering target: none set in the proposal; USD 10,000 is proposed here, awaiting Amish (OPF-DEC-001 D5).

## Out of scope

- Masks, respirators and any finished product (downstream projects).
- Any respirator performance or certification claim (OPF-CLM-001).
- Industrial-rate production: the machine makes media for testing and small-lot use.

## Prior work

- Industrial melt blowing (Exxon die nose US 3,825,380, expired) and corona charging (Wadsworth and Hersh, US 4,375,718, expired): OPF-FTO-001.
- University pilot lines, for example the NC State Nonwovens Institute 1.2 m line with corona bars up to 50 kV.
- Low-cost centrifugal melt spinning of PP (Molina et al. 2022), option PF3 here.
- The Helpful Engineering proposal (screw or plunger, precision die, hot air, drum or conveyor, corona charging), options PF1 and PF2 here.

## Kill criteria (project stop rules, not a product claim)

The project stops or changes course if any of these holds at TRL 4:

- The steady line current cannot be held at or under 12 A on one 15 A circuit with the die producing web, and a second circuit is not accepted.
- Measured mean fibre diameter above 8 um at the design point after tuning.
- Charged web below 90 % NaCl efficiency at 0.3 um with pressure drop under 10 mm H2O at the lab's flat-sheet flow, after charging is optimised (a media benchmark, not a respirator claim).
- Ozone or aldehyde levels at the operator above the workplace limits with the exhaust running.
- No independent team can build the die from the drawings.

## User research and co-design

Every target here is a proposal until reviewed with the project team, a polymer specialist and an electrostatics specialist (the proposal's capability gaps), and a test laboratory.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
