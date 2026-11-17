---
id: creative-arts.animation.blender.hair-sculpt-mode
name: hair-sculpt-mode
category: creative-arts
field: animation
product: blender
tags: [blender, hair, hair-curves, hair-sculpt-mode, comb-brush, puff-brush, snake-hook]
level: practitioner
status: docs-checked
description: "Groom Blender Curves hair in Sculpt Mode: Comb, Snake Hook, Grow/Shrink, Pinch, Puff, Smooth, Slide, Selection Paint, selection modes, mirror and surface snapping."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/introduction.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/brushes/comb_curves.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/brushes/snake_hook_curves.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/brushes/grow_shrink_curves.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/brushes/pinch_curves.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/brushes/puff_curves.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/brushes/slide_curves.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/brushes/selection_paint.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/brushes/smooth_curves.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# hair-sculpt-mode

## Setup
Select the head mesh, Add > Curve > **Empty Hair** (adds an empty Curves object with the selected mesh as surface). Check Curves Data > Surface (object and UV Map), then enter **Sculpt Mode** on the Curves object. Curves Sculpt tools only use the original mesh of the surface object, not its modifiers.

## Brushes
- **Comb**: moves control points while preserving segment length; Curve Falloff applies from tip to root.
- **Snake Hook**: extends curves along the stroke; only tips can be extended, and existing points are resampled.
- **Grow / Shrink**: change length keeping the point count (Ctrl toggles Direction); Scale Uniform, Minimum Length.
- **Pinch**: converges adjacent curves to the cursor centre; Ctrl inverts.
- **Puff**: makes curves stand up, aligned to the surface normal, without moving points closer to the root.
- **Smooth**: makes nearby curve segments more parallel.
- **Slide**: slides curves along the surface and rotates them by the normal change (needs a surface).
- **Add**, **Delete**, **Density** (see hair-density-brush).
- **Selection Paint**: paints a selection used as a mask by other tools (Shift extends, Ctrl subtracts); visibility via Selection Opacity in overlays.

## Modes and menus
- Select mode (keys 1, 2): Control Points or Curve. Select menu: All, None, Invert, Random, Endpoints, Grow.
- Header: **Mirror** (axis) and **Use Sculpt Collision** (curves cannot pass through the surface object).
- Curves menu: **Snap to Deformed Surface** (needs unchanged surface topology), **Snap to Nearest Surface** (run after topology changes), **Convert to Particle System**.
- Overlay **Cage Opacity** shows the original curves when procedural deformations or child curves are used.

## Gotchas
- For guide-based workflows groom few guides, then add density with Interpolate Hair Curves (hair-interpolate).
- Curves Sculpt mode works on all kinds of curves, not only hair.

## Verify
Toggle modifiers off: the guides look groomed; with node groups on, final density follows the groom.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed each brush description, selection modes and shortcuts, Curves menu operators, Mirror, Use Sculpt Collision and Cage Opacity on the Curves Sculpting pages; Add > Curve > Empty Hair confirmed in the 5.2 Add menu UI script and the object.curves_empty_hair_add API entry. Removed the Deform Curves on Surface auto-modifier claim, the Front-faces-only option, radius and strength shortcut claims and the undo-memory advice.
Method: documentation only; no commands were run.
