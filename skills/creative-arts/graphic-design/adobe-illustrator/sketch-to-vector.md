---
id: creative-arts.graphic-design.adobe-illustrator.sketch-to-vector
name: sketch-to-vector
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, sketch-to-vector, vectorising, image-trace, pen-tool, template-layer, inking, line-art, illustration-workflow]
level: practitioner
status: draft
description: "Turn a hand sketch into clean Illustrator vector art: scan and prep, template layer, choose trace or redraw, ink with pen and brushes, then close shapes for colour."
sources:
  - https://helpx.adobe.com/illustrator/using/image-trace.html
  - https://helpx.adobe.com/illustrator/using/layers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hand sketch to clean vector

**Goal:** a pencil or ink drawing turned into crisp, scalable, colourable vector artwork that keeps the
character of the hand drawing.

## 1. Capture the sketch
- Scan at 300-600 ppi greyscale (phone capture with even light works for roughs). Crop, and in Photoshop
  use Levels to push the paper to white and lines to near-black; remove smudges.
- Tighten the drawing on paper or in Procreate first: vector time spent fixing anatomy is wasted.

## 2. Set up in Illustrator
- File > Place with **Template** checked: the image goes on a locked, dimmed template layer
  (or set layer options > Template, dim to 30-50%).
- New layers above for line art, colour and shadows.

## 3. Choose the method
- **Image Trace (Line Art / Sketched Art preset)** for textured ink drawings where the wobble is the
  style. Tune Threshold, Noise and Paths, then Expand (see image-trace-settings skill).
- **Redraw with the Pen / Curvature tool** for clean commercial work: fewest points on extremes,
  smooth curves, consistent stroke.
- **Brush inking:** Paintbrush or Blob Brush with a pressure-sensitive tablet, calligraphic brush set
  to Pressure for line weight variation; raise Fidelity toward Smooth.
- Mix: trace for texture, redraw for main contours.

## 4. Prepare for colour
- Close shapes: lines must meet. Use Live Paint (gaps tolerance) or outline strokes and use Shape Builder
  to create fillable regions.
- Put flat colour on a layer below line art; Multiply blend for line art over colour if needed.
- Expand variable-width strokes (Object > Expand Appearance) only at the end.

## Gotchas
- Tracing a weak sketch produces weak vectors faster; fix the drawing first.
- Too many anchor points make wobbly curves; Simplify or redraw.
- Mixing stroked paths and outlined shapes makes later edits painful; decide one approach per layer.

## Verify
- [ ] At 400% zoom, curves are smooth with no kinks or stray points.
- [ ] Every colour area fills cleanly; line weights consistent at final size.
