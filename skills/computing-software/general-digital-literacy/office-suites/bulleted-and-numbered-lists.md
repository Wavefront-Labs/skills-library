---
id: computing-software.general-digital-literacy.office-suites.bulleted-and-numbered-lists
name: bulleted-and-numbered-lists
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, bullets-and-numbering, bulleted-list, numbered-list, multilevel-list, restart-numbering, list-indent]
level: intro
status: docs-checked
description: "Create bulleted, numbered and multilevel lists, restart or continue numbering and fix list indents in Word, Google Docs and LibreOffice."
sources:
  - https://support.microsoft.com/en-us/word/autoformat-as-you-type
  - https://support.microsoft.com/en-us/word/change-the-numbering-in-a-numbered-list
  - https://support.microsoft.com/en-us/word/change-bullet-indents-in-word
  - https://support.microsoft.com/en-us/word/add-chapter-numbers-to-captions-in-word
  - https://support.google.com/docs/answer/3300615
  - https://support.google.com/docs/answer/179738
  - https://help.libreoffice.org/latest/en-US/text/swriter/04/01020000.html
  - https://help.libreoffice.org/latest/en-US/text/swriter/02/06140000.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bulleted and numbered lists

**Goal:** lists that number themselves correctly and indent consistently.

## Create
- **Word** (AutoFormat As You Type): start a line with `*`, `-` or `>` plus a space or tab for bullets,
  or `1` followed by a period or tab for numbers. Press `Enter` twice to end the list.
- **Google Docs:** toolbar list buttons, or `Ctrl+Shift+7` numbered / `Ctrl+Shift+8` bulleted.
  `Tab` starts a nested list; `Enter` twice returns to the main list.
- **LibreOffice Writer:** `F12` toggles an ordered (numbered) list, `Shift+F12` an unordered (bulleted) list.
- **Multilevel lists (1, 1.1, 1.1.1) in Word:** Home › Paragraph › Multilevel List.

## Restart or continue numbering
- **Word:** right-click the number › **Restart at 1**, or **Set Numbering Value** for any start number.
- **Google Docs:** double-click the first number › Format › Bullets & numbering › List options ›
  **Restart numbering** (enter the start number) or **Continue previous numbering**.
- **LibreOffice:** right-click in the list › List › **Restart Numbering** (also Format › Lists ›
  Restart Numbering).

## Fix the indent
- **Word:** click a bullet or number, right-click › **Adjust List Indents**: bullet position, text
  indent, and *Follow number with* Tab character / Space / Nothing.
- **Google Docs:** Format › Align & indent › Indentation options (e.g. Special indent: Hanging).

## Gotchas
- Typing numbers by hand without the list feature means re-numbering every time an item is added.
  Check: clicking a real list number highlights all numbers in that list.
- Pasted lists often bring a different list style. Paste text only, then reapply the list.
- For documents with numbered chapters in Word, apply a chapter-numbering multilevel list definition
  to the Heading 1 style so numbering follows the headings.

## Verify
- [ ] Insert an item in the middle: following numbers update automatically.

## Checked
2026-10-27 against Microsoft Support Word pages (Microsoft 365), Google Docs Editors Help and the
LibreOffice help (master). Confirmed: Word AutoFormat list triggers and Enter-twice ending; Restart at 1,
Set Numbering Value and Adjust List Indents options; Docs list shortcuts and the Format › Bullets &
numbering › List options restart/continue path; LibreOffice F12/Shift+F12 and List › Restart Numbering.
Method: documentation only; no commands were run.
