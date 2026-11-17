---
id: creative-arts.comics-and-sequential-art.lettering.narrator-caption-styles
name: narrator-caption-styles
category: creative-arts
field: comics-and-sequential-art
product: lettering
tags: [lettering, lettering-captions, caption-boxes, narrator-caption-style, caption-colour-coding, first-person-captions, caption-font]
level: practitioner
status: draft
description: "Design caption box styles per narrator: box shape, fill colour, font or italic choice, and a style sheet so multiple first-person narrators stay distinguishable through the book."
sources:
  - https://blambot.com/pages/comic-book-grammar-tradition
  - https://kleinletters.com/Blog/
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Coloring+and+Lettering+Comics
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Narrator caption styles

**Goal:** readers know who is narrating from the caption's look alone.

## Building blocks
- **Box shape**: rectangle (standard), rounded corners, torn paper, ragged edge, no box
  (floating text).
- **Fill colour**: a distinct pale tint per narrator (light enough that black text keeps
  strong contrast), or a dark fill with white/light text for an ominous voice.
- **Font**: dialogue font, its italic, or a distinct caption face; avoid more than one
  extra face.
- **Stroke**: thin black, coloured, or none.

## Style sheet
Write one entry per voice and share it with the colourist (if they colour boxes) and
editor:
```
Omniscient narrator: white box, black 0.5 pt stroke, dialogue font italic
Mara (1st person): pale yellow fill (C0 M5 Y25 K0), no stroke, dialogue font
Teo (1st person): pale blue fill (C20 M0 Y0 K0), no stroke, dialogue font
Journal: off-white torn-paper box, handwriting font
```
Build them as Illustrator graphic + paragraph styles (or CSP sub tool presets).

## Placement
- Top-left of the panel for narration that reads first; butted against the panel
  border is common.
- Multiple captions in a panel stack in reading order with a small gap or butted.

## Gotchas
- Two narrators with near-identical tints, especially after CMYK conversion.
- Coloured boxes with grey text: low contrast in print.

## Verify
- [ ] Each narrator has a distinct, documented style.
- [ ] Contrast checked in print proof.
