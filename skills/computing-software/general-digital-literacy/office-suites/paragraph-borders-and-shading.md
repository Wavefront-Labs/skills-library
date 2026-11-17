---
id: computing-software.general-digital-literacy.office-suites.paragraph-borders-and-shading
name: paragraph-borders-and-shading
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, wp-formatting, paragraph-borders, paragraph-shading, word]
level: intro
status: docs-checked
description: "Put a box, a rule above or below, or a background shade on a paragraph in Word or Google Docs, and remove a stubborn line that AutoFormat added."
sources:
  - https://support.microsoft.com/en-us/word/add-a-border-to-some-text-in-word
  - https://support.microsoft.com/en-us/word/remove-a-line-in-word
  - https://support.microsoft.com/en-us/word/insert-a-horizontal-line
  - https://support.microsoft.com/en-us/word/autoformat-as-you-type
  - https://support.microsoft.com/en-us/word/word-options-display
  - https://support.google.com/docs/answer/1663349
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Paragraph borders and shading

## Word
1. Click in the paragraph (or select several).
2. **Home › Borders** drop-down: pick a border, or *No Border* to remove one.
3. For style, colour and width: **Borders and Shading…** › *Borders* tab (Setting, Style, Color, Width).
   Set *Apply to: Paragraph* (not *Text*, which boxes only the selected text).
4. Shading: *Shading* tab › *Fill* colour and pattern.

## Google Docs
- **Format › Paragraph styles › Borders and shading**: choose position (top, bottom, left, right,
  between), width, dash, colour, background colour and padding; *Reset* clears them.

## Remove a line you can't select
- Typing three `-`, `_`, `=`, `~`, `#` or `*` on a line by itself then Enter makes Word draw a
  bottom border on an empty paragraph. Press Backspace straight away to undo it, or put the cursor just
  above the line › **Borders › No Border**.
- Stop it happening: **File › Options › Proofing › AutoCorrect Options › AutoFormat As You Type** › clear
  *Border Lines*.

## Gotchas
- For callout boxes that move independently, a text box or 1-cell table can be easier than borders.
- Page colour (Design › Page Color) prints only when File › Options › Display › *Print background
  colors and images* is ticked.

## Verify
- [ ] Print preview shows the box/shade where expected and no stray lines remain.

## Checked
2026-10-27 against Microsoft Support (add a border to text, remove a line, insert a horizontal line,
AutoFormat As You Type, Word Options Display; Word for Microsoft 365) and Google Docs Editors Help
(paragraph formatting). Confirmed: Borders and Shading dialog and Apply to Text/Paragraph, Shading Fill,
the three-character border trigger and its characters, No Border fix, Border Lines option, Docs Borders
and shading settings, background printing option. Removed unconfirmed claims about merging adjacent
borders, the Options distance dialog and paragraph-shading printing. Method: documentation only; no commands were run.
