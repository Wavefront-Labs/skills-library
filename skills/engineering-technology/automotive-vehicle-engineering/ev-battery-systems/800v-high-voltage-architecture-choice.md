---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.800v-high-voltage-architecture-choice
name: 800v-high-voltage-architecture-choice
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [800v-architecture, 800v, high-voltage-architecture, voltage-class-b, charging-voltage, sic-inverter, pack-architecture]
level: practitioner
status: gated
description: "Weigh 400 V versus 800 V traction systems: current, cable and loss savings, charging implications, component availability and compatibility with 400 V chargers."
sources:
  - "ISO 6469 series and UN R100 voltage class definitions; confirm current editions"
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# High-voltage architecture choice

1. Same power at double voltage means half the current: `P = V*I`; conductor loss `I^2 R` falls to a quarter for the same cable, or cable cross-section can be reduced.
2. Charging: 800 V packs reach high charge power with lower current (less cable heating), enabling high-power charging (250-350 kW class is a vendor figure (gated: unconfirmed, source is paywalled or blocked)); needs compatible chargers.
3. Compatibility with 400 V chargers: either a DC-DC boost stage, or pack/inverter re-configuration (split pack switched in series/parallel), or use the motor inverter as a booster; each has cost, mass and efficiency impacts.
4. Components: SiC inverters, 1200 V class semiconductors, higher insulation rating for connectors and cables, creepage/clearance, contactors/fuses rated for the voltage; voltage class B (above 60 V DC up to 1500 V DC) is the ISO 6469 / UN R100 definition (gated: unconfirmed, source is paywalled or blocked); FMVSS 305 applies above 60 V DC or 30 V AC working voltage (49 CFR 571.305, fetched from LII); confirm the current edition.
5. Auxiliary loads: HVAC compressor and PTC need matching voltage; DC-DC converters designed for the range.
6. Trade study: cost of components versus charging time, cable mass, efficiency; the benefit is not automatic.

**Gotchas:** higher voltage raises isolation monitoring and partial-discharge requirements.

## Verify
- [ ] Charge-time and loss comparison for the two architectures on the same vehicle.
- [ ] Component voltage ratings and insulation coordination reviewed.
