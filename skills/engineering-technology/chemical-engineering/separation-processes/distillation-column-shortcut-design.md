---
id: engineering-technology.chemical-engineering.separation-processes.distillation-column-shortcut-design
name: distillation-column-shortcut-design
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, distillation, fractionation, column-design, shortcut-method, fug, fenske, underwood, gilliland, kirkbride, eduljee, minimum-reflux, minimum-stages, relative-volatility, key-components, tray-efficiency, oconnell, flooding, column-diameter, trays, packing, mccabe-thiele, dstwu, radfrac, aspen-plus, hysys, chemcad]
level: practitioner
status: verified
description: "Shortcut-design a distillation column: key components, Fenske Nmin, Underwood Rmin, Gilliland stages, Kirkbride feed stage, efficiency and diameter by flooding."
sources:
  - "Seader, Henley & Roper, Separation Process Principles (method only)"
  - "Kister, Distillation Design (method only)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shortcut (FUG) design of a distillation column

**Goal:** in an hour, get stage count, reflux, feed location and diameter good enough to
cost the column and to initialise a rigorous model (RadFrac/HYSYS column).

## 1. Specify the split
- Choose **light key (LK)** and **heavy key (HK)**: the adjacent components whose split you
  specify. Set recoveries, e.g. 99% LK overhead and 99% HK in bottoms (or purities).
- Estimate distillate and bottoms by assuming non-keys go entirely to their side (check
  later). Pick column pressure so the condenser can use cooling water: overhead bubble point
  ≥ ~45–50 °C (≈10–15 K approach above warm cooling-water return) (gated: unconfirmed, source is paywalled or blocked); otherwise you need
  refrigeration, or a lower-pressure column if the bottoms would decompose.
- Relative volatility α_LK/HK at top and bottom; use the geometric mean if they differ by
  less than ~30% (gated: unconfirmed, source is paywalled or blocked), otherwise the shortcut is shaky; go straight to rigorous.
- Check for azeotropes first (T-xy, residue curves). FUG assumes none between the keys.

## 2. Fenske: minimum stages (total reflux)
N_min = ln[(x_LK/x_HK)_D · (x_HK/x_LK)_B] / ln α_avg
N_min counts theoretical stages including the partial reboiler.

## 3. Underwood: minimum reflux
Solve Σ α_i z_i /(α_i − θ) = 1 − q for θ between α_HK and α_LK (q = 1 saturated liquid,
q = 0 saturated vapour), then R_min + 1 = Σ α_i x_i,D /(α_i − θ).

## 4. Choose R, then Gilliland
Operating reflux R = 1.2–1.5 R_min (1.2–1.3 for expensive energy; the optimum is flat) (gated: unconfirmed, source is paywalled or blocked).
Gilliland via the Eduljee fit: X = (R − R_min)/(R + 1), Y = 0.75[1 − X^0.5668],
N = (N_min + Y)/(1 − Y).
**Feed stage (Kirkbride):** N_R/N_S = [(B/D)(z_HK/z_LK)(x_LK,B/x_HK,D)²]^0.206.

## Worked example (benzene–toluene, sat. liquid, z = 0.5, α ≈ 2.4)
Specs x_D = 0.95, x_B = 0.05 benzene.
- Fenske: ln(19·19)/ln 2.4 = 5.89/0.875 ≈ **6.7** stages.
- Underwood (q = 1): 1.2/(2.4 − θ) + 0.5/(1 − θ) = 0 → θ ≈ 1.41; R_min + 1 =
  2.28/0.99 − 0.05/0.41 ≈ 2.19 → **R_min ≈ 1.19**.
- R = 1.3·R_min ≈ 1.54. X = 0.14, Y ≈ 0.50, N ≈ (6.7 + 0.50)/0.50 ≈ **14.6** theoretical stages.
- Kirkbride: symmetric split → feed near the middle.
- With 65% overall efficiency: (14.6 − 1 reboiler)/0.65 ≈ 21 trays. Arithmetic recomputed: N_min 6.73, theta 1.412, R_min 1.186, X 0.140, Y 0.504, N 14.6, 20.9 trays. A numerical McCabe–Thiele stepping of the same data gives 14 stages, feed on stage 7 (computed), so the FUG result is within a stage; if yours is not, recheck α.

## 5. Efficiency and hardware
- Overall tray efficiency: O'Connell correlation on α·μ_L (feed viscosity in cP); typically
  50–80% for hydrocarbons, lower (30–50%) for viscous or high-α systems. Packed columns:
  HETP ≈ 0.3–0.6 m for random/structured packing in clean service (vendor data rules) (gated: unconfirmed, source is paywalled or blocked).
- Tray spacing 0.45–0.6 m; add 1–2 m top disengagement and a bottoms sump (3–5 min hold-up
  is a common start; depends on reboiler type and control) (rules of thumb (gated: unconfirmed, source is paywalled or blocked)).

## 6. Diameter from flooding
u_flood = C_sb·√((ρ_L − ρ_V)/ρ_V), C_sb from the Fair flooding chart (≈0.06–0.10 m/s at
0.6 m spacing (gated: unconfirmed, source is paywalled or blocked); read it from the chart for your flow parameter and correct for surface
tension (σ/20)^0.2). Design at 70–85% of flood; net area ≈ 85–90% of column area after
downcomers. D = √(4·V_vol/(π·u_design·A_net/A)). Size at both top and bottom; use the larger
or swage. Check weeping at turndown.

## Gotchas
- Distributing non-keys: if a component has α between the keys, Fenske at total reflux tells
  you its split; don't assume it all goes one way.
- Sub-cooled reflux and feed enthalpy change internal flows; q > 1 for cold feed.
- High-purity specs (ppm) make N_min and R_min extremely sensitive to α; use rigorous.
- Aspen DSTWU gives exactly this method; use it to seed RadFrac, not to finalise
  (see engineering-technology.chemical-engineering.aspen.flowsheet-building-and-convergence).

## Verify
- [ ] Keys, recoveries and pressure justified; azeotrope check done.
- [ ] N_min, R_min, R and N calculated and reproduced in DSTWU or by McCabe–Thiele.
- [ ] Real trays/packing height from a stated efficiency/HETP source.
- [ ] Diameter at ≤ 85% flood at top and bottom, turndown checked.
- [ ] Rigorous model initialised from these values matches product specs.
