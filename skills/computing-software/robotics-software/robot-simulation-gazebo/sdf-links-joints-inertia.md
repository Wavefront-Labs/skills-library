---
id: computing-software.robotics-software.robot-simulation-gazebo.sdf-links-joints-inertia
name: sdf-links-joints-inertia
category: computing-software
field: robotics-software
product: robot-simulation-gazebo
tags: [sdf-model, link, joint, inertial, revolute-joint, gz-models]
level: practitioner
status: docs-checked
description: "Specify SDF link inertial (mass, inertia, auto inertia) and joint types, axes and limits."
sources:
  - https://raw.githubusercontent.com/gazebosim/sdformat/sdf14/sdf/1.11/inertial.sdf
  - https://raw.githubusercontent.com/gazebosim/sdformat/sdf14/sdf/1.11/joint.sdf
  - https://raw.githubusercontent.com/gazebosim/gz-sim/gz-sim9/tutorials/inertia.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SDF links, inertia and joints

## Inertial (SDF 1.11 spec)
```xml
<link name="base">
  <inertial>
    <mass>1.0</mass>
    <pose>0 0 0 0 0 0</pose>
    <inertia><ixx>0.004</ixx><iyy>0.004</iyy><izz>0.002</izz><ixy>0</ixy><ixz>0</ixz><iyz>0</iyz></inertia>
  </inertial>
</link>
```
Values are illustrative. Spec defaults: mass 1.0, ixx/iyy/izz 1.0, products 0.
- The inertial `pose` is the centre-of-mass frame relative to the link frame; the
  `inertia` is about the centre of mass in that frame.
- Products of inertia use the -m x y sign convention (not +m x y). The spec advises
  aligning the centre-of-mass frame with principal axes so all products are zero.
- `fluid_added_mass` (optional) is a symmetric 6x6 matrix (21 unique elements named xx, xy,
  ... rr); it should be zero when the surrounding fluid is negligible relative to the body.

## Automatic inertia (Gazebo tutorial, needs SDF 1.11 or newer)
- `<inertial auto="true"/>` computes mass, inertia and inertial pose from the link's
  collision geometries; the default is false.
- Supported shapes: box, capsule, cylinder, ellipsoid, sphere, mesh.
- Set `<density>` (kg/m^3, default 1000) in each `<collision>`; densities may differ per
  collision and are aggregated. No collisions gives an `ELEMENT_MISSING` error.
- With auto true, any `<pose>` and `<inertia>` you wrote are overwritten.
- In libSDFormat 14.7.0 / 15.2.0 and newer, an explicit `<mass>` takes precedence over
  density and the result is scaled to match.
- Meshes need water-tight triangle meshes; the tutorial recommends basic shapes for better
  performance, and `convex_hull` or `convex_decomposition` mesh optimisation for
  non-water-tight meshes.

## Joints (SDF 1.11 spec)
- `<joint name type>` with `<parent>` and `<child>` (child may not be `world`; parent may
  be). Default joint pose is in the child link frame.
- Types: continuous, revolute, gearbox, revolute2, prismatic, ball, screw, universal, fixed.
- `<axis><xyz>` (default 0 0 1, should be normalised, optional `expressed_in` frame).
- `<axis><limit>`: `lower` and `upper` (radians revolute, metres prismatic; omit for
  continuous), `effort` (not enforced if negative) and `velocity`, both default inf.
- `<axis><dynamics>`: `damping`, `friction`, `spring_reference`, `spring_stiffness`.
- `axis2` is for revolute2 and universal joints.

## Self-check
`gz sim` loads the model and the joint moves only within the limits you set.

## Checked
Method: docs-checked 2026-11-09 against the sdformat 1.11 inertial.sdf and joint.sdf and the gz-sim9 automatic inertia tutorial (raw GitHub, read in full). Removed as unconfirmed: the box inertia formula, "bad values explode the sim", "collision-less links fall through the world", "overlapping collisions cause jitter", the simple-collision/detailed-visual advice, the claim that the child pose follows rules of the SDF version, and the landing-page source gazebosim.org/docs. The collision/visual geometry spec was not read.
