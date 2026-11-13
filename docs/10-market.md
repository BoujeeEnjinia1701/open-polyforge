---
doc_id: OPF-MKT-001
title: Open PolyForge market and viability
project: Open PolyForge
doc_type: Market and viability
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First market and viability note with cited benchmarks and cost per square metre
---

# Open PolyForge market and viability

Open PolyForge is not a commercial product: it is resilience capacity, a documented machine a maker space, university or NGO can build when industrial supply fails. At about USD 14,075 of parts it costs a fraction of a percent of an industrial line, but its media costs more per square metre than normal market media and roughly matches the 2020 shortage price. Its value is availability, not price. Checked 2026-11-12.

Table 1. Benchmarks.

| Benchmark | Figure (cited) | Compared with Open PolyForge PF1 |
| --- | --- | --- |
| Industrial melt-blown line | Upward of EUR 3.8 million (USD 4.23 million) a line, at least five to six months to make ([NPR, 2020](https://www.kunc.org/npr-news/2020-03-16/covid-19-has-caused-a-shortage-of-face-masks-but-theyre-surprisingly-hard-to-make)) | About 0.3 % of the cost; output many orders of magnitude lower |
| Conventional melt-blowing facility | USD 0.1 to 1 million and several months ([Molina et al. 2022](https://rcastoragev2.blob.core.windows.net/f7a4c484a3a6a85ae30da4d11485fa82/PMC9017944.pdf)) | 1.4 to 14 % of the cost |
| Centrifugal melt spinning rig | About USD 1,000 upper estimate for motor, heater and chuck (Molina et al. 2022) | PF3's principle; a cheaper start (D3), lower media quality |
| Used 300 mm melt-blown lab line | Price on request ([Exapro listing](https://www.exapro.com/rolbatch-meltblownmaster-prox-300-p240212040)) | Not priced; to assess |
| Melt-blown fabric, China | Under USD 6,000 per tonne before the outbreak, about USD 60,000 in March 2020 (NPR); CNY 20,000 to 300,000 to 400,000 per tonne ([Yicai Global](https://yicaiglobal.com/news/china-mask-makers-see-raw-material-prices-soar-20-fold-on-supply-bottlenecks)) | At 25 g/m2: USD 0.15 per m2 before, USD 1.50 per m2 at the peak |

Table 2. Estimated cost per square metre of PF1 sheets (OPF-CAL-001; assumptions stated).

| Item | Value | Basis |
| --- | --- | --- |
| Parts per machine | USD 14,075.15 | bom/bom.csv (value-engineering target USD 10,000, proposed; USD 4,075.15 over) |
| Output | 1.9 to 2.5 m2/h of sheets | OPF-CAL-001 section 7 |
| Use | 500 h a year for 5 years (assumed) | About 950 to 1,250 m2 a year |
| Capital per m2 | USD 2.25 to 2.96 | Parts over 5 years of output |
| Energy per m2 | USD 0.02 steady, about USD 0.05 to 0.08 with warm-up and doffing | 14.01 cents/kWh, EIA STEO 2026 commercial average |
| Resin per m2 | 25 g at a melt-blown grade price to assess | Small-lot price not found |
| Total, excluding resin and labour | About USD 2.3 to 3.0 per m2 | Above the 2020 peak market price of about USD 1.50 per m2 |

## Segments and route

| Segment | Users and region | Value proposition | Route |
| --- | --- | --- | --- |
| University and maker-space labs | North America first (Ann Arbor contacts in the proposal), then wherever a capable fabrication community exists | Documented, reproducible media machine for research and test lots | Open repo, build workshops, Helpful Engineering community |
| Emergency planners and NGOs | Global | Pre-positioned know-how and a buildable machine | Build packages with partners; downstream mask projects certify their own products |
| Downstream filtration projects | Global | Media of known, measured properties for their development | Test lots under the release limitation |

The open, non-commercial route is the Helpful Engineering model: the design, build plan and test results are published under CERN-OHL-P-2.0, Apache-2.0 and CC-BY-4.0, and any team may build it.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
