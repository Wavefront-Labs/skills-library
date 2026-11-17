---
id: computing-software.general-digital-literacy.office-suites.document-properties-and-inspect-document
name: document-properties-and-inspect-document
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, document-setup, document-properties, inspect-document, metadata, remove-personal-information]
level: practitioner
status: docs-checked
description: "Strip hidden comments, revisions, headers, hidden text and personal properties from a Word file with Document Inspector before sharing it."
sources:
  - https://support.microsoft.com/en-us/office/collab-files/remove-hidden-data-and-personal-information-by-inspecting-documents-presentations-or-workbooks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Document Inspector

**Goal:** the file you send contains nothing you did not mean to share (old comments, tracked changes, your name in properties, hidden text).

## Inspect before sharing (Word)
1. Inspect a **copy** of the original: removed data often cannot be restored.
2. **File > Info > Check for Issues > Inspect Document**.
3. Tick the categories to check: *Comments, Revisions, Versions, and Annotations*; *Document Properties and Personal Information*; *Headers, Footers, and Watermarks*; *Hidden Text*; *Custom XML Data*; *Invisible Content*. Select **Inspect**.
4. Select **Remove All** next to each result you want stripped, then **Reinspect > Inspect** to confirm.

## Gotchas
- Review and accept or reject tracked changes yourself first so the text is what you intend before removing revision data.
- The Hidden Text inspector cannot detect text hidden by other methods, for example white text on a white background.
- Excel and PowerPoint have their own inspector categories (for example hidden rows and columns in Excel); deleting hidden rows or columns that hold data can change formulas.
- The inspector cannot detect some objects (shapes, charts, ActiveX controls, pictures, SmartArt) that sit in hidden columns.

## Verify
- [ ] Re-run Inspect Document: no items found for the categories you cleared.

## Checked

2026-10-27. Microsoft Support 'Remove hidden data and personal information by inspecting documents, presentations, or workbooks' (Word/Excel/PowerPoint, read 2026-10-27): menu path, Word inspector category names, Remove All, Reinspect, copy advice, hidden-text and object limits. Removed: File > Info property editing, Mac path, Title-for-screen-readers, 'remove personal information on save' semantics, EXIF and PDF viewer advice (not on the page). Description narrowed to match.

Method: documentation only; no commands were run.
