---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.macpherson-strut-layout
name: macpherson-strut-layout
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [macpherson-strut, mcpherson, strut-suspension, strut-axis, side-load, top-mount, lower-control-arm]
level: practitioner
status: draft
description: "Lay out a MacPherson strut axle: strut axis and steering axis, side load and spring offset, top mount, lower arm and roll centre trade-offs."
sources:
  - "Reimpell, Stoll and Betzler, The Automotive Chassis"
  - "Milliken and Milliken, Race Car Vehicle Dynamics"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# MacPherson strut layout

1. Structure: strut (spring and damper) fixed to the knuckle, top mount to body, lower control arm (A-arm or L-arm) with a ball joint; the steering axis runs from the top mount centre to the lower ball joint.
2. Packaging benefits: compact width, few parts, low cost; disadvantages: strut height needs a tall body mount, limited camber control in roll compared with a double wishbone.
3. Instant centre: the top link direction is perpendicular to the strut axis through the top mount; the lower arm line intersects it to give the front-view instant centre; fine-tune roll centre by lower arm inclination.
4. Side load: lateral force at the wheel produces bending in the strut and friction in the damper rod; offset or tilted spring axis (and bent springs or off-axis spring seats) produce a force opposing side load to reduce rod friction.
5. Top mount: rubber stiffness sets noise isolation and steering feel; includes bearing for steering rotation; check force paths into the strut tower.
6. Knuckle and ball joint location control scrub radius and kingpin offset.
7. Verify kinematics (toe/camber change), compliance and durability loads.

**Gotchas:** strut friction harming small-amplitude ride; tower stiffness.

## Verify
- [ ] Rod side-load computed and reduced by spring offset.
- [ ] Camber and roll centre sweeps meet the kinematics targets.
