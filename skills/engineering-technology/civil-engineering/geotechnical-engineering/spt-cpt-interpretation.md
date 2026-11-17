---
id: engineering-technology.civil-engineering.geotechnical-engineering.spt-cpt-interpretation
name: spt-cpt-interpretation
category: engineering-technology
field: civil-engineering
product: geotechnical-engineering
tags: [in-situ-testing, spt, cpt, n-value, energy-correction, n60, cone-resistance, sleeve-friction, soil-behaviour-type, friction-ratio, site-investigation]
level: practitioner
status: draft
description: "Interpret SPT and CPT data: energy and overburden corrections, N60, CPT qt, friction ratio and soil behaviour type, with the limits of the correlations."
sources: ["ASTM D1586 Standard Penetration Test", "ASTM D5778 Electronic Friction Cone and Piezocone Penetration Testing of Soils", "Robertson, Interpretation of Cone Penetration Tests", "FHWA NHI-01-031 Subsurface Investigations"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# SPT and CPT interpretation

## SPT
- N is blows for the last 300 mm of a 450 mm drive of the split spoon (63.5 kg hammer, 760 mm drop). Record refusal (commonly 50 blows for under 150 mm).
- Correct to N60 = N * (ER/60) * CB * CR * CS (hammer energy ratio, borehole diameter, rod length, sampler liner). Overburden correction (N1)60 = N60 * CN, CN about (Pa/sigma'v)^0.5, capped near 1.7 to 2.
- Correlations to relative density and phi' scatter widely; unreliable in gravels (spoon bounces) and clays (use su from lab or vane). Use as ranking, not as a sole design parameter.

## CPT
- Record qc, fs, u2. Corrected tip qt = qc + u2(1 - a), a the cone area ratio (about 0.8). Friction ratio Rf = fs/qc * 100.
- Robertson soil behaviour type (Ic index): low Rf and high qc = sands, high Rf and low qc = clays. It is a behaviour classification, not grain size: confirm with boreholes.
- Undrained strength su = (qt - sigma_v)/Nkt, Nkt about 10 to 20, calibrate locally.
- Pore-pressure dissipation tests give consolidation coefficients.

## Gotchas
- Poor seating or pre-drilling invalidates the near-surface; check zero drift.
- Do not extend correlations beyond the soil type they were fitted to.

## Verify
Hammer energy certificate available; at least one borehole or sample per soil unit alongside CPTs.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
