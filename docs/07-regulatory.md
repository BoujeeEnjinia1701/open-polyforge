---
doc_id: OPF-REG-001
title: Open PolyForge regulatory and standards register
project: Open PolyForge
doc_type: Regulatory register
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First register of machine safety, electrical codes, workplace exposure and the downstream respirator benchmarks
---

# Open PolyForge regulatory and standards register

The machine is workshop equipment that makes filter media; no product approval is required for the machine itself at this stage, and no respirator claim is made (OPF-CLM-001). Machine safety, electrical and workplace standards are used as design references, not as certifications. Checked 2026-11-12.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | NFPA 79 (2024), Electrical Standard for Industrial Machinery ([summary](https://www.wevolver.com/article/nfpa-79-the-electrical-standard-for-industrial-machinery)) | US | Electrical equipment of machines: disconnects, protection, stop functions, wiring | Design reference for the panel, stops and wiring (PR-012, PR-013) | Electrical lead | Applies as practice; inspection to assess |
| R2 | IEC 60204-1:2016+AMD1:2021, Safety of machinery, electrical equipment of machines ([IEC webstore](https://webstore.iec.ch/publication/71256)) | International, EU (EN 60204-1) | As R1 outside North America; stop categories 0 and 1 | Reference for builds outside North America | Electrical lead | Applies as practice |
| R3 | UL 508A, Industrial Control Panels ([summary](https://www.wevolver.com/article/ul-508a-the-standard-for-industrial-control-panels)) | US | Construction and short-circuit current rating of control panels | Panel built to its practice, not listed | Electrical lead | Practice only; listing not sought |
| R4 | NEC 2020 210.19(A), 210.20(A), Table 210.21(B)(2) ([guide](https://open-exam-prep.com/study-guides/ak-electrician/ch06/ch06-sec01)) | US | Continuous loads at 125 %; 12 A cord-and-plug load on a 15 A receptacle, 16 A on 20 A | Sets the power budget (PR-001); nameplate marking of a current-limited machine to resolve (OPF-DEC-001 D2) | Electrical lead | To assess with an electrician or the authority having jurisdiction |
| R5 | ISO 13850, emergency stop function (named reference) | International | Emergency stop design | Two latching red-on-yellow stations (PR-013) | Safety lead | Met by design, edition to confirm |
| R6 | ISO 14119, interlocking devices with guards (named reference) | International | Guard interlocks and guard locking | Door switch with guard locking (PR-012) | Safety lead | Met by design, edition to confirm |
| R7 | ISO 13732-1, hot surface burn thresholds ([summary](https://inzonex.co.uk/insulation/safety/hot-surface-standards/)) | International | Contact burn thresholds (bare metal about 70 C at 1 s) | Touchable surfaces at most 60 C (PR-024) | Safety lead | To verify (V7) |
| R8 | OSHA ozone PEL 0.1 ppm 8 h TWA; NIOSH REL 0.1 ppm ceiling ([OSHA](https://www.osha.gov/chemicaldata/9)) | US | Workplace ozone | Operator limit (PR-015) | Safety lead | To verify (V6) |
| R9 | Local exhaust ventilation practice, capture velocity about 0.5 m/s ([CCOHS](https://www.ccohs.ca/oshanswers/prevention/ventilation/hoods.html)) | Canada (guidance) | Hood design | Enclosure and branch hood (PR-014) | Safety lead | Met by design, to measure |
| R10 | 42 CFR Part 84, including 84.181 ([eCFR text, 2009 edition](https://govinfo.gov/content/pkg/CFR-2009-title42-vol1/pdf/CFR-2009-title42-vol1-sec84-181.pdf)) | US | Approval of respirators; NaCl filter efficiency test | Downstream benchmark only: a finished respirator, not this media or machine, would need it; the NaCl method is the media test benchmark (PR-009) | Test lead | Does not apply to the machine; benchmark |
| R11 | EN 149 and GB 2626 (named references) | EU, China | Filtering half masks | Downstream benchmarks only | Downstream projects | Does not apply |
| R12 | Electrical inspection by the maker space or local authority | Local | Fixed wiring, receptacle rating, make-up air | Before first power (BLD safety stops) | Maker-space lead | To assess |

> **Safety:** The machine carries mains voltage, heaters to 430 C, molten polymer, high voltage to 30 kV and moving parts. The release limitation applies: no media from a prototype machine is used in a mask or respirator until its efficiency, pressure drop and charge decay are measured by a qualified laboratory and the finished product is certified to its own standard.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
