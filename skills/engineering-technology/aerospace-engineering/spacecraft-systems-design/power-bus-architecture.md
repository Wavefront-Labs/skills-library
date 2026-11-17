---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.power-bus-architecture
name: power-bus-architecture
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [power-bus, power-subsystem, direct-energy-transfer, peak-power-tracking, bus-voltage, battery-charge-regulator]
level: practitioner
status: draft
description: "Choose a spacecraft power bus architecture (unregulated, regulated, sun-regulated), set bus voltage and plan protection, distribution and fault isolation."
sources:
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Fortescue et al., Spacecraft Systems Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Power bus architecture

**Goal:** a bus that delivers regulated power through sunlight and eclipse with failure isolation.

## Architectures
- **Direct energy transfer (DET)**: array power goes straight to the bus; shunt regulation in sunlight, battery discharge in eclipse. Simple, efficient; the bus is regulated in sunlight and follows the battery in eclipse (a sun-regulated bus) or is fully regulated with extra converters.
- **Peak power tracking (PPT / MPPT)**: a DC-DC converter runs the array near its maximum power point; gains power at end of life and cold arrays, costs conversion loss and mass.
- **Unregulated bus**: bus voltage follows battery voltage; loads need their own regulation.
- **Fully regulated bus**: a charge regulator and discharge regulator hold bus voltage across modes.

## Design steps
1. Choose bus voltage: higher voltage reduces harness current and mass; legacy buses are 28 V, larger platforms use 50 V to 100 V or more, and small satellites often use 3.3 V and 5 V or a battery-direct bus. Check launch and range rules for high voltage in vacuum (discharge risk).
2. Define modes: sunlight, eclipse, battery charge, safe mode, launch.
3. Choose protections: latching current limiters, fuses, overvoltage and undervoltage cutoffs, separation of essential and non-essential loads.
4. Size converters, harness losses, and diodes.
5. Define grounding: single-point ground, structure return, isolation for noisy loads.
6. Analyse failure cases: short on a load, array string loss, battery cell failure.

## Gotchas
- Arrays and battery states change bus behaviour across life; analyse beginning and end of life.
- Inrush currents from converters and motors need controlled start-up.
- Keep a power-positive safe mode sized with the worst-case attitude.

## Verify
- [ ] A power-balance simulation over an orbit shows positive battery energy balance and bus voltage within limits in all modes.
