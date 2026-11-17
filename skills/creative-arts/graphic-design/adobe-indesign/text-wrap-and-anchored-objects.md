---
id: creative-arts.graphic-design.adobe-indesign.text-wrap-and-anchored-objects
name: text-wrap-and-anchored-objects
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-text-frames, text-wrap, anchored-objects, contour-wrap, ignore-text-wrap, inline-graphics, custom-anchored-position, object-styles]
level: practitioner
status: draft
description: "Wrap text around images in InDesign (bounding box, contour, jump object) and anchor objects to text so sidebars, icons and images move with their paragraph."
sources:
  - https://helpx.adobe.com/indesign/using/wrapping-text-around-objects.html
  - https://helpx.adobe.com/indesign/using/anchored-objects.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Text wrap and anchored objects

**Goal:** images and boxes that push text away cleanly, and objects that travel with their text when copy reflows.

## Text wrap (Window > Text Wrap, Alt+Ctrl+W / Opt+Cmd+W)
| Mode | Use |
|---|---|
| Wrap around bounding box | rectangular images, sidebars |
| **Wrap around object shape** (contour) | cut-out images: Contour Options > Type: Alpha Channel, Photoshop Path, Detect Edges, Same as Clipping |
| Jump object | text stops above and resumes below (full-width images in a column) |
| Jump to next column | everything below goes to the next column |
- Offsets: match the gutter or baseline (e.g. 4 mm, or one line); for contour wraps 2-3 mm.
- **Wrap To:** Both sides / Side towards spine / Largest area. Avoid text on both sides of a small image in narrow columns.
- Put wrap settings in **object styles** for consistency.
- Text frames can ignore wraps: Text Frame Options > **Ignore Text Wrap** (captions sitting on an image).
- Preferences > Composition: **Text Wrap Only Affects Text Beneath** (so wraps on lower objects do not push text above them).

## Anchored objects (move with text)
- **Inline:** paste or place an object at the text cursor - it behaves like a character (icons, small figures in text). Adjust Y offset.
- **Above Line:** object sits on its own line above the anchor point; alignment left/center/right.
- **Custom:** drag the blue square of a frame into the text to anchor it, then Object > Anchored Object > Options:
  position relative to text frame, column edge, page margin or edge; **Relative to Spine** for left/right pages
  (a margin note that flips to the outside margin automatically); Keep Within Top/Bottom Column Boundaries.
- Anchor markers show with Type > Show Hidden Characters (yen-like symbol) and View > Extras > Show Text Threads.

## Typical uses
- Sidebar boxes and pull quotes anchored near their paragraph in long documents.
- Margin icons or numbers anchored to headings.
- Figures in technical documents that stay near their reference.

## Gotchas
- Anchored objects with text wrap only affect text **after** the anchor in the same story in some cases - test.
- Too many custom anchored objects slow composition in long documents.
- Contour wraps on soft-edged images use detect edges poorly; draw a path in Photoshop for clean wraps.

## Verify
- [ ] Wrap offsets consistent (object styles); no tiny word fragments squeezed beside images.
- [ ] Reflowing text moves anchored objects correctly; margin notes flip to the outer margin.
