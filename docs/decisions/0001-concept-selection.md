---
doc_id: OPF-DDR-001
title: "0001: Concept selection"
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
    change: Concept selection argued; PF3 and PF1 within 10 %, proposed, awaiting Amish
---

# 0001: Concept selection

Status: **proposed, awaiting Amish** (OPF-DEC-001 D1). Nothing here is decided.

## Context

The Helpful Engineering proposal asks for a melt-blown PP machine on a 2 ft x 8 ft bench from 120 V power, with a screw or plunger feeding a precision die and hot air, a drum or conveyor, and corona charging. Three working principles were modelled at D3 and scored against OPF-URS-001 (OPF-OPT-001): PF1 screw extruder, melt pump and slot die (171 of 255), PF2 ram extruder into the same die (164) and PF3 centrifugal melt spinning (187).

## Options and evidence

- **PF3 (187):** about 700 W against 1,331 W, about USD 4,000 of parts against USD 14,075, no precision die, demonstrated by Molina et al. (2022) with a 15 cm ring at 3,500 rpm (fibre means 3.4 to 5.2 um). But that web's quality factor was 0.0018 per Pa against 0.0100 for the reference respirator media (OPF-STM-001 X8, fails), the web is batch and uneven, and the principle is centrifugal spinning, not melt blowing: choosing it changes the project's title, pitch and working principle.
- **PF1 (171):** the proposal's path, continuous and metered, with the established route to 1 to 5 um charged web. Its constraint is power: the die is 48 mm wide (F1), output about 2 m2/h of sheets, nameplate to resolve (D2).
- **PF2 (164):** simpler feed, no melt pump, but batch (duty at most about 32 %) with trapped-air and residence-time risks; 12 % below PF3, not put forward. Fallback if the screw cannot feed the 1,550 MFR melt.

## Recommendation

Both PF3 and PF1 go to Amish without a pick (within 10 %). The engineering view, for Amish to weigh, favours PF1 for the project as proposed (media quality and continuity), with the PF3 ring rig as an early, cheap bench for resin, charging and testing (D3). PF1 is carried in the drawing set, BOM and build plan so a constructable design exists at TRL 3.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
