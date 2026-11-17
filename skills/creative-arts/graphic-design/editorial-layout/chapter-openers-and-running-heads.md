---
id: creative-arts.graphic-design.editorial-layout.chapter-openers-and-running-heads
name: chapter-openers-and-running-heads
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, book-design, chapter-openers, running-heads, sinkage, drop-cap, folios, start-on-recto, text-variables, chapter-numbers]
level: practitioner
status: draft
description: "Design book chapter openers and running heads: sinkage, chapter number and title styles, first-paragraph treatment, verso and recto running head content, and folio placement."
sources:
  - https://www.chicagomanualofstyle.org/book/ed18/part1/ch01/toc.html
  - https://helpx.adobe.com/indesign/using/text-variables.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chapter openings and running heads

**Goal:** chapters that start with a clear, consistent ceremony, and running heads that tell readers where
they are without competing with the text.

## Chapter opener
- **Start on recto** for formal books (InDesign Paragraph Style > Keep Options > Start Paragraph: On Next
  Odd Page); trade fiction often allows any page to save paper.
- **Sinkage:** text begins lower than on normal pages, a fixed number of lines (e.g. 8-12 lines down);
  keep it identical on every opener and on the baseline grid.
- Elements: chapter number (word, numeral or ornament), title, optional epigraph, then the first paragraph.
- **First paragraph:** no indent (flush left), with a drop cap, raised initial, or the first words in small
  caps (InDesign nested style: small caps through first line or first 3 words).
- No running head on openers; folio often dropped to the foot or omitted.

## Running heads
- Convention (Chicago): verso shows the **book or part title**, recto the **chapter title**; in reference and
  multi-author books, verso chapter title and recto section heading or author.
- Use InDesign **text variables** (Running Header - Paragraph Style: Chapter Title) on parent pages so the
  head updates from the text.
- Set small: same size as body or smaller, in small caps or italic, tracked caps if all caps, with space
  above the text block equal to whole lines.
- Folios: outer corners (top or bottom) for easy flipping; can share the line with the running head.

## Parent pages
- `A-Text` with running heads and folios; `B-Opener` with none, applied to chapter openers.
- A script or the Start Paragraph rule plus parent page application keeps it consistent in long books.

## Gotchas
- Running heads longer than half the measure: use a shortened title (ask the editor for short titles).
- Blank versos before a recto opener should be truly blank (no running head or folio).
- Text variable runs heads from the first occurrence on a page; check pages where a new chapter title appears
  mid-page (unusual in books, common in reports).

## Verify
- [ ] Every opener has identical sinkage and treatment; no running heads on openers or blank pages.
- [ ] Running heads correct on every spread after final reflow.
