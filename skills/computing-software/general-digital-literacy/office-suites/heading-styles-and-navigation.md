---
id: computing-software.general-digital-literacy.office-suites.heading-styles-and-navigation
name: heading-styles-and-navigation
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, heading-styles, styles, headings, navigation-pane, document-outline, modify-style, normal-style]
level: intro
status: docs-checked
description: "Apply Heading 1-3 styles, modify a style once to update the whole document and navigate long documents with the Navigation pane or Docs outline."
sources:
  - https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2
  - https://support.microsoft.com/en-us/word/customize-or-create-new-styles
  - https://support.microsoft.com/en-us/word/use-the-navigation-pane-in-word
  - https://support.google.com/docs/answer/179738
  - https://support.google.com/docs/answer/1663349
  - https://support.google.com/docs/answer/6367684
  - https://help.libreoffice.org/latest/en-US/text/swriter/04/01020000.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heading styles and document navigation

**Goal:** structure a document so headings look consistent, drive the table of contents and are
navigable.

## Apply
- **Word:** Home › Styles gallery, or `Ctrl+Alt+1/2/3` for Heading 1/2/3, `Ctrl+Shift+N` Normal.
- **Google Docs:** style box ("Normal text") or `Ctrl+Alt+1..6`, `Ctrl+Alt+0` normal text.
- **LibreOffice:** Paragraph Style box or `Ctrl+1/2/3`, `Ctrl+0` Body Text.

## Modify once, update everywhere
- **Word:** right-click the style in the Styles gallery › **Modify** (font, spacing…). Or format one
  heading how you like › right-click the style › **Update Heading 1 to Match Selection**.
- **Google Docs:** format one heading › Format › Paragraph styles › Heading 1 › **Update 'Heading 1'
  to match**. Format › Paragraph styles › Options › **Save as my default styles** to reuse in new docs.
- **LibreOffice:** Styles deck (`F11`); `Ctrl+Shift+F11` updates the current style from the selection.

## Navigate
- Word: `Ctrl+F` or View › **Navigation Pane** › Headings tab; drag a heading there to move its whole
  section.
- Google Docs: View › Show outline (left pane) lists headings.
- LibreOffice: Navigator (`F5`) lists headings.

## Gotchas
- Big bold Normal text is not a heading: it won't show in the outline, TOC or to screen readers.
- Word's Navigation pane does not show headings inside tables, text boxes, headers or footers.
- Don't skip levels (H1 then H3); readers and accessibility checkers expect a hierarchy.

## Verify
- [ ] Navigation pane / outline lists every heading at the right level.

## Checked
2026-10-27 against the Microsoft Word shortcuts, styles and Navigation pane pages (Microsoft 365), Google
Docs Editors Help (shortcuts, paragraph styles, outline) and the LibreOffice shortcut help (master).
Confirmed every shortcut and menu path listed, including Update to Match Selection, Save as my default
styles and Navigation-pane drag to move. Removed unconfirmed claims about LibreOffice drag-reorder and
Word's default Keep with next. Method: documentation only; no commands were run.
