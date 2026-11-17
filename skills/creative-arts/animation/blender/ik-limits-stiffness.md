---
id: creative-arts.animation.blender.ik-limits-stiffness
name: ik-limits-stiffness
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, ik-limits, ik-stiffness, ik-lock, itasc, itasc-solver, inverse-kinematics]
level: practitioner
status: docs-checked
description: "Constrain Blender IK solving per bone: IK Lock, Limit, Stiffness, and the iTaSC solver (Animation vs Simulation mode, precision, iterations, SDLS/DLS)."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/properties/inverse_kinematics.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/posing/bone_constraints/inverse_kinematics/introduction.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/tracking/ik_solver.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# ik-limits-stiffness

## Per-bone IK settings (Properties > Bone > Inverse Kinematics, Pose Mode)

- **Lock X/Y/Z**: disallow movement around the axis. Knees/elbows lock two axes so they bend on one (hinge).
- **Limit X/Y/Z** + Min/Max: limit movement around the axis.
- **Stiffness X/Y/Z**: stiffness around the axis; its influence is disabled when the axis is locked.
- **IK Stretch**: stretch influence to the IK target (see `ik-stretch`).
- With the iTaSC solver the panel adds **Control Rotation** (a joint rotation constraint that follows the bone's pose rotation) with a **Weight**.
- If a Pole Target is used, IK locking does not work on the root bone of the chain.

## Solvers (Properties > Armature > Inverse Kinematics, Pose Mode)

- **Standard**: most people use it.
- **iTaSC** (instantaneous Task Specification using Constraints): a generic multi-constraint IK solver that handles multiple constraints per bone, weighed against each other, plus Distance and Joint Rotation constraints.
  - **Animation** mode: stateless; starts from the pose given by F-Curve interpolation and iterates until the precision is reached; target velocity is ignored.
  - **Simulation** mode: stateful; estimates target velocity, runs in true time, ignores keyframed rotation (except via Control Rotation) and builds a state cache. Settings: **Reiteration** (Never, Initial, Always), **Auto Step** with Min/Max, or fixed **Steps**, **Feedback**, **Max Velocity**.
  - **Precision**: maximum end-effector variation between iterations at which the solver stops. **Iterations**: upper bound. **Solver**: SDLS (automatic damping) or DLS (manual **Damping Max** and **Damping Epsilon**, tuned per armature). SDLS does not work with a Distance constraint, so use DLS if a singular pose is expected.
  - On the IK constraint, iTaSC adds IK Type: Copy Pose (with Axis Reference and Lock Position/Rotation X/Y/Z) or Distance (Limit Mode Inside, Outside, On Surface).

## When to use

- Mechanical/robot chains with many joints and limits: iTaSC Simulation.
- Character limbs: Standard + pole target, locks on hinge joints.
- Tentacles: Spline IK instead.

## Gotchas

- Simulation mode keeps state from earlier frames (a state cache), so results depend on how playback reached a frame.
- With a Pole Target, IK locking does not work on the chain's root bone.

## Verify

Drag the IK target through its range: hinge joints bend only on their free axis and stop at limits; no jitter frame to frame.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Bone Inverse Kinematics properties, IK introduction (Standard and iTaSC) and IK constraint pages: Lock, Limit, Stiffness, IK Stretch, Control Rotation, solver choices, Animation versus Simulation behaviour, Precision, Iterations, SDLS/DLS and the Distance restriction, IK Type options. Removed the unconfirmed Stiffness range, FK-limit remark, stiffness-relative remark and render-farm claim.

Method: documentation only; no commands were run.
