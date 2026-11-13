---
doc_id: OPF-PRC-001
title: Open PolyForge design precis
project: Open PolyForge
doc_type: Precis
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First precis for the carried option PF1 (screw extruder, melt pump and slot die), with PF3 as the alternative awaiting Amish
---

# Open PolyForge design precis

Open PolyForge is a bench-top machine that makes electrostatically charged melt-blown polypropylene web for filter media testing. The carried design (option PF1, the Helpful Engineering proposal's main path) melts a commercial melt-blown resin in a desktop screw extruder, meters it with a gear melt pump through a 40-capillary split die, draws it into fibres with two hot air jets onto a traversing drum, and charges the web with a -25 kV corona bar, all on one 2 ft x 8 ft bench and one 120 V, 15 A circuit. The die is only 48 mm wide because the air heater sets the power: at 13.8 W per millimetre of slot, a 15 A circuit carries about 56 mm (OPF-CAL-001, fix F1). It draws about 1,331 W (11.1 A) steady, lays 4 g/min of polymer and gives about 1.9 to 2.5 m2/h of 25 g/m2 sheets once doffing is counted; parts cost about USD 14,075 against a proposed USD 10,000 value-engineering target. The choice between PF1 and the centrifugal spinner PF3 is **proposed, awaiting Amish**: their scores are within 10 % (OPF-OPT-001, OPF-DEC-001 D1). CONCEPT, NOT FOR FABRICATION.

## How it works

Pellets fall from a guarded hopper into the extruder, which melts them to 250 C and keeps a steady pressure at the melt pump inlet. The pump turns at about 34 rpm and pushes 5.5 cm3/min through a heated melt adapter into the die, where a 6 mm inlet and a manifold slot spread the melt across a 0.3 mm pre-land to 40 grooves, 0.27 mm square at 1 mm pitch, cut in the lower half of the split die. At the nose two air knives, each a 5 mm land at 0.3 mm from the nose face with a 2 mm plenum behind it, blow 2.62 g/s of 270 C air at about 140 m/s along the faces. The air draws each thread of melt into a fibre, targeted at 1 to 5 um, which cools and lands 200 mm away on a 200 mm aluminium drum turning at 30 rpm and traversing +-40 mm, building a 140 mm wide sheet. A row of 14 needles 40 mm above the drum, held at -25 kV with a 1 mA limit, charges the web. When a sheet reaches its basis weight the melt pump stops, the die stays hot, and the operator opens the guard-locked door, cuts off the sheet and restarts (about 1.5 to 2 min). The enclosure is exhausted to outdoors at 0.10 m3/s; the extruder outlet has a branch hood.

## Main components

| # | Component | Made or bought | Material |
| --- | --- | --- | --- |
| 1 | Base frame | Made: cut and welded | SHS 40 x 3 steel |
| 2 | Desktop single-screw extruder, 5/8 in | Bought module | Steel, stainless barrel |
| 3 | Melt tube and adapter | Made: turned | 303 stainless |
| 4 | Melt gear pump, 0.16 cm3/rev | Bought | Stainless |
| 5 | Melt pump drive | Bought; bracket made | NEMA 23 with 10:1 gearbox |
| 6 | Die body halves | Made: CNC, grooved, lapped | 17-4PH or 303 stainless |
| 7 | Air knives | Made: CNC, lapped land | Stainless (same alloy) |
| 8 | Cartridge heaters | Bought | 120 V |
| 14 | Collector drum | Made | Aluminium tube and discs, steel shaft |
| 16, 17 | Drum belt drive and traverse | Bought | Steppers, rails, lead screw |
| 19 | Corona bar | Made | Acetal, stainless needles |
| 21, 22, 23 | Enclosure, panels, door interlock | Made and bought | Aluminium SHS, 6 mm polycarbonate |
| 24 | Exhaust hoods | Made | Galvanised steel |
| 25 | Linear diaphragm air pump, 200 NL/min | Bought | |
| 26 | Inline air heater, 1,000 W | Bought | Stainless |
| 28, 29, 30 | Control panel, emergency stops, PID controllers | Bought | UL 508A practice |
| 31 | HV supply, 0 to -30 kV, 1 mA | Bought | |
| 33, 34 | Mounting plates, fasteners | Made, bought | Steel |

## Changes from the team concept

- The proposal's machine is option PF1; it is modelled at D3 and carried, not chosen. Its plunger alternative is PF2; a third principle, centrifugal melt spinning, is PF3.
- The die width is set by the power budget, not by a laboratory die size (fix F1); a second circuit for the air heater is proposed to Amish (D2).
- Fixes F2 to F10 under the standing instruction: load manager, corona interlocks, fume capture and hopper guard at the extruder, air knife land and plenum, groove size, doffing cycle, heater low-flow protection, heated melt tube, fire controls (OPF-DEC-001, OPF-DDR-003).
- 5 or 6 axis machining is not needed: the capillaries are grooves cut in one face of a split die on a 3-axis mill (OPF-DDR-002).

## First-order numbers (OPF-CAL-001)

- Steady draw 1,331 W (11.1 A) nominal, 1,643 W pessimistic, capped at 12 A; nameplate sum 2,480 W.
- Air 2.62 g/s (122 NL/min) at 270 C and 140 m/s; heater 663 W; air side 23 to 27 kPa.
- Polymer 4.0 g/min (0.24 kg/h), 0.10 g/hole/min; groove pressure 0.17 to 0.73 MPa; pump 34 rpm.
- Web 9.6 m2/h laid at full capture, 6.7 to 8.6 deposited, 1.9 to 2.5 m2/h of sheets with doffing; 140 mm wide at 25 g/m2.
- Corona -25 kV at 40 mm, 5 W; exhaust 0.10 m3/s; ozone 0.35 ppm in the duct at an assumed yield.
- Warm-up about 32 min; 148 kg on the bench; 2,288 x 600 mm footprint.

## Safety

> **Safety:** This is a machine for technically capable operators in a ventilated workshop. It carries mains voltage (120 V), heaters up to 430 C, molten polymer at 250 C that flows almost like oil, hot air jets at 140 m/s, high voltage to 30 kV and moving machinery. Everything hot, charged or moving is inside a guard-locked enclosure; opening the door stops the drum and traverse, removes high voltage and the bar must be grounded before reaching in. Two emergency stops remove heater, motor and high-voltage power. Each heater zone has an independent 300 C cut-out, and the air heater cuts out on low air flow. Fumes and ozone are exhausted to outdoors; the corona runs only with extraction proven, and an ozone monitor sits at the operator. Purge only with the door shut into a catch tray, wearing a face shield, heat-resistant gloves and an apron. Polypropylene fly is combustible: clean it each shift and keep an extinguisher at the bench. A qualified electrician inspects the panel before first power.

## Release limitation

No media from a prototype machine is used in a mask or respirator until its efficiency, pressure drop and charge decay are measured by a qualified laboratory and the finished product is certified to its own respirator standard (STANDARDS 25.5c; OPF-CLM-001).

## Open questions

Decisions and items to confirm are in the design decisions register (OPF-DEC-001).

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
