---
id: creative-arts.graphic-design.adobe-indesign.cross-references-and-hyperlinks
name: cross-references-and-hyperlinks
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, cross-references, hyperlinks, text-anchors, cross-reference-formats, interactive-pdf, long-documents, see-page]
level: practitioner
status: draft
description: "Create live InDesign cross-references (see page 42) and hyperlinks: paragraph and anchor targets, building blocks in formats, updating, and exporting them as live PDF links."
sources:
  - https://helpx.adobe.com/indesign/using/cross-references.html
  - https://helpx.adobe.com/indesign/using/hyperlinks.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cross-references and hyperlinks

**Goal:** "see Chapter 4, page 87" references that update when pages move, and links that work in the
exported PDF or EPUB.

## Cross-references (Window > Type & Tables > Cross-References)
1. Put the cursor where the reference goes, click **Create New Cross-Reference**.
2. Link To: **Paragraph** (choose a paragraph style, e.g. Heading 2, then the paragraph) or **Text Anchor**
   (create anchors first with Hyperlinks panel > New Hyperlink Destination > Text Anchor).
3. Document: this document or another in the book.
4. **Format:** Full Paragraph & Page Number, Paragraph Text, Page Number, etc. Edit formats with building
   blocks: `<pageNum />`, `<paraText />`, `<paraNum />`, `<fullPara />`, `<chapNum />`, `<txtAnchrName />`,
   wrapped in literal text (`see page <pageNum />`), and a character style for the reference.
5. The reference is live text; when its target moves, the panel shows it as out of date: **Update
   Cross-References**. Book: update all documents from the Book panel menu.

## Hyperlinks (Window > Interactive > Hyperlinks)
- Select text or a frame, **Create New Hyperlink**: URL, File, Email, Page, Text Anchor, Shared Destination.
- Apply a character style to show links. URLs typed in text can be converted with **Convert URLs to Hyperlinks**.
- Cross-references are hyperlinks too: they work in PDF when **Hyperlinks** is checked on export (Interactive
  PDF always; Print PDF needs the Include > Hyperlinks option).

## Gotchas
- Cross-references to deleted paragraphs show a broken icon; resolve before final output.
- Paragraph text in references breaks oddly if headings contain forced line breaks; use a heading without
  manual breaks or a text anchor.
- Links panel ordering: hyperlinks set on frames are lost if the frame is replaced.
- Cross-references to other documents need the book open to update.

## Verify
- [ ] Cross-References panel shows no out-of-date or unresolved items.
- [ ] Test links in the exported PDF with the hand tool in Acrobat.
