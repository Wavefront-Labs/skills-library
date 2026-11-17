---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.liquid-cooling-plate-design
name: liquid-cooling-plate-design
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [cold-plate, liquid-cooling, cooling-plate, coolant-flow, thermal-interface-material, temperature-uniformity]
level: practitioner
status: gated
description: "Design a pack cold plate: coolant flow from heat load and temperature rise, channel layout, thermal interface, pressure drop and cell temperature spread."
sources:
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design"
  - "Incropera et al., Fundamentals of Heat and Mass Transfer"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Liquid cooling plate design

1. Heat load from the heat-generation estimate for the worst duty (e.g. 6 kW).
2. Coolant flow: `mdot = Q/(cp*dT_coolant)`; with 50/50 water-glycol (cp about 3.4 kJ/(kg K) (gated: unconfirmed, source is paywalled or blocked)) and 5 K coolant rise, 6 kW needs about 0.35 kg/s (computed 0.353 kg/s, about 20 L/min at density 1.04 kg/L (gated: unconfirmed, source is paywalled or blocked)). Coolant temperature rise sets cell-to-cell difference along the circuit.
3. Layout: serpentine, parallel microchannel or stamped plate; parallel paths with balanced flow reduce temperature spread but need good manifold design.
4. Interface: thermal gap filler or pad between cells and plate; its thickness and conductivity often dominate the thermal resistance; control compression and tolerance stack.
5. Pressure drop: pump capability and flow target; check at cold coolant viscosity.
6. Targets: maximum cell temperature below the limit (for example 40-45 C in fast charge (gated: unconfirmed, source is paywalled or blocked), check cell supplier) and cell-to-cell spread of a few K.
7. Verify with CFD and a thermal test with cell heaters or at-load test.

**Gotchas:** air in the loop, leak sealing and galvanic corrosion in the circuit; condensation under cold plate.

## Verify
- [ ] Cell temperature spread measured under worst-duty profile.
- [ ] Leak test and pressure-drop measurement pass.
