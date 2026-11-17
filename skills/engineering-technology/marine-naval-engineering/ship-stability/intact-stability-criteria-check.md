---
id: engineering-technology.marine-naval-engineering.ship-stability.intact-stability-criteria-check
name: intact-stability-criteria-check
category: engineering-technology
field: marine-naval-engineering
product: ship-stability
tags: [ship-stability, intact-stability, is-code, is-code-2008, imo, solas, gz-curve, righting-lever, metacentric-height, gm, free-surface-correction, kn-curves, weather-criterion, downflooding-angle, loading-condition, stability-booklet, limiting-kg, maxsurf-stability, ghs]
level: practitioner
status: verified
description: "Check a loading condition against IMO IS Code 2008: GM with free-surface correction, GZ curve areas 0.055/0.09/0.03 m·rad, GZ 0.20 m, weather criterion."
sources:
  - "IMO International Code on Intact Stability, 2008 (IS Code), resolution MSC.267(85), as amended"
  - "IMO MSC.1/Circ.1281 explanatory notes to the IS Code"
  - "Barrass & Derrett, Ship Stability for Masters and Mates"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Intact stability check to the IS Code 2008

**Goal:** for one loading condition, compute the corrected GM and GZ curve and show,
criterion by criterion, that it meets IS Code 2008 Part A (general cargo and passenger
ship baseline). Ship-type rules (grain, timber deck cargo, high-speed craft, offshore
vessels) add or replace criteria; check which Part B or other code applies.

## 1. Build the condition
1. Sum weights: lightship (from the inclining experiment) + every deadweight item and
   tank. For each: mass, LCG, VCG (KG), TCG. Displacement W = sum m; KG = sum(m KG)/W.
2. Find draft and trim from hydrostatics at W and LCG (free-trim).
3. **Free-surface correction:** for each slack tank FSM = rho_tank x i_t, where
   i_t = l b^3 / 12 for a rectangular tank. The IS Code calls for the maximum
   free-surface effect for each tank type that may be slack (check the code's
   rules for which tanks to include and the small-tank exemptions).
   GG' = sum FSM / W. Fluid KG = KG + GG'.
4. GM0 = KM - KG(fluid).

## 2. Compute the GZ curve
GZ(theta) = KN(theta) - KG(fluid) sin(theta), using KN cross curves at the actual
displacement and free trim, from 0 to at least 60 deg or the vanishing angle.
Find the **downflooding angle theta_f**: the heel at which a non-weathertight
opening (air pipe, vent, door) immerses. Areas are truncated there.

## 3. General criteria (IS Code Part A, 2.2)
Checked against the full text of resolution MSC.267(85) Annex 2 (copy hosted by the University of Cantabria): 2.2.1 areas 0.055, 0.09, 0.03 m.rad, 2.2.2 GZ 0.2 m at 30 deg or more, 2.2.3 max GZ at 25 deg or more, 2.2.4 GM0 0.15 m, 2.3.1 weather criterion (16 deg or 80% of deck-edge immersion, area b >= area a, theta_2 the least of theta_f, 50 deg, theta_c), 2.3.2 P = 504 Pa and lw2 = 1.5 lw1, 2.3.4 roll angle 109 k X1 X2 sqrt(r s), 3.1.3 maximum free-surface effect for variable-level tanks.

| Criterion | Requirement |
|---|---|
| Area under GZ 0-30 deg | >= 0.055 m.rad |
| Area 0-40 deg, or 0-theta_f if less | >= 0.090 m.rad |
| Area 30-40 deg, or 30-theta_f if less | >= 0.030 m.rad |
| GZ at an angle >= 30 deg | >= 0.20 m |
| Angle of max GZ | >= 25 deg (2.2.3; the Administration may accept an equivalent-safety alternative if not practicable) |
| Initial GM0 (corrected) | >= 0.15 m |

Integrate with Simpson's rule at 5 deg spacing or finer, and convert degrees to
radians (1 rad = 57.3 deg). Example: GZ at 0, 10, 20, 30 deg = 0, 0.12, 0.28,
0.44 m. Simpson's 3/8 over 0-30 with h = 10 deg = 0.1745 rad:
A = 3/8 x 0.1745 x (0 + 3x0.12 + 3x0.28 + 0.44) = 0.0654 x 1.64 = 0.107 m.rad, pass.

## 4. Severe wind and rolling (weather) criterion, 2.3
1. Steady wind lever lw1 = P A Z / (1000 g W), with P = 504 N/m2 (unless the
   Administration allows a reduced value for restricted service), A = projected
   lateral windage area above the waterline (m2), Z = vertical distance from the
   centre of A to the centre of underwater lateral area or roughly half draft (m),
   W in tonnes.
2. Gust lever lw2 = 1.5 lw1.
3. Steady heel theta_0 under lw1 must not exceed 16 deg or 80 % of the deck-edge
   immersion angle, whichever is less.
4. Roll angle theta_1 = 109 k X1 X2 sqrt(r s), with factors from the code's tables
   (bilge keels, B/T, Cb, roll period). Roll back to theta_0 - theta_1.
5. Area b (from the lw2 intersection to the lesser of 50 deg, theta_f, or the second
   lw2 intersection) must be >= area a (windward side): b >= a.

## Gotchas
- Using KN at the wrong displacement, or at fixed trim when the vessel trims heavily
  when heeled, overstates GZ.
- A forgotten air pipe can pull theta_f below 40 deg (35 deg, for example) and fail the 0-40 area on paper.
- Free-surface effect from small tanks adds up; do not drop it without the code's
  exemption test.
- Superstructures count as buoyant only if they are weathertight and modelled as such.
- Grain ships use their own criteria: IS Code 3.4 requires compliance with the International Code for the Safe Carriage of Grain in Bulk (MSC.23(59)); read its numeric criteria there and do not apply Part A alone.

## Verify
- [ ] KG includes the free-surface correction; GM0 >= 0.15 m.
- [ ] All three areas computed with correct truncation at theta_f, in m.rad.
- [ ] GZ >= 0.20 m at or beyond 30 deg; max GZ at >= 25 deg.
- [ ] Weather criterion: theta_0 limit and b >= a both shown.
- [ ] Every condition in the stability booklet checked, including arrival with
      10 % consumables, which is often the worst.
