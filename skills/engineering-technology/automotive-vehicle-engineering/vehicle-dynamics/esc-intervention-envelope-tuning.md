---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.esc-intervention-envelope-tuning
name: esc-intervention-envelope-tuning
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [esc-tuning, esc, electronic-stability-control, yaw-rate-error, sideslip, intervention, brake-intervention, stability-rollover]
level: practitioner
status: gated
description: "Describe how ESC logic compares reference yaw rate with measured yaw rate and sideslip, and how an OEM tunes thresholds and brake or torque interventions."
sources:
  - "van Zanten, Bosch ESP Systems (SAE paper series)"
  - "FMVSS 126 (sine-with-dwell, S5.2 yaw-rate ratios, checked in eCFR) and UN R140 (approval of passenger cars with regard to ESC systems; UN treaty record); confirm current texts"
  - "https://www.ecfr.gov/current/title-49/subtitle-B/chapter-V/part-571/subpart-B/section-571.126 (FMVSS 126, Electronic stability control systems for light vehicles)"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# ESC intervention envelope

- **Reference yaw rate:** from steering angle and speed with a steady-state bicycle model, limited by estimated friction: `r_ref = min(V*delta/(L*(1 + (V/V_char)^2)), mu_est*g/V)` (textbook form (gated: unconfirmed, source is paywalled or blocked)) with V_char the characteristic speed.
- **Error:** `e = r_meas - r_ref`; plus sideslip angle estimate from integrated lateral acceleration/yaw rate (observer). Intervene when |e| or sideslip exceeds thresholds that vary with speed and friction.
- **Intervention:** brake the outer front wheel to correct oversteer, inner rear to correct understeer; engine torque reduction in parallel. Control gains are tuned per vehicle on test surfaces (low-mu, split-mu, high-mu).
- **Tuning workflow:** sine-with-dwell, fishhook, J-turn, lane change, brake in turn, split-mu, at laden and unladen, with tyre and CG variants; log intervention timing and driver comfort.
- Suppliers (Bosch, Continental, ZF and others) typically provide the software; OEMs do the application (calibration) work under regulation.

**Gotchas:** thresholds too tight give nuisance interventions in sporty driving; too loose fail regulatory tests.

## Verify
- [ ] Regulatory manoeuvre pass margins documented.
- [ ] Nuisance-intervention test drive on public-road-like events logged.
