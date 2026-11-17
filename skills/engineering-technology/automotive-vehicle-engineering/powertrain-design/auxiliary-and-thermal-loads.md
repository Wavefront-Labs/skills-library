---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.auxiliary-and-thermal-loads
name: auxiliary-and-thermal-loads
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [auxiliary-load, hvac, cabin-heating, ptc-heater, heat-pump, 12v-loads, thermal-load, efficiency-mapping]
level: practitioner
status: gated
description: "Estimate auxiliary and thermal energy use (HVAC, pumps, 12 V loads) and its effect on EV range, including cold-weather heating and heat-pump options."
sources:
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
  - "SAE thermal management literature"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Auxiliary and thermal loads

1. 12 V loads: ECUs, lighting, infotainment, pumps, fans, typically a few hundred watts average (gated: unconfirmed, source is paywalled or blocked); supplied through the DC-DC converter.
2. Cabin heating: heat demand depends on ambient, ventilation and insulation; resistive (PTC) heaters deliver heat at COP 1, drawing perhaps 3-6 kW in cold conditions (gated: unconfirmed, source is paywalled or blocked); heat pumps deliver COP above 1 (about 2-3 at mild cold, falling at very low temperature (gated: unconfirmed, source is paywalled or blocked)).
3. Cooling/AC: compressor load around 1-3 kW depending on conditions (gated: unconfirmed, source is paywalled or blocked).
4. Battery and powertrain thermal conditioning: preconditioning before fast charge, cold-start warm-up, using waste heat from the motor and inverter where possible.
5. Range impact: at low speed in cold weather auxiliaries can be a major share of consumption; at motorway speed aero dominates.
6. Test and model: cold, hot and moderate ambient scenarios; include cabin thermal mass.
7. Strategies: seat/steering wheel heating, pre-conditioning while plugged in, recirculation control.

**Gotchas:** range claims at 23 C standard cycles hide cold performance.

## Verify
- [ ] Energy budget by consumer for cold, mild, hot cases.
- [ ] Preconditioning benefit quantified.
