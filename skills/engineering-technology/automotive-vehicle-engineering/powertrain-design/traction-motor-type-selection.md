---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.traction-motor-type-selection
name: traction-motor-type-selection
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [motor-selection, pmsm, induction-motor, ipm, wound-rotor-synchronous, switched-reluctance, traction-motor]
level: practitioner
status: draft
description: "Select a traction motor type (IPM PMSM, induction, wound-field, switched reluctance) against efficiency, cost, magnet supply, speed range and thermal limits."
sources:
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
  - "Pyrhonen et al., Design of Rotating Electrical Machines"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Traction motor type selection

- **Interior permanent magnet synchronous (IPM PMSM):** highest torque and power density and efficiency over a wide area; uses rare-earth magnets (cost, supply risk); needs field weakening above base speed with possible back-EMF risk in faults; most common in passenger EVs.
- **Induction (squirrel-cage):** no magnets, robust, cheaper; lower efficiency at light load, rotor losses and heat; good at high speed and for low-cost designs.
- **Wound-rotor (externally excited) synchronous:** no magnets, adjustable field gives efficiency and field control; needs slip rings/brushes or contactless rotary transformers.
- **Switched reluctance:** simple and robust, no magnets; torque ripple and acoustic noise challenges.
- Selection criteria: peak and continuous torque/power, efficiency map weighting on the target cycle, cost including magnets, speed range (field-weakening ratio), thermal design, NVH, safety in faults (uncontrolled generation, short-circuit torque), supply chain.
- Decide with a model of each option on the same vehicle and cycle.

**Gotchas:** comparing peak efficiency numbers alone; use cycle-weighted efficiency.

## Verify
- [ ] Cycle-weighted efficiency and cost compared for the candidates.
- [ ] Fault behaviour at high speed reviewed for the chosen type.
