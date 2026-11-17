---
id: engineering-technology.automotive-vehicle-engineering.nvh.firing-order-excitation-and-engine-orders
name: firing-order-excitation-and-engine-orders
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [engine-orders, firing-order, engine-excitation, order-analysis, balance-shaft, inertia-forces]
level: practitioner
status: gated
description: "Compute engine order content from cylinder count and cycle, identify unbalanced forces and couples by layout, and map orders to rpm for diagnosing noise."
sources:
  - "Heywood, Internal Combustion Engine Fundamentals"
  - "Harrison, Vehicle Refinement"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Firing-order excitation and engine orders

1. Four-stroke firing frequency: `f_fire = (rpm/60)*(N_cyl/2)`; the dominant order is `N_cyl/2` (2nd for a 4-cylinder, 1.5 for a 3-cylinder, 3rd for an in-line 6, 4th for a V8). Example: a 4-cylinder at 3000 rpm: firing frequency 100 Hz.
2. Harmonics: multiples of the firing order and half-orders for misfire or cylinder-to-cylinder variation.
3. Inertial balance (textbook statements (gated: unconfirmed, source is paywalled or blocked); check with the engine design): inline-4 has a free second-order vertical force (needs balance shafts at twice crank speed for refinement); inline-3 has a first-order rocking couple; inline-6 is smooth in primary and secondary forces and couples; V8 cross-plane has a first-order couple managed by counterweights.
4. Torque pulsations from gas pressure create rotating torque variation transmitted to mounts and driveline; the flywheel and dual-mass flywheel reduce transmission.
5. Plot orders vs rpm on a Campbell diagram to match resonances (body, driveline, exhaust) with orders to find rpm where booms occur.
6. Use order tracking (see order-tracking) to measure.

**Gotchas:** crank/cam order mixing; rpm signal quality.

## Verify
- [ ] Campbell diagram orders match the measured peaks.
- [ ] Predicted free forces for the engine layout confirmed with the engine supplier data.
