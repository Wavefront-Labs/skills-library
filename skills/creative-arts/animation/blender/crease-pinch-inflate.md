---
id: creative-arts.animation.blender.crease-pinch-inflate
name: crease-pinch-inflate
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, crease-pinch-inflate, crease-brush, pinch-brush, inflate-brush, blob-brush, wrinkles]
level: practitioner
status: docs-checked
description: "Cut wrinkles, sharpen forms and swell volumes with Blender's Crease, Pinch/Magnify, Inflate/Deflate and Blob sculpt brushes: key settings, Ctrl inversion and when each fits."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/crease.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/pinch.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/inflate.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/blob.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/brushes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# crease-pinch-inflate

Goal: the secondary-form brushes (creases, sharp ridges, swelling), used after primary forms are blocked with Clay Strips or Grab.

## Brush assets and types

These are brush assets from the Essentials library, each based on a brush type: Crease Polish (Shift-C) and Crease Sharp use the Crease type, Pinch/Magnify (P) uses Pinch, Inflate/Deflate (I) uses Inflate, Blob uses Blob.

## Crease

- Creates sharp indents or ridges by pushing or pulling the mesh while pinching the vertices together; it can also sharpen and polish existing creases. Crease Polish is a Draw brush with a pinching effect; Crease Sharp is much sharper and stronger.
- **Pinch** setting: 0 makes it behave like Draw; 1 with strength 0 behaves like the Pinch brush.
- Enable pressure sensitivity on Strength to regulate the add/subtract effect while pinching.
- Use Stabilize Stroke (Stroke panel, Shift-S) for clean long lines.

## Pinch / Magnify

Pulls geometry toward the brush centre. Inverted with Ctrl it Magnifies, pushing geometry away from the centre. Useful for polishing angles and creases.

## Inflate / Deflate

Like Draw, but vertices move along their own normals, which suits strongly curved meshes. **Direction** is Inflate or Deflate (different from the normal Add/Subtract). The Inflate mesh filter does the same to all unmasked areas at once.

## Blob

Like Draw, but vertices are pushed outward like an inverted pinch, giving a more consistent spherical curvature and thickening strokes.

## Gotchas

- With Dyntopo on, most brushes subdivide the mesh during the stroke, so fine creases get the detail they need.
- Use a mask or auto-masking to protect neighbouring forms when inflating thin parts.

## Verify

View with a matcap: folds should read clean and crisp, and a few Shift-Smooth passes should soften the form without destroying it.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/brushes (crease, pinch, inflate, blob, brushes list): brush asset names and shortcuts (Shift-C, P, I), Crease Pinch semantics (0 is Draw, 1 with strength 0 is Pinch), Ctrl Magnify, Inflate/Deflate direction and normals, Blob behaviour, Stabilize Stroke Shift-S. Removed unconfirmed value recommendations (0.5, 0.9), the Pinch slider range and tearing or Multires behaviour claims.
Method: documentation only; no commands were run.
