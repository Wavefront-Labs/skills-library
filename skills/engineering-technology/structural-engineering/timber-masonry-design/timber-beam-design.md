---
id: engineering-technology.structural-engineering.timber-masonry-design.timber-beam-design
name: timber-beam-design
category: engineering-technology
field: structural-engineering
product: timber-masonry-design
tags: [timber-masonry-design, timber-beam, wood-beam, joist, glulam, sawn-lumber, lvl, nds, asd, lrfd, adjustment-factors, load-duration, cd, size-factor, volume-factor, beam-stability, creep, deflection, notches, bearing, eurocode-5, en-1995-1-1, kmod, kdef, as-1720]
level: practitioner
status: verified
description: "Design a sawn or glulam timber beam to NDS (ASD/LRFD) with Eurocode 5 notes: adjustment factors, bending, shear, bearing, creep deflection and lateral stability."
sources:
  - "AWC National Design Specification (NDS) for Wood Construction and NDS Supplement"
  - "EN 1995-1-1 Eurocode 5 - Design of timber structures, General"
  - "Breyer, Cobeen, Fridley and Pollock, Design of Wood Structures - ASD/LRFD"
  - "AS 1720.1 Timber structures - Design methods"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Timber beam design — the adjustment factors are the design

**Goal:** a joist, header or glulam beam that passes bending, shear, bearing and
long-term deflection checks with every applicable adjustment factor applied, and
none that don't apply.

References are NDS 2018/2024 (US). EC5 notes use the recommended values, which
National Annexes may change. The engineer of record must confirm the governing edition. Checked this session against AWC's free NDS 2018 PDFs (Chapter 2 and Appendix N, text extracted): CD, KF, φb and λ below (F). Other NDS clauses, EN 1995 and AS 1720 values were not readable and are unconfirmed (gated: unconfirmed, source is paywalled or blocked).

## 1. Inputs
- Species, grade and size. Take reference values (Fb, Fv, Fc⊥, E, Emin) from the NDS
  Supplement table for that product. Sawn dimension lumber, timbers, glulam stress
  classes and SCL (LVL/PSL, manufacturer values) all differ.
- Service conditions: moisture (dry service is below 19% MC for sawn lumber),
  temperature, treatment (incising), and load duration.

## 2. Adjusted bending stress (ASD)
F′b = Fb × CD × CM × Ct × CL × CF × Cfu × Ci × Cr (sawn lumber). For glulam, use CV in
place of CF and apply only the lesser of CL and CV.

- **CD (load duration):**
  - permanent: 0.9;
  - occupancy live: 1.0;
  - snow: 1.15;
  - construction: 1.25;
  - wind/seismic: 1.6.
  Check **each** load combination with its own CD. D alone at 0.9 can govern for
  heavily dead-loaded beams.
- **Cr (repetitive member):** 1.15 for three or more dimension-lumber members at
  24 in (610 mm) or less on centre, connected by load-distributing sheathing (gated: unconfirmed, source is paywalled or blocked).
- **CF (size):** from the Supplement. Deeper sawn members get less than 1.0.
- **CL (beam stability, NDS 3.3.3):**
  - CL = 1.0 when the compression edge is continuously braced and the ends are held
    against rotation;
  - otherwise compute RB = √(le·d/b²), with RB ≤ 50, and le from Table 3.3.3.
  The NDS 4.4.1 depth-to-breadth rules give quick bracing requirements (for example
  d/b ≤ 2 needs no lateral support (gated: unconfirmed, source is paywalled or blocked)).
- **LRFD:** multiply the reference value by KF (2.54 for bending), φb = 0.85 and the
  time effect factor λ in place of CD (NDS 2018 Tables N1 to N3: KF 2.54, φb 0.85). λ is 0.6 for 1.4D; for 1.2D + 1.6L + 0.5(Lr or S or R) it is 0.8 for occupancy live load, 0.7 for storage and 1.25 for impact; 0.8 for 1.2D + 1.6(Lr or S or R) + (L or 0.5W); and 1.0 for the wind and seismic combinations. Table N3 is keyed to ASCE 7-16 combinations; check the 2024 table for that edition.

## 3. Checks
1. **Bending:** fb = M/S ≤ F′b.
2. **Shear:** fv = 1.5V/(b·d) ≤ F′v. For uniformly loaded beams you may ignore loads
   within d of the support face.
3. **Bearing perpendicular to grain:** fc⊥ = R/(b·lb) ≤ F′c⊥. Short bearing on top
   plates and hangers often governs. Cb increases capacity for bearings less than 6 in
   long that are at least 3 in from the member end (gated: unconfirmed, source is paywalled or blocked).
4. **Notches (NDS 3.2.3, 3.4.3):**
   - sawn-lumber end notches on the tension side at most d/4 (gated: unconfirmed, source is paywalled or blocked);
   - no notches in the middle third of the span (gated: unconfirmed, source is paywalled or blocked);
   - the reduced shear capacity at a tension-side end notch must be checked;
   - avoid notching glulam without engineering.

## 4. Deflection and creep
- Total long-term deflection, NDS 3.5.2: Δ = Kcr·ΔLT + ΔST.
  - Kcr = 1.5 for seasoned lumber, glulam and SCL in dry service (gated: unconfirmed, source is paywalled or blocked);
  - Kcr = 2.0 for unseasoned or wet service (gated: unconfirmed, source is paywalled or blocked).
  Put permanent load (and sustained live, e.g. storage) in ΔLT.
- Common limits (IBC Table 1604.3): floors L/360 under live load and L/240 under
  total load (gated: unconfirmed, source is paywalled or blocked).
- **Floor bounce:** many designers use L/480 under live load or a stiffness and
  frequency criterion. Joists that meet L/360 can still feel lively.
- **Rough sizing:** floor joists span about 18–22 × depth, and glulam floor beams
  about 15–20 × depth. These are rough rules only.

## 5. Eurocode 5 summary
- fm,d = kmod·fm,k/γM.
  - γM = 1.3 for solid timber and 1.25 for glulam (recommended values (gated: unconfirmed, source is paywalled or blocked)).
  - kmod for service class 1/2 is about 0.6 permanent, 0.8 medium-term and 0.9
    short-term (gated: unconfirmed, source is paywalled or blocked). Use the kmod of the shortest-duration action in the combination.
- kh is the depth factor, and kcrit handles lateral torsional buckling.
- Final deflection: w_fin = w_inst·(1 + kdef), with variable actions taken at ψ2.
  kdef for solid timber is 0.6 in service class 1 and 0.8 in class 2 (gated: unconfirmed, source is paywalled or blocked).
- Australia (AS 1720.1): φ·k1·k4·k6·k9·k12·f′b·Z, using the duration factor k1.
  Cross-check the factor set before use.

## Verify
- [ ] Reference values come from the correct Supplement table or manufacturer data for the product.
- [ ] Every combination is checked with its own CD (or λ or kmod).
- [ ] CL or bracing is justified. CV and CL are not stacked for glulam.
- [ ] Bending, shear (with notches) and bearing are all checked.
- [ ] Creep-adjusted deflection meets the limits, with vibration or bounce considered for floors.
- [ ] NDS/EC5/AS edition and National Annex are confirmed by the engineer of record.
