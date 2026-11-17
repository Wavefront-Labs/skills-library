---
id: engineering-technology.petroleum-engineering.formation-evaluation.quick-look-log-interpretation
name: quick-look-log-interpretation
category: engineering-technology
field: petroleum-engineering
product: formation-evaluation
tags: [petrophysics, well-logs, quick-look, log-interpretation, vshale, gamma-ray, larionov, density-porosity, neutron-porosity, density-neutron-crossover, gas-effect, archie, water-saturation, cementation-exponent, saturation-exponent, rw, sp-log, pickett-plot, cutoffs, net-pay, net-to-gross, resistivity, las]
level: practitioner
status: gated
description: "Quick-look petrophysics: Vshale from GR, density-neutron porosity and gas crossover, Rw from SP or Pickett plot, Archie Sw with a/m/n, cutoffs and net pay."
sources:
  - "Archie, The Electrical Resistivity Log as an Aid in Determining Some Reservoir Characteristics (Trans. AIME, 1942)"
  - "Asquith & Krygowski, Basic Well Log Analysis (AAPG Methods in Exploration 16)"
  - "Schlumberger Log Interpretation Charts (current edition)"
  - "Bateman, Openhole Log Analysis and Formation Evaluation"
  - "Pickett, A Review of Current Techniques for Determination of Water Saturation from Logs (JPT, 1966)"
  - "Worthington, Net Pay — What Is It? What Does It Do? (SPE 123561)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quick-look log interpretation — from a log suite to porosity, Sw and net pay

**Goal:** in an hour, turn a standard open-hole suite (GR, SP, caliper, deep/shallow resistivity, bulk density, neutron, PEF, sonic) into zone-by-zone Vsh, porosity, water saturation and net pay, with the assumptions written down.

## 1. Set up and QC

- Load LAS; depth-match all curves to the main pass. Check caliper and density correction (DRHO > ~0.05–0.1 g/cc flags bad density (gated: unconfirmed, source is paywalled or blocked)), mud type (WBM/OBM), Rmf and temperature at BHT.
- Correct Rw/Rmf to formation temperature with Arps: R2 = R1·(T1 + 6.77)/(T2 + 6.77) (°F) (gated: unconfirmed, source is paywalled or blocked).
- Zone the well: clean sands/carbonates vs shales; pick shale and clean baselines per zone.

## 2. Shale volume from GR

IGR = (GR − GRclean) / (GRshale − GRclean). Linear Vsh = IGR is the conservative (high) estimate. Non-linear corrections reduce it: Larionov tertiary rocks Vsh = 0.083·(2^(3.7·IGR) − 1); older rocks Vsh = 0.33·(2^(2·IGR) − 1) (both Larionov forms computed: each gives Vsh = 0.99 to 1.0 at IGR = 1 and 0 at IGR = 0; the coefficients themselves (gated: unconfirmed, source is paywalled or blocked)). Radioactive non-shale minerals (K-feldspar, mica, uranium in carbonates) inflate GR — use spectral GR (Th+K) or neutron–density separation instead.

## 3. Porosity

- Density porosity: φD = (ρma − ρb) / (ρma − ρf); ρma 2.65 sandstone, 2.71 limestone, 2.87 dolomite; ρf ~1.0–1.1 g/cc depending on mud filtrate (gated: unconfirmed, source is paywalled or blocked).
- Neutron porosity is read on the matrix scale it was recorded (usually limestone units) — convert before comparing.
- Quick-look total porosity in liquid-filled rock: φ ≈ (φN + φD)/2 when both are on the correct matrix.
- **Gas effect:** gas lowers φN and raises φD → crossover (φD > φN). Use φ ≈ √((φN² + φD²)/2). Shale does the opposite (φN ≫ φD). PEF (~1.8 sand, ~5.1 limestone, ~3.1 dolomite (gated: unconfirmed, source is paywalled or blocked)) confirms lithology.
- Effective porosity: φe ≈ φt·(1 − Vsh) as a first pass.

## 4. Rw

- **SP:** SSP = −K·log(Rmfe/Rwe), K ≈ 61 + 0.133·T(°F) mV (gated: unconfirmed, source is paywalled or blocked). Read SSP in a thick, clean, water-bearing sand; convert equivalent to actual resistivities with chart SP-2 or its equations. Unreliable in OBM, with Rmf ≈ Rw, or in thin/shaly beds.
- **Pickett plot:** log(Rt) vs log(φ) in water zones plots as a line of slope −m; the Sw = 100% line intercept at φ = 1 gives a·Rw. Iso-Sw lines are parallel, offset by n·log(Sw). This also checks m.
- Or use produced-water analysis/catalogue Rw — often best.

## 5. Archie water saturation
Algebra checked: Pickett form log Rt = −m log φ + log(a·Rw) − n log Sw follows directly from Archie; Sw = 1 at φ = 1 gives intercept a·Rw.

Sw = ( a·Rw / (φ^m · Rt) )^(1/n).

Defaults: a = 1, m = 2, n = 2 (carbonates/consolidated); Humble sands a = 0.62, m = 2.15 (or a = 0.81, m = 2). Vuggy carbonates m 2.5–3+; fractures m < 2 (all of these (gated: unconfirmed, source is paywalled or blocked)). Use core-measured m and n (SCAL) when available. Archie assumes clean rock: in shaly sands use Simandoux, Indonesia or dual-water/Waxman–Smits, which give lower Sw than Archie. Rt from the deepest resistivity, corrected for invasion (tornado charts) where Rxo and Rt differ.

Bulk volume water BVW = φ·Sw; roughly constant BVW in a zone suggests irreducible water saturation (zone will produce water-free).

## 6. Cutoffs and net pay

Apply in sequence: Vsh < cutoff (often 0.3–0.5 (gated: unconfirmed, source is paywalled or blocked)) → net sand; plus φ > cutoff (e.g. 6–10% sandstone, 3–5% tight carbonate (gated: unconfirmed, source is paywalled or blocked); better tied to a core k–φ cross-plot at k ≈ 0.1–1 mD) → net reservoir; plus Sw < cutoff (often 0.5–0.6 (gated: unconfirmed, source is paywalled or blocked)) → net pay. Report gross, net, N/G, and pay-averaged φ and Sw. Cutoffs are field-specific: derive them from core, tests or the sensitivity of hydrocarbon pore-thickness (φ·(1−Sw)·h) to the cutoff.

## Gotchas

- Washouts (caliper ≫ bit) give low density/high neutron — false shale or false porosity.
- Low-resistivity pay (laminated sand/shale, conductive minerals, fresh vs salty formation water) is missed by Archie with Rt from induction logs; check high-resolution or tri-axial resistivity.
- Neutron on the wrong matrix scale fakes or hides crossover.
- Light hydrocarbons and OBM filtrate both affect shallow reads.
- Using one m/n for all facies hides most of the Sw uncertainty.

## Verify

- [ ] Shale and clean baselines picked per zone; Vsh method stated.
- [ ] Porosity matches core or a second method within ~±2 p.u.
- [ ] Rw from two independent sources (SP, Pickett, water sample) agree.
- [ ] Water zones compute Sw ≈ 1 (sanity check of a, m, n, Rw).
- [ ] Cutoffs documented with their basis; net pay and averages tabulated.
- [ ] Gas crossover zones flagged and porosity corrected.

Net pay and Sw feed the volumetric checks in engineering-technology.petroleum-engineering.reservoir-engineering.decline-curve-analysis-and-reserves and the static model in engineering-technology.petroleum-engineering.petrel-eclipse.building-an-eclipse-simulation-deck.
