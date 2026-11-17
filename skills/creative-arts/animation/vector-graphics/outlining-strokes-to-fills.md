---
id: creative-arts.animation.vector-graphics.outlining-strokes-to-fills
name: outlining-strokes-to-fills
category: creative-arts
field: animation
product: vector-graphics
tags: [outline-stroke, stroke-to-path, convert-lines-to-fills, vector-drawing, svg-export, line-art]
level: practitioner
status: draft
description: "Convert strokes to filled shapes before scaling, deforming or exporting: menu commands per app, when to keep live strokes, and avoiding stroke-width surprises."
sources:
  - https://helpx.adobe.com/animate/user-guide.html
  - https://inkscape.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Outlining strokes to fills

A stroke is a rendering property, not geometry: its width, caps and joins are applied when drawing. Converting to a fill turns the line into a closed shape you can boolean, deform or colour with gradients.

## Commands
- **Illustrator**: Object > Path > Outline Stroke.
- **Inkscape**: Path > Stroke to Path.
- **Animate**: Modify > Shape > Convert Lines to Fills.

## When to outline
- Before scaling art in a pipeline that ignores stroke scaling (for example, if "scale strokes" is off, a scaled rig keeps the original stroke thickness).
- Before boolean operations that need real geometry (`boolean-path-operations.md`).
- Before deforming with meshes or warps that treat strokes poorly.
- Before exporting to targets that do not support variable stroke or dashes (`svg-pipeline-for-motion-graphics.md`).
- To give a line a gradient that follows its shape.

## When to keep live strokes
- While the design is still changing: strokes remain editable by width, and outline at the end.
- In rigs where line weight should stay constant while the part scales, or when animating line thickness with motion graphics tools.

## Gotchas
- Outlining is destructive for editing: keep a copy of the original.
- Dashes and arrowheads expand into many shapes.
- Round caps and joins become arcs; miter joins can spike at sharp angles (limit set by the miter limit).
- Outlined results often have many nodes. Check node counts (`vector-asset-optimisation-for-animation.md`).

## Verify
- [ ] Source file keeps the live-stroke version.
- [ ] Outlined art scaled to 200% keeps the intended line weight.
- [ ] Node count is acceptable.
