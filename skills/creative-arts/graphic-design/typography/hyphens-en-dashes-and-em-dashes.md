---
id: creative-arts.graphic-design.typography.hyphens-en-dashes-and-em-dashes
name: hyphens-en-dashes-and-em-dashes
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, typographic-details, punctuation, dashes, hyphen, en-dash, em-dash, minus-sign, figure-dash, ranges, copyfitting, find-change, keyboard-shortcuts]
level: intro
status: draft
description: "Use hyphen, en dash, em dash and minus sign correctly in typeset text, with keyboard entry, house-style spacing choices, and Find/Change clean-up of supplied copy."
sources:
  - https://www.chicagomanualofstyle.org/book/ed17/part2/ch06/toc.html
  - https://practicaltypography.com/hyphens-and-dashes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hyphens, en dashes and em dashes

**Goal:** every dash in a document is the right character with consistent spacing.

## Which one
| Character | Use | Example |
|---|---|---|
| **Hyphen** `-` | compound words, line-break hyphenation | well-known, e-mail |
| **En dash** `–` (U+2013) | ranges and connections; in UK style also as a spaced parenthetical dash | 1990–2000, pages 12–18, London–Paris train, pre–Second World War |
| **Em dash** `—` (U+2014) | parenthetical break in US style (usually closed up) | The plan—if it was one—failed. |
| **Minus** `−` (U+2212) | maths and negative numbers; aligns with + | −5 °C |
| Figure dash `‒` (U+2012) | within phone numbers in tabular setting | rarely needed |

House styles: **US/Chicago** closed em dash (`word—word`); **UK/most European** spaced en
dash (`word – word`). Pick one per document and stick to it. Use a thin or hair space around
an em dash if closed-up looks cramped in the chosen face.

## Typing them
| | Windows | macOS | InDesign |
|---|---|---|---|
| En dash | Alt+0150 | Option+- | Alt+- / Option+- |
| Em dash | Alt+0151 | Option+Shift+- | Alt+Shift+- / Option+Shift+- |
| Minus | Alt+8722 (in some apps) or glyphs panel | Glyphs/Character Viewer | Glyphs panel |
In InDesign Find/Change, `^=` is en dash, `^_` is em dash, `^~` non-breaking hyphen, `^-` discretionary hyphen.

## Clean up supplied copy (Find/Change, Text tab)
1. `--` -> `^_` (em dash) or ` - ` (space hyphen space) -> ` ^= ` per house style.
2. Ranges: GREP `(\d)-(\d)` -> `$1~=$2` (en dash between digits). Check results: phone numbers,
   ISBNs and part numbers must keep hyphens - review with Find Next rather than Change All
   if unsure.
3. Make spaced en dashes non-breaking before: `~S~=` (non-breaking space + en dash) keeps
   the dash from starting a line.

## Line-break behaviour
- Lines may break after an em/en dash; avoid starting a line with a dash (non-breaking space before).
- Hyphenated compounds can break at their hyphen - use a **non-breaking hyphen** for things
  like product codes.

## Verify
- [ ] Find `--` and ` - ` returns nothing in body text.
- [ ] Ranges use en dashes; negative numbers use minus in tables.
- [ ] One consistent parenthetical-dash style throughout.
