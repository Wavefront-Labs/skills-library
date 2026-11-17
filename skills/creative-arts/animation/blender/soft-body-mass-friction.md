---
id: creative-arts.animation.blender.soft-body-mass-friction
name: soft-body-mass-friction
category: creative-arts
field: animation
product: blender
tags: [blender, soft-body, soft-body-mass, soft-body-friction, soft-body-speed, mass-vertex-group]
level: practitioner
status: docs-checked
description: "Set Blender soft body object settings: mass and the Control Point mass vertex group, friction of the surrounding medium, speed time scaling and collision collection."
sources:
  - https://docs.blender.org/manual/en/latest/physics/soft_body/settings/object.html
  - https://docs.blender.org/manual/en/latest/physics/soft_body/settings/simulation.html
  - https://docs.blender.org/manual/en/latest/physics/soft_body/collision.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# soft-body-mass-friction

## Object settings (Physics > Soft Body > Object)

- **Friction**: friction of the surrounding medium. It dampens movement; the larger it is, the more viscous the medium, and it appears whenever a vertex moves relative to that medium.
- **Mass**: mass of the vertices. Larger mass slows acceleration and adds inertia, so braking is harder, except for gravity, where motion is the same whatever the mass.
- **Control Point**: a vertex group of painted weights used for per-vertex mass values.

## Simulation (Speed)

**Speed** sets the internal timing of the soft body: the correlation between frame rate and simulation tempo. The manual's example: at 25 frames per second, set Speed to 1.3 to match real-world free fall. Use it to adjust the scale of scene and sim.

## Collision Collection

Collision Collection limits which colliders affect the soft body: when set, a collider must belong to the collection (and still needs Collision physics).

## Mass vs goal

High mass with a weak goal gives a large lagging overshoot; low mass with a strong goal gives a tight, quick jiggle. Tune them together (see `soft-body-goal`).

## Recipe: antenna with a heavy ball tip

Mass vertex group (Control Point) heavier on the ball than at the base; goal group weight high at the base fading toward the tip; Edges Pull moderately high and Damp moderate.

## Gotchas

- Mass does not change gravitational acceleration, only inertia against springs and forces such as wind.
- Changing frame rate changes sim tempo unless Speed is adjusted.

## Verify

Increasing Mass visibly slows the jiggle; a high Friction makes motion syrupy.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Friction, Mass and Control Point definitions, the gravity-versus-mass note, Speed and its 25 fps / 1.3 example, and the Collision Collection prerequisite. Corrected: friction is a medium viscosity (not specifically air), and Speed is under Simulation. Removed the friction value suggestion, recipe numbers and the "very low mass needs more solver steps" claim.
Method: documentation only; no commands were run.
