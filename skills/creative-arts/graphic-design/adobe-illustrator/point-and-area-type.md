---
id: creative-arts.graphic-design.adobe-illustrator.point-and-area-type
name: point-and-area-type
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-type, area-type, point-type, text-threading, area-type-options, overset, auto-size, character-styles, paragraph-styles]
level: practitioner
status: draft
description: "Set text in Illustrator with point type and area type: converting between them, area type options (columns, inset, first baseline), threading overflow, and styles for consistency."
sources:
  - https://helpx.adobe.com/illustrator/using/creating-type.html
  - https://helpx.adobe.com/illustrator/using/threading-text.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Point and area type in Illustrator

**Goal:** text frames that behave predictably and never hide overflow.

## Point vs area type
- **Point type:** click with the Type tool (T). One line per Enter. Dragging the bounding
  box **scales** the letters. For headlines, labels, logos.
- **Area type:** drag a box with the Type tool, or click inside any closed path. Text wraps.
  Resizing the box reflows text. For paragraphs and captions.
- **Convert:** double-click the circle widget on the right edge of the bounding box (hollow
  circle = point, filled = area), or Type > Convert To Area/Point Type.

## Area Type Options (Type > Area Type Options)
- Rows and columns with gutter (simple multi-column text without InDesign).
- **Inset Spacing** (padding inside the shape).
- **First Baseline:** Ascent, Cap Height, Leading, x Height or Fixed - pick Cap Height to
  make text tops align to a grid.
- **Auto Size** (Illustrator 2014+): box grows vertically with text so nothing overflows.

## Overflow and threading
- A red **+** in the out-port means overset (hidden) text.
- Click the out-port, then click or drag to create a linked frame; text flows on.
  Type > Threaded Text > Remove Threading / Release Selection to undo.

## Styles
Window > Type > Paragraph Styles / Character Styles. Even in Illustrator, set up Body,
Caption, Heading styles for multi-artboard projects (brochures, infographics) so copy
changes stay consistent. A **+** after the style name = local override; Alt/Option-click
the style to clear.

## Gotchas
- Scaling point type with the bounding box produces odd sizes (13.47 pt). Set size in the
  Character panel instead, or scale with Shift and round afterwards.
- Area type inside a shape with stroke: the stroke disappears when converted - keep a
  separate shape for the outline.
- Pasting from Word brings local formatting; use Paste Without Formatting.

## Verify
- [ ] No red + overflow anywhere (Select > Object > Text Objects and inspect).
- [ ] Type sizes are round numbers; styles used without + overrides on body text.
