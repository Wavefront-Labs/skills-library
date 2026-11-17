---
id: creative-arts.graphic-design.adobe-indesign.bullets-and-numbering
name: bullets-and-numbering
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, paragraph-styles, character-styles, bullets-and-numbering, numbered-lists, defined-lists, hanging-indent, list-levels, convert-numbering-to-text]
level: practitioner
status: draft
description: "Build bulleted and numbered lists in InDesign via paragraph styles: hanging indents, bullet characters, numbering levels, and defined lists across stories."
sources:
  - https://helpx.adobe.com/indesign/using/bullets-numbering.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bullets and numbering

**Goal:** lists with aligned text, consistent bullets and numbering that stays correct when items are added or moved.

## Set it in the paragraph style (Bullets and Numbering section)
- **List Type:** Bullets or Numbers.
- **Bullet character:** add from any font (e.g. en dash, square, brand glyph); give it a **character style**
  (colour, size, baseline shift) rather than local formatting.
- **Text After:** `^t` (tab).
- **Hanging indent:** Left Indent = e.g. 5 mm, First Line Indent = -5 mm, **Tab Position** = 5 mm. Text wraps under
  the first word, not under the bullet.
- Align bullets with the left edge of body text, or hang them into the margin (negative left offset) - a typographic choice; be consistent.

## Numbering
- **Format:** 1, 2, 3 / i, ii / A, B; **Number** field like `^#.^t` (number, full stop, tab). `^#` = current number, `^1` level 1 number for nested formats (`^1.^#`).
- **Mode:** Continue from Previous Number or Start At.
- **Level:** 1-9 for nested lists; set "Restart Numbers at This Level After" a higher level.
- Right-align numbers when lists exceed 9 items: Alignment Right, with the tab after aligned.

## Defined lists (numbering across frames and stories)
Type > Bulleted and Numbered Lists > **Define Lists**: e.g. `Figures`, `Steps`, with **Continue Numbers across
Stories** / across Documents in a Book. Assign the list in the paragraph style. Figure captions numbered
`Figure ^#` continue through unthreaded caption frames.

## Converting
Right-click > Convert Numbering to Text (freezes numbers, e.g. before exporting text or for EPUB quirks). Avoid
in working files.

## Gotchas
- Pasted lists from Word arrive with typed bullets and tabs - remove them (Find/Change) and use the style.
- Space between list items: Space Before/After in the style, not empty returns.
- Restarting numbering for a new list: right-click > Restart Numbering, or a separate "List first" style with Start At 1.

## Verify
- [ ] Turnover lines align under text, not bullets; bullets styled via character style.
- [ ] Inserting an item renumbers correctly; caption numbering continues across frames.
