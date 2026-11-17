---
id: creative-arts.literary-writing.novel-writing.ebook-formatting-epub
name: ebook-formatting-epub
category: creative-arts
field: literary-writing
product: novel-writing
tags: [literary-writing, novel-writing, self-publishing, ebook-formatting, epub, epub3, epubcheck, pandoc, navigation-document, dublin-core]
level: practitioner
status: docs-checked
description: "Produce a valid EPUB 3 for a novel: clean source, Pandoc conversion with TOC, cover and CSS, required package metadata, and EPUBCheck validation."
sources: ["https://www.w3.org/TR/epub-33/", "https://www.w3.org/publishing/epubcheck/", "https://pandoc.org/MANUAL.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Formatting an ebook (EPUB)

**Goal:** an EPUB 3 that validates and carries the metadata and navigation readers need.

## 1. Clean the source (general practice)
Use paragraph styles rather than manual formatting; no tabs or blank lines for spacing.
Consistent smart quotes, dashes and ellipses.

## 2. Convert with Pandoc
```bash
pandoc book.md -o book.epub --toc --epub-cover-image=cover.jpg --css=book.css --metadata title="Title"
```
- `--toc` adds a table of contents; `--toc-depth=NUMBER` sets its depth.
- `--epub-cover-image=FILE` sets the cover. `--css=URL` replaces Pandoc's default
  `epub.css` styling (see it with `pandoc --print-default-data-file epub.css`).
- `--epub-embed-font=FILE` embeds a font (repeatable); add matching `@font-face`
  declarations to your CSS.
- `--split-level=NUMBER` sets the heading level at which the EPUB is split into files
  (default: level-1 headings; only internal composition, not what readers see). Use 2
  or 3 for large documents with few level-1 headings. `--epub-chapter-level` is a
  deprecated synonym.
- Metadata: Pandoc writes `dc:title`, `dc:creator`, `dc:date`, `dc:language` (from `lang`,
  else locale) and a random-UUID `dc:identifier`. Override any with `--epub-metadata=FILE`
  (XML of Dublin Core elements) or YAML metadata.

## 3. What the EPUB 3.3 spec requires
- The package document MUST contain `dc:title`, `dc:identifier` and `dc:language`, plus
  the `dcterms:modified` property. Other metadata is optional.
- The `unique-identifier` attribute on the package points at the `dc:identifier` that
  is the primary identifier.
- An EPUB publication MUST contain an EPUB navigation document conforming to section 7
  of the spec.

## 4. Validate with EPUBCheck
`epubcheck book.epub` checks a file against the EPUB specifications (EPUB 2 and 3); a
clean run reports "No errors or warnings detected!". It is an open-source (MIT) W3C
project maintained by the DAISY Consortium, distributed as a command-line tool or Java
library.

## Verify
- [ ] Title, identifier, language and modified date present.
- [ ] Navigation document lists every chapter.
- [ ] EPUBCheck reports no errors.

## Checked
2026-11-09. Confirmed against the Pandoc manual (options and metadata defaults), the
W3C EPUB 3.3 spec (required metadata, navigation document, unique identifier) and the
EPUBCheck page (usage, scope, licence). The EPUBCheck page was a short landing page.
Removed because not on pages read: Vellum, Atticus, Kindle Create, Sigil and Calibre
claims, KDP cover ratio and retailer acceptance claims, CSS and dark-mode advice,
front-matter and sample advice, Kindle Previewer guidance. The KDP help source was dropped
as unread.
Method: documentation only; no commands were run.
