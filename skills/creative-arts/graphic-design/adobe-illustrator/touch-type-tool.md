---
id: creative-arts.graphic-design.adobe-illustrator.touch-type-tool
name: touch-type-tool
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-type, touch-type-tool, per-glyph-transform, character-rotation, baseline-shift, live-text-editing, glyph-alternates, kerning]
level: intro
status: draft
description: "Adjust single characters in Illustrator while text stays live: Touch Type scaling, rotating and shifting glyphs, baseline shift, and on-canvas glyph alternates."
sources:
  - https://helpx.adobe.com/illustrator/using/touch-type-tool.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Touch Type tool and per-glyph edits

**Goal:** playful or optically corrected typography (bouncing letters, a raised initial, a nudged
accent) without outlining the text.

## Touch Type tool (Shift+T, under the Type tool)
- Click a character: a box appears around it.
  - Top-left dot: **scale vertically**; top-right dot: **scale proportionally**; bottom-right: scale horizontally.
  - Top centre dot: **rotate**.
  - Drag the middle: **move** (becomes baseline shift and kerning values).
- Text stays live: you can still edit words, change the font, and spell-check.
- Edits are stored as character attributes, visible in the Character panel.

## Same edits via the Character panel
- **Baseline shift** (Alt/Option+Shift+up/down arrows in steps).
- **Character rotation**.
- Horizontal/vertical scale (avoid for real typography - distorts stroke weights; prefer a different width of the family).
- Kerning: Alt/Option+left/right arrows; tracking on selections.

## Glyph alternates on canvas
Select a single character with the Type tool; a small menu of **alternates** appears below it (if the font
has them). Window > Type > Glyphs shows all alternates for the selection (see OpenType features skill).

## Typical uses
- Optical adjustment in headlines: nudge a T or quote mark, raise a colon in time ranges (10:30).
- Display layouts with bounce or scale variation.
- Logo explorations before committing to outlines.

## Gotchas
- Touch Type edits survive font changes but may look wrong with a different typeface - review after swaps.
- Pasting text into other apps loses the per-character transforms.
- Large scale distortions of glyphs look amateur; switch to a heavier weight instead of scaling.

## Verify
- [ ] Text still editable (Type tool can change letters).
- [ ] No horizontally/vertically scaled glyphs unless intentional for effect.
