---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.twist-beam-and-solid-axle-layout
name: twist-beam-and-solid-axle-layout
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [twist-beam, torsion-beam, solid-axle, panhard-rod, watts-link, leaf-spring, roll-steer]
level: practitioner
status: draft
description: "Design a twist-beam or live-axle rear suspension: beam torsion stiffness, trailing-arm bushes, roll steer, lateral location and packaging."
sources:
  - "Reimpell, Stoll and Betzler, The Automotive Chassis"
  - "Milliken and Milliken, Race Car Vehicle Dynamics"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Twist beam and solid axle layout

1. **Twist beam (compound crank):** trailing arms joined by a cross-beam that twists in roll and provides roll stiffness; cheap, compact, with flat load floor; kinematic changes through bushing compliance.
2. Roll stiffness: set by beam section (open profile such as V or U) and its position relative to the shear centre; check stress and fatigue in welds near the arms.
3. Behaviour: low bump camber change; roll steer determined by the bush axes (trailing-arm bush angles) and beam position; compliance steer under lateral loads from the front bushes; use bushes with angled axes to get toe-in under lateral load.
4. **Live (solid) axle:** with leaf springs or coil springs and control arms; lateral location by Panhard rod or Watts link; roll centre height determined by the lateral link height; heavy unsprung mass but robust for loads.
5. Panhard rod: lateral displacement of the axle with bump (arc); long rods and mid-travel horizontal reduce this.
6. Compare with multi-link on cost, mass, packaging, ride and handling targets.
7. Durability: weld seams, bush loads, spring seats.

**Gotchas:** ride harshness from wheel-hop of a heavy axle; handling consequences of high roll centre.

## Verify
- [ ] Roll steer and compliance steer measured on K&C rig vs target.
- [ ] Weld fatigue life with road-load data meets the requirement.
