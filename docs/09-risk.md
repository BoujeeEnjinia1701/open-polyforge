---
doc_id: OPF-RSK-001
title: Open PolyForge risk register and hazard analysis
project: Open PolyForge
doc_type: Risk register
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First project risk register, preliminary hazard analysis and first-pass design FMEA for PF1
---

# Open PolyForge risk register and hazard analysis

The highest risks are power and electrical acceptance, the air supply margin, and media quality that cannot be predicted on paper. The highest design FMEA items are uneven flow across the 40 grooves and a high-voltage spark-over. Scores are 1 (low) to 5 (high).

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Machine cannot be accepted on one 15 A receptacle | Nameplate 2,480 W; load manager not accepted as a limiting means | Second circuit or 20 A supply needed | 4 | 3 | Electrical lead | Electrician view early; D2 options |
| P2 | Fibres too coarse | Low air pressure margin, low air temperature when trimmed | Media below the benchmark | 3 | 4 | Process lead | Measure at TRL 4 (V3); D3 ring rig to learn early |
| P3 | Melt pump cost or lead time | Specialist part | Schedule, cost | 3 | 3 | Program manager | Used pump, second source (C1) |
| P4 | Screw cannot feed 1,550 MFR melt | Low viscosity | No steady flow | 3 | 4 | Process lead | Inlet-pressure control; PF2 fallback |
| P5 | Specialists not recruited | Capability gaps named in the proposal (polymer, electrostatics, die machining) | Delay | 3 | 4 | Helpful Engineering recruiting | Recruitment collateral (OPF-PLN-001) |
| P6 | Media misused in masks | Pressure in an emergency | Harm, liability | 3 | 5 | Project lead | Release limitation on every document and label (OPF-CLM-001) |
| P7 | D1 decision delayed | PF3 and PF1 within 10 % | Schedule | 3 | 2 | Project lead | Decision request in OPF-PLN-001 |

## Preliminary hazard analysis

Table 2. Hazards. Severity and likelihood 1 to 5.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Electric shock, mains | Faulty wiring, open panel | Injury, death | 5 | 2 | Panel to NFPA 79 and UL 508A practice, earthing, inspection before power | Low |
| H2 | Electric shock, high voltage | Reaching in with HV on | Injury | 4 | 2 | Guard locking, HV off and grounding stick before entry, 1 mA limit | Low |
| H3 | Burns from hot surfaces and melt | Die 250 C, heater sheath to 430 C, melt splash at purge | Burns | 4 | 3 | Enclosure, insulation, PPE, purge with the door shut | Medium |
| H4 | Entanglement and crushing | Drum, belt, traverse, extruder screw | Hand injury | 4 | 2 | Interlocked enclosure, hopper lid, two e-stops | Low |
| H5 | Fumes and aerosol | Hot PP oxidation | Irritation | 3 | 3 | Enclosure exhaust and branch hood to outdoors | Medium, to measure |
| H6 | Ozone and NOx | Corona | Respiratory irritation | 3 | 3 | HV only with extraction proven, ozone monitor | Medium, to measure |
| H7 | Fire | PP fly, condensate, hot heater shell, spark-over | Burns, property | 4 | 2 | Insulated shell, clean each shift, cleanable duct, extinguisher, cut-outs | Low |
| H8 | Overheated air heater | Low air flow | Heater failure, fire | 4 | 2 | Pressure switch, check valve, pump run-on | Low |
| H9 | Noise | 140 m/s jet | Hearing | 2 | 2 | Enclosure; measure (V7) | Low |
| H10 | Heavy lift | 148 kg machine, 13 kg modules | Strain | 3 | 2 | Assemble in place; two-person lifts | Low |

## Design FMEA (first pass, PF1)

Table 3. Design FMEA. S severity, O occurrence, D detection (1 to 10); RPN = S x O x D.

| Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Die grooves | Split melt evenly over 40 holes | Uneven flow | Uneven basis weight | Low die pressure (0.17 to 0.73 MPa), manifold, pre-land tolerance | 6 | 6 | 5 | 180 | Measure basis-weight profile (V2); shim the pre-land |
| Split die faces | Seal grooves | Melt leaks between grooves | Flash, shot | Faces not flat to a few um | 6 | 4 | 4 | 96 | Lap and blue-check; clamp torque |
| Air knives | Give two equal jets | Unequal gaps | Fibres blown sideways, rope | Thermal growth, shim error | 6 | 5 | 5 | 150 | Set hot; measure each knife's pressure |
| Air pump | Deliver 122 NL/min | Flow low at 27 kPa | Coarse fibres | Pump curve at 60 Hz | 6 | 4 | 3 | 72 | Read the curve (C2), measure (V1) |
| Air heater | 270 C air | Overheats | Heater burn-out | Low flow | 7 | 3 | 2 | 42 | Pressure switch (F8) |
| Load manager | Hold 12 A | Trips the breaker | Stoppage | Simultaneous warm-up | 4 | 4 | 3 | 48 | Sequenced warm-up (F2) |
| Melt pump | Meter 5.5 cm3/min | Slip | Rate drift | 3.5 to 5 Pa s melt | 5 | 5 | 4 | 100 | Calibrate (V2) |
| Extruder | Feed the pump | Starves the pump | Pump cavitates | Back-flow of thin melt | 6 | 4 | 4 | 96 | Inlet-pressure control; PF2 fallback |
| Corona bar | Charge the web | Spark-over to the drum | Burnt web, fire, supply trip | Humidity, sharp drum edge, wrong polarity | 7 | 3 | 5 | 105 | Fixed negative, current limit, rounded drum edges, step-up test (V4) |
| Enclosure | Contain hazards | Door opened while running | Exposure | Interlock bypassed | 8 | 2 | 3 | 48 | Guard locking (ISO 14119 type 2) |
| Exhaust | Capture fumes and ozone | Low airflow | Exposure | Fan or duct blocked | 6 | 3 | 3 | 54 | Airflow switch interlocks HV and heaters |
| Polycarbonate panels | Guard | Softening | Loss of guard | Radiant heat | 6 | 2 | 4 | 48 | Distance, insulation, IR survey (V7) |

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
