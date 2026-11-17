---
id: engineering-technology.structural-engineering.steel-design.steel-beam-design
name: steel-beam-design
category: engineering-technology
field: structural-engineering
product: steel-design
tags: [steel-design, steel-beam, wide-flange, w-shape, i-beam, universal-beam, flexure, lateral-torsional-buckling, ltb, unbraced-length, cb, compactness, local-buckling, shear, deflection, floor-vibration, aisc-360, lrfd, asd, eurocode-3, en-1993-1-1, as-4100, composite-beam, web-crippling]
level: practitioner
status: verified
description: "Design a rolled steel I-beam for flexure, lateral-torsional buckling, shear and deflection to AISC 360 LRFD, with Eurocode 3 and AS 4100 cross-references."
sources:
  - "ANSI/AISC 360 Specification for Structural Steel Buildings (Chapters B, F, G, J)"
  - "AISC Steel Construction Manual (Parts 1, 3)"
  - "AISC Design Guide 11, Vibrations of Steel-Framed Structural Systems Due to Human Activity"
  - "EN 1993-1-1 Eurocode 3 - Design of steel structures, General rules"
  - "AS 4100 Steel structures"
  - "Salmon, Johnson and Malhas, Steel Structures: Design and Behavior"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Steel beam design — flexure, LTB, shear, serviceability

**Goal:** pick the lightest practical rolled I-section that satisfies strength
(yielding, lateral-torsional buckling, local buckling, shear) and serviceability
(deflection, vibration) for a defined bracing condition.

Clause references below are AISC 360-16/22 LRFD, with US units where formulas are
dimensional. The engineer of record must confirm the governing edition. AISC 360 (aisc.org returned 403), IBC (codes.iccsafe.org returned 403) and EN/AS standards could not be read, so clause numbers and limits are unconfirmed (gated: unconfirmed, source is paywalled or blocked) unless marked computed.

## 1. Set up
1. Determine the factored moment and shear envelopes (e.g. 1.2D + 1.6L; see the
   load-combinations skill). Also get service loads for deflection.
2. **Define Lb:** the distance between points braced against *lateral movement of
   the compression flange or twist of the section*.
   - A metal deck welded or screwed to the top flange braces it for gravity load. It
     does **not** brace the bottom flange under uplift or near continuous supports.
   - Cantilevers and the negative-moment regions of continuous beams have the bottom
     flange in compression.
3. Starting depth: non-composite floor beams at about span/20, composite at about
   span/24, roof purlins at about span/24–/30. These are rules of thumb, not code
   values.

## 2. Flexure (AISC Chapter F2, doubly symmetric compact I-shapes)
- **Compactness (Table B4.1b):**
  - flange: bf/(2tf) ≤ 0.38√(E/Fy) (9.15 at Fy = 50 ksi, computed with E = 29,000 ksi);
  - web: h/tw ≤ 3.76√(E/Fy) (90.6 at Fy = 50 ksi, computed).
  Almost all W-shapes in Fy = 50 ksi steel are compact. The few with non-compact
  flanges are footnoted in the AISC Manual tables, so check the footnote.
- **Plastic moment:** Mp = Fy·Zx, with φb = 0.90.
- **LTB:**
  - Lp = 1.76·ry·√(E/Fy) (42.4·ry at Fy = 50 ksi, computed).
  - Lr comes from the F2-6 expression (it uses rts, J, c, Sx and ho). Read it from
    Manual Table 3-2 rather than recomputing.
  - Lb ≤ Lp: Mn = Mp.
  - Lp < Lb ≤ Lr: Mn = Cb·[Mp − (Mp − 0.7Fy·Sx)·(Lb − Lp)/(Lr − Lp)] ≤ Mp.
  - Lb > Lr: elastic buckling, Fcr from F2-4.
- **Cb** = 12.5Mmax / (2.5Mmax + 3MA + 4MB + 3MC), using the quarter-point moments of
  the unbraced segment. Typical values:
  - 1.0 is the uniform-moment, conservative case;
  - about 1.14 for a uniformly loaded simple span braced only at the ends (computed from the Cb formula: 1.136);
  - about 1.67 for a segment with moment varying linearly to zero (computed: 1.667).
- **Load height:** AISC Cb assumes shear-centre loading. Top-flange (destabilising)
  loads on long unbraced spans are unconservative with plain Cb (see the Commentary).
  EC3 and AS 4100 (load-height factor kl) treat this explicitly.

## 3. Shear (Chapter G)
For most rolled W-shapes, h/tw ≤ 2.24√(E/Fy) (53.9 at Fy = 50 ksi, computed). Then φv = 1.00, Cv1 = 1.0 and
Vn = 0.6·Fy·Aw with Aw = d·tw. Shear rarely governs except for short, heavily loaded
spans, coped ends and transfer beams.

## 4. Local effects at concentrated loads and supports (J10)
Check web local yielding, web crippling and (for unrestrained flanges) sidesway web
buckling. Add bearing stiffeners rather than upsizing the beam. Check coped beams for
block shear and cope buckling (Manual Part 9).

## 5. Serviceability
- Deflection, IBC Table 1604.3 for floors: L/360 under live load and L/240 under total
  load (gated: unconfirmed, source is paywalled or blocked). Brittle finishes, glazing support and long spans often warrant L/480 or an
  absolute cap (e.g. 20–25 mm, roughly 3/4–1 in) under live load.
- Pre-camber for dead load is common on long composite beams (about 0.75–0.8 of the
  wet-concrete deflection). Do not camber beams under about 7.5 m (25 ft) or
  moment-connected beams (practice figures (gated: unconfirmed, source is paywalled or blocked)).
- **Floor vibration** often governs long-span office and lab floors. Use AISC Design
  Guide 11 (walking acceleration against ISO-based limits, e.g. 0.5%g for offices (gated: unconfirmed, source is paywalled or blocked)).
- **Roof ponding:** AISC Appendix 2 for flat roofs.

## 6. Other codes
- **EC3:** Mc,Rd = Wpl·fy/γM0 (Class 1/2), with γM0 = 1.0 recommended (gated: unconfirmed, source is paywalled or blocked). LTB:
  Mb,Rd = χLT·Wpl·fy/γM1, with χLT from the 6.3.2.2 or 6.3.2.3 curves. National
  Annexes alter the curves and the f-factor.
- **AS 4100:** φMs = 0.9·fy·Ze (gated: unconfirmed, source is paywalled or blocked). Member capacity is φMb = φ·αm·αs·Ms ≤ φMs, with
  effective length Le = kt·kl·kr·L.

## Verify
- [ ] Lb is defined per segment, including the bottom flange under uplift and at continuous supports.
- [ ] Compactness is checked (or the Manual footnote is confirmed).
- [ ] Cb is computed per segment, not used as a blanket value, and load height is considered.
- [ ] Shear and concentrated-load web checks are complete.
- [ ] Live and total deflections, plus vibration where relevant, meet the project criteria.
- [ ] Code edition and National Annex values are confirmed by the engineer of record.
