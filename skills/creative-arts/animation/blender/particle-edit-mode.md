---
id: creative-arts.animation.blender.particle-edit-mode
name: particle-edit-mode
category: creative-arts
field: animation
product: blender
tags: [blender, particles, particle-edit-mode, particle-edit, combing, hair-styling]
level: practitioner
status: docs-checked
description: "Edit legacy particle hair and baked particle paths in Particle Edit Mode: brushes, selection modes, options, operators, and the manual's deprecation note for hair."
sources:
  - https://docs.blender.org/manual/en/latest/physics/particles/mode.html
  - https://docs.blender.org/manual/en/latest/physics/particles/emitter/cache.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# particle-edit-mode

Note from the manual: Particle Edit Mode, specifically for hair, is deprecated. Use the Curves hair object with Curves Sculpt Mode instead (see hair-sculpt-mode) for new work.

## Enter

Hair setup per the manual: create a Hair particle system, give it an initial velocity in the Normal direction, create a simulation and tick Hair Dynamics. Then choose **Particle Edit** from the Mode menu in the 3D Viewport header. Press T to show the toolbar if needed.

Emitter, Cloth and Soft Body paths can only be edited after they are **baked in memory** (not with Disk Cache). Bake from Object Mode first. The manual notes that editing a cached cloth simulation is currently not working.

## Brushes (Toolbar)

- **Comb**: moves keypoints (like Proportional Editing). Option Deflect Emitter (hair only) keeps keypoints out of the emitting mesh, with Distance.
- **Smooth**: parallels visually adjacent segments.
- **Add**: new particles, with Count, Interpolate (shape from existing hairs), Steps, Keys.
- **Length**: scales segments, Grow or Shrink.
- **Puff**: rotates hair around its root, Add stands it up and Sub lays it down; Puff Volume applies it to unselected end points.
- **Cut**: scales segments until the last keypoint reaches the brush.
- **Weight**: mainly for soft body, since the weight defines the soft body Goal.
- Radius **F** and Strength **Shift F**.

## Selection and display

- Select modes: **Path** (only whole particles), **Point** (all keypoints visible), **Tip** (only the last keypoint). Switch to Point mode to see and select keypoints.
- Keys: A all, Alt A none, Ctrl I invert, B box, C circle, Ctrl Alt LMB lasso, L select linked, Shift L unselect linked.
- Options: Auto-Velocity (Emitter), Mirror X, Preserve Strand Length, Preserve Root Positions (turn off to move roots).
- Cut Particles to Shape: choose a Shape Object and press Cut.
- Viewport Display: Path Steps, Children (Hair), Particles (Emitter), Fade Time.

## Operators (Particle menu)

Rekey, Subdivide (adds keypoints), Mirror, Merge by Distance (after mirroring), Unify Length (averages the selected hair length), Show/Hide (H and Alt H). You cannot duplicate or extrude keys.

## Verify

Exit Particle Edit and play: the groom persists. With Hair Dynamics the edited shape is the starting shape.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST).
Confirmed: deprecation note for hair; setup steps; baked-in-memory requirement; brush list and options; select modes and shortcuts; Options and Viewport Display names; Particle menu operators.
Removed as unconfirmed: Connect/Disconnect Hair advice, the claim that changing segment count resets grooming, "Remove Doubles" (the manual names Merge by Distance), and the claim that Weight paints hair-dynamics goal weight (the manual describes soft body goal).
Method: documentation only; no commands were run.
