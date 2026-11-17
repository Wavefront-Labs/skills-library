---
id: engineering-technology.aerospace-engineering.propulsion-engineering.thrust-lapse-with-altitude-mach
name: thrust-lapse-with-altitude-mach
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, gas-turbine, brayton-cycle, thrust-lapse, engine-lapse, altitude-effects, bypass-ratio, conceptual-design]
level: practitioner
status: verified
description: "Estimate how engine thrust falls with altitude and Mach using simple lapse relations, and know when to use a cycle deck instead."
sources:
  - "Mattingly, Heiser and Pratt, Aircraft Engine Design"
  - "Raymer, Aircraft Design: A Conceptual Approach"
  - "Torenbeek, Synthesis of Subsonic Airplane Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Thrust lapse

**Goal:** thrust available at altitude and speed for sizing and mission analysis.

## Simple models
- Thrust scales roughly with total pressure ratio relative to sea level: `delta0 = P_t0 / P_sl`; lapse `alpha = T/T_SL`.
- Mattingly's simple model for high-bypass turbofans (bypass ratio about 5 or more) in the region below the throttle break: `alpha = delta0 (1 - 0.49 sqrt(M))` (coefficient from Mattingly (gated: unconfirmed, source is paywalled or blocked)). Other correlations exist for low-bypass turbofans and turbojets; take them from the reference and check the stated validity (Mach range, bypass ratio, throttle ratio).
- At altitude in the stratosphere thrust tends to fall about in proportion to density.

## Procedure
1. Compute `theta0` and `delta0` from altitude and Mach (ISA).
2. Apply the lapse model to get thrust fraction relative to sea-level static thrust.
3. For takeoff, use static and low-speed thrust (higher thrust with ram effects minimal); for cruise use the cruise lapse.
4. Replace the correlation with a cycle deck or engine manufacturer data when available.

## Gotchas
- Throttle break (flat-rating) temperature: below the break temperature thrust is constant; above, it falls.
- Installation losses (bleed, power extraction, inlet loss) reduce uninstalled thrust.

## Verify
- [ ] Lapse at sea-level static equals 1.0; the model gives about 0.20 at 35,000 ft, Mach 0.8 (computed: ISA static pressure 23,842 Pa, `delta0` = 0.359, `alpha` = 0.201); confirm with manufacturer data.
