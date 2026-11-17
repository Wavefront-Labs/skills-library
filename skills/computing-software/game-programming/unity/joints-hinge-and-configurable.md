---
id: computing-software.game-programming.unity.joints-hinge-and-configurable
name: joints-hinge-and-configurable
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-physics, unity-joints, configurablejoint, hingejoint, articulationbody, joint-drives, game-programming]
level: advanced
status: docs-checked
description: "Configure a Unity Configurable Joint: anchors, axis motion, limits, drives, projection, break force and mass scale, plus where the other joint components are documented."
sources: ["https://docs.unity3d.com/Manual/joints-section.html", "https://docs.unity3d.com/Manual/class-ConfigurableJoint.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Joints: configurable joint reference

**Goal:** set up a Configurable Joint (ragdoll poses, physical grabs, custom constraints) with the documented properties.
Unity 6000.x docs.

## What joints are
A Joint connects a Rigidbody to another Rigidbody, or to a fixed point in space. Joints can apply forces that move rigid
bodies, and joint limits can restrict that movement. Configure through the `Joint` class or the Joint component. The
Joints section lists Character, Fixed, Hinge and Spring Joint component references plus "Create a configurable joint".
Their property pages were not read for this version, so no per-joint guidance is given for them.

A Configurable Joint incorporates the functionality of the other joint types and gives greater control of character
movement. It suits customising ragdoll movement and enforcing poses.

## Connection and axes
- **Connected Body**: set to None to attach to a fixed position in space. **Connected Articulation Body**: optional; if
  not set the joint connects to the world.
- **Anchor**: centre of the joint, used by all physics calculations. **Axis** / **Secondary Axis** define the joint's
  local coordinate system; the third axis is orthogonal.
- **Auto Configure Connected Anchor** (default on) matches Connected Anchor to the anchor's global position; turn it off to
  set **Connected Anchor** manually.
- **X/Y/Z Motion** and **Angular X/Y/Z Motion**: Free, Locked or Limited.

## Limits
- **Linear Limit** (Limit distance, Bounciness, Contact Distance) with **Linear Limit Spring**; spring 0 makes the limit
  impassable, non-zero makes it elastic.
- **Low/High Angular X Limit** (angle, Bounciness, Contact Distance), **Angular X Limit Spring**, **Angular YZ Limit
  Spring**, **Angular Y Limit**, **Angular Z Limit** (upper and lower the same).
- A higher Contact Distance makes fast objects less likely to break past a limit but costs slightly more performance.
- **Edit Angular Limits** adds a Scene-view gizmo once the angular motion is Limited.

## Drives
- **Target Position** / **Target Velocity**; **Target Rotation** (quaternion, relative to the body the joint is attached
  to unless Swap Bodies is set) / **Target Angular Velocity**.
- **X/Y/Z Drive**: Position Spring, Position Damper, Maximum Force, Use Acceleration (acceleration drive instead of force
  drive). Set Maximum Force high enough that it does not clip the computed force.
- **Rotation Drive Mode**: X & YZ uses Angular X Drive and Angular YZ Drive; Slerp uses the Slerp Drive for all axes.
- **Configured in World Space** computes targets and drives in world space instead of local space.

## Stability and breaking
- **Projection Mode** (None, or Position and Rotation), **Projection Distance**, **Projection Angle**: snap the joint back
  when it moves beyond its constraints.
- **Mass Scale** / **Connected Mass Scale** (0.00001 to infinity): the solver does better when connected bodies have similar
  mass; these apply fake masses to make them roughly equal, at some cost in physical behavior.
- **Enable Preprocessing** off keeps certain "impossible" configurations more stable instead of drifting.
- **Enable Collision**: lets the jointed objects collide with each other; otherwise they pass through.
- **Break Force**: beyond it the joint is permanently broken and deleted, but only when axes are Limited or Locked.
  **Break Torque** breaks regardless of Free, Limited or Locked axes.
- **Swap Bodies** swaps processing order of the bodies (different joint motion, no effect on bodies and anchors).

## Checked
Date: 2026-11-07.
Read in full: "Joints" section page (6000.6 docs) and "Configurable Joint component reference" (all properties).
Removed as unconfirmed: the pick-the-joint table (Fixed, Hinge, Spring, Character, ArticulationBody advice), HingeJoint
code with `JointLimits` / `JointSpring`, `OnJointBreak`, the claim that `targetPosition` is negated, mass ratio under 10:1,
`solverIterations`, `maxAngularVelocity` and ArticulationBody guidance, and the invented Verify checklist. The Hinge,
Fixed, Spring and Character Joint pages and the "Create a configurable joint" pages were not opened. The "Joints" page is a
short index, so this skill is limited to the Configurable Joint reference.
Method: documentation only; no commands were run.
