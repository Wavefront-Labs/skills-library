---
id: creative-arts.graphic-design.adobe-indesign.footnotes-and-endnotes
name: footnotes-and-endnotes
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, footnotes, endnotes, document-footnote-options, footnote-numbering, span-footnotes, word-import, long-documents, academic-books]
level: practitioner
status: draft
description: "Set footnotes and endnotes in InDesign: import from Word, numbering and restart rules, footnote layout and separator rule, spanning columns, and endnote placement."
sources:
  - https://helpx.adobe.com/indesign/using/footnotes.html
  - https://helpx.adobe.com/indesign/using/endnotes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Footnotes and endnotes

**Goal:** notes that stay attached to their reference, renumber automatically, and look consistent
through the whole book.

## Import
- Word footnotes and endnotes come in as live notes when placing a .docx with **Import Options** > Include
  Footnotes / Include Endnotes checked.
- Insert manually: Type > **Insert Footnote** or **Insert Endnote** at the cursor.

## Footnotes: Type > Document Footnote Options
- **Numbering and Formatting:** style (1, 2, 3 / i, ii / symbols * dagger), start at, **Restart Numbering
  Every** page, spread or section; reference number in text with a character style (superscript); footnote
  paragraph style; separator between number and text (tab or em space).
- **Layout:** space before first footnote, space between footnotes, first baseline offset, **Place End of
  Story Footnotes at Bottom of Text**, **Allow Split Footnotes** (continues to the next column), and the
  **Rule Above** (weight, length, offset; separate rules for first and continued footnotes).
- **Span Footnotes Across Columns** (CC 2015+) for multi-column frames; otherwise notes sit under the
  column containing the reference.

## Endnotes: Type > Document Endnote Options
- Endnote frame on a new page or in a chosen story, heading, number style, scope (document or section).
- For a book with endnotes per chapter, keep each chapter as a document and set numbering per document.
- InDesign endnotes are live and cross-linked; older documents may have converted Word endnotes as static
  text with hyperlinks.

## Typographic conventions
- Footnote text 1-2 pt smaller than body with proportional leading, ideally on the baseline grid
  increment or a half increment.
- Reference figures after punctuation in English prose (Chicago), before it in some other languages.

## Gotchas
- Footnotes cannot sit in tables in older versions; they convert or are lost on import. Check tables.
- Large footnotes push body text to the next page; Allow Split Footnotes avoids gaps.
- A paragraph style with **Keep Lines Together** can fight footnotes; check overset and page breaks.

## Verify
- [ ] Numbering restarts where specified; references and notes match across every page.
- [ ] No overset notes (Preflight shows overset text).
