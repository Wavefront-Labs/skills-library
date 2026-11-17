---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.stall-warning-and-alpha-protection
name: stall-warning-and-alpha-protection
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-dynamics, envelope-protection, fly-by-wire, stall-protection, stall-warning, alpha-protection, stick-shaker, angle-of-attack-sensor]
level: advanced
status: draft
description: "Design stall warning and angle-of-attack protection: alpha thresholds vs configuration and Mach, warning margins, sensor redundancy, and the certification context."
sources:
  - "14 CFR Part 25 sections 25.201 and 25.207"
  - "EASA CS-25 same sections"
  - "Pratt, Flight Control Systems: Practical Issues in Design and Implementation"
  - "https://www.law.cornell.edu/cfr/text/14/25.201"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Stall warning and alpha protection

**Goal:** keep the aircraft out of stall with robust warning or limiting. Practice guidance; the certification basis and AMC govern.

## Concepts
- **Stall warning:** cues (aural, stick shaker, visual) beginning before the stall; 25.207 requires a warning margin: 25.207(c) (eCFR text checked October 2026): when speed is reduced at no more than 1 knot per second, warning must begin in each normal configuration at a speed exceeding the speed at which the stall is identified under 25.201(d) by not less than 5 knots or 5% CAS, whichever is greater (read the current text for the other conditions, including accelerated stalls and icing).
- **Stick pusher:** actively pitches the nose down near stall on aircraft with unacceptable stall characteristics (deep stall tendency).
- **Alpha protection (fly-by-wire):** control laws that limit angle of attack: `alpha_prot` where the law transitions from load-factor demand to angle-of-attack control, and `alpha_max` that cannot be exceeded by pilot inputs.

## Design workflow
1. Define the stall angle of attack versus flap, Mach, and slat settings from wind tunnel and flight data.
2. Choose thresholds with margin relative to measured stall (and buffet) angle of attack.
3. Sensor architecture: multiple independent angle-of-attack sensors with voting and monitoring, and a defined behaviour when sensors disagree (inhibit or revert, not act on one source).
4. Test: gust, turn entry, wings-level and accelerated stalls, ice-contaminated conditions in simulation and flight.
5. Safety assessment: show failure conditions are acceptably improbable and annunciated.

## Gotchas
- A single-sensor-fed active law has been the root of accidents; require redundancy and monitoring.
- Thresholds must account for sensor installation error and dynamic effects (lag, pitch rate).

## Verify
- [ ] Warning onset and alpha thresholds are verified against flight-test stall data at several configurations and Mach.
