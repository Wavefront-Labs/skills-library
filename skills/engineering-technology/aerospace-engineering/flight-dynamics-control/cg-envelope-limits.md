---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.cg-envelope-limits
name: cg-envelope-limits
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [cg-limits, centre-of-gravity-envelope, weight-and-balance, forward-cg-limit, aft-cg-limit, static-stability]
level: practitioner
status: verified
description: "Derive forward and aft CG limits from trim authority, static margin and ground-handling criteria, and build a loading envelope in percent MAC."
sources:
  - "Raymer, Aircraft Design: A Conceptual Approach"
  - "FAA 14 CFR 25.27 (center of gravity limits) and 25.25 (weight limits)"
  - "Nelson, Flight Stability and Automatic Control"
  - "https://www.law.cornell.edu/cfr/text/14/25.27"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# CG envelope

**Goal:** the range of CG positions in which the aircraft is safe to fly and handle on the ground.

## Limits
- **Aft limit**: the smallest allowable static margin (neutral point minus CG) for stability and handling, minus a margin to handle uncertainty in neutral-point prediction. Static margins for conventional aircraft are positive and typically of the order of a few percent to 10 percent MAC; targets differ by category and by use of stability augmentation (gated: unconfirmed, source is paywalled or blocked).
- **Forward limit**: elevator or stabiliser authority to trim at the lowest speed with flaps down, and to rotate at take-off; also nose-gear loads and landing flare.
- **Ground limits**: tipping on the tail (aft), nose-gear overload (forward), steering load.
- **Structural limits**: maximum weights per regime and loading envelope for fuel, baggage, passengers.
- Regulations require the applicant to establish the weight and CG limits (14 CFR 25.27 for CG limits, with weight limits under 25.25, and the CS-25 equivalents; 25.27 requires extreme forward and aft limits for each practicably separable operating condition, none beyond the applicant's selected extremes, the structurally proven extremes, or those where each flight requirement is met); this skill gives working practice.

## Procedure
1. Locate the neutral point (see neutral-point-static-margin).
2. Set the aft limit = neutral point minus the minimum static margin.
3. Run the trim curve for the most demanding forward condition (full flaps, approach speed, ground effect) and find the forward CG at which elevator reaches its limit with margin (see longitudinal-trim-curve).
4. Build the loading envelope: for each loading station (fuel, seats, cargo) compute weight and CG; envelope the extremes.
5. Express limits as percent MAC versus weight (the limit usually narrows at maximum weight).

## Gotchas
- Fuel burn moves CG; check the whole mission.
- Gear position and flap trim shifts matter.
- A passenger loading plan, not the weight alone, gives the CG for operations.

## Verify
- [ ] All certified loading cases lie inside the envelope with the forward and aft margin applied.
