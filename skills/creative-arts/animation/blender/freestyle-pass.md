---
id: creative-arts.animation.blender.freestyle-pass
name: freestyle-pass
category: creative-arts
field: animation
product: blender
tags: [blender, freestyle-pass, freestyle-as-render-pass, freestyle, compositing, render-passes, npr]
level: practitioner
status: docs-checked
description: "Render Freestyle lines as a separate pass: As Render Pass option, compositing lines over the beauty with Alpha Over, colour grading lines separately and EXR output."
sources:
  - https://docs.blender.org/manual/en/latest/render/freestyle/view_layer/freestyle.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# freestyle-pass

Goal: lines as their own layer so comp can recolour, blur or fade them without re-rendering.

## Enable

1. Render Properties → *Freestyle* on (*Line Thickness Mode*: Absolute pixels or Relative to 480 px image height).
2. View Layer Properties → *Freestyle* panel → **As Render Pass**.
3. Freestyle lines are then not shown on top of the render image; they come out as a render pass for compositing.

## Composite

Combine the Freestyle pass with the rendered image using an *Alpha Over* node (the manual's own recommendation). Put colour, blur or mix nodes on the Freestyle branch only.

## Gotchas

- Without As Render Pass the lines are drawn directly onto the image; there is nothing separate to composite.
- The View Map Cache option is a view layer setting but its cache is shared by all view layers and scenes, so rendering several Freestyle view layers gives no cache gain.

## Verify

Render a frame and confirm the lines appear only after the Alpha Over node and vanish from the final when it is bypassed.

## Checked

2026-10-27 against the Blender 5.2 manual (Render Properties and View Layer Freestyle pages). Confirmed As Render Pass behaviour, the Alpha Over recommendation, Line Thickness Mode and the shared view map cache. Removed unconfirmed claims about socket format and premultiplication, EXR and File Output specifics, and motion blur and depth of field behaviour.
Method: documentation only; no commands were run.
