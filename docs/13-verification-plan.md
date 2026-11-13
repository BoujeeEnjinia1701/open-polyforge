---
doc_id: OPF-VER-001
title: Open PolyForge verification plan
project: Open PolyForge
doc_type: Verification plan
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First verification plan, TRL 4 test families on paper only
---

# Open PolyForge verification plan

Planned TRL 4 verification on paper. Nothing here is run at TRL 3. Method: STANDARDS section 25.7. The gate to further work is V1, V2, V3 and V5 together: the machine holds 12 A, makes web in its window, the fibres are in range and the charged web meets the media benchmark.

Table 1. Test families.

| Family | Method and observations | Evidence needed for the gate | Options | Requirements |
| --- | --- | --- | --- | --- |
| V1 Power and air | True-RMS line current and power factor through warm-up and steady running; air flow (rotameter), pump outlet and knife pressures, heater outlet temperature | 12 A or less; 122 NL/min at the measured pressure; equal knife pressures | PF1 (PF2) | PR-001, PR-002, PR-025 |
| V2 Melt and web | Melt pump calibration at run pressure; basis weight of 100 cm2 discs across the web; flash at the nose; residence and purge time | 25 g/m2 +-2.5, CV 10 % or less over 100 mm; output 2 m2/h or more of sheets | PF1 | PR-003, PR-005, PR-006, PR-007, PR-016, PR-023 |
| V3 Fibres | SEM of web samples at three set points; mean and distribution of fibre diameter | Mean 1 to 5 um | PF1 (PF3 for comparison if D3) | PR-004 |
| V4 Corona | Step-up of voltage and current at two humidity levels; spark-over margin; stored-charge check with the grounding stick; nuisance static | No spark-over at -25 kV; current at or below 1 mA | PF1 | PR-010, PR-012 |
| V5 Media (laboratory) | NaCl efficiency at about 0.3 um and pressure drop on a TSI 8130A-type tester, uncharged and charged, before and after ageing (benchmark: 42 CFR 84.181 aerosol and conditioning) | 90 % or more under 10 mm H2O after charging; decay recorded | PF1 | PR-008, PR-009 |
| V6 Exposure | Exhaust flow; smoke test at openings; ozone at the operator; aldehyde sampling | 0.10 m3/s; ozone under 0.1 ppm; aldehydes under limits | PF1 | PR-014, PR-015 |
| V7 Safety functions | Interlock, guard locking and e-stop function tests; over-temperature cut-outs; IR survey of the outside; noise at the operator | All functions stop as designed; outside surfaces 60 C or less | PF1 | PR-011, PR-012, PR-013, PR-024 |
| V8 Reproducibility | An independent team builds and runs from the package | Machine runs to V1 and V2 | PF1 | PR-018, PR-020 |

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
