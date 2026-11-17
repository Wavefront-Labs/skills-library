---
id: creative-arts.animation.blender.text-paragraph
name: text-paragraph
category: creative-arts
field: animation
product: blender
tags: [blender, text-object, text-paragraph, text-alignment, character-spacing, line-spacing, word-spacing, typography]
level: practitioner
status: docs-checked
description: "Lay out Blender text: horizontal alignment (Left, Center, Right, Justify, Flush), vertical alignment, character/word/line spacing, Offset X/Y, Shear and Size."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/texts/properties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# text-paragraph

Goal: titles and multi-line text that look typeset, not default.

## Properties > Data > Paragraph

- **Alignment > Horizontal**:
  - *Left*, *Center*, *Right*: align to the frames when frames are used; otherwise the object origin is the start, mid-point or end of the text.
  - *Justify*: flushes a line only when it ends at a word wrap (not a newline) and uses whitespace instead of character spacing.
  - *Flush*: always flushes the line, using character spacing.
  - Justify and Flush only work within frames (see text-boxes).
- **Alignment > Vertical** (in the manual's order): *Top*, *Top Baseline*, *Middle*, *Bottom Baseline*, *Bottom*. With frames they refer to the frame edges; without frames they refer to the object origin (Middle centres the text on the origin and grows both ways).
- **Spacing**: *Character Spacing* (factor scaling the space between characters), *Word Spacing* (factor scaling whitespace), *Line Spacing* (factor scaling the vertical space between lines).
- **Offset X, Y**: offset of the text from the object origin, applied to each frame when frames are used.

## Font > Transform

- **Size**: size of the whole text (individual characters cannot be sized separately; characters from different fonts may look different in size).
- **Shear**: inclination of the whole text; it is not the same as the italic style.
- **Small Caps Scale** and underline position/thickness are in the same panel.
- Per-character kerning: in Edit Mode, `Alt Left` / `Alt Right` decreases/increases the spacing at the cursor (Text > Kerning also has Reset Kerning).

## Gotchas

- The reference point of the first line differs for Top Baseline with and without frames; check the origin after changing alignment.
- Justify and Flush without a frame do nothing useful.

## Verify

Origin sits where expected for the chosen alignment; edit the text and the layout stays centred.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Text Properties > Font, Paragraph; Editing Text Objects > Kerning). Confirmed: all alignment options and their frame/origin rules, spacing factors, Offset X/Y, Size, Shear, Small Caps Scale, Alt Left/Right kerning. Removed as unconfirmed: default Character Spacing 1.0, Shear range, typographic numeric tips and the advice about object scale.
Method: documentation only; no commands were run.
