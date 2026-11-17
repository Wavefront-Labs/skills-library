---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.single-speed-reduction-gear-selection
name: single-speed-reduction-gear-selection
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [ev-reduction-gear, reduction-gear, final-drive-ratio, ev-gear-ratio, motor-speed, single-speed]
level: practitioner
status: gated
description: "Select the EV reduction ratio from top speed, motor maximum speed and launch torque, and check efficiency, NVH and gear loading."
sources:
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
  - "Naunheimer et al., Automotive Transmissions"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Single-speed reduction gear selection

1. Maximum motor speed `n_max` and top speed `v_max` give the ratio upper bound: `i = n_max*2*pi*Re/(60*v_max)`; choose slightly below that if power is available at top speed.
2. Launch and grade: wheel force `F = T_motor*i*eta/Re` must meet launch/grade targets: larger i gives more wheel force per unit motor torque.
3. Typical ratios are roughly 7-11:1 for passenger EVs with motors reaching 12,000-18,000 rpm (illustrative (gated: unconfirmed, source is paywalled or blocked); compute for your case: at Re 0.33 m and 180 km/h the formula gives 8.3:1 for 12,000 rpm and 12.4:1 for 18,000 rpm).
4. Trade-off: high i lets a smaller motor torque meet launch (smaller motor) but needs higher motor speed (bearing, magnet retention, losses, NVH).
5. Efficiency: gear mesh loss around 1-2% per mesh (gated: unconfirmed, source is paywalled or blocked); fewer meshes lowers loss; consider planetary or two-stage helical layouts.
6. NVH: helical gears with high contact ratio, gear micro-geometry, housing stiffness.
7. Two-speed options improve top-end efficiency but add shift complexity.

**Gotchas:** efficiency map overlay: place cruise points at high-efficiency region by choosing i.

## Verify
- [ ] Performance (launch, top speed, 80-120 km/h) computed with the chosen ratio.
- [ ] Motor speed limit not exceeded at v_max with worn tyre radius.
