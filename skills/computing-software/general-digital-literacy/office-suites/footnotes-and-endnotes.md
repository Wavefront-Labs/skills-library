---
id: computing-software.general-digital-literacy.office-suites.footnotes-and-endnotes
name: footnotes-and-endnotes
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, styles, headings, footnotes, endnotes, convert-footnotes]
level: practitioner
status: docs-checked
description: "Insert, number, convert and delete footnotes and endnotes in Word and Google Docs, and fix separator, numbering-restart and continuation problems."
sources:
  - https://support.microsoft.com/en-us/word/training/insert-footnotes-and-endnotes-in-word
  - https://support.microsoft.com/en-us/word/delete-a-footnote-endnote-or-separator
  - https://support.microsoft.com/en-us/accessibility/word/use-a-screen-reader-to-read-and-edit-footnotes-and-endnotes-in-word
  - https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2
  - https://support.google.com/docs/answer/86629
  - https://support.google.com/docs/answer/179738
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Footnotes and endnotes

## Insert
- Word: cursor after the word/punctuation › **References › Insert Footnote** (**Ctrl+Alt+F**) or
  **Insert Endnote** (**Ctrl+Alt+D**). Type the note; double-click the mark at the start of the note
  to return to the text.
- Google Docs: **Insert › Page elements › Footnote** (**Ctrl+Alt+F**). In pageless format all footnotes
  appear together at the end of the document.
- Delete a note by deleting its **reference mark in the body**, not the note text; Word renumbers the rest.
- Remove all notes in Word: Replace (`Ctrl+H`), *Find what* `^f` (footnotes) or `^e` (endnotes),
  *Replace with* empty › Replace All.

## Options (Word: Footnote and Endnote dialog from the References tab)
- Location, layout and number format of footnotes or endnotes.
- Numbering that restarts part-way needs a section break where the restart should happen.
- **Convert…**: convert all footnotes to endnotes, all endnotes to footnotes, or swap them (a common
  journal requirement). Word for the web cannot convert; open the file in desktop Word.

## Formatting
- Notes use the *Footnote Text* and *Endnote Text* styles; modify the style, not each note.
- Separator line: **View › Draft**, double-click a note reference, choose *Footnote Separator* in the
  Footnotes pane list and edit or delete the line.

## Gotchas
- Placement: after punctuation in most English styles ("…in 2020.¹").
- Citation styles such as APA use in-text citations, not footnotes; Chicago notes-bibliography uses them.

## Verify
- [ ] Walk every note in order (Word: References › Next Footnote) and check there are no gaps.

## Checked
2026-10-27 against Microsoft Support Word footnote pages (Microsoft 365, 2024, 2021), the Word keyboard
shortcuts page and Google Docs Editors Help. Confirmed: Insert Footnote/Endnote and their shortcuts,
deleting the reference mark, ^f/^e removal, the Footnote and Endnote dialog options and Convert Notes
choices, section breaks for restarts, Footnote Text style, Draft-view separator editing, Docs Insert ›
Page elements › Footnote and Ctrl+Alt+F. Removed unconfirmed claims (Shift+F5 jump, continuation
separator behaviour, Docs having no endnotes, paste behaviour). Method: documentation only; no commands were run.
