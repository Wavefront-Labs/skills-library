---
id: computing-software.general-digital-literacy.office-suites.captions-and-cross-references
name: captions-and-cross-references
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, styles, table-of-contents, figure-captions, cross-references, table-of-figures]
level: practitioner
status: docs-checked
description: "Number figures and tables with captions, refer to them with cross-references that update, and build a table of figures in Word."
sources:
  - https://support.microsoft.com/en-us/word/add-format-or-delete-captions-in-word
  - https://support.microsoft.com/en-us/word/add-chapter-numbers-to-captions-in-word
  - https://support.microsoft.com/en-us/word/create-a-cross-reference
  - https://support.microsoft.com/en-us/word/insert-a-table-of-figures
  - https://support.microsoft.com/en-us/word/word-options-display
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Captions and cross-references

**Goal:** "see Figure 3" stays correct after you add, delete or reorder figures.

## Captions
1. Select the picture/table › **References › Insert Caption**.
2. Label: Figure, Table, Equation, or **New Label** (e.g. "Chart"); type any text after the label.
   Position: below figures, above tables (common convention).
3. **Numbering…** › *Include chapter number* (chapter headings need a unique style such as Heading 1
   with a chapter-numbering multilevel list) → "Figure 2-3".
4. **AutoCaption…** can caption chosen object types automatically as you insert them.
- Captions use the *Caption* style; modify that style to restyle every caption.
- For a picture with text wrapping, set the wrapping before captioning, then select caption and
  picture and **Group** them so they move together.

## Cross-references
**Insert › Cross-reference** › Reference type: Figure/Table/Heading/Bookmark/Footnote ›
Insert reference to: e.g. label and number, page number, above/below › tick **Insert as hyperlink** ›
Insert. Create the target (caption, heading, bookmark) first.

## Update
Caption numbers and cross-references are fields. **Ctrl+A** then **F9** updates all (needed after
deleting or moving captions). File › Options › Display › *Update fields before printing* refreshes
fields on print.

## Table of figures
**References › Insert Table of Figures**. After changes select it › **References › Update Table**
(or F9) › Update entire table.

## Gotchas
- "Error! Reference source not found." = the target was deleted. Re-insert the cross-reference.
- Typing "Figure 3" by hand is not a field and will not update. If captions show as
  `{SEQ ...}` codes, press Alt+F9 to switch back to results.

## Verify
- [ ] Insert a new figure at the start, Ctrl+A, F9: every caption and reference renumbers.

## Checked
2026-10-27 against Microsoft Support Word pages (Word for Microsoft 365, 2024, 2021). Confirmed: Insert
Caption, New Label, AutoCaption and the Caption style; chapter numbers via Numbering › Include chapter
number; floating figure grouping; Insert › Cross-reference with Insert as hyperlink; Ctrl+A, F9 update
and Alt+F9 field codes; Update fields before printing; Insert/Update Table of Figures. Removed an
unconfirmed Google Docs claim. Method: documentation only; no commands were run.
