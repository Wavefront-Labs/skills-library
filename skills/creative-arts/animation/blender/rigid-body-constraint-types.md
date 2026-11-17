---
id: creative-arts.animation.blender.rigid-body-constraint-types
name: rigid-body-constraint-types
category: creative-arts
field: animation
product: blender
tags: [blender, rigid-body, rigid-body-constraint-types, hinge, motor-constraint, generic-spring, connect-rigid-bodies, breakable-constraints, breaking-threshold]
level: practitioner
status: verified
description: "Link Blender rigid bodies with constraints (fixed, point, hinge, slider, piston, generic, generic spring, motor), the Connect tool, and breakable thresholds for destruction."
sources:
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/constraints/introduction.html
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/constraints/types/index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# rigid-body-constraint-types

## Types (Physics > Rigid Body Constraint > Type)

API `RigidBodyConstraint.type`: `FIXED`, `POINT`, `HINGE`, `SLIDER`, `PISTON`, `GENERIC`, `GENERIC_SPRING`, `MOTOR`. Defaults in 4.5.14: linear limits -1 to 1, angle limits -45 to 45 degrees, spring stiffness 10 and damping 0.5 per axis, breaking threshold 10, motor target velocity 1 and max impulse 1.

- **Fixed**: the two objects move as one, with a little physics slop.
- **Point**: ball joint; any rotation around the constraint location, no relative translation.
- **Hinge**: one rotational degree of freedom about the **Z** axis of the object hosting the constraint (unlike the other single-axis rotational constraints, which use X). Optional **Z Angle** limit with Lower and Upper.
- **Slider**: translation along the constraint object's **X** axis only; **X Axis** limit with Lower and Upper.
- **Piston**: translation along X plus rotation around X; has **X Axis** and **X Angle** limits.
- **Generic**: per-axis linear (X/Y/Z Axis) and angular (X/Y/Z Angle) limits with Lower and Upper. Clamping translation to zero acts like Point; clamping rotation to zero keeps alignment; both together behave much like Fixed. A nonzero spread lets a value oscillate in its range.
- **Generic Spring**: Generic plus springs per axis (**Stiffness** and **Damping** for each translation and rotation axis). Damping set to 1 prevents spring forces from realigning the anchors and causes strange behaviour.
- **Motor**: Linear Motor and Angular Motor, each with **Enable**, **Target Velocity** and **Max Impulse**. The rotation axis is the host's **X** axis, so it needs a matching Hinge setup with aligned axes (otherwise it appears to do nothing). Breakable is disabled for Motor.

## Creating constraints

- Constraints attach to an **Empty**; the empty gives the location and axes, and the **Objects > First / Second** fields point at the two bodies. The anchors are calculated at the start of the animation and then stay fixed in each object's local space.
- Quickest: select both objects and use **Object > Rigid Body > Connect**, which creates an empty named "Constraint" already pointing at the two.
- Or use the **Rigid Body Constraint** button in the Physics tab on one of the two objects; that object then plays the role of the empty (setting it to Passive helps drive it).

## Common options

- **Enabled**; **Disable Collisions** (lets the constrained objects pass through each other); **Breakable** with **Threshold** (impulse strength that must be reached before the constraint breaks); **Limits** (set both limits to 0 to lock an axis); **Override Iterations** with **Iterations** (stronger or weaker than the world solver setting).

## Gotchas

- Hinge and Motor use different axes (Z versus X); rotate the empty, not the bodies, to aim them.
- Enabling a constraint mid-sim between badly aligned objects often gives dramatic results: objects can bounce out of camera.
- Animate Motor Target Velocity, Hinge limits and similar for varied effects.

## Verify

Play: hinges swing on the correct axis, motors spin once aligned, fixed pieces hold and break only past the threshold.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: every constraint type's axes and limits, Generic Spring damping warning, Motor fields and Z-versus-X note, Connect and the Physics-tab creation route, common options. Removed the unconfirmed Connect dialog options (Type, Location, Connection Pattern), the "Add Constraint" menu entry, the Disable Collisions default and the Bullet spring-type remark; the manual does not document them.
Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): RigidBodyConstraint type items, use_limit_lin_x/y/z, use_limit_ang_x/y/z, use_spring_*, spring_stiffness_*, spring_damping_*, use_motor_lin and use_motor_ang with target velocity and max impulse, use_breaking and breaking_threshold, use_override_solver_iterations, disable_collisions, object1 and object2; bpy.ops.rigidbody.connect exists; spring_type SPRING1/SPRING2 also exists. Not run (confirmed from the manual only): which axis each type uses (Hinge Z, others X), the Motor alignment note, anchors being fixed at animation start, and the creation workflows.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
