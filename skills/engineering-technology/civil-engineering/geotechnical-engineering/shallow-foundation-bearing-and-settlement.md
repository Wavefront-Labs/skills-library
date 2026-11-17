---
id: engineering-technology.civil-engineering.geotechnical-engineering.shallow-foundation-bearing-and-settlement
name: shallow-foundation-bearing-and-settlement
category: engineering-technology
field: civil-engineering
product: geotechnical-engineering
tags: [geotechnical-engineering, foundation-design, shallow-foundation, pad-footing, strip-footing, spread-footing, bearing-capacity, bearing-resistance, settlement, consolidation, terzaghi, meyerhof, vesic, brinch-hansen, eurocode-7, en-1997, design-approach-1, aashto-lrfd, lrfd, allowable-stress-design, factor-of-safety, spt, cpt, schmertmann, effective-width, site-investigation, soil-mechanics]
level: practitioner
status: verified
description: "Design a pad or strip footing: interpret site investigation, compute bearing resistance (Terzaghi/Meyerhof, Eurocode 7 DA1 vs LRFD), and check settlement limits."
sources: ["EN 1997-1 Eurocode 7: Geotechnical design - Part 1, incl. Annex D", "AASHTO LRFD Bridge Design Specifications, Section 10", "Das, Principles of Foundation Engineering", "Terzaghi, Peck & Mesri, Soil Mechanics in Engineering Practice", "Bond & Harris, Decoding Eurocode 7", "FHWA GEC 6: Shallow Foundations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Shallow foundation design — bearing resistance and settlement, done in the right order

**Goal:** size a pad or strip footing so that (a) bearing failure has the required
margin under the governing code and (b) total and differential settlement stay within
what the structure tolerates. In practice settlement governs more often than bearing.

## 1. Read the site investigation for the design profile
1. From boreholes/CPTs, draw a **design soil profile**: layers, groundwater level
   (and its seasonal high), and parameters per layer with how each was derived.
2. Decide **drained vs undrained**: clays under rapid loading → undrained (cu)
   short-term *and* drained (c′, φ′) long-term; sands → drained only.
3. Correlations to state explicitly: SPT N60 → φ′ (e.g. Peck/Hanson/Thornburn or
   similar charts (gated: unconfirmed, source is paywalled or blocked)), CPT qc → φ′ and constrained modulus, cu from CPT using Nkt
   ≈ 10–20 (site-calibrate) (gated: unconfirmed, source is paywalled or blocked). Choose **characteristic values** as a cautious estimate
   (EC7 2.4.5.2), not the mean of the test results.
4. Founding depth: below topsoil, fill, the zone of seasonal moisture change (reactive
   clays) and frost depth.

## 2. Bearing resistance (general formula)
q_ult = c′·Nc·sc·dc·ic + q·Nq·sq·dq·iq + 0.5·γ′·B′·Nγ·sγ·dγ·iγ

- Nq = e^(π tanφ′)·tan²(45° + φ′/2); Nc = (Nq − 1)·cot φ′.
- Nγ differs by author: EC7 Annex D uses 2(Nq − 1)tanφ′; Vesic uses 2(Nq + 1)tanφ′;
  Meyerhof and Brinch Hansen give lower values (the two Nγ forms were seen in secondary sources only (gated: unconfirmed, source is paywalled or blocked)). State which you used.
- **Undrained:** q_ult = (π + 2)·cu·sc + q, with sc = 1 + 0.2·B′/L′ (EC7 Annex D; the (π + 2) form and this sc confirmed in the JRC Eurocode training slides by Frank, eurocodes.jrc.ec.europa.eu, fetched).
- **Eccentric load:** effective dimensions B′ = B − 2e_B. Keep e within B/6 so the
  whole base stays in contact (more stringent limits apply to some foundations;
  check your code).
- **Groundwater:** if the water table is within about B below the founding level, use
  the submerged unit weight γ′ in the Nγ term (and in q if it is above founding level).
- Inclined loads and sloping ground need the i and slope factors; they reduce resistance
  sharply and are easy to forget.

## 3. Apply the code's safety format
- **Traditional ASD:** q_allow = q_ult / FS with FS = 2.5–3.0 on bearing (3 is common) (gated: unconfirmed, source is paywalled or blocked).
- **Eurocode 7 Design Approach 1** (used in the UK and some others; check the national
  annex — many countries use DA2):
  - Combination 1: actions γG = 1.35, γQ = 1.5; material factors 1.0.
  - Combination 2: γG = 1.0, γQ = 1.3; tan φ′ and c′ factored by 1.25, cu by 1.4 (these combinations and R = 1.0 for spread-foundation bearing match the JRC/Frank training slides; confirm in EN 1997-1 Annex A and the national annex).
  - Show Vd ≤ Rd for both; Combination 2 usually governs bearing.
- **US AASHTO LRFD:** factored load ≤ φb·q_n. Resistance factors for bearing on soil
  are about 0.45–0.50 depending on soil type and method (gated: unconfirmed, source is paywalled or blocked) —
  confirm the exact value for your method and edition.

## 4. Settlement
- **Sands:** Schmertmann's strain-influence method from CPT, or Burland & Burbidge from
  SPT. Elastic theory with a modulus correlated from CPT is acceptable if stated.
- **Clays:** immediate (undrained elastic) + primary consolidation
  (Cc or Cr from oedometer, using σ′p — the preconsolidation pressure — to choose which)
  + secondary compression for organic soils. Time from cv.
- **Limits (rules of thumb):** ~25 mm total for isolated footings on sand with ~20 mm
  differential (Terzaghi & Peck); angular distortion 1/500 as a safe limit for framed
  buildings (Bjerrum), 1/300 for first cracking in panels (all of the settlement limits here are (gated: unconfirmed, source is paywalled or blocked)). Use the structural engineer's
  actual tolerances when available.
- Settlement is computed with **unfactored (SLS)** loads and characteristic parameters.

## Gotchas
- Big footings fail on settlement, small footings on bearing — check both every time.
- Nγ and the depth factors carry most of the disagreement between methods; many
  practitioners ignore depth factors (d = 1) because the overburden may be removed later.
- Interbedded soft layers under a stiff crust: check punching through to the weak layer
  (load-spread or two-layer method).
- Reactive (expansive) clays and collapsible soils need different design approaches;
  bearing formulas don't address them.

## Verify
- [ ] Characteristic parameters and groundwater are stated with their derivation.
- [ ] Both short-term (undrained) and long-term (drained) cases checked for clays.
- [ ] Bearing resistance uses effective width for eccentric loads and the right γ′.
- [ ] The safety format matches the governing code and national annex (FS, DA1/DA2, or LRFD φ).
- [ ] Total and differential settlement computed with SLS loads and compared with stated tolerances.
- [ ] Founding depth clears fill, topsoil, frost and seasonal moisture zones.
