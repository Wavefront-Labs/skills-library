---
id: engineering-technology.aerospace-engineering.aerodynamics.ground-effect-lift-drag
name: ground-effect-lift-drag
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, high-lift, ground-effect, induced-drag-reduction, takeoff, landing, wing-height, mccormick]
level: practitioner
status: verified
description: "Estimate how proximity to the ground cuts induced drag and raises lift near takeoff and landing, using a simple induced-drag reduction factor."
sources:
  - "McCormick, Aerodynamics Aeronautics and Flight Mechanics"
  - "Raymer, Aircraft Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Ground effect

**Goal:** a quick estimate of the induced-drag reduction as wing height above ground falls.

## Model
Induced drag is multiplied by a factor `phi` as a function of height `h` over span `b`:
`phi = (16 h / b)^2 / (1 + (16 h / b)^2)`
(McCormick form, with h the height of the wing above the ground (gated: unconfirmed, source is paywalled or blocked); other fits exist, for example a Torenbeek-derived exponential). At `h/b = 0.1` phi is about 0.72; at `h/b = 0.25` about 0.94. So effect is notable only below roughly one quarter span.
Then `CD = CD0 + phi * CL^2 / (pi AR e)`. Lift at fixed angle of attack rises slightly; at fixed `CL` there is less downwash so the effective angle is smaller.

## Use
1. Compute `h/b` for the main wing at the field height (use gear position and attitude).
2. Apply phi in the takeoff-run and landing-flare calculations; it matters for landing float and takeoff lift-off acceleration.
3. Note the tail sees changed downwash, leading to a nose-down pitching change in ground effect; confirm trim authority.

## Gotchas
- The form is an approximation; configuration with flaps down and high-mounted wings differ.
- Do not apply it to the ground roll with gear on the ground without checking the actual `h/b` including any ground-plane model.

## Verify
- [ ] Factor goes to 1 for large h/b and to near 0 as h tends to 0 (physically bounded by wheels).
- [ ] Takeoff-distance sensitivity to the factor is reported (it is usually small).
