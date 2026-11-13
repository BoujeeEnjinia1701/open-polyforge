---
doc_id: OPF-DDR-003
title: "0003: STEM fixes"
project: Open PolyForge
doc_type: Decision record
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: Fixes F1 to F10 under the standing instruction of 2026-10-23, including those found by the independent review
---

# 0003: STEM fixes

Status: made under Amish's standing instruction of 2026-10-23 (STANDARDS section 20, fix rule); Amish can reverse them. Each keeps the working principle.

## F1: die width set by the power budget (OPF-STM-001 S1)

Air at 2.62 g/s per 48 mm of slot heated from 35 to 270 C needs 663 W, 13.8 W per mm. A 150 mm laboratory-width die at the same design would draw about 3,061 W (25.5 A) with three pumps. Options weighed: (a) narrow the die; (b) lower air temperature (coarser fibres); (c) recuperate heat (the air leaves with the fibres; tens of watts at most from the extruder body); (d) a second circuit (to Amish, D2). Chosen: (a), 40 capillaries and two 48 mm slots at 0.10 g/hole/min. Cost: none; output falls to 4 g/min.

## F2: load manager (S2, S3, S55)

The pessimistic steady draw is 1,643 W, and the nameplate sum 2,480 W. A controller measures line current (not power, because of power factor) and caps summed heater duty at 12 A; warm-up is sequenced (barrel, pump and die first; air second). Cost: a current sensor and firmware. Marking and acceptance go to Amish (D2).

## F3: corona interlocks (S27, S33)

HV is enabled only with the door guard-locked, extraction airflow proven and the drum turning; the supply is current-limited to 1 mA and fixed negative; the bar is grounded before the door unlocks; an ozone monitor sits at the operator. Cost: about USD 300 for the monitor.

## F4: fume capture and guarding at the extruder (S28, S31)

The extruder sits outside the enclosure. A branch hood over its outlet and a fixed perforated lid on the hopper are added. Cost: about USD 50.

## F5: air knife land and plenum (S7, S41, S45), found by the independent review

A knife parallel to the whole 43 mm nose face at 0.3 mm makes a laminar slot needing 36.5 kPa, 43 to 47 kPa in all, beyond a diaphragm pump. Options: (a) a short 5 mm land with a 2 mm plenum behind it; (b) a bigger air gap (more air, more power); (c) a compressor (another circuit). Chosen: (a), slot 16.5 kPa, 23 to 27 kPa in all; pump raised from the 150 to the 200 NL/min, 30 kPa class (USD 0 change in the BOM price used). Knives of the die's alloy, gaps set with shims at temperature.

## F6: groove size (S12), found by the independent review

A 0.30 mm square groove passes 43 % more than a 0.30 mm hole. Grooves are 0.27 mm square, a 0.30 mm round equivalent. Cost: none.

## F7: doffing cycle (S20), found by the independent review

A sheet reaches 25 g/m2 in about 0.55 min; opening the door stops the drum and HV but the die would keep extruding. The melt pump now stops before the door unlocks and the die stays hot; output is reported as 1.9 to 2.5 m2/h of sheets. A continuous take-off is D4.

## F8: heater low-flow protection (S42), found by the independent review

At reduced flow the 1,000 W heater would exceed its 430 C rating. A pressure switch at the heater inlet removes heater power, a check valve protects the pump, and the pump runs on 5 min after the heater stops. Cost: in BOM 27.

## F9: heated melt tube (S47), found by the independent review

A 100 W band heater on its own zone keeps the short melt tube between the extruder flange and the pump molten. Cost: USD 35 (BOM 38).

## F10: fire controls (S49), found by the independent review

PP fly and wax-like condensate are combustible. The heater shell is insulated and outside the fibre stream, the duct is cleanable, fly is cleaned each shift, and an extinguisher and PPE sit at the bench. Cost: USD 120 (BOM 39).

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
