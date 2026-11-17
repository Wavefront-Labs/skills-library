---
id: creative-arts.animation.motion-graphics.ae-track-mattes
name: ae-track-mattes
category: creative-arts
field: animation
product: motion-graphics
tags: [track-matte, track-mattes, alpha-matte, luma-matte, after-effects, masking, compositing]
level: practitioner
status: draft
description: "Use track mattes in After Effects: alpha versus luma mattes, inverted options, the matte-layer picker in recent versions, precomposing, and common edge mistakes."
sources:
  - https://helpx.adobe.com/after-effects/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Track mattes (After Effects)

A **track matte** uses one layer (the matte) to define the transparency of another layer (the fill).

## Types
| Matte type | The fill layer shows where the matte is... |
|---|---|
| Alpha Matte | opaque (uses the matte's alpha channel) |
| Alpha Inverted Matte | transparent |
| Luma Matte | bright (uses luminance) |
| Luma Inverted Matte | dark |

## Setting it
- In the Timeline use the **TrkMat** column: in current versions each layer has a track-matte dropdown, and a layer picker (pick whip) where you choose the matte layer. Since recent releases the matte layer can sit anywhere in the stack and one matte can drive several layers; the matte layer's own visibility is turned off automatically. In older versions the matte had to sit directly above the fill layer, and moving or reordering layers broke the pairing. If the TrkMat column is hidden, toggle it from the Timeline panel menu or press F4 to show the Switches/Modes panes.
- Use **Alpha** mattes with shapes, masks or text; **Luma** mattes with greyscale images, gradients, video.

## Practice
1. Build the matte as a **shape layer** or solid with a mask; animate it independently.
2. To matte a group, **precompose** the group first (`ae-precompose-and-nesting.md`).
3. Use **Luma Inverted** or the **Invert** option instead of re-drawing the matte.
4. Combine mattes by stacking: matte a precomp that is itself matted.
5. Feather the matte's edge (mask feather, blur on the matte) for soft reveals (`ae-mask-modes-feather.md`).

## Related blend modes
**Stencil Alpha**, **Stencil Luma**, **Silhouette Alpha** and **Silhouette Luma** act on all layers beneath, instead of only one. Use them for cut-outs through everything below.

## Edge problems
- Dark or light fringes: when mattes come from video, check for premultiplication (`premultiplied-alpha.md`) or use a choke (`matte-choke-spill-suppression.md`).
- Layers that are time-remapped or stretched need the matte to match; precompose both together.

## Verify
- [ ] Matte layer hidden and still driving the fill.
- [ ] Edges are clean at 100% and 200% zoom.
