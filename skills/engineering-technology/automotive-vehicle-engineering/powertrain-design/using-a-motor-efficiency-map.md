---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.using-a-motor-efficiency-map
name: using-a-motor-efficiency-map
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [motor-efficiency-map, efficiency-map, iso-efficiency, motor-losses, operating-points, cycle-weighting]
level: practitioner
status: gated
description: "Read and use motor and inverter efficiency maps: iso-efficiency contours, loss maps, overlaying cycle operating points and weighting designs by cycle."
sources:
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Motor efficiency map use

1. Map axes: speed vs torque; contours of combined motor + inverter efficiency (peak commonly 92-97% for modern traction drives (gated: unconfirmed, source is paywalled or blocked); typical use areas lower).
2. Light-load/low-speed regions have low efficiency because fixed losses dominate; high torque at low speed has copper losses; high speed has iron losses.
3. Overlay operating points from a simulated cycle: compute torque/speed at each time step, plot as a scatter or as a time-weighted histogram.
4. Cycle-weighted efficiency = total mechanical energy out / total electrical in (motoring) and electrical out / mechanical in (regen), kept separately.
5. Use to choose gear ratio, base speed and number of drive units (e.g. disconnect axle) so common points fall in high-efficiency areas.
6. Use losses, not efficiency, when interpolating maps and when computing power at low torque.

**Gotchas:** maps depend on DC voltage and temperature; use maps at the right bus voltage.

## Verify
- [ ] Cycle-weighted motoring and regen efficiencies reported.
- [ ] Sensitivity of the weighted efficiency to ratio shown.
