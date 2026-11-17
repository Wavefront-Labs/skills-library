---
id: creative-arts.graphic-design.adobe-photoshop.point-and-paragraph-type
name: point-and-paragraph-type
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-type, point-type-vs-paragraph-type, paragraph-type, point-type, character-panel, paragraph-panel, anti-aliasing, type-layers, match-font]
level: practitioner
status: draft
description: "Set type properly in Photoshop: when to use point vs paragraph type, Character and Paragraph panel settings, anti-aliasing, keeping type live and vector, and font matching."
sources:
  - https://helpx.adobe.com/photoshop/using/creating-type.html
  - https://helpx.adobe.com/photoshop/using/formatting-characters.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Point and paragraph type in Photoshop

**Goal:** live, crisp, editable type that behaves predictably when copy changes.

## Point vs paragraph
- **Point type:** click once with the Type tool (T). Each line grows until you press Enter.
  Use for headlines, labels, single lines. Dragging the bounding box **scales** the type.
- **Paragraph type:** drag a box with the Type tool. Text wraps inside the box. Use for
  body copy and anything that may get longer. Dragging the box **reflows** text.
- Convert between them: Type > Convert to Paragraph Text / Point Text.
- Overflow on paragraph type shows a + in the bottom handle; text beyond it is hidden but
  still there (and will be exported if you resize).

## Character panel essentials (Window > Character)
Font, size, **leading** (default Auto = 120%; set explicitly), **tracking** (whole
selection), **kerning** (between two letters: Metrics, Optical or manual with
Alt/Option+arrow keys), baseline shift, faux bold/italic (avoid: use the real weight),
OpenType features (ligatures, stylistic alternates).

## Paragraph panel
Alignment, indents, space before/after, **Hyphenate** (off for headlines), and the
**Every-line Composer** (better rag and justification than Single-line).

## Anti-aliasing
Options bar: None, Sharp, Crisp, Strong, Smooth. **Sharp** or **Crisp** for small screen
text; Smooth for large display type. Mac LCD / Windows LCD options mimic system rendering
for UI mockups.

## Keep it vector
- Type layers stay vector until rasterised. Saving a Photoshop PDF keeps vector type.
  JPEG/PNG exports rasterise at document resolution.
- For print, body copy should live in InDesign or Illustrator, not Photoshop: Photoshop
  text at 300 ppi is softer than true vector text in a PDF from layout software.

## Match Font
Select an area containing type in an image, Type > Match Font: suggests similar fonts
(Adobe Fonts and installed). Treat as a starting point, verify the letterforms.

## Gotchas
- Missing font warning on open: replacing changes metrics; check line breaks.
- Scaling a point type box non-uniformly distorts letters - change size instead.

## Verify
- [ ] Headlines are point type, body copy is paragraph type with no overflow +.
- [ ] No faux bold/italic; leading set explicitly; type layers not rasterised.
