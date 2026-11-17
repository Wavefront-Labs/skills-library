---
id: engineering-technology.chemical-engineering.separation-processes.underwood-minimum-reflux
name: underwood-minimum-reflux
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-distillation-shortcuts, underwood-minimum-reflux, underwood-equations, minimum-reflux, shortcut-distillation, feed-quality-q, theta-roots, pinch-zone, multicomponent-distillation]
level: advanced
status: verified
description: "Compute minimum reflux ratio with Underwood's equations: find roots theta between volatilities, handle feed condition q, and treat distributing components."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Underwood minimum reflux

**Goal:** the minimum reflux ratio R_min for the specified split.

## Equations (constant relative volatility and constant molar overflow)
1. Solve for theta: sum_i alpha_i x_F,i / (alpha_i - theta) = 1 - q, where q is the feed thermal condition (q = 1 for saturated liquid, 0 for saturated vapour). The relevant root lies between the relative volatilities of the light and heavy keys: alpha_HK < theta < alpha_LK.
2. Then R_min + 1 = sum_i alpha_i x_D,i / (alpha_i - theta), using the distillate composition from the Fenske distribution (or specified).
For a binary system a single root is used and the result matches the pinch at the feed.

## Procedure
1. Compute alpha_i relative to the heavy key at an average column temperature.
2. Find theta with a bracketed root finder in the key interval.
3. Use the distillate composition at minimum reflux; if non-keys distribute, use the multiple roots (one for each distributing group) and solve the system.
4. Compute R_min; design at a multiple of R_min, commonly 1.1 to 1.5 (economic optimum often around 1.1 to 1.3 for pre-heated feed) (gated: unconfirmed, source is paywalled or blocked), refined by cost.
5. Compute minimum vapour rate V_min = (R_min + 1) D.

## Worked check
Binary, alpha = 2, z_F = 0.5, saturated liquid (q = 1), x_D = 0.95: 2(0.5)/(2 - theta) + 0.5/(1 - theta) = 0 gives theta = 1.333. R_min + 1 = 2(0.95)/(2 - 1.333) + 0.05/(1 - 1.333) = 2.85 - 0.15 = 2.70, so R_min = 1.70 (recomputed; the McCabe-Thiele pinch at x = 0.5, y* = 0.667 gives (0.95 - 0.667)/(0.667 - 0.5) = 1.70, agreeing).

## Gotchas
- Strongly non-ideal mixtures violate constant alpha; use a rigorous minimum reflux calculation (pinch search in a simulator).
- Negative reflux or theta outside the interval indicates infeasible specs.

## Verify
- [ ] Binary check against the McCabe-Thiele pinch construction.
- [ ] R_min positive and below infinity for the specified split.
