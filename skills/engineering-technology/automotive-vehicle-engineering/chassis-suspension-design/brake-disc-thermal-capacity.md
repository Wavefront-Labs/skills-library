---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.brake-disc-thermal-capacity
name: brake-disc-thermal-capacity
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [brake-disc-thermal, disc-temperature, brake-energy, heat-capacity, fade-margin, ventilated-disc, brake-sizing]
level: practitioner
status: gated
description: "Estimate disc temperature rise from braking energy and heat capacity, set a design cycle and check cooling, mass and thermal-fade margin."
sources:
  - "Limpert, Brake Design and Safety"
  - "Newcomb and Spurr, Braking of Road Vehicles"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Disc thermal capacity

1. Energy to stop from speed v: `E = 0.5*m*v^2`. Example: 1800 kg from 100 km/h (27.8 m/s): `E = 0.5*1800*27.78^2 = 694 kJ`.
2. Axle share: front about 60-75% of brake energy at typical deceleration (gated: unconfirmed, source is paywalled or blocked); per disc half of the axle energy: for 70% front, about 243 kJ per front disc (computed).
3. Adiabatic temperature rise: `dT = E_disc/(m_disc*c)` with cast iron c about 460 J/(kg K) (gated: unconfirmed, source is paywalled or blocked): with an 8 kg disc, `243000/(8*460) = 66 K` (computed) per stop from 100 km/h. A stop from 200 km/h has four times the energy.
4. Design events: repeated stops (e.g. standard fade tests), a mountain descent (continuous power `P = m*g*v*sin(theta)`), and a high-speed stop; keep the maximum disc temperature below the pad and disc limits (cast-iron discs and pads have specific temperature capabilities; check supplier data) and brake fluid below boiling.
5. Cooling: ventilated discs and ducting lower the equilibrium temperature; convection coefficient grows with speed.
6. Disc mass and size set heat capacity; larger diameter increases torque (via effective radius) but needs wheel packaging (see wheel-package).
7. Validate with a dynamometer (inertia dyno) and a vehicle test with thermocouples.

**Gotchas:** thermal gradients cause cracks/judder; check hot judder.

## Verify
- [ ] Simulation vs measured disc temperature after the design cycle within about 10%.
- [ ] Fluid temperature below the safe limit with margin.
