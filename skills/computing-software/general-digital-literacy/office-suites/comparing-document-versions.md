---
id: computing-software.general-digital-literacy.office-suites.comparing-document-versions
name: comparing-document-versions
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, compare-documents, combine-documents, redline, version-comparison, track-changes, compare-versions]
level: intro
status: docs-checked
description: "Compare two versions of a document to see every change as tracked redlines with Word Compare, Google Docs Compare documents or LibreOffice Compare Document."
sources:
  - https://support.microsoft.com/en-us/word/compare-and-merge-two-versions-of-a-document
  - https://support.google.com/docs/answer/18512262
  - https://help.libreoffice.org/latest/en-US/text/shared/guide/redlining_doccompare.html
  - https://help.libreoffice.org/latest/en-US/text/shared/00/00000401.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comparing two versions of a document

**Goal:** someone sent back an edited copy without track changes; see exactly what changed.

## Word
1. Review › Compare › **Compare Documents** (two versions) or **Combine Documents** (merge a
   revised copy into a new copy based on the original).
2. Original document = your version, Revised document = theirs › OK.
3. The result is a new document with the differences as revision marks; the originals are untouched.
   Accept/reject as usual.

## Google Docs
Open the primary doc › Tools › **Compare documents** › optionally set *Attribute differences to* and
*Include comments from the selected document* › select the other doc (a Google Doc, or a Word .docx
stored in Drive) › Compare › Open. A third doc opens with every difference as a suggested edit.
Changes to column layout and table column widths are not compared.

## LibreOffice Writer
Open the **newer** (reviewer's) document › File › **Compare Document** (Review › Compare in the tabbed
interface) › choose the older original. Insertions and deletions are marked in the reviewer's document;
accept or reject them, then save under a new name.

## Gotchas
- Always start from the right file: LibreOffice expects you to open the newer document and compare it
  with the older one.
- Comparing heavily reformatted documents floods the result with formatting changes; review in passes.

## Verify
- [ ] Spot-check three changes in the comparison against the two originals.

## Checked
2026-10-27 against Microsoft Support (Compare and merge two versions of a document), Google Docs Editors
Help (Compare documents) and the LibreOffice help (master). Confirmed: Word Compare Documents and Combine
Documents with Original/Revised; Docs Tools › Compare documents options, .docx support and the
exclusions; LibreOffice File › Compare Document and the newer-then-older workflow (the old Edit › Track
Changes path was corrected). Removed unconfirmed Word option names and the PDF tip.
Method: documentation only; no commands were run.
