---
id: engineering-technology.aerospace-engineering.aircraft-structures.wing-box-sizing
name: wing-box-sizing
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, wing-box, semi-monocoque, thin-walled, skin-stringer, spar, rib, panel-buckling, shear-flow, bredt-batho, bending-moment, limit-load, ultimate-load, factor-of-safety, margin-of-safety, far-25, cs-25, v-n-diagram, mmpds, a-basis, b-basis, fatigue, damage-tolerance, composites, schrenk]
level: advanced
status: gated
description: "Size a semi-monocoque wing box: limit/ultimate loads, spanwise shear and bending, skin-stringer panel buckling, spar webs, margins of safety."
sources:
  - "https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-14?part=25&section=25.337"
  - "https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-14?part=25&section=25.305"
  - "https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-14?part=25&section=25.625"
  - "https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-14?part=25&section=25.571"
  - "https://en.wikipedia.org/wiki/Buckling"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Wing-box sizing — from flight envelope to skin, stringer and spar thicknesses

**Goal:** a first-pass wing box with positive margins of safety at every station for the
critical ultimate loads, ready for detailed FEM and fatigue checks.

## 1. Loads definition (regulation sets the factors)
- **Limit load** = maximum expected in service; **ultimate = 1.5 × limit** (FAR/CS 25.303) (gated: unconfirmed, source is paywalled or blocked)
  unless another factor is specified. No detrimental permanent deformation at limit
  (25.305), no failure at ultimate for at least 3 s.
- Manoeuvre envelope (25.337): positive limit n from `2.1 + 24000/(W + 10000)` (W in lb),
  not less than 2.5 and need not exceed 3.8, with W the design maximum takeoff weight
  (25.337(b)); negative limit not less than −1.0 up to Vc, varying linearly to zero at Vd.
  Gust loads often govern for light wing loadings and outboard
  stations. Build the V-n diagram and keep both.
- Special factors: fitting factor of at least 1.15 (25.625) unless the fitting is proven by tests simulating actual stress conditions or the joint is made under approved practices backed by comprehensive test data; castings and bearing factors where applicable.
- Load cases to carry forward: +n at max weight with min fuel in wing (max root bending),
  −1 g, gust, roll manoeuvre (torsion), landing and taxi (download), fuel-tank pressure.

## 2. Spanwise shear, bending and torsion
1. Lift distribution: Schrenk's approximation for quick work; VLM or CFD loads later.
2. Subtract **inertia relief**: wing structure, fuel, engines/nacelles (as point loads).
   Ignoring fuel relief over-sizes the root; the critical case is often low fuel.
3. Integrate from tip inboard: shear `V(y)`, bending `M(y)`, torque `T(y)` about the
   flexural axis. Correct for sweep by working along the structural axis.

## 3. Idealise and size the covers (bending)
- Treat each cover as an effective panel: running load `N_x ≈ M / (h_eff · w_box)`,
  with `h_eff` the mean spar height between cover centroids and `w_box` the box width.
- **Upper cover (compression)** is stability-critical:
  - skin buckling between stringers: `σ_cr = k π² E / [12 (1 − ν²)] · (t/b)²`; k ≈ 4 for
    simply supported edges (≈ 3.6 E (t/b)² with ν = 0.3). Skins are commonly allowed to
    buckle above some fraction of limit load in metal transports; then use effective
    width (von Kármán) for the post-buckled skin.
  - stringer column buckling between ribs (Euler–Johnson with the effective skin), plus
    local crippling of stringer flanges (a flanged section can carry load in its corners after the flanges buckle locally; crippling is failure of the whole section).
  - Rib pitch is the main lever on column and panel stability; take a starting value from
    similar structures and iterate.
- **Lower cover (tension)** is usually fatigue/damage-tolerance critical, not static:
  hold 1 g stress well below static capability. Choose cover alloys and tempers from the
  programme's material specification.

## 4. Spars and webs (shear and torsion)
- Shear flow from vertical shear split by spar stiffness; torsion via Bredt–Batho
  `q = T / (2 A_enclosed)` for the closed cell (multi-cell boxes need compatibility of
  twist rate).
- Web shear buckling: `τ_cr = k_s π² E / [12 (1 − ν²)] · (t/b)²`, k_s taken from a plate-buckling reference for the
  edge conditions and aspect ratio. Post-buckled diagonal tension
  (Wagner beams) is standard for metal webs but loads the stiffeners and flanges, so size
  them for it.

## 5. Margins of safety
`MS = allowable / (applied_limit × 1.5 × special factors) − 1 ≥ 0`.
- Allowables: use the statistically based values the certification basis requires
  (MMPDS values for metals; composites from test-based allowables).
- Composites: apply environmental knock-downs (hot/wet), BVID compression-after-impact
  allowables and the certification-basis statistics; open-hole compression often sizes the skin.
- Aim for small positive margins at sizing; large margins are weight,
  negative margins are a redesign.

## 6. Then check what static sizing misses
- Fatigue and damage tolerance (25.571): crack growth and residual strength, inspection
  intervals; lower cover and joints at root.
- Aeroelastic: torsional stiffness for divergence/flutter and aileron reversal; the box
  may need thicker skins than strength alone suggests.
- FEM confirms load paths, but check the FEM free-body sums against your hand loads.

## Verify
- [ ] V-n envelope built and all critical cases (manoeuvre, gust, −1 g, low-fuel) run.
- [ ] Shear and bending diagrams include inertia relief and close to zero at the tip.
- [ ] Every station has MS ≥ 0 for strength and stability at ultimate.
- [ ] Upper-cover buckling and crippling checked against rib pitch and stringer spacing.
- [ ] Lower cover 1 g stress compatible with fatigue targets.
- [ ] Hand-calculated root bending matches FEM reaction within a few percent.

## Checked
2026-11-01. Confirmed in the eCFR text: 25.337(b) manoeuvre load factor formula (W is design maximum takeoff weight, floor 2.5, cap 3.8), 25.337(c) negative factor, 25.305 (limit load without detrimental deformation, ultimate for at least 3 seconds), 25.625 fitting factor 1.15 with its exceptions, 25.571 as the fatigue and damage-tolerance rule. Confirmed in Wikipedia Buckling: crippling and diagonal tension (Wagner beams). The plate buckling constant 4 pi^2 / (12 (1 - 0.3^2)) = 3.62 for k = 4 was computed (python). Removed: rib pitch range, alloy tempers, cover depth ratio, k_s value, A/B-basis wording, margin target, 25.341 and 25.613 citations, Schrenk and Needham/Gerard detail. Gated: the 1.5 ultimate factor from 25.303 (the eCFR page returned only a stub).
Method: documentation only; no commands were run.
