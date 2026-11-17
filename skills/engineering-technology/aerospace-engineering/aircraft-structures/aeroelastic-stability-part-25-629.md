---
id: engineering-technology.aerospace-engineering.aircraft-structures.aeroelastic-stability-part-25-629
name: aeroelastic-stability-part-25-629
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, aeroelasticity, flutter, part-25-629, aeroelastic-stability, flutter-margin, flight-flutter-test, failure-cases]
level: advanced
status: verified
description: "Plan aeroelastic stability substantiation under 25.629: flutter, divergence and control reversal checks across the envelope, with the margins and tests agreed with the authority."
sources:
  - "14 CFR Part 25 section 25.629"
  - "EASA CS-25 section 25.629 and AMC"
  - "FAA advisory circular 25.629 series"
  - "https://www.law.cornell.edu/cfr/text/14/25.629"
  - "https://www.law.cornell.edu/cfr/text/14/25.629"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Aeroelastic stability under 25.629

**Goal:** show freedom from flutter, divergence and control reversal in the flight envelope with margin. Read the current rule text and AMC for the exact margins and conditions; this is practice guidance.

## Scope (check the text)
This is practice guidance, not certification advice; the certification basis and the regulator (FAA, EASA) govern, and a qualified flutter specialist must sign off the compliance work.
- Stability throughout the speed range up to a margin beyond `V_D / M_D` (25.629(b)(1): the V_D/M_D versus altitude envelope enlarged by 15 percent in equivalent airspeed at constant Mach and at constant altitude, with a proper margin of stability up to V_D/M_D and no large or rapid reduction as it is approached; 25.629(b)(2): the failure and adverse conditions of 25.629(d), against a speed envelope defined there. The text of 25.629 gives no numerical damping value; damping criteria come from the accepted means of compliance (AMC/AC), so confirm them there).
- Considered conditions: normal operation and certain failures, malfunctions and adverse conditions (for example engine failures, control system failures, free play, ice).
- Includes the effects of fuel, stores, stiffness variations and the control system (aeroservoelastic).

## Process
1. Define the envelope, cases, and failure conditions list.
2. Structural dynamics model correlated with ground vibration test data.
3. Unsteady aerodynamics tuned with wind-tunnel data where available.
4. Compute flutter, divergence and reversal results across the cases; document margins.
5. Flight flutter testing: excite the structure (control surface pulses, sweeps, or dedicated exciters), track frequency and damping trends with speed, and expand the envelope in increments with real-time monitoring.
6. Compile the compliance report.

## Gotchas
- Free-play limits and maintenance checks feed the compliance (and the ALS or maintenance programme).
- Damping estimation from noisy flight data needs careful method choice.

## Verify
- [ ] Damping trend plots from flight test extrapolate to a stable margin beyond the limit speed.
