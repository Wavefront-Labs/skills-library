---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.random-vibration-loads-and-miles-equation
name: random-vibration-loads-and-miles-equation
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [spacecraft, spacecraft-structures, mechanisms, random-vibration, miles-equation, asd, grms, launch-environment]
level: practitioner
status: verified
description: "Estimate random-vibration response of spacecraft units with Miles' equation and set test and design levels, with notching and primary-structure caveats."
sources:
  - "NASA GSFC-STD-7000 (General Environmental Verification Standard)"
  - "Wijker, Spacecraft Structures"
  - "Launch vehicle user guides"
  - "NASA NTRS 19900015329 (random vibration 3-sigma load factor): https://ntrs.nasa.gov/api/citations/19900015329/downloads/19900015329.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Random vibration loads (Miles' equation)

**Goal:** response estimate and test level for units under random launch vibration.

## Miles' equation
For a single-degree-of-freedom system with natural frequency `f_n`, amplification `Q`, base input acceleration spectral density `ASD(f_n)` (g^2/Hz), flat near the resonance:
`G_rms = sqrt( (pi/2) f_n Q ASD(f_n) )`; peak response is commonly taken as 3 times `G_rms` for design (3 sigma, about a 0.26 percent exceedance probability for a Gaussian response).
`Q = 1/(2 zeta)` with `zeta` the damping ratio; take `Q` from measured data or the programme rule (no free source was found for a `Q = sqrt(f_n)` shortcut, so do not use it unreviewed).

## Using it
1. Get the random vibration spectrum for the unit's mounting location from the launch vehicle user guide or the programme's derived levels (often unit-level qualification and acceptance spectra come from GEVS-style standards).
2. Estimate first mode `f_n` of the unit or panel (from FE or tests).
3. Compute `G_rms`, 3-sigma load, and stress or mounting margins (see structural margin practice).
4. For primary structure, use coupled loads analysis with the launcher; Miles' equation is for first-pass unit checks.

## Test practice
- Notching of the input at primary resonances is limited by the programme's rules and agreed with the launch authority.
- Compare sine-sweep signatures before and after random runs to detect structural changes.

## Gotchas
- Miles' equation assumes a white-noise input over the resonance and a single mode.
- Multi-mode and nonlinear behaviour (bolted joints) violate the assumption.

## Verify
- [ ] Example: `f_n = 100 Hz`, `Q = 10`, `ASD = 0.04 g^2/Hz` gives `G_rms` of about 7.9 g (check with the formula).
