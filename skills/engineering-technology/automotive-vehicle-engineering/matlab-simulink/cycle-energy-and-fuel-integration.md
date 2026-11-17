---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.cycle-energy-and-fuel-integration
name: cycle-energy-and-fuel-integration
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [cycle-energy-integration, energy-integration, fuel-consumption, kwh-per-100km, integrator, drive-cycle]
level: practitioner
status: gated
description: "Integrate fuel mass or battery energy over a cycle in Simulink and convert to l/100 km or kWh/100 km with SOC and correction handling."
sources:
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Integrate energy and fuel over a cycle

- **ICE:** integrate fuel mass flow `mdot_f` (kg/s) to mass; volume = mass / density (gasoline roughly 0.74 kg/l, diesel roughly 0.83 (gated: unconfirmed, source is paywalled or blocked); use the certified density of the test fuel from the regulation or lab certificate). Consumption `l/100km = V/(distance_km)*100`.
- **EV:** integrate DC battery power `P = V*I` (positive discharging, negative charging) to Wh, divide by distance. Decide the measurement point (battery DC vs wall AC with charger losses) and state it.
- **Hybrids:** SOC change must be corrected to charge-neutral. Run several cycles with different start SOC and extrapolate to dSOC = 0 (the regulations define correction methods; confirm the current text), or use equivalent-fuel correction.
- Use an Integrator with a reset at cycle start, and also log distance with an integrator on v.
- Use trapezoidal sample logging to avoid aliasing at coarse steps.

**Gotchas:** forgetting auxiliary and thermal loads in EV energy; counting regen as negative energy without efficiency losses already in the model.

## Verify
- [ ] Energy balance: battery energy = wheel energy + losses within a few percent.
- [ ] Hybrid result reported at dSOC near zero.
