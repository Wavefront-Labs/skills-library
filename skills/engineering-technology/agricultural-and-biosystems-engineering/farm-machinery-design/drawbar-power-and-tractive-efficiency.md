---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.drawbar-power-and-tractive-efficiency
name: drawbar-power-and-tractive-efficiency
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, drawbar-power, tractor-performance, tractive-efficiency, traction, rolling-resistance, motion-resistance]
level: practitioner
status: verified
description: "Compute drawbar power, axle power and tractive efficiency for a tractor in a given soil, and identify where power is lost between engine and drawbar."
sources:
  - "ASABE D497 Agricultural Machinery Management Data (paywalled; index at https://www.asabe.org)"
  - "OECD tractor tests (https://www.oecd.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Drawbar power and tractive efficiency

**Goal:** know how much of the engine power becomes pull and how to improve it.

## Quantities
- Drawbar power `P_db = F_db x v` (F in kN, v in m/s gives kW).
- Net traction = gross traction - motion resistance.
- Tractive efficiency `TE = P_db / P_axle`; overall = `P_db / P_engine`.
- Components: transmission loss, motion (rolling) resistance, slip loss. `TE = (1 - slip) x (net traction / gross traction)`.

## Typical values
On firm soil and good tire/ballast, TE of 0.75-0.85 is quoted for a tyred tractor; on soft or tilled soil it is lower (roughly 0.5-0.7) (gated: unconfirmed, source is paywalled or blocked; the figures come from the ASABE data standards). Tracked machines are often more efficient on soft soil. Check against the Nebraska/OECD test report for the specific model.

## Using it
1. Get engine or PTO power from the test report; apply transmission efficiency (about 0.85-0.9 for mechanical drivelines (gated: unconfirmed, source is paywalled or blocked); use the test data).
2. Estimate TE from soil index (cone index, see tire-inflation skill) or from similar tests.
3. `P_db = P_engine x transmission eff x TE`. Compare with the implement's required drawbar power.
4. If power is inadequate: add ballast within limits, drop inflation to spec minimum, change gear/speed or implement size.

## Gotchas
- Pull-versus-speed trade: gear down and throttle back to save fuel only if the engine stays near its torque peak.
- Do not quote drawbar power at zero slip; it is a function of load and soil.

## Verify
- [ ] Measured slip is in the working range (see wheel-slip skill).
- [ ] Calculated P_db fits the implement's draft x speed.
