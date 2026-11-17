---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.d-value-z-value-and-thermal-death-kinetics
name: d-value-z-value-and-thermal-death-kinetics
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, d-value-z-value, thermal-processing, canning-process, thermal-death-time, survivor-curve, f-value, log-reduction, f0]
level: practitioner
status: verified
description: "Fit D and z values from survivor curves, apply log-linear inactivation, and convert time-temperature histories to equivalent lethality with the F-value integral."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Singh & Heldman, Introduction to Food Engineering"
  - "https://www.ecfr.gov/current/title-21/part-113"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# D-value, z-value and thermal death kinetics

**Goal:** quantify microbial or quality-attribute inactivation against time and temperature.

## Definitions
- **D-value**: time at constant temperature for a 10-fold (1-log) reduction. `log N0 - log N = t / D`.
- **z-value**: temperature increase that reduces D ten-fold. `D_T = D_ref x 10^((T_ref - T)/z)`.
- **F-value**: equivalent time at the reference temperature: `F = integral 10^((T(t) - T_ref)/z) dt`. For low-acid canned foods the convention is `F0` with T_ref 121.1 C (250 F) and z 10 C (18 F), designed around Clostridium botulinum spores.
- The botulinum cook ("12D") reduces C. botulinum spores by 12 log cycles; with the classic D121.1 of 0.21 min this gives F0 = 12 x 0.21 = 2.52 min, about 2.5 min, and commercial processes usually go beyond that for spoilage organisms (the process authority sets the target).

## Fitting D and z
1. Hold samples at several constant temperatures (capillary tubes or thermal death time cans), take survivors at times, plot log N versus t; the slope is -1/D at each temperature.
2. Plot log D versus T; slope is -1/z.
3. Check for shoulders or tails (non-log-linear behaviour); use Weibull or other models if present, and do not extrapolate far outside the tested range.

## Using F
Integrate the measured product cold-spot temperature (see heat penetration skill) in small time steps (trapezoid rule), compare to the required F.

## Gotchas
- D and z depend on the medium (pH, aw, fat); use values measured in your product.
- Come-up and cooling contributions can be a large part of F for small containers.
- Regulatory process establishment must be by a qualified process authority.

## Verify
- [ ] Recompute F from a logged run; it meets or exceeds the scheduled process F.
