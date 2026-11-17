---
id: creative-arts.animation.blender.proportional-falloff
name: proportional-falloff
category: creative-arts
field: animation
product: blender
tags: [blender, proportional-editing, proportional-falloff, falloff-types, connected-only, projected-from-view, soft-selection]
level: practitioner
status: docs-checked
description: "Soft-select in Blender with proportional editing: O to toggle, wheel radius, the eight falloff types, Connected Only, Projected from View, and Object Mode use."
sources:
  - https://docs.blender.org/manual/en/latest/editors/3dview/controls/proportional_editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# proportional-falloff

Goal: smooth organic tweaks of many vertices (or objects) with the right falloff shape and limits.

## Controls

- `O` toggles proportional editing (Object Mode and Edit Mode).
- During a transform: the mouse wheel or `PageUp/PageDown` changes the radius (also available in the Proportional Editing popover); the influence circle shows it.
- `Shift O` opens the falloff pie menu (or click the Falloff icon in the header).

## Falloff types

The manual shows all eight profiles (Constant, Random, Linear, Sharp, Root, Sphere, Smooth, Inverse Square) in pictures without describing them in text. The use notes below are practice suggestions.

| Type | Suggested use |
|---|---|
| Smooth | general shaping |
| Sphere | rounded, broad influence |
| Root | wide spread |
| Inverse Square | peaked centre |
| Sharp | spikes, horns |
| Linear | ramps |
| Constant | block moves with a hard edge (no falloff) |
| Random | roughening |

## Options

- **Connected Only** (`Alt O`, Edit Mode only): the falloff spreads via connected geometry rather than by radius alone, so you can edit one finger without affecting the others; the icon gets a blue centre when active.
- **Projected from View**: depth along the view is ignored when applying the radius.
- In Object Mode the tool works on whole objects, so nearby objects are affected too.

## Gotchas

- Proportional editing left on is the #1 "why did the whole mesh move": check the header icon before precise work.
- Adjust the radius to the size of the model; a very small model needs a small radius (practice).

## Verify

Watch the influence circle while transforming and check the Proportional Editing popover for the falloff and size in use.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against editors/3dview/controls/proportional_editing.rst: O toggle, Object and Edit Mode, radius via wheel or PageUp/PageDown, Shift O falloff pie, the eight falloff profiles, Connected Only (Alt O, Edit Mode only), Projected from View. Removed unconfirmed claims: Graph Editor/UV/Dope Sheet support, remembered size, default radius 1.0, mirror behaviour, profile descriptions (now marked practice).

Method: documentation only; no commands were run.
