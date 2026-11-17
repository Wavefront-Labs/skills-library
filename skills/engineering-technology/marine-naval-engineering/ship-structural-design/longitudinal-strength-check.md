---
id: engineering-technology.marine-naval-engineering.ship-structural-design.longitudinal-strength-check
name: longitudinal-strength-check
category: engineering-technology
field: marine-naval-engineering
product: ship-structural-design
tags: [ship-structural-design, longitudinal-strength, hull-girder, bending-moment, still-water-bending-moment, wave-bending-moment, hogging, sagging, section-modulus, iacs, iacs-ur-s11, iacs-ur-s7, csr, csr-bc-ot, class-rules, dnv, abs, lloyds-register, material-factor, high-tensile-steel, scantlings]
level: advanced
status: gated
description: "Hull girder longitudinal strength to IACS UR S11: still-water envelope, wave bending moments, minimum and required section modulus, stresses, worked example."
sources:
  - "IACS Unified Requirement S11, Longitudinal strength standard (current revision)"
  - "IACS Unified Requirement S7, Minimum longitudinal strength standards"
  - "IACS Common Structural Rules for Bulk Carriers and Oil Tankers (CSR BC&OT)"
  - "Hughes & Paik, Ship Structural Analysis and Design (SNAME)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Longitudinal strength check (IACS UR S11 basis)

**Goal:** show that the midship section has enough section modulus and that hull
girder stresses stay within the permissible value for the governing hogging and sagging
moments. UR S11 (Rev.8 2015 text checked) is the common basis behind most class rules for ships 90-500 m;
bulk carriers and oil tankers use the IACS CSR BC&OT and container ships add UR S11A.
Always work to your class society's current rule edition, which takes precedence.

## 1. Still-water bending moment (Ms)
1. For every loading condition (including ballast, partial and intermediate stages of
   loading and ballast exchange), integrate weight minus buoyancy along the length to
   get shear force and bending moment. Use a loading program or Maxsurf/GHS-style
   longitudinal strength analysis.
2. Take the **envelope**: the largest hogging and sagging Ms at each station. These
   become the permissible still-water values in the loading manual (with margin).

## 2. Wave bending moment (Mw), UR S11
Wave coefficient Cw:
- 90 <= L <= 300 m: Cw = 10.75 - ((300 - L)/100)^1.5
- 300 < L <= 350 m: Cw = 10.75
- 350 < L <= 500 m: Cw = 10.75 - ((L - 350)/150)^1.5

Midship (distribution factor M = 1.0 between 0.4L and 0.65L from the aft end):
- Hogging: Mw = +190 M Cw L^2 B Cb x 10^-3 (kNm)
- Sagging: Mw = -110 M Cw L^2 B (Cb + 0.7) x 10^-3 (kNm)
L is rule length (m), B moulded breadth (m), Cb not less than 0.6.

## 3. Section modulus requirements
1. **Minimum:** Zmin = Cw L^2 B (Cb + 0.7) k x 10^-6 (m3), at deck and at keel. This minimum comes from UR S7, not S11 (gated: unconfirmed, S7 text not fetched; confirm the formula and coefficient there). UR S11.3.1.1(ii) only requires compliance with S7.
   Also check the S11.3.1.2 minimum moment of inertia at midships: Imin = 3 C L^3 B (Cb + 0.7) cm4.
2. **Stress-based:** Zreq = |Ms + Mw| / sigma_p, with sigma_p = 175/k N/mm2 within
   0.4L amidships. In units: Z (cm3) = M (kNm) x 10^3 / sigma (N/mm2).
3. Material factor k: 1.0 for ordinary hull structural steel, below 1.0 for higher tensile steel "according to S4" (S11.3.1.1). Typical values 0.78 (AH32), 0.72 (AH36), 0.68 (AH40) (gated: unconfirmed, UR S4 not fetched).
4. Required Z is the larger of 1 and 2. Outside midships, the rule tapers the
   requirement; check the class rule for the distribution.

## 4. Actual section modulus
1. Include only **continuous longitudinal members** effective over at least 0.4L:
   deck, shell, bottom, inner bottom, longitudinal bulkheads, longitudinals.
   Deduct hatch openings and large lightening holes; exclude short superstructures.
2. Compute neutral axis and I about it; Zdeck = I / (z_deck - z_NA),
   Zkeel = I / z_NA. Under CSR use net (as-built minus corrosion addition) scantlings.
3. Stresses: sigma = (Ms + Mw) / Z at deck and keel, compared with sigma_p.

## Worked mini-example
L = 150 m, B = 24 m, Cb = 0.75, mild steel (k = 1).
- (Arithmetic recomputed: Cw 8.913, sag 767,669 kNm, hog 685,9xx kNm, Zmin 6.98 m3, Zreq 6.67 m3.)
- Cw = 10.75 - (1.5)^1.5 = 10.75 - 1.837 = 8.913.
- Mw sag = 110 x 8.913 x 22 500 x 24 x 1.45 x 10^-3 = about 767 700 kNm.
- Mw hog = 190 x 8.913 x 22 500 x 24 x 0.75 x 10^-3 = about 685 900 kNm.
- Zmin = 8.913 x 22 500 x 24 x 1.45 x 10^-6 = 6.98 m3.
- If the sagging Ms envelope is 400 000 kNm: Zreq = 1 167 700 x 10^3 / 175 cm3
  = 6.67 m3. Zmin governs: design for at least 6.98 m3 at deck and keel.

## Gotchas
- Section modulus is necessary, not sufficient: the deck and bottom panels must
  also pass **buckling** checks, and most failures in service are buckling or fatigue.
- Hull girder **shear** (side shell and longitudinal bulkhead thickness near quarter
  length) has its own rule requirement; do not skip it.
- High-tensile steel lowers k but not stiffness: deflection and fatigue get worse.
- A heavy-ballast or alternate-hold condition often sets the envelope, not full load.
- Ultimate strength (hull girder collapse) is a separate CSR check.

## Verify
- [ ] Ms envelope covers every booklet condition and intermediate stages.
- [ ] Cw, hogging and sagging Mw hand-checked against the software.
- [ ] Z at deck and keel both >= the larger of Zmin and Zreq.
- [ ] Only continuous members counted; openings deducted; net scantlings if CSR.
- [ ] Shear, buckling and fatigue checks run separately and recorded.
