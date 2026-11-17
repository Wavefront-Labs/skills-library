---
id: creative-arts.animation.blender.soft-body-solver
name: soft-body-solver
category: creative-arts
field: animation
product: blender
tags: [blender, soft-body, soft-body-solver, soft-body-step-size, error-limit, choke]
level: practitioner
status: docs-checked
description: "Stabilise Blender soft body simulations with solver settings: min/max step, auto-step, error limit, choke, fuzzy and diagnostics for missed collisions and jitter."
sources:
  - https://docs.blender.org/manual/en/latest/physics/soft_body/settings/solver.html
  - https://docs.blender.org/manual/en/latest/physics/soft_body/collision.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# soft-body-solver

## Settings (Physics > Soft Body > Solver)

- **Step Size Min**: minimum simulation steps per frame. Increase it if the soft body misses fast-moving collision objects.
- **Max**: maximum steps per frame. Normally the number of steps is set dynamically through the Error Limit.
- **Auto-Step**: uses velocities to choose step sizes automatically, so the solver does the work that fast motion needs.
- **Error Limit**: rules the overall quality; the most critical setting for how precisely collisions are checked. The manual says to start with half the average edge length, and to decrease it if you see visible errors, jitter or over-exaggerated responses. The solver does adaptive step sizing based on how "bad" it is doing.
- **Fuzzy**: fuzziness on collision. High values make collision handling faster but less stable and less accurate.
- **Choke**: calms down (reduces the exit velocity of) a vertex or edge once it penetrates a collision mesh.
- **Diagnostics > Print Performance to Console**: prints how the solver is doing.
- **Diagnostics > Estimate Transforms**: estimates a matrix split into centre of mass, rotation and scale (the manual does not say more).

## Exploding or leaky sim checklist

1. Lower Error Limit and carefully raise Step Size Min (the manual's collision advice).
2. Raise Choke (up to the maximum if needed) if repelled vertices misbehave.
3. Make collision Outer and Inner padding large enough, without overlapping zones of opposite faces.
4. Check collider face normals.
5. Reduce spring stiffness (Pull, Push) or raise Damp; the manual notes high Pull values near the maximum get unstable.

## Gotchas

- Speed (Simulation panel) ties sim tempo to frame rate, so changing frame rate changes behaviour unless Speed is adjusted.
- Changing any setting means clearing the cache and re-simulating.

## Verify

Run the same sim with a high and a lower Error Limit: the lower value reduces jitter; Print Performance to Console reports solver stats.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: all Solver panel fields and the error-limit guidance, the Good Collisions list in the soft body collision page. Corrected the label Estimate Transform Matrix to Estimate Transforms. Removed the numeric ranges for Step Size Min and Error Limit and the "leave Auto-Step on" advice, which are not in the manual.
Method: documentation only; no commands were run.
