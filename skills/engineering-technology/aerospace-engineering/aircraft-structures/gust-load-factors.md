---
id: engineering-technology.aerospace-engineering.aircraft-structures.gust-load-factors
name: gust-load-factors
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, loads, flight-loads, gust-loads, gust-alleviation-factor, mass-ratio, discrete-gust, continuous-turbulence]
level: practitioner
status: gated
description: "Estimate gust load factor increments with the gust alleviation factor and mass ratio, and understand how discrete gust and continuous turbulence rules fit in."
sources:
  - "14 CFR Part 25 section 25.341"
  - "EASA CS-25 section 25.341 and AMC"
  - "Hoblit, Gust Loads on Aircraft: Concepts and Applications"
  - "https://www.law.cornell.edu/cfr/text/14/25.341"
  - "eCFR 14 CFR 25.341, https://www.ecfr.gov/current/title-14/part-25/section-25.341"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Gust load factors

**Goal:** vertical load factor increments from gusts for envelope and sizing.

## Simplified (quasi-steady) formula
`delta_n = (rho0 * Ude * Kg * V_e * a) / (2 * W/S)` with `a` the lift-curve slope (per radian), `V_e` equivalent airspeed, `Ude` the derived (equivalent) gust velocity, and the gust alleviation factor
`Kg = 0.88 * mu / (5.3 + mu)`, mass ratio `mu = 2 (W/S) / (rho * c_bar * g * a)`.
Use consistent units. This was the classical Part 25 method and remains the basis for early design and light aircraft (gated: unconfirmed, the classical formula and its constants are not in the current 25.341 text, which was replaced by the dynamic criteria below).

## Current transport rules
25.341 now requires dynamic analysis: discrete gust (tuned gust of specified shape and gradient length with the reference gust velocity and flight-profile alleviation factor) and continuous turbulence (power spectral density with design turbulence intensities). Confirmed from eCFR 25.341 (current): discrete gust gradients H investigated across 30 to 350 ft; reference gust 56.0 ft/s EAS at sea level between `V_B` and `V_C`, reduced linearly to 44.0 ft/s at 15,000 ft and to 20.86 ft/s at 60,000 ft; 0.5 times that at `V_D`; the design gust velocity is `U_ref` times the flight profile alleviation factor `F_g`, which rises linearly to 1.0 at the maximum operating altitude (the equations for `F_g` and the gust shape are in the rule; read them there). Continuous turbulence: `P_L = P_L,1g +/- U_sigma A`, turbulence scale L = 2,500 ft, reference intensity `U_sigma,ref` 90 ft/s TAS at sea level to 79 ft/s at 24,000 ft then constant to 60,000 ft, half of that at `V_D`. Use the rule and AMC for any compliance work.

## Procedure
1. Compute `mu`, `Kg`, `a` at the flight condition.
2. Add `delta_n` to 1 g in positive and negative sense at `V_B`, `V_C` and `V_D`.
3. Compare with manoeuvre envelope; the larger governs.
4. For compliance, run the dynamic gust analyses with the aeroelastic model.

## Gotchas
- Units: `rho0` is sea-level density, `Ude` and `V` in equivalent airspeed.
- Quasi-steady results can be unconservative for flexible aircraft.

## Verify
- [ ] Hand calculation matches the spreadsheet for a reference condition.
