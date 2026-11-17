---
id: creative-arts.animation.blender.mask-node-feather
name: mask-node-feather
category: creative-arts
field: animation
product: blender
tags: [blender, mask-node, mask-node-feather, mask-feather, masking, compositor]
level: practitioner
status: docs-checked
description: "Use roto masks in the compositor with the Mask node: Masks data-block, Feather, Size Source, Motion Blur Samples and Shutter, and combining masks with keys and grades."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/input/mask.html
  - https://docs.blender.org/manual/en/latest/movie_clip/masking/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# mask-node-feather

Goal: bring a roto mask into the compositor with the right resolution, softness and motion blur.

## Mask node (Input category)

Selects a Mask data-block (see the masking manual section) and outputs it as a black-and-white **Mask**. It can be used with other nodes, for example to invert, multiply or mix, or as a factor input.
- **Masks**: the selectable mask data-block.
- **Feather**: use or ignore feather points defined on the splines.
- **Size Source**: **Scene Size** (the render resolution, scaling with different resolutions), **Fixed** (a size in pixels) or **Fixed/Scene** (a pixel size that scales with the render resolution percentage).
- **Motion Blur** panel: for animated masks, builds a motion-blurred mask from surrounding frames, with **Samples** (higher is smoother but slower) and **Shutter** (duration in seconds, the simulated exposure time per frame).

## Combining

- Mask as Factor of a Mix node to grade only an area (the manual's example isolates an object to protect it from correction).
- Mask multiplied with a key's matte to restrict the key, or combined with a Maximum to add areas.
- Garbage and core mattes for the Keying node (see keying-node-settings).

## Tips

- Use Scene Size so masks match at any render percentage.
- Feather drawn per point on the mask splines varies along the edge, which a blur of the whole mask cannot do.

## Gotchas

- A mask drawn against a clip of a different resolution than the render can appear scaled; check the aspect.
- Motion blur samples neighbouring frames, so a mask held without animation has nothing to blur.

## Verify

View the mask through a Viewer over the plate (Mix at 50 percent). Edges should follow the subject, with soft feathers where intended.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Mask node Masks, Feather, Size Source (Scene Size, Fixed, Fixed/Scene), Motion Blur Samples and Shutter, and the mixing example. Removed the Mask-node render-button, resolution-normalisation and keyframe claims.
Method: documentation only; no commands were run.
