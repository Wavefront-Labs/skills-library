---
id: creative-arts.visual-art.procreate.quickshape-and-streamline
name: quickshape-and-streamline
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, quickshape, streamline, procreate-shapes, line-stabilisation, editshape, procreate-quickshape]
level: practitioner
status: draft
description: "Draw clean lines, circles and polygons in Procreate with QuickShape hold-to-snap and Edit Shape, and steady wobbly strokes with StreamLine."
sources: ["https://procreate.com/handbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# QuickShape and StreamLine in Procreate

**Goal:** get geometric precision (QuickShape) and smooth, confident curves (StreamLine) without leaving freehand drawing. Menu names follow the Procreate Handbook; confirm in your version, as interface labels move between releases.

## QuickShape
1. Draw a line, circle, ellipse, triangle, rectangle or other closed polygon in one stroke and **hold at the end** without lifting the Pencil or finger.
2. The stroke snaps to the nearest clean shape and an **Edit Shape** button appears at the top of the canvas. Tap it to convert corners, change type (line, ellipse, polygon) or drag nodes.
3. While still holding, touch the canvas with a second finger to constrain: ellipses become perfect circles, lines snap to common angles, rectangles become squares. (Handbook describes this as the constrain gesture; test it on your device.)
4. Lift to commit. If the shape is not wanted, undo with a two-finger tap.
5. The shape is painted with the current brush onto the current layer; it is raster, not vector, so settle on size before committing.

## StreamLine
- Smooths the path of a stroke by lagging the brush behind the pointer, so small hand tremors are averaged out.
- Set **per brush** in Brush Studio under the Stabilization (Stroke path) area, and also reachable as a quick slider by tapping the brush in the Brush Library and choosing its settings. Higher values give smoother, slower-following strokes.
- Useful for inking and long sweeping lines; keep it low for expressive sketching because high values make the stroke trail the pen.
- Related controls in the same panel: Stabilization and Motion Filtering. They behave differently from StreamLine (they average the input rather than add lag), so tune one at a time.

## Gotchas
- QuickShape triggers on an accidental pause. If shapes snap when you don't want them, avoid resting at the end of strokes or turn the QuickShape hold delay down in the gesture preferences.
- StreamLine is per brush: a smooth ink brush does not make your sketching pencil smooth.
- Snapped shapes cannot be re-drawn vector-style after commit; use Edit Shape before lifting.

## Verify
- [ ] A held circle becomes a circle and Edit Shape appears.
- [ ] Constraining with a second finger gives an exact circle or square.
- [ ] The same slow diagonal stroke looks visibly smoother at higher StreamLine than at zero.
