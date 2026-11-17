---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.whole-body-vibration-evaluation
name: whole-body-vibration-evaluation
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [whole-body-vibration, iso-2631, frequency-weighting, vibration-comfort, rms-acceleration, vdv]
level: practitioner
status: gated
description: "Evaluate ride comfort from seat accelerations with ISO 2631-1 weighting, RMS and vibration dose, and compare to comfort reaction bands."
sources:
  - "ISO 2631-1 (whole-body vibration), confirm current edition"
  - "Griffin, Handbook of Human Vibration"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Whole-body vibration evaluation

1. Measure acceleration at the seat surface (and floor, backrest) in x, y, z with a seat pad accelerometer; sample at least 500 Hz with anti-alias filter.
2. Weight each axis: Wk for z at the seat, Wd for x and y; (backrest and feet use other weightings). Frequency range 0.5-80 Hz for health/comfort per the standard.
3. Weighted RMS `aw = sqrt(1/T * integral(aw(t)^2 dt))`. For overall comfort combine axes `av = sqrt(kx^2 ax^2 + ky^2 ay^2 + kz^2 az^2)` with multiplying factors from the standard.
4. For shocks, use crest factor; when above about 9 use VDV (vibration dose value) instead.
5. Interpretation guide in the standard (m/s^2): below about 0.315 not uncomfortable, 0.315-0.63 a little, 0.5-1.0 fairly, 0.8-1.6 uncomfortable, 1.25-2.5 very, above 2.0 extremely (ranges overlap by design). Confirm in the edition (weightings, multiplying factors, crest factor 9 and this comfort table are allgated: unconfirmed, source is paywalled or blocked).
6. Report speed, road, seat, load.

**Gotchas:** transducer axis and sign, using unweighted data.

## Verify
- [ ] Weighted RMS reproduces within repeat scatter across three runs.
- [ ] Axis weighting factors documented.
