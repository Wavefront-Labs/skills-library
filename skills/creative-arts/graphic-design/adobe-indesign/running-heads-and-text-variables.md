---
id: creative-arts.graphic-design.adobe-indesign.running-heads-and-text-variables
name: running-heads-and-text-variables
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, parent-pages, running-heads, text-variables, running-header-paragraph-style, chapter-number-variable, file-name-variable, output-date, dictionary-headers]
level: practitioner
status: draft
description: "Automate InDesign running heads with text variables: Running Header from paragraph or character styles, chapter numbers, file name and dates in the slug."
sources:
  - https://helpx.adobe.com/indesign/using/text-variables.html
  - https://helpx.adobe.com/indesign/using/creating-running-headers-footers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running heads and text variables

**Goal:** headers and footers that always show the current chapter or section title without manual typing.

## Running Header variable (Type > Text Variables > Define)
1. **New** > Type: **Running Header (Paragraph Style)** (or Character Style for a short form).
2. **Style:** the style to pick up, e.g. `Chapter Title` or `H1`.
3. **Use:** First on Page or **Last on Page** (dictionaries use both: first entry on left page, last on right).
4. Options: Delete End Punctuation; Change Case (Upper/Lower/Title/Sentence).
5. Text Before/After (e.g. a tab or em space).
6. Insert into a text frame on the **parent page**: Type > Text Variables > Insert Variable.

The header updates on every page from the nearest matching paragraph. If a page has no such paragraph,
it carries over the last one from earlier pages.

## Short running heads
Long chapter titles do not fit in a header: create a hidden/minimal paragraph style (e.g. `Running
Head Text`) or use a **character style** applied to a short part of the title, and base the variable on it.
Some designers put a non-printing text frame with the short title on each chapter opener, styled with the
target style.

## Other useful variables
- **Chapter Number** (with Book panel numbering) for `Chapter 3` labels and figure numbering.
- **File Name**, **Output Date**, **Modification Date** in the slug for proofs (see bleed and slug skill).
- **Custom Text** for repeated phrases (product name that may change).
- **Last Page Number** for "Page 3 of 12" (Section or Document scope).
- **Metadata Caption** for image captions (see live captions skill).

## Gotchas
- Variables do not break across lines - a long header will compress horizontally. Keep them short or use
  Change Case and short-form styles.
- Variables are text; converting to text (Type > Text Variables > Convert Variable to Text) freezes them.
- Recto/verso headers often differ (book title on left, chapter on right): use separate frames on the left
  and right parent pages.

## Verify
- [ ] Flick through the document: every running head matches the content of its page.
- [ ] No compressed (squashed) variable text; slug info updates on output.
