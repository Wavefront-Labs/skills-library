---
id: engineering-technology.aerospace-engineering.aircraft-structures.s-n-curves-and-mean-stress
name: s-n-curves-and-mean-stress
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [s-n-curve, fatigue, mean-stress, goodman, stress-concentration, metallic-fatigue]
level: practitioner
status: draft
description: "Use S-N curves for metallic airframe fatigue with mean-stress corrections, stress concentration factors and R-ratio, and know what the curve does not capture."
sources:
  - "Niu, Airframe Structural Design"
  - "MMPDS (fatigue data chapters)"
  - "Schijve, Fatigue of Structures and Materials"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# S-N curves and mean stress

**Goal:** fatigue life estimate from stress amplitude and mean for a detail.

## Terms
- Stress ratio `R = sigma_min/sigma_max`; amplitude `sigma_a = (sigma_max - sigma_min)/2`; mean `sigma_m`.
- A published S-N curve belongs to a stated `R`, notch (`Kt`) and material. Use the curve that matches the detail.
- Basquin form for the high-cycle range: `sigma_a = sigma_f' * (2N)^b`.

## Mean-stress corrections (to an equivalent `R = -1` amplitude)
- Goodman: `sigma_a / S_e + sigma_m / S_u = 1`, conservative for tension means.
- Gerber: `sigma_a / S_e + (sigma_m / S_u)^2 = 1`, fits ductile metals better.
- Walker or Smith-Watson-Topper forms fit data better with fitted exponents; use when test data exist.
- Compressive mean stress is usually beneficial; do not extend Goodman into it blindly.

## Procedure
1. Find the local stress at the detail, including `Kt`. Use the fatigue notch factor `Kf <= Kt` (notch sensitivity) if the curve is for unnotched specimens.
2. Convert mean and amplitude to an equivalent amplitude.
3. Read life from the curve for the right `R` or the corrected curve.
4. Apply scatter factors per your certification approach (safe life) or move to damage tolerance (see damage-tolerance-part-25-571).

## Gotchas
- Surface finish, size and environment shift the curve; cite the source of the data.
- Fastener holes, fretting and cladding often govern real life.
- S-N data have large scatter in life (factors of several); never quote a single life without the scatter.

## Verify
- [ ] The calculated allowable amplitude at `R = -1` and `sigma_m = 0` returns the curve value.
