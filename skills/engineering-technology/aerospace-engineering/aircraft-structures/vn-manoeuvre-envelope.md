---
id: engineering-technology.aerospace-engineering.aircraft-structures.vn-manoeuvre-envelope
name: vn-manoeuvre-envelope
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, loads, flight-loads, vn-diagram, manoeuvre-envelope, load-factor, design-speeds, part-25-337]
level: practitioner
status: verified
description: "Construct a transport-category V-n manoeuvre and gust envelope from design speeds and load factor limits, citing the governing regulation text rather than memory."
sources:
  - "14 CFR Part 25 sections 25.331 to 25.345"
  - "EASA CS-25 subpart C"
  - "Niu, Airframe Structural Design"
  - "https://www.law.cornell.edu/cfr/text/14/25.331"
  - "eCFR 14 CFR 25.337, https://www.ecfr.gov/current/title-14/part-25/section-25.337"
  - "eCFR 14 CFR 25.345, https://www.ecfr.gov/current/title-14/part-25/section-25.345"
  - "eCFR 14 CFR 25.333 and 25.335, https://www.ecfr.gov/current/title-14/part-25/section-25.335"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# V-n manoeuvre envelope

**Goal:** the flight envelope defining limit load factors versus equivalent airspeed.

## Elements
- Positive limit manoeuvre load factor for transports per 25.337(b): `n = 2.1 + 24000/(W + 10000)` with W the design takeoff weight in pounds, not less than 2.5 and not more than 3.8. Negative limit factor not less than -1.0 up to `V_C`, varying linearly to zero at `V_D` (25.337(c)). Lower factors are allowed only if design features make the higher values impossible to exceed (25.337(d)). Verify against the current regulation text and your aircraft's certification basis. Worked check (computed): W = 100,000 lb gives 2.1 + 24000/110000 = 2.32, so the 2.5 floor governs; W = 30,000 lb gives 2.70.
- Stall boundary: `n = rho0 V^2 S CN_max /(2 W)` with equivalent airspeed `V_e` (curve from 0 to `V_A`, the design manoeuvring speed).
- Design speeds (25.335, all equivalent airspeeds): `V_S1`, `V_A`, `V_B` (design speed for maximum gust intensity, 25.335(d)), `V_C` (design cruising speed), `V_D` (design dive speed), `V_F` (design flap speeds, 25.335(e)). The envelope itself is 25.333(b).
- Flap envelopes (25.345): with flaps at takeoff, approach and landing positions, manoeuvre to a positive limit load factor of 2.0 plus 25 ft/s EAS gusts; en route flaps use the 25.337(b) factor and the 25.341 gust and turbulence conditions; a 1.5 g manoeuvre at maximum takeoff weight in the landing configuration.
- Ultimate loads = limit loads x factor of safety 1.5 (25.303).

## Procedure
1. Set weight cases (max takeoff, max landing, zero fuel) and altitude cases.
2. Compute stall curves from `CN_max` for each configuration.
3. Plot manoeuvre limits and overlay gust load factor lines (see gust skill).
4. Take the outer envelope; list corner points as load cases for the loads team.

## Gotchas
- Use equivalent airspeed, not true airspeed.
- Corner points need load cases at each weight and cg combination.

## Verify
- [ ] Envelope corners match values computed by hand from the cited paragraph.
