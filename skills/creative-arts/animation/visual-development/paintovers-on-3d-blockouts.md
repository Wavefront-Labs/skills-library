---
id: creative-arts.animation.visual-development.paintovers-on-3d-blockouts
name: paintovers-on-3d-blockouts
category: creative-arts
field: animation
product: visual-development
tags: [visual-development, color-key, paintover, 3d-blockout, lighting-key, art-direction]
level: practitioner
status: draft
description: "Paint over 3D blockouts or renders: use the render for perspective and form, then repaint light, colour and design to set the target and give clear notes."
sources:
  - https://www.khanacademy.org/computing/pixar
  - https://books.google.com/books?vid=ISBN9780740785504
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Paintovers on 3D blockouts or renders

Goal: fast, accurate visual targets by painting on top of 3D renders - both for creating
keys and for giving notes on work in progress.

## Inputs to export
- Beauty or clay render at the final camera and resolution.
- Helper passes: Z-depth (for fog), normal or AO (for form), object/material ID masks
  (for fast selections), shadow pass.

## Method
1. Load passes as layers; keep the original render locked underneath.
2. Use ID masks to select and recolour areas quickly.
3. Repaint light: adjust the key direction, add or remove shadows, push values toward the
   value thumbnail.
4. Add atmosphere with the depth pass; paint edge control (lost and found edges).
5. Redesign as needed: shapes, props, set dressing.
6. For notes on WIP: put the paintover beside the original, annotate changes with arrows and
   short text, and give values/colours as swatches.

## Failure modes
- Paintover that ignores the camera/geometry, so it cannot be achieved in 3D.
- Paintover too polished: the team reads it as final art and loses time matching noise.
- Notes without the before image.

## Verify
- [ ] Same camera and resolution as the shot.
- [ ] Changes annotated; swatches provided.
- [ ] Achievability checked with lighting/look-dev.

Related: `creative-arts.animation.visual-development.maquettes-and-3d-blockouts-for-reference`,
`creative-arts.animation.art-direction.look-development`.
