---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.lateral-load-transfer-calculation
name: lateral-load-transfer-calculation
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [lateral-load-transfer, load-transfer, roll-centre-height, roll-moment, geometric-transfer, elastic-transfer]
level: practitioner
status: verified
description: "Calculate lateral load transfer per axle split into geometric and elastic parts from roll centre heights, CG height and roll stiffness distribution."
sources:
  - "Milliken and Milliken, Race Car Vehicle Dynamics"
  - "Gillespie, Fundamentals of Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Lateral load transfer calculation

Inputs: mass m, lateral acceleration ay, track `tf, tr`, CG height h, roll axis height at the CG hr (interpolated from front and rear roll centre heights), front weight fraction, roll stiffnesses `Kf, Kr` (N m/rad).

1. Roll moment on sprung mass about the roll axis: `M = ms*ay*(h - hr)`; roll angle `phi = M/(Kf + Kr - ms*g*(h - hr))` (the last term is the gravitational roll-over contribution).
2. Elastic transfer at the front: `dFz_f_elastic = Kf*phi/tf`; rear similarly.
3. Geometric transfer: `dFz_f_geo = ms_f*ay*hrf/tf` (front roll-centre height times that axle's sprung mass share), plus unsprung transfer `mu_f*ay*h_ug/tf` through the wheel centre height.
4. Total per axle = elastic + geometric + unsprung. With the gravity term in `phi` (step 1), the listed terms exceed `m*ay*h_cg/t` by `ms*g*(h - hr)*phi/t`, the extra load shift from the sprung mass moving outboard as the body rolls. Subtract it (or compute `phi` without the gravity term) and the sum equals `m*ay*h_cg/t` for equal tracks (computed; worked case 2493.0 vs 2383.9 N, difference 109.1 N = gravity term).
5. Distribution LLTD = front total / total.

**Gotchas:** mixing sprung and total mass; ignoring that RC heights move; using stiffness without the tyre/bushing compliance.

## Verify
- [ ] Front + rear transfer, less `ms*g*(h - hr)*phi/t`, sums to total m*ay*h/t within rounding for equal track.
- [ ] LLTD moves in the expected direction when front bar stiffness is raised.
