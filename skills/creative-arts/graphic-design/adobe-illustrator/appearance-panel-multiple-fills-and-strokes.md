---
id: creative-arts.graphic-design.adobe-illustrator.appearance-panel-multiple-fills-and-strokes
name: appearance-panel-multiple-fills-and-strokes
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, appearance-panel, illustrator-effects, multiple-fills-strokes, offset-path, live-effects, stacked-strokes, outlined-text, non-destructive]
level: practitioner
status: draft
description: "Stack multiple fills, strokes and live effects on one Illustrator object or live text with the Appearance panel, keeping complex looks editable."
sources:
  - https://helpx.adobe.com/illustrator/using/appearance-attributes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Appearance panel: multiple fills and strokes

**Goal:** layered effects (double outlines, offset shadows, sticker borders) on a single
editable object - including live text that can still be retyped.

## Panel basics (Window > Appearance, Shift+F6)
- Lists Stroke, Fill, Opacity and effects for the selected object, **top to bottom = front to back**.
- **Add New Stroke / Add New Fill** buttons at the bottom; drag rows to reorder.
- Each fill or stroke can have its own effects and opacity (twirl it open).
- Object-level effects sit at the bottom and affect the whole stack.

## Recipe: sticker-style outlined headline on live text
1. Type the word. In Appearance, select the "Characters" row and set fill and stroke to None
   (otherwise character colours sit on top of everything).
2. Add New Fill: brand colour (this is the letter colour).
3. Add New Stroke **below** the fill: white, 12 pt, round join. Moves the outline behind the
   letters so it never thins the letterforms.
4. Add another stroke below that: dark, 18 pt - double outline.
5. Add a fill at the bottom with **Effect > Distort & Transform > Transform** move 4 pt x/y -
   offset drop shadow that follows the text.
Text stays editable; change the word and everything updates.

## Recipe: inline/offset border on a shape
Add a second stroke and apply **Effect > Path > Offset Path** (-3 pt) to that stroke only.

## Tips
- **New Art Has Basic Appearance** (panel menu) off = new objects inherit the current look.
- Save the look as a **graphic style** (see that skill) to reuse.
- Select > Same > Appearance selects all objects with the same stack.
- Clear Appearance resets to no fill/stroke; Reduce to Basic Appearance keeps one fill + stroke.

## Output
Live effects stay live in .ai and PDF (rasterised effects at Document Raster Effects
Resolution - set 300 ppi for print). For cutters, embroidery or handing to other apps,
**Object > Expand Appearance** on a copy.

## Gotchas
- Strokes on top of fills eat into thin letters - keep outline strokes below the fill.
- Effects on the Characters row vs on the type object behave differently; put effects on
  the object-level fills you added.

## Verify
- [ ] Retyping the text keeps the full look.
- [ ] Document Raster Effects Resolution is 300 ppi for print jobs.
