---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.torque-speed-envelope-and-base-speed
name: torque-speed-envelope-and-base-speed
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [torque-speed-envelope, base-speed, constant-power, field-weakening, peak-torque, continuous-rating]
level: practitioner
status: gated
description: "Define the motor torque-speed envelope: base speed, constant-torque and constant-power regions, voltage limits, and continuous versus peak ratings."
sources:
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
  - "Pyrhonen et al., Design of Rotating Electrical Machines"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Torque-speed envelope and base speed

1. From performance: required wheel force at launch sets peak torque after the reduction ratio; required top speed/power sets maximum power and speed.
2. Envelope: constant torque `Tmax` up to **base speed** `w_b`, constant power `Pmax = Tmax*w_b` above (field weakening for PMSM, flux reduction for induction), then falling at very high speed where voltage and current limits tighten.
3. Choose base speed to balance: low base speed gives strong launch torque and long constant-power range; the motor and inverter size scale with `Tmax` (current) and speed (voltage).
4. Voltage dependence: available torque at high speed falls if DC bus drops (low SOC); specify envelope at minimum voltage.
5. Continuous rating: thermal limit gives lower torque (often about 40-60% of peak for a lightly-cooled design (gated: unconfirmed, source is paywalled or blocked); check design) sustained; peak lasts 10-30 s limited by winding temperature (gated: unconfirmed, source is paywalled or blocked).
6. Check the ratio of maximum to base speed (extended speed ratio) against the machine type capabilities.

**Gotchas:** quoting peak power at nominal voltage only.

## Verify
- [ ] Envelope plotted at minimum and nominal DC voltage.
- [ ] Vehicle performance (0-100, 80-120, grade) meets targets from the envelope.
