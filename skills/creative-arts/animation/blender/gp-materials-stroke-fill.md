---
id: creative-arts.animation.blender.gp-materials-stroke-fill
name: gp-materials-stroke-fill
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-materials-stroke-fill, gp-fill-material, gp-stroke-material, gp-holdout]
level: practitioner
status: docs-checked
description: "Set up Grease Pencil materials: stroke line/dots/squares, fill solid/gradient/texture, holdout, self overlap, alignment, slot locking and assigning to strokes."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/materials/properties.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/edit/stroke_menu.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/edit/selecting.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/properties/layers.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gp-materials-stroke-fill

Goal: a material palette that gives clean line, flat fill and special effects.

## Structure
Grease Pencil materials are not shader node trees. Each material has a **Stroke** and a **Fill** component, enabled independently in the Surface panel. Each stroke references one material slot; the active slot is used for new strokes and existing strokes keep theirs until reassigned. Keep a palette such as a line-only material, fill-only skin and shadow materials, and a holdout.

## Stroke component
- **Line Type**: Line, Dots, Squares.
- **Style**: Solid (Base Color) or Texture (Image, Blend, UV Factor).
- **Placement** (Dots, Squares): Count, Radius (Spacing) or Density.
- **Alignment** (Dots, Squares): Path, Object or Fixed; **Rotation** limited to -90 to 90 degrees.
- **Self Overlap**: how overlapping parts of one stroke blend, mainly for semi-transparent materials.
- **Holdout**: the stroke removes colour from strokes and fills beneath.
- Randomize (Dots, Squares): Size, Strength, Rotation, Hue, Saturation, Value, Noise Scale.

## Fill component
- **Style**: Solid, Gradient (Linear or Radial, Secondary Color, Flip Colors, Blend) or Texture (Image, Clip Image).
- Location X/Y, Rotation, Scale X/Y for gradient and texture mapping.
- **Holdout**: the fill removes colour from strokes underneath.

## Slots, locking and assigning
- Slot icons: show in onion-skin ghosts, hide, lock (locked materials cannot be edited in Edit mode).
- Specials: Show All, Hide Others, Lock All, Unlock All, **Lock Unselected**, Lock Unused, Copy Material to Selected, Copy All Materials to Selected, Remove Unused Slots; Isolate Material buttons lock or hide all but the active one.
- Edit mode: select strokes, Stroke > **Assign Material**; Stroke > Set as Active Material copies a stroke's material to the active slot. Layers have **Ignore Material Locking** if needed.
- Settings > **Pass Index** targets materials from modifiers and compositing.

## Vertex colour on top
Vertex Paint, the Tint brush and the Color Attribute paint mode mix a per-point colour with the material Base Color (see gp-vertex-paint). Edit the material for global recolouring.

## Verify
Edit mode > Select > Select Similar > Material selects exactly the strokes that should share the look.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed Line Type, Style, Placement, Alignment, Self Overlap, Holdout, gradient and texture fill options, slot specials and Lock Unselected on the material properties page; Assign Material and Select Similar on the Stroke menu and Selecting pages. Removed the unconfirmed material-order holdout claim, the stroke-only-on-fill-brush claim and the header Material dropdown; the texture Mix factor is named Blend in the manual.
Method: documentation only; no commands were run.
