---
id: creative-arts.animation.color.power-windows
name: power-windows
category: creative-arts
field: animation
product: color
tags: [power-windows, secondary-grading, windows, vignette, shapes, davinci-resolve, relighting, grading, softness]
level: practitioner
status: draft
description: "Use Resolve power windows (circle, linear, polygon, curve, gradient) to relight, vignette and direct the eye in animated shots, with softness and inside/outside grades."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://www.blackmagicdesign.com/products/davinciresolve/training
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Power windows

**Goal:** shape light in the grade: brighten a face, darken edges, add a sky gradient, separate a
character from the background. Windows are vector shapes that limit a correction.

## Shapes

| Window | Typical use |
|---|---|
| Circular | face lift, vignette (inverted) |
| Linear | split screens, horizon line |
| Polygon | architecture, hard-edged areas |
| Curve (Bezier) | character silhouettes, irregular areas |
| Gradient | skies, floors, graduated filter effect |

## Procedure

1. New serial node, Window palette, enable a shape; drag in the viewer. Show the outline
   (on-screen controls) only while editing.
2. Softness: Soft 1 (overall), Soft 2-4 on curve windows per side; inside/outside softness
   with Bezier windows. Soft edges matter more than accurate edges for relight.
3. Grade inside. For the outside, either invert the window, or right-click node and **Add Outside
   Node**, which grades the complement with a linked matte.
4. Combine shapes in one node (several windows union) or use mask mode (one subtracts another).
5. If anything moves, track it (`creative-arts.animation.color.window-tracking`).

## Animation-specific uses

- Restore focus lost in comp: a subtle (+0.05 to +0.1 gain) soft oval on the speaking character.
- Unify a sequence where backgrounds were painted at different values: gradient windows on sky.
- Vignettes are a style decision; keep them consistent per sequence (save as a gallery still or a
  shared node).

## Gotchas

- Hard-edged windows read as a spotlight or a mistake. Viewers notice edges moving more than the
  correction itself.
- Strong window grades on flat colour show as a visible "blob": keep moves small and soft, or
  build the light in comp/render instead.
- Window positions are relative to the image; a reframe/resize after the grade (output sizing vs
  input sizing) can shift them. Know which sizing stage your show uses.

## Verify

Toggle the node on/off (Ctrl+D) during playback: the change is felt, not seen; no edge is visible
on a moving frame.
