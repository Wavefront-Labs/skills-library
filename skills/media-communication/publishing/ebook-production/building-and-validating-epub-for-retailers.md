---
id: media-communication.publishing.ebook-production.building-and-validating-epub-for-retailers
name: building-and-validating-epub-for-retailers
category: media-communication
field: publishing
product: ebook-production
tags: [ebook-production, ebook, epub, epub3, reflowable, fixed-layout, sigil, calibre, epubcheck, ace-by-daisy, accessibility, kindle, kindle-previewer, kdp, kpf, apple-books, kobo, google-play-books, nav-document, opf, xhtml, css, metadata, alt-text, ebook-conversion, publishing, digital-publishing]
level: practitioner
status: docs-checked
description: "Build an EPUB 3 package that follows the W3C spec, passes EPUBCheck and Ace accessibility checks, and carries the required metadata before you deliver it to retailers."
sources:
  - https://www.w3.org/TR/epub-33/
  - https://www.w3.org/TR/epub-a11y-11/
  - https://github.com/w3c/epubcheck
  - https://daisy.github.io/ace/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building and validating EPUB for retailers

**Goal:** one clean EPUB 3 file that validates, carries its required metadata, and meets
the accessibility metadata rules before it goes to any retailer.

## 1. Know the format
An EPUB is a ZIP (OCF container). Per EPUB 3.3:
- The `mimetype` file must be the first file in the ZIP and must not be compressed or encrypted.
- `META-INF/container.xml` is required and identifies the package document(s).
- The package document holds metadata, a manifest of resources and a spine (reading order).
- The publication must contain an EPUB navigation document.
- Fixed-layout content is designated `pre-paginated` in the package document.

## 2. Required package metadata
The package metadata must contain `dc:title`, `dc:identifier` and `dc:language`. Retailers
add their own listing requirements: read each retailer's current upload guide.

## 3. Accessibility metadata (EPUB Accessibility 1.1)
- Must include `accessMode`, `accessibilityFeature` and `accessibilityHazard`.
- Should include `accessibilitySummary` and `accessModeSufficient`.
- If the publication includes page navigation (for example mapped to a print edition),
  it must include a page list.
- Legal accessibility obligations for the markets you sell in: check them yourself.

## 4. Validate
- **EPUBCheck** is the conformance checker for EPUB; it runs as a command-line tool or Java
  library and is maintained by the DAISY Consortium on behalf of W3C. Fix every error.
  Follow the install and run instructions on its project page.
- **Ace by DAISY** is an accessibility checker for EPUB and produces HTML and JSON reports.
- Also open the file in the reading systems you target; rendering differs, and each
  retailer documents its own preview and upload process.

## Verify
- [ ] `mimetype` first and stored uncompressed; `container.xml` present.
- [ ] `dc:title`, `dc:identifier`, `dc:language` present.
- [ ] Navigation document present; spine order matches the book.
- [ ] Required accessibility metadata present; page list included if page navigation is.
- [ ] EPUBCheck reports no errors; Ace report reviewed.

## Checked
2026-11-01. Confirmed in the EPUB 3.3 spec (sections on OCF ZIP container, package document, required metadata, navigation document, fixed layout), the EPUB Accessibility 1.1 spec (required/recommended metadata, page list), the EPUBCheck project page and the Ace project page. Removed: authoring-tool steps (InDesign, Calibre, Pandoc, Sigil), CSS and image advice, file-size and royalty remarks, Kindle Previewer and retailer specifics, the EU accessibility act date, alt-text requirement wording and the command line, none of which those pages state.
Method: documentation only; no commands were run.
