---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.sprayer-boom-height-and-stability
name: sprayer-boom-height-and-stability
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, boom-stability, sprayer-design, boom-height, boom-suspension, spray-pattern-overlap, height-control]
level: practitioner
status: draft
description: "Set boom height and nozzle overlap for uniform distribution, and design or diagnose boom suspension: roll and yaw behaviour, auto height control and transport."
sources:
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
  - "Hunt & Wilson, Farm Power and Machinery Management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sprayer boom height and stability

**Goal:** uniform spray distribution across the width at all speeds.

## Height and overlap
Flat fan nozzles must overlap; the manufacturer gives minimum heights for each spray angle and spacing. Typical guidance: 110 degree nozzles at 50 cm spacing need about 50 cm boom height above the target; 80 degree nozzles need higher, about 75 cm. Follow the maker's chart; height is measured to the target canopy, not the ground.

## Boom suspension
- Passive pendulum suspensions isolate roll; hydraulic or electronic levelling add active control using ultrasonic or radar sensors.
- Yaw (fore-aft whip) is a function of boom width, speed, and steering movements; use dampers and yaw control.
- Stiffness: boom frame resonance must be away from forcing frequencies (field roughness and tractor movement).

## Setup and checks
1. Calibrate height sensors at the working height on a flat surface.
2. Check boom folding geometry for level wings.
3. Test on a rough track: observe the movement of the boom ends at working speed.
4. Fit and check breakaway hinges for obstacle strikes.

## Gotchas
- Faster speeds on rough ground cause bounce and uneven distribution.
- Boom drop during transport damages nozzles and hydraulics.
- Wear in pivot bushes allows sag.

## Verify
- [ ] Patternator or visual check shows even deposits along the boom (see nozzle test).
- [ ] Boom height stays within about 10 cm of target in an operating test.
