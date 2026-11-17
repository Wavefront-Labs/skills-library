---
id: creative-arts.graphic-design.editorial-layout.font-embedding-and-subsetting
name: font-embedding-and-subsetting
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, pdf-x, print-ready-pdf, font-embedding, font-subsetting, fstype-permissions, document-properties-fonts, missing-fonts-pdf, outline-fallback]
level: practitioner
status: draft
description: "Make sure print PDFs embed every font: subsetting thresholds, checking Document Properties > Fonts, fonts that forbid embedding (fsType), and fallbacks when a font will not embed."
sources:
  - https://helpx.adobe.com/indesign/using/pdf-options.html
  - https://learn.microsoft.com/en-us/typography/opentype/spec/os2#fstype
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Font embedding and subsetting

**Goal:** a PDF that renders identically on the printer's RIP because every glyph travels inside it.

## Embedding and subsetting
- PDF/X requires all fonts embedded. InDesign/Illustrator export settings: Advanced > **Subset fonts when percent of
  characters used is less than: 100%** - embeds only used glyphs (smaller files) for nearly every font.
- Subsetting is normal and fine for print. For PDFs that will be **edited** later (corrections in Acrobat, form fields),
  full embedding (0% threshold) may be needed and must be allowed by the licence.

## Check the PDF
- Acrobat > File > Properties > **Fonts** tab: every font should show **(Embedded Subset)** or (Embedded). Anything
  without is not embedded - the RIP will substitute.
- Preflight "Fonts not embedded" check (see Acrobat preflight skill).

## Fonts that will not embed
- Each font has **fsType** embedding permissions set by the foundry: Installable, Editable, Print & Preview, or
  **Restricted License** (no embedding). Restricted fonts fail PDF/X export with a warning.
- Options: get a version/licence that allows embedding; replace the font; or, for small amounts of display text,
  **convert to outlines** (InDesign: Type > Create Outlines on a copy; Illustrator) - note licence terms, and that
  outlined text is no longer searchable.
- Placed PDFs/AI files may contain non-embedded fonts - fix them at source before placing.

## Other font issues in PDFs
- Missing font in the source document (pink highlight) exports with a substitute - resolve before export.
- Type 1 fonts are unsupported in current Adobe apps (see font formats skill).
- Very old TrueType fonts with broken tables can rasterise or garble - test proofs.

## Verify
- [ ] Document Properties > Fonts lists every font as embedded or embedded subset.
- [ ] No restricted fonts; outlines only where necessary and licensed.
