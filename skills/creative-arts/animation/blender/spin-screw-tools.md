---
id: creative-arts.animation.blender.spin-screw-tools
name: spin-screw-tools
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-editing, spin-tool, screw-tool, spin-duplicates, lathe, revolve]
level: practitioner
status: docs-checked
description: "Lathe profiles in Blender Edit Mode with Spin (Steps, Angle, Center, Axis, Use Duplicates, Auto Merge) and Screw (Steps, Turns, open profile) versus the Screw modifier."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/tools/spin.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/screw.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/screw.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# spin-screw-tools

Goal: lathe profiles into vases, wheels and bolts, or duplicate parts radially.

## Spin (toolbar Spin tool, or Mesh > Extrude > Spin)

1. Draw a profile in Edit Mode and snap the **3D cursor** to the rotation centre (for example Mesh > Snap > Cursor to Selection on a centre vertex).
2. The view decides the spin axis; use the top view (`Numpad 7`) to spin around Z. Select the geometry, choose the Spin tool and drag its gizmo.
3. Options (tool settings and redo panel): **Steps** (copies along the sweep), **Angle** (e.g. 180 for half a turn), **Center X/Y/Z** (defaults to the cursor), **Axis X/Y/Z** (defaults to the view axis), **Use Duplicates** (keeps the original selection as a separate island unlinked from the spin result), **Auto Merge** (merges first and last duplicates on a full revolution), **Flip Normals**.
4. A spin leaves duplicate vertices along the profile: select the seam vertices and run Merge by Distance, then recalculate normals outside (`Alt N`).

## Screw (Edge menu > Screw)

- Extrudes the selection along a helix in world space. The selection must include exactly one open profile (connected edges that do not form a closed loop, even a single loose edge); it defines the height offset and radial offset per turn. With none or several the operator fails with "You have to select a string of connected vertices too."
- Place the 3D cursor at the centre and make the screen vertical axis the turn axis (side view for the global Z axis).
- Options: **Steps** (per 360 degree turn), **Turns**, **Center X/Y/Z**, **Axis X/Y/Z** (invert to flip clockwise and counterclockwise). The geometry moves along the direction given by the open profile's endpoints.
- To drop a guide profile afterwards, hover its faces, press `L`, then delete.

## Modifier alternative

The **Screw modifier** is non-destructive (Angle, Screw, Iterations, Merge, Calculate Order, Stretch UVs); see `screw-profile`. Use the Edit Mode tools for one-off geometry.

## Gotchas

- Wrong axis usually means the view direction or cursor position is wrong; set Center and Axis numerically in the redo panel.
- A full spin without Auto Merge leaves a duplicated seam; run Merge by Distance.

## Verify

Select All by Trait > Non Manifold on a closed vase selects only the intended open rim; vertex count after merging matches the original profile.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Spin and Screw (Edit Mode) pages: menu paths, options, defaults for Center and Axis, error text, Use Duplicates and Auto Merge meanings. Corrected Use Duplicates (separate islands, not radial copies) and modifier option names (Calculate Order, Stretch UVs). Removed unconfirmed pole-fan note.
Method: documentation only; no commands were run.
