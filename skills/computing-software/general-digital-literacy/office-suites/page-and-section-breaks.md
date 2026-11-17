---
id: computing-software.general-digital-literacy.office-suites.page-and-section-breaks
name: page-and-section-breaks
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, section-breaks, page-breaks, columns, next-page-break, continuous-break, keep-with-next]
level: intro
status: docs-checked
description: "Insert page and section breaks and newspaper columns in Word, Google Docs and LibreOffice instead of pressing Enter until text moves to the next page."
sources:
  - https://support.microsoft.com/en-us/word/use-section-breaks-to-change-the-layout-or-formatting-in-one-section-of-your-word-document
  - https://support.microsoft.com/en-us/word/customize-page-numbers-and-their-formats-in-different-word-document-sections
  - https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2
  - https://support.google.com/docs/answer/11526892
  - https://support.google.com/docs/answer/1663349
  - https://support.google.com/docs/answer/179738
  - https://help.libreoffice.org/latest/en-US/text/swriter/04/01020000.html
  - https://help.libreoffice.org/latest/en-US/text/swriter/guide/pageorientation.html
  - https://help.libreoffice.org/latest/en-US/text/swriter/00/00000404.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Page breaks, section breaks and columns

**Goal:** control where pages start and change layout part-way through a document.

## Page break
`Ctrl+Enter` in Word, Google Docs and LibreOffice. Never press Enter repeatedly: the next edit moves
everything and leaves a half-empty page.

## Section breaks (different layout in one document)
Needed for: a landscape page, different headers per chapter, restarting page numbers, columns for
part of a page.
- **Word:** Layout › Breaks › *Next Page* (new section on the next page), *Continuous* (new section on
  the same page, e.g. two columns under a one-column title) or *Even Page*/*Odd Page* (chapters that
  must start on an odd or even page).
- **Google Docs:** Insert › Break › Section break (next page) or Section break (continuous).
  View › Show section breaks to see them (hidden by default). Pages format only.
- **LibreOffice:** Insert › Section (for columns or other settings on part of a page), or page styles
  via Insert › More Breaks › Manual Break (choose the next page's style).

## Columns
- **Word:** put Continuous section breaks around the text and set the columns for that section.
  Force text to the next column with a column break (`Ctrl+Shift+Enter`).
- **Google Docs:** columns are available in pages format, not pageless.
- **LibreOffice:** Format › Columns, or Insert › Section › Columns tab; column break `Ctrl+Shift+Enter`.

## Keep things together instead
To stop a heading or paragraph splitting across pages use paragraph settings, not breaks: Google Docs
Format › Line & paragraph spacing › *Keep with next* / *Keep lines together* (or *Add page break
before*); LibreOffice Format › Paragraph › Text Flow.

## Gotchas
- See breaks with `Ctrl+Shift+8` (Word, show all nonprinting characters) or View › Formatting Marks,
  `Ctrl+F10` (LibreOffice).
- If a formatting change lands in the wrong section, undo, move the cursor after the section break and
  try again.

## Verify
- [ ] Adding a paragraph early in the document does not leave a nearly blank page later.

## Checked
2026-10-27 against Microsoft Support Word section-break pages and shortcuts (Microsoft 365), Google Docs
Editors Help (breaks, paragraph spacing, shortcuts) and the LibreOffice help (master). Confirmed: Ctrl+Enter
in all three; Word break types; Docs section breaks, Show section breaks and Keep with next/Keep lines
together; LibreOffice Manual Break with page style, Insert › Section, Format › Columns, Text Flow,
Ctrl+Shift+Enter and Ctrl+F10. Removed unconfirmed Word menu paths for columns and Keep with next and
the section-break deletion rule. Method: documentation only; no commands were run.
