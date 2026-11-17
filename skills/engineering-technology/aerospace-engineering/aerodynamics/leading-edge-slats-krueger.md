---
id: engineering-technology.aerospace-engineering.aerodynamics.leading-edge-slats-krueger
name: leading-edge-slats-krueger
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, high-lift, slats, leading-edge-devices, krueger-flap, droop-nose, stall-angle, slot-flow]
level: practitioner
status: draft
description: "Choose and size leading-edge devices (slats, Krueger flaps, droop) to raise CLmax and stall angle, with their gap and drag trade-offs."
sources:
  - "Raymer, Aircraft Design: A Conceptual Approach"
  - "Rudolph, High-Lift Systems on Commercial Subsonic Airliners (NASA contractor report)"
  - "Torenbeek"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Leading-edge slats and Krueger flaps

**Goal:** postpone leading-edge separation to raise stall angle and `CLmax`, especially with trailing-edge flaps deployed.

## Principles
- A slat creates a slot that reduces the suction peak on the main element's leading edge; the main element can then carry a higher angle of attack before separating. Gain in `CLmax` is mostly through the later stall angle, not a higher lift slope.
- Krueger flaps hinge out from the lower surface: simpler mechanically and fit thin lower-surface cavities, generally less effective than slats.
- Fixed droop or slotted leading edges on light aircraft are cheap and have a drag cost.

## Design points
1. Span: cover outboard wing (and often inboard if engines allow); gaps at engine pylons need a vortex or strake fix.
2. Deflection and gap: gap size is a sensitive optimum (CFD or test). A common takeoff setting is a smaller gap and angle than landing.
3. Interaction with flap: the slat reduces the main-element suction peak that the flap would otherwise worsen.
4. Noise: slat cove and edge are a major airframe noise source on approach; consider cove fairings.

## Gotchas
- Retracted slats must seal; fit tolerance affects cruise drag.
- A slat that deploys asymmetrically is a safety-critical failure; asymmetry protection is part of the system safety assessment (see Part 25 flight control requirements).
- Slats on swept wings affect pitching moment and pitch-up behaviour near stall.

## Verify
- [ ] Wing CLmax and stall alpha with devices come from test or CFD, not only correlations.
- [ ] Gap and overlap tolerances are in the drawing and in the manufacturing plan.
