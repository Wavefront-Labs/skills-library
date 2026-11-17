---
id: engineering-technology.structural-engineering.foundation-design.pad-footing-design
name: pad-footing-design
category: engineering-technology
field: structural-engineering
product: foundation-design
tags: [foundation-design, pad-footing, spread-footing, isolated-footing, column-footing, shallow-foundation, bearing-pressure, eccentricity, kern, punching-shear, two-way-shear, one-way-shear, footing-reinforcement, dowels, development-length, aci-318, eurocode-2, eurocode-7, as-3600, reinforced-concrete, overturning, uplift]
level: practitioner
status: verified
description: "Structurally design an isolated RC pad footing: plan size from SLS bearing, eccentricity, punching and one-way shear, flexural steel and detailing to ACI 318 / EC2."
sources:
  - "ACI 318 Building Code Requirements for Structural Concrete (Chapters 13, 22, 25)"
  - "EN 1992-1-1 Eurocode 2 (sections 6.4 and 9.8)"
  - "EN 1997-1 Eurocode 7 - Geotechnical design"
  - "Wight, Reinforced Concrete: Mechanics and Design (footings chapter)"
  - "Bowles, Foundation Analysis and Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Pad footing design — plan size from the soil, thickness from punching

**Goal:** an isolated column footing whose plan area satisfies the geotechnical
bearing and settlement criteria at service load. Its depth and reinforcement must
satisfy punching, one-way shear, flexure and load transfer at factored load.

Bearing capacity and settlement themselves are covered in
`engineering-technology.civil-engineering.geotechnical-engineering.shallow-foundation-bearing-and-settlement`.
This skill starts from the allowable (or factored) bearing pressure the geotechnical
engineer provides. Clauses are ACI 318-19 unless noted, and the engineer of record
must confirm the governing edition. ACI 318 and EN 1992 are paywalled: clause numbers and coefficients are unconfirmed against the text (gated: unconfirmed, source is paywalled or blocked). The geometric pressure formulas in section 1 were computed (kern stress 200 and 22.2 kPa for P=1000 kN, B=L=3 m, e=0.4 m; partial-contact q_max = 2P/(3L(B/2−e)) equals 2P/(L × 3(B/2−e)) for the triangular block) and the referenced skill ids resolve.

## 1. Plan size (service loads)
1. Take the service axial load P, the moments M and the horizontal shears H at the
   column base. Add the footing and backfill weight, or use a net allowable pressure
   with only the excess over removed soil.
2. Required area: A ≥ P/q_allow. Square footings for concentric columns; rectangular
   ones where the plan is constrained or the moment is one-way.
3. **Eccentricity** e = M/P (include H × footing depth):
   - e ≤ B/6 (within the kern): q = (P/A)·(1 ± 6e/B);
   - e > B/6: partial contact. q_max = 2P / (3·L·(B/2 − e)).
   Avoid partial contact under sustained load. Under wind or seismic it may be
   acceptable if overturning has a factor of safety of at least 1.5 (or EQU factors
   pass).
4. Check uplift and sliding (friction μ ≈ tan(2/3 φ′) as a typical assumption (gated: unconfirmed, source is paywalled or blocked), from
   geotechnical advice) for the 0.9D or 0.6D cases.

## 2. Depth (factored loads)
Use the factored net pressure qu = Pu/A, excluding the self-weight of footing and
soil, which cancels in shear and flexure.
1. **Two-way (punching) shear** at d/2 from the column face (perimeter b0):
   - φVc = 0.75 × min(4, 2 + 4/β, αs·d/b0 + 2) × λs·λ·√f′c·b0·d (psi units), with
     αs = 40 for an interior column;
   - net shear Vu = qu × (A − area inside the perimeter).
   ACI 318-19 introduced the size-effect factor λs for two-way shear. How it applies
   to footings (13.2.7 and 22.6) is unconfirmed (gated: unconfirmed, source is paywalled or blocked), so check your
   edition. Punching usually sets the thickness.
2. **One-way shear** at d from the face: φVc = 0.75 × 2λ√f′c·b·d. Footings do not need
   stirrups, so make the section deep enough.
3. **Minimum depth:** at least 6 in (150 mm) above the bottom bars (ACI 13.3.1.2).
   Practically use 300 mm (12 in) or more, and aim for a depth that avoids shear
   reinforcement.
4. **EC2:** check punching at control perimeters within 2d. For footings, 6.4.4 lets
   you deduct the soil pressure inside the perimeter, so iterate on the critical
   distance a ≤ 2d. Use vRd,c = CRd,c·k·(100ρl·fck)^(1/3)·(2d/a), with
   CRd,c = 0.18/γc.

## 3. Flexure
- Critical section at the column face (or halfway between face and edge of a steel
  base plate). Mu = qu·B·c²/2, where c is the cantilever length.
- Use As from the RC beam method (see `rc-beam-design`). As,min = 0.0018·b·h for
  Grade 60. This is the slab minimum (ACI 7.6.1.1 / 24.4.3.2), which designers
  conventionally apply to footings (gated: unconfirmed, source is paywalled or blocked). Check how your edition words it.
- **Rectangular footings:** short-direction steel is concentrated in a central band
  of width B: γs = 2/(β + 1) of the total in the band, where β = long/short ratio
  (ACI 13.3.3.3).
- **Spacing:** at most 3h or 18 in. 150–300 mm (6–12 in) is typical.

## 4. Load transfer and detailing
- **Bearing at the column interface:** φ = 0.65, with strength 0.85f′c·A1·√(A2/A1)
  and √(A2/A1) ≤ 2.
- **Dowels:** at least 0.005Ag of the column (ACI 16.3.4.1). Develop them in
  compression into the footing (ldc) and in tension where the column has uplift or
  moment. Hooked dowels resting on the bottom mat are typical. Footing depth often
  governs from ldc.
- **Cover:** 3 in (75 mm) cast against earth. Use a blinding layer.
- Check the development length of the bottom bars from the critical section to the
  footing edge. Use hooks if short.

## Verify
- [ ] Service bearing pressure ≤ allowable, including footing and soil weight, at the governing eccentricity.
- [ ] Overturning, sliding and uplift are checked for the minimum-dead combinations.
- [ ] Punching (b0 at d/2, or EC2 perimeters) and one-way shear pass without stirrups.
- [ ] Flexural steel ≥ minimum, with band steel for rectangular footings and spacing limits met.
- [ ] Bearing, dowel area and development lengths are satisfied.
- [ ] The geotechnical parameters and the code edition are confirmed with the geotechnical engineer and the engineer of record.
