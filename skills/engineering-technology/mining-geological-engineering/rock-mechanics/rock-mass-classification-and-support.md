---
id: engineering-technology.mining-geological-engineering.rock-mechanics.rock-mass-classification-and-support
name: rock-mass-classification-and-support
category: engineering-technology
field: mining-geological-engineering
product: rock-mechanics
tags: [mining-geological-engineering, rock-mechanics, ground-control, geotechnical-engineering, rock-mass-classification, rmr, rmr89, bieniawski, q-system, barton, nga, gsi, geological-strength-index, hoek-brown, rqd, joint-roughness, esr, unsupported-span, rock-bolts, rockbolting, shotcrete, ground-support, stability-graph, mathews, hydraulic-radius, pillar-design, rocscience, core-logging]
level: practitioner
status: gated
description: "Classify a rock mass with RMR, Q-system and GSI, convert between them, and turn the rating into span, support and Hoek-Brown strength estimates for design."
sources:
  - "Bieniawski, Engineering Rock Mass Classifications (1989)"
  - "Barton, Lien and Lunde (1974), Engineering classification of rock masses for the design of tunnel support"
  - "NGI, Using the Q-system: Rock mass classification and support design (handbook)"
  - "Hoek, Carranza-Torres and Corkum (2002), Hoek-Brown failure criterion — 2002 edition"
  - "Hoek and Diederichs (2006), Empirical estimation of rock mass modulus"
  - "Brady and Brown, Rock Mechanics for Underground Mining"
  - "Potvin (1988) and Hutchinson and Diederichs, Cablebolting in Underground Mines"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rock-mass classification and support — RMR, Q and GSI into design inputs

**Goal:** log a rock mass consistently, rate it with at least two systems, and turn
the ratings into first-pass span limits, support and strength parameters — then hand
them to numerical or limit-equilibrium analysis for the final design.

## 1. Collect the inputs (core and mapping)
- **RQD** (Deere): sum of intact core pieces ≥ 100 mm ÷ run length × 100. Exclude
  drilling breaks. From mapping, estimate via volumetric joint count Jv:
  `RQD ≈ 115 − 3.3·Jv` (Palmström; RQD = 100 when Jv < 4.5) (gated: unconfirmed, source is paywalled or blocked).
- Intact strength (UCS or point-load Is50 × ~20–25 (gated: unconfirmed, source is paywalled or blocked), calibrate per rock type).
- Joint sets, spacing, persistence, roughness, aperture, infill, weathering, water.
- Log by **geotechnical domain**, not by drill run; one average for a whole hole
  hides the weak zone that governs.

## 2. Rate with RMR89 (Bieniawski)
Sum five parameters (0–100): UCS (0–15), RQD (3–20), joint spacing (5–20), joint
condition (0–30), groundwater (0–15); then apply the orientation adjustment
(0 to −12 for tunnels, larger for slopes and foundations) (gated: unconfirmed, source is paywalled or blocked).

| RMR | 81–100 | 61–80 | 41–60 | 21–40 | <21 |
|---|---|---|---|---|---|
| Class | I very good | II good | III fair | IV poor | V very poor |

## 3. Rate with Q (Barton/NGI)
`Q = (RQD/Jn) × (Jr/Ja) × (Jw/SRF)` — block size × inter-block shear strength ×
active stress. Range 0.001–1000.
- **Equivalent dimension** De = span (or height) / ESR. ESR ≈ 3–5 for temporary
  mine openings, ~1.6 for permanent mine openings, ~1.0 for main road/rail tunnels (gated: unconfirmed, source is paywalled or blocked).
- **Maximum unsupported span** ≈ 2·ESR·Q^0.4 (m) (gated: unconfirmed, source is paywalled or blocked).
- **Bolt length** ≈ 2 + 0.15·B/ESR (m), B = span (gated: unconfirmed, source is paywalled or blocked).
- Read bolt spacing and shotcrete thickness from the Q support chart (NGI handbook).
- Rough conversion: `RMR ≈ 9·ln Q + 44` (Bieniawski; gated: unconfirmed, source is paywalled or blocked) — scatter is large (±10 or more); use it to
  cross-check, not to replace a rating.

## 4. GSI and Hoek-Brown strength
- GSI from the chart (structure vs surface condition), or for RMR89 > 23 with dry
  groundwater rating and no orientation adjustment: `GSI ≈ RMR89 − 5` (gated: unconfirmed, source is paywalled or blocked).
- Generalised Hoek-Brown with disturbance factor D (0 undisturbed/TBM, up to 1 for
  heavily blasted pit slopes):
```
mb = mi·exp((GSI − 100)/(28 − 14D))
s  = exp((GSI − 100)/(9 − 3D))
a  = 0.5 + (exp(−GSI/15) − exp(−20/3))/6
Erm = Ei·(0.02 + (1 − D/2)/(1 + exp((60 + 15D − GSI)/11)))   (Hoek–Diederichs)
```
Checked: Erm form (Hoek and Diederichs 2006, eq. 4, rocscience PDF) and s, a forms (the 2006 paper restates s = exp((GSI-100)/9) for D = 0 and a = 1/2 + 1/6(exp(-GSI/15) - exp(-20/3))). The D-dependent 28-14D and 9-3D denominators are from Hoek, Carranza-Torres and Corkum 2002 and were not re-fetched (gated: unconfirmed, source blocked).
Typical mi: granite ~32, sandstone ~17, limestone ~8–12, shale ~6 (gated: unconfirmed, source is paywalled or blocked) (use the published
table and lab triaxials where available). Software: RocData/RSData-type tools fit these.

## 5. Mining-specific uses
- **Open stopes:** modified stability number N′ = Q′·A·B·C (Q′ omits Jw/SRF; A stress,
  B joint orientation, C gravity factors) plotted against **hydraulic radius**
  HR = area/perimeter of each stope face on the stability graph.
- **Pillars:** tributary-area stress σp = σv·(total area / pillar area); compare with an
  empirical pillar strength formula calibrated to similar rock (e.g. Hedley-Grant,
  Lunder-Pakalnis). Target factors of safety depend on pillar role and regulator —
  confirm locally.
- **Slopes:** use GSI/Hoek-Brown strengths in limit-equilibrium (Bishop, Spencer,
  Morgenstern-Price) and check structurally controlled planar/wedge failures with
  kinematic analysis separately.

## Gotchas
- Q and RMR penalise water and stress differently; never double-count by applying
  SRF *and* a separate stress reduction to the same rating.
- GSI is for jointed rock behaving isotropically; a single dominant structure needs
  a kinematic or anisotropic model instead.
- Empirical span/support charts are case-history fits; outside their database
  (very deep, squeezing, rockburst-prone) they are not conservative.
- Core-derived RQD depends on hole orientation relative to jointing — use several
  hole directions or Jv from mapping.
- Final ground-support designs are safety-critical: they need review by a competent
  geotechnical engineer and must meet the governing mine regulator's ground-control rules.

## Verify
- [ ] Ratings done per geotechnical domain, with RMR and Q cross-checked.
- [ ] Span and support from Q compared against site experience and the support chart.
- [ ] Hoek-Brown parameters use a justified D and mi, not defaults.
- [ ] Structurally controlled failure checked separately from rock-mass failure.
- [ ] Design reviewed by a competent geotechnical engineer and monitored after excavation.
