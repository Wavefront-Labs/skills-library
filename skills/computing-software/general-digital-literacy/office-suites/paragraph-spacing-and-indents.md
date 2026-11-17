---
id: computing-software.general-digital-literacy.office-suites.paragraph-spacing-and-indents
name: paragraph-spacing-and-indents
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, paragraph-formatting, paragraph-spacing, indents, line-spacing, alignment, justify, hanging-indent, first-line-indent, ruler]
level: intro
status: docs-checked
description: "Control alignment, line spacing, space before/after and first-line or hanging indents with the ruler and paragraph dialog instead of extra Enter and Tab presses."
sources:
  - https://support.microsoft.com/en-us/word/adjust-indents-and-spacing-in-word
  - https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2
  - https://support.google.com/docs/answer/1663349
  - https://support.google.com/docs/answer/3300615
  - https://support.google.com/docs/answer/179738
  - https://help.libreoffice.org/latest/en-US/text/swriter/04/01020000.html
  - https://help.libreoffice.org/latest/en-US/text/swriter/00/00000405.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Paragraph alignment, spacing and indents

**Goal:** tidy, consistent paragraphs without blank lines and spaces used for layout.

## Alignment
`Ctrl+L` left, `Ctrl+E` centre, `Ctrl+R` right, `Ctrl+J` justify (Word/LibreOffice; Google Docs
uses `Ctrl+Shift+L/E/R/J`). Justified text in narrow columns makes "rivers" of white space; left
align body text unless a house style says otherwise.

## Spacing
- **Word:** Home › Line and Paragraph Spacing › Line Spacing Options, or the Paragraph dialog
  launcher › *Indents and Spacing* tab for exact values (e.g. 1.15 line, 6 pt before, 6 pt after).
- **Google Docs:** Format › Line & paragraph spacing › Single/1.15/1.5/Double, *Add space after
  paragraph*, or **Custom spacing**.
- **LibreOffice:** Format › Paragraph › Indents & Spacing.
- Use **space after** instead of pressing Enter twice; blank paragraphs break page layout and clutter
  navigation for screen-reader users.

## Indents
| Type | Use | How |
|---|---|---|
| Left indent | Quotations, nested blocks | Word `Ctrl+M` increase, `Ctrl+Shift+M` decrease |
| First-line | Book-style paragraphs | Word Paragraph dialog, Indents and Spacing tab |
| Hanging | Bibliographies, references | Word `Ctrl+T`; Docs Format › Align & indent › Indentation options › Special indent: Hanging |

## Gotchas
- Spaces or Tabs at the start of lines to line things up break as soon as the font changes;
  use indents or a table.
- Show hidden marks with `Ctrl+Shift+8` (Word) / View › Formatting Marks (LibreOffice) to see stray
  Enters and Tabs.

## Verify
- [ ] With formatting marks shown, there are no empty paragraphs used as spacers.

## Checked
2026-10-27 against Microsoft Support (Adjust indents and spacing; Word shortcuts, Microsoft 365), Google
Docs Editors Help (paragraph formatting, lists/indents, shortcuts) and the LibreOffice help (master).
Confirmed: all alignment shortcuts, Word Line and Paragraph Spacing and Paragraph dialog, Ctrl+M,
Ctrl+Shift+M, Ctrl+T, Ctrl+Shift+8, Docs spacing and hanging indent paths, LibreOffice Indents & Spacing and
Formatting Marks. Removed unconfirmed ruler-marker and "same style spacing" claims.
Method: documentation only; no commands were run.
