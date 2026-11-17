---
id: computing-software.general-digital-literacy.office-suites.tab-stops-and-leaders
name: tab-stops-and-leaders
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, paragraph-formatting, tab-stops, tab-leaders, ruler, decimal-tab]
level: practitioner
status: docs-checked
description: "Line up text with left, centre, right, decimal and bar tab stops and dot leaders in Word, instead of pressing space or Tab repeatedly."
sources:
  - https://support.microsoft.com/en-us/word/using-the-ruler-in-word
  - https://support.microsoft.com/en-us/word/insert-or-add-tab-stops
  - https://support.microsoft.com/en-us/word/show-dots-or-leaders-between-tabs
  - https://support.microsoft.com/en-us/word/use-decimal-tabs-to-line-up-numbers-with-decimal-points
  - https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tab stops and leaders

**Goal:** columns of text that stay aligned however fonts change: price lists, agendas, signature
lines, simple tables of contents.

## Word
- Show the ruler: **View › Ruler**. Show marks: **Ctrl+Shift+8** to see tab characters.
- Click the tab selector at the ruler's left end to choose **Left, Center, Right, Decimal or Bar**, then
  click the bottom of the ruler where you want the stop. Drag a stop off the ruler (downwards) to delete it.
- Exact positions and leaders: **Home › Paragraph dialog launcher › Tabs…** › *Tab stop position*
  (e.g. 15 cm), *Alignment*, *Leader* (dots, dashes…) › **Set** › OK. *Clear* / *Clear All* remove stops.
- Example agenda line: right tab at the right margin with a dot leader, type `Welcome` Tab `9:00`.
- Tabs belong to the paragraph; select all affected lines before setting them. Put them in a style
  to reuse.
- Word for the web shows tabs but cannot set or remove them; open the desktop app.

## Google Docs and other editors
For aligned columns that must survive editing, a borderless 2-column table is often simpler than tabs.

## When to use a table instead
More than one line per cell, wrapping text, or more than 3 columns: insert a table and hide borders.
Tables reflow better on narrow screens and are read correctly by screen readers.

## Gotchas
- Pressing Tab several times works until the font or text changes, then everything misaligns.
- Decimal tabs align numbers on the decimal point.
- A Bar tab inserts a vertical line that prints unless you clear the stop.

## Verify
- [ ] Change the font size: columns stay aligned.

## Checked
2026-10-27 against Microsoft Support Word tab and ruler pages (Word for Microsoft 365, 2024, 2021) and
the Word keyboard shortcuts. Confirmed: View › Ruler, tab selector types including Bar, click-to-set and
drag-off-to-clear, Tabs dialog position/alignment/leader/Set/Clear All, decimal tab behaviour, Word for
the web limitation, Ctrl+Shift+8. Removed unconfirmed Google Docs ruler and leader claims and the
default-stop spacing rule. Method: documentation only; no commands were run.
