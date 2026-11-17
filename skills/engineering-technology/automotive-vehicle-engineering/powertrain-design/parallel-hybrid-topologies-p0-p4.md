---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.parallel-hybrid-topologies-p0-p4
name: parallel-hybrid-topologies-p0-p4
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [parallel-hybrid, p0, p1, p2, p3, p4, mild-hybrid, belt-starter-generator, hybrid-topology]
level: practitioner
status: gated
description: "Choose a parallel hybrid motor position (P0 to P4): what each can do, losses, packaging, and the functions and regen capability it enables."
sources:
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# P0 to P4 parallel hybrid topologies

- **P0:** belt-driven starter-generator on the engine front (position definitions P0-P4 follow the Wikipedia hybrid-vehicle-drivetrain article, a secondary source). Cheap, mild hybrid; stop-start, small torque assist, limited regen (belt limits power) (gated: unconfirmed, source is paywalled or blocked).
- **P1:** motor on the crankshaft (between engine and clutch/transmission). Better torque assist and regen; no EV mode unless a clutch isolates the engine.
- **P2:** motor between the engine clutch and the transmission input. Enables EV drive, engine disconnect, strong regen and assist; common in plug-in hybrids.
- **P3:** motor at the transmission output. Higher efficiency regen path (skips gearbox losses for some modes (gated: unconfirmed, source is paywalled or blocked)), still fixed ratio.
- **P4:** motor on a separate axle, commonly the rear axle (e.g. electric rear axle on front-drive engine car); provides AWD without a driveshaft; regen on that axle.
- Choose using: functions required (EV range, boost, regen power), cost, packaging, NVH (engine start events), thermal.
- Voltage: 48 V mild vs high voltage for strong hybrids.
- Combine architectures (P2+P4) for performance PHEVs.

**Gotchas:** engine start smoothness in P2 with a clutch requires careful torque filling.

## Verify
- [ ] Table of functions vs topology matched to requirement list.
- [ ] Vehicle simulation of the cycle for 2-3 candidate topologies.
