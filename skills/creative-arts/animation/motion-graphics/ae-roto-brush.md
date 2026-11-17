---
id: creative-arts.animation.motion-graphics.ae-roto-brush
name: ae-roto-brush
category: creative-arts
field: animation
product: motion-graphics
tags: [roto-brush, masks, rotoscoping, after-effects, refine-edge, freeze, span, propagation, segmentation, roto-brush-3]
level: practitioner
status: draft
description: "Isolate moving subjects with After Effects Roto Brush: base frames, propagation spans, Refine Edge for hair, freezing results, and when to hand-roto instead."
sources:
  - https://helpx.adobe.com/after-effects/using/roto-brush-refine-matte.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Roto Brush

**Goal:** a moving matte for a subject in footage or flattened animation (to put graphics behind a
character, grade it separately, or extract it) faster than drawing masks frame by frame.

## Procedure

1. Double-click the layer to open the Layer panel. Select Roto Brush (Alt+W).
2. On a clear frame (the **base frame**), paint strokes inside the subject (green). Alt-paint to
   subtract background (red). Quality: Best (newer, ML-based model) when available.
3. Roto Brush propagates forward and backward from the base frame over a span (shown in the layer
   timeline). Step through; correct with more strokes where it slips. Each corrected frame becomes
   part of propagation.
4. Add another base frame where the subject changes a lot (turns, occlusions).
5. **Refine Edge** tool (or Refine Edge Matte checkbox): paint along hair/fur/motion-blurred edges;
   adjust Smooth, Feather, Contrast, Shift Edge, Reduce Chatter in the effect controls.
6. **Freeze** the result when done (button at the bottom of the layer panel) to cache the
   segmentation; it stops recalculation and speeds playback.

## When not to use it

- Flat-colour animation with clean outlines: a colour key or the original render's alpha/ID pass is
  cleaner. Roto Brush is for footage and flattened archival animation.
- Long shots with heavy occlusion: plan hand roto with simple shapes or outsource roto.

## Gotchas

- Chatter (edge boil) shows in final composites; use Reduce Chatter and slight feather, or Refine Edge
  with motion blur option.
- Strokes on frames outside the span do not affect it; extend spans by dragging their ends.
- Changing the layer's in/out or replacing footage invalidates the freeze.

## Verify

Composite the matted subject over a bright contrasting solid and play at speed: edges stay on the
subject with no lagging limbs, chatter acceptable at delivery size.
