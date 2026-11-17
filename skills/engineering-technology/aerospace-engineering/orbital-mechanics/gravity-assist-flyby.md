---
id: engineering-technology.aerospace-engineering.orbital-mechanics.gravity-assist-flyby
name: gravity-assist-flyby
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [gravity-assist, flyby, swingby, turn-angle, powered-flyby, interplanetary]
level: practitioner
status: gated
description: "Compute a gravity assist flyby: hyperbolic turn angle, heliocentric speed change, periapsis limits and when a powered flyby helps."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Gravity assist

**Goal:** change heliocentric velocity using a planet's gravity.

## Relations
- In the planet frame the hyperbolic excess speed `v_inf` has the same magnitude before and after the encounter; only the direction changes.
- Turn angle `delta = 2 asin(1/e)` with `e = 1 + r_p v_inf^2/mu_planet`.
- The heliocentric velocity change is the vector difference of the outgoing and incoming `v_inf` (magnitude up to `2 v_inf sin(delta/2)`).
- Powered flyby: a burn at periapsis adds energy more efficiently than at large distance (Oberth effect).

## Procedure
1. Get the incoming `v_inf` vector (planet-relative) from the heliocentric arrival state.
2. Pick the desired outgoing heliocentric velocity (from the next transfer arc), difference it with the planet velocity to get the outgoing `v_inf` vector.
3. Check the magnitudes match; if not, add a powered flyby burn at periapsis or a deep-space manoeuvre.
4. Compute the turn angle needed, solve for `r_p`; check `r_p` above the surface and atmosphere with margin.
5. Chain the legs for multi-flyby tours (Cassini used Venus, Venus, Earth, Jupiter flybys (gated: unconfirmed, source is paywalled or blocked)).

## Check
Computed example: v_inf = 5 km/s, r_p = 6,678 km at Earth (mu = 398,600 km3/s2): e = 1.419, turn angle 89.6 deg, max heliocentric change 2 v_inf sin(delta/2) = 7.05 km/s = 2 v_inf / e, as the relations state.

## Gotchas
- A flyby cannot change `v_inf` magnitude without a burn; the energy gain is in the heliocentric frame.
- The sphere-of-influence patch is an approximation; refine with numerical integration.
- Flyby altitude uncertainty must be managed by trajectory correction manoeuvres.

## Verify
- [ ] Incoming and outgoing `v_inf` magnitudes equal each other in the planet frame, and the turn angle matches `r_p`.
