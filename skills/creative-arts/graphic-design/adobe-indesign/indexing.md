---
id: creative-arts.graphic-design.adobe-indesign.indexing
name: indexing
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-index, index-markers, index-panel, cross-references-index, see-also, book-index, long-documents]
level: practitioner
status: draft
description: "Build a back-of-book index in InDesign: index markers, topics and subtopics, page ranges, see and see-also references, generating across a book, and styling the index."
sources:
  - https://helpx.adobe.com/indesign/using/creating-index.html
  - https://www.chicagomanualofstyle.org/book/ed18/part3/ch15/toc.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Indexing in InDesign

**Goal:** an accurate, regenerable index whose page numbers follow the text through every reflow.

## Concepts
- **Index marker:** an invisible anchor in the text (Type > Show Hidden Characters shows it) tied to a
  **topic**. Page numbers come from where markers sit, so the index survives repagination.
- **Topics** can have up to four levels (main entry, subentries).

## Adding entries (Window > Type & Tables > Index)
1. Select the word in text, click **Create New Index Entry** in the Index panel (or Ctrl/Cmd+Alt/Option+U
   for a quick entry with defaults; Shift+Alt+Ctrl+[ for a proper-name entry inverted as `Last, First`).
2. Set topic levels, **Sort By** (to index `St. Louis` as `Saint Louis`, or numerals as words), and type:
   - Current Page, **To End of Story**, To Next Use of Style, For Next # of Paragraphs, **To Next Style Change**
     (page ranges), Suppress Page Range.
   - **See**, **See also**, See herein: cross-references with no page numbers.
3. **Add All** indexes every occurrence of the selected text in the document (check each; not all are relevant).
4. Page number style override: bold or italic page numbers for main discussions and illustrations.

## Generate
- Index panel > **Generate Index**: title, title style, Replace Existing Index, Include Book Documents,
  Include Entries on Hidden Layers, Nested vs Run-in, section headings (A, B, C), and level styles.
- Load the place gun and flow into the index pages. Regenerate after every change.
- For a **book**: one index per book, with Book mode in the Index panel so topics are shared.

## Editorial rules (Chicago Manual of Style ch. 15)
- Index concepts, not every word; use the reader's terms; avoid long undifferentiated runs of page numbers
  (more than five or six: split into subentries).
- Prefer **See** for synonyms to send readers to the main term, **See also** for related topics.

## Gotchas
- Markers placed inside overset text or on pasteboard produce no page numbers or errors.
- Deleting text deletes its markers. Index late, after copy is final, but before final pagination checks.
- Topics with mistyped duplicates (`colour`, `color`) show as separate entries; check the topic list.

## Verify
- [ ] Spot-check 20 entries against the pages.
- [ ] Regenerated index after the last edit; no `see` references point to missing topics.
