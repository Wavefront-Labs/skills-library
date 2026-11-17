---
id: creative-arts.animation.motion-graphics.responsive-design-mogrt
name: responsive-design-mogrt
category: creative-arts
field: animation
product: motion-graphics
tags: [responsive-design, motion-templates, mogrt, responsive-design-time, protected-region, sourcerecttime, auto-resize-box, after-effects, expressions]
level: advanced
status: draft
description: "Make templates adapt to duration and text length: Responsive Design Time protected regions, and sourceRectAtTime expressions for auto-sizing boxes and layout."
sources:
  - https://helpx.adobe.com/after-effects/using/responsive-design.html
  - https://ae-expressions.docsforadobe.dev/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Responsive design for templates

**Goal:** one template that works for a 3-second or 10-second lower third and for short or long names,
without the editor touching keyframes.

## Responsive Design - Time

Protected regions keep intro and outro animation at fixed speed while the middle stretches.
1. In the master comp, add a composition marker over the intro (Composition - Responsive Design -
   Time - Create Intro) and outro (Create Outro), or set markers and tick **Protected Region** in the
   marker dialog.
2. When the comp/mogrt is stretched in Premiere or nested in AE, protected regions keep their timing;
   the unprotected middle stretches.

## Responsive layout with sourceRectAtTime

A background box that fits its text, with padding:
```javascript
// on the box shape's Rectangle Size
var t = thisComp.layer("Name");
var r = t.sourceRectAtTime(time, false);
var pad = [40, 20];
[r.width + pad[0]*2, r.height + pad[1]*2];
```
```javascript
// on the box shape's Rectangle Position (align with text's box, in layer space)
var t = thisComp.layer("Name");
var r = t.sourceRectAtTime(time, false);
[r.left + r.width/2, r.top + r.height/2];
```
Parent the box to the text layer (or match its position) so both move together. For left-anchored
growth, set the text paragraph alignment left and the anchor point to the left edge:
`var r=sourceRectAtTime(); [r.left, r.top + r.height/2]` on the text layer's Anchor Point.

## Stacking two text lines

Position the second line below the first using the first line's measured height plus a gap, so long
names that wrap push the title down.

## Gotchas

- `sourceRectAtTime` measures the layer's content box at a given time; text animators that scale
  characters change it during the animation. Measure at a fixed time (`sourceRectAtTime(inPoint+1)`)
  if needed.
- Expression-heavy templates slow Premiere playback; keep expressions simple and avoid per-frame
  loops.
- Empty text gives width 0; guard with `Math.max(r.width, minWidth)`.

## Verify

Test strings: one character, a very long name, a two-line wrap, and durations of 3 s and 12 s: box fits
with consistent padding, intro and outro timing unchanged.
