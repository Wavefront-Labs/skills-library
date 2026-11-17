---
id: engineering-technology.aerospace-engineering.aerodynamics.shock-buffet-onset-margin
name: shock-buffet-onset-margin
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, transonic, supersonic, buffet, shock-buffet, buffet-onset, buffet-margin, cl-buffet, part-25-251]
level: advanced
status: verified
description: "Define buffet onset on a CL vs Mach plot, assess margin for transonic cruise from CFD or flight test, and frame it against the airworthiness requirement."
sources:
  - "14 CFR Part 25 section 25.251"
  - "EASA CS-25 section 25.251"
  - "Lee, Self-excited shock wave oscillations on airfoils (Progress in Aerospace Sciences)"
  - "https://www.law.cornell.edu/cfr/text/14/25.251"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Shock buffet onset and margin

**Goal:** know how far the cruise point is from buffet onset at the relevant altitude and Mach.

## Concepts
- At transonic speed and high `CL`, shock-induced separation causes self-excited shock oscillation: buffet. Buffet onset limits the usable `CL` at high altitude.
- The buffet boundary is plotted as `CL_buffet` vs Mach for a given weight, altitude and configuration. Cruise margin is expressed as extra `g` or `CL` before onset.

## Regulatory frame
14 CFR 25.251 (eCFR text checked October 2026) requires flight demonstration of freedom from vibration and buffeting that would prevent control or cause structural damage, and, for airplanes with M_D above 0.6 or maximum operating altitude above 25,000 ft, determination of the buffet-onset load-factor envelopes in the cruise configuration so that probable excursions beyond them are not unsafe. The rule text states no numerical margin: the commonly quoted 1.3 g cruise margin comes from FAA/EASA advisory material and certification practice, so confirm it in the current advisory circular or AMC for your certification basis.

## Estimating onset
1. CFD: run a CL sweep at the Mach; indicators are trailing-edge pressure divergence, onset of separation (skin friction), or unsteady RANS showing shock oscillation. Steady RANS can predict onset only approximately.
2. Wind tunnel: dynamic strain gauge or wing-tip accelerometer RMS vs CL; the onset is where the RMS rises above the baseline.
3. Flight test: accelerometer RMS in a wind-up turn at constant Mach; the break defines the onset.

## Gotchas
- Different criteria give different onset values; state the criterion used.
- Reynolds number effects are strong; tunnel results need correction.
- Margin must hold at the aft cg and highest altitude weight.

## Verify
- [ ] Margin vs onset is stated in g or CL at the critical altitude, weight and cg.
- [ ] The criterion for onset is stated and applied consistently across sources.
