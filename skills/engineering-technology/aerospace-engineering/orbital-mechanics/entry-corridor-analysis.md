---
id: engineering-technology.aerospace-engineering.orbital-mechanics.entry-corridor-analysis
name: entry-corridor-analysis
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [entry-corridor, entry-flight-path-angle, skip-out, peak-deceleration, allen-eggers, atmospheric-entry]
level: practitioner
status: gated
description: "Find the entry corridor between skip-out and overload or heating limits, and estimate ballistic peak deceleration with the Allen-Eggers result."
sources:
  - "Vinh, Busemann and Culp, Hypersonic and Planetary Entry Flight Mechanics"
  - "Curtis, Orbital Mechanics for Engineering Students"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Entry corridor

**Goal:** the allowable range of entry flight path angles at the entry interface.

## Limits
- **Shallow (overshoot) limit**: a vehicle that enters too shallow skips out of the atmosphere or fails to decelerate enough to be captured on the intended orbit.
- **Steep (undershoot) limit**: peak deceleration, peak heating or heat load above what the crew or the thermal protection allows.
- Lifting entry widens the corridor because the lift can be modulated (see lifting-entry-guidance).

## Ballistic estimate (Allen-Eggers, exponential atmosphere, constant flight path angle)
- Peak deceleration `a_max = V_E^2 sin(gamma_E) / (2 e H)` (with `e` Euler's number, `H` the scale height, and `gamma_E` the magnitude of entry flight path angle). It is independent of ballistic coefficient; the altitude at which it occurs depends on the ballistic coefficient.
- Example: `V_E = 7.8 km/s`, `gamma_E = 3 deg`, `H = 7.2 km` gives 8.3 g (computed).

## Procedure
1. Fix the entry interface (for example 120 km altitude) and entry speed (about 7.8 km/s for LEO return, about 11 km/s for lunar return).
2. Simulate across `gamma_E`; for each find peak g, peak heating (see sutton-graves-stagnation-heating), landing footprint and skip behaviour.
3. Mark the corridor bounds with margins for navigation error, atmosphere variation and vehicle aerodynamic uncertainty.
4. Compare the corridor width with the delivery accuracy of the deorbit or return burn.

## Gotchas
- Real atmospheres vary with season and latitude, shifting both limits.
- Pure ballistic corridors for high-speed entry are only a few tenths of a degree wide (gated: unconfirmed, source is paywalled or blocked), so guidance with lift is used.

## Verify
- [ ] The Allen-Eggers peak deceleration agrees with a numerical entry simulation to within about 10 to 20 percent.
