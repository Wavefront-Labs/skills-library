---
id: creative-arts.graphic-design.adobe-illustrator.align-and-distribute
name: align-and-distribute
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, align-to-key-object, distribute-spacing, align-panel, key-object]
level: intro
status: draft
description: "Align and distribute in Illustrator: align to selection, artboard or key object, distribute exact spacing, and preview vs geometric bounds."
sources:
  - https://helpx.adobe.com/illustrator/using/move-align-distribute-objects.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Align and distribute

## Align To (Align panel, Shift+F7)
- **Align to Selection** - aligns relative to the bounding box of all selected objects.
- **Align to Artboard** - centre logos on the page.
- **Align to Key Object** - select several, then click once more on one object (thicker
  outline). Everything aligns to it and it does not move. Fastest way to align to a fixed element.

## Distribute
- Distribute Objects (left/centre/right edges) distributes by edge positions, which looks uneven with different sizes.
- **Distribute Spacing**: equal gaps. With a key object you can type an exact gap (e.g. 12 pt) -
  all objects get exactly that spacing from the key object.

## Bounds
- Preferences > General > **Use Preview Bounds** on: alignment includes stroke width and effects.
  Off: aligns geometric paths - two shapes with different stroke weights then look misaligned.
- Type: Align Glyph Bounds (Point/Area Text) in Align panel options aligns to actual letter shapes instead of the text frame - for optically centred type in buttons.

## Gotchas
- Groups align as one unit; ungroup or Isolation mode to align contents.
- Clipping masks align by the mask path, not hidden content - correct behaviour, but surprising.

## Verify
- [ ] Spacing measured with smart guides equals the target value.
