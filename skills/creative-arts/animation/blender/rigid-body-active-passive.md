---
id: creative-arts.animation.blender.rigid-body-active-passive
name: rigid-body-active-passive
category: creative-arts
field: animation
product: blender
tags: [blender, rigid-body, rigid-body-active-passive, animated-rigid-body, kinematic, rigid-body-deactivation, rigid-body-damping, sleeping]
level: practitioner
status: docs-checked
description: "Set Blender rigid body types: Active vs Passive, the Animated toggle and handing a keyed object to the sim, plus Deactivation, Start Deactivated and damping."
sources:
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/introduction.html
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/properties/dynamics.html
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/tips.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# rigid-body-active-passive

## Types

Add from the Physics tab (Rigid Body button) or Object > Rigid Body > Add Active / Add Passive. Only mesh objects can be rigid bodies.

- **Active**: dynamically simulated. **Passive**: stays static (floor, walls).
- **Animated** (Physics > Rigid Body > Settings): lets the animation system also control the body. It applies to both types.
- Common mistake: keyframing a Passive object without ticking **Animated**; it moves, but the physics engine still treats it as being at its starting place.

## Handing over from animation to simulation

1. Keyframe the location or rotation of an Active body together with the **Animated** checkbox.
2. When the curve on Animated switches to disabled, the physics engine takes over from the object's last known location, rotation and velocities.
3. Bake if needed (see `rigid-body-bake-to-keyframes`).

## Deactivation and damping (Physics > Rigid Body > Dynamics, Active bodies only)

- **Damping Translation / Rotation**: amount of linear and angular velocity lost over time.
- **Deactivation** (checkbox): allows resting bodies to be deactivated; improves performance and stability but can cause glitches.
  - **Start Deactivated**: the body starts deactivated and activates when a moving active body comes near; proximity uses the bounding box.
  - **Linear Velocity / Angular Velocity**: velocity below which the body is deactivated.

## Gotchas

- Scale influences the sim and is always controlled by the animation system; apply scale (Ctrl+A) unless you need dynamic scaling.
- Simulation overrides the displayed transform but does not change the object's location and rotation values; use Apply Object Transform to apply the result.
- Enabling a constraint mid-sim between badly aligned objects can fling them.

## Verify

Play from the first frame of the cache: passive objects stay fixed, animated ones push actives, deactivated stacks wait until hit.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Active and Passive definitions, the Animated checkbox behaviour and the keyframe-then-disable handoff, the Dynamics panel fields (damping, deactivation, Start Deactivated, velocities), the scale note and Ctrl+A. Removed the claim that damping is "per second" and the "short-lived force field" and "leave a gap" advice, which the manual does not cover.
Method: documentation only; no commands were run.
