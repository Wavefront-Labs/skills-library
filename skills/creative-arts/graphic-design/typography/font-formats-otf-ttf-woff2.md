---
id: creative-arts.graphic-design.typography.font-formats-otf-ttf-woff2
name: font-formats-otf-ttf-woff2
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, opentype, font-management, font-formats, woff2, woff, otf, ttf, cff, truetype-outlines, variable-font-files, subsetting, type-1-end-of-support]
level: practitioner
status: draft
description: "Know font file formats: OTF (CFF) vs TTF outlines, WOFF/WOFF2 for the web, variable font files, collections, subsetting, and retiring PostScript Type 1."
sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/
  - https://www.w3.org/TR/WOFF2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Font formats: OTF, TTF, WOFF2

**Goal:** the right font file for each use, and no surprises from obsolete formats.

## Desktop formats
- **OpenType (.otf / .ttf)**: one cross-platform format with two outline flavours:
  - **CFF/PostScript outlines** (usually `.otf`): cubic curves; common from type foundries' print lines.
  - **TrueType outlines** (usually `.ttf`): quadratic curves; strong hinting for screens; most system and variable fonts.
  Both support full OpenType features (ligatures, figures, small caps) - the extension does not limit features.
- **TrueType Collection (.ttc/.otc):** several fonts in one file (system fonts).
- **Variable fonts:** one file containing axes (weight, width, optical size, slant) - usually `.ttf`; named instances
  appear in font menus (see variable fonts skill).
- **PostScript Type 1** (.pfb/.pfm, .lwfn): **unsupported** in Adobe Creative Cloud apps since January 2023; documents
  using them show missing fonts. Replace with OpenType versions (metrics may differ - check reflow).

## Web formats
- **WOFF2**: compressed OpenType (Brotli), ~30% smaller than WOFF; supported by all modern browsers. Serve only WOFF2
  for modern projects.
- WOFF: older compressed format; fallback for very old browsers only.
- Do not serve raw TTF/OTF on the web (bigger, sometimes licence-prohibited).
- Convert with the foundry's webfont kit (licence permitting) or tools like `fonttools` (`pyftsubset`, `--flavor=woff2`).

## Subsetting
Remove unused glyphs (e.g. keep Latin only) to shrink files: `pyftsubset Font.ttf --unicodes="U+0000-00FF,U+2000-206F"
--layout-features='*' --flavor=woff2`. Keep `--layout-features='*'` so OpenType features survive. Use `unicode-range`
in CSS to load subsets on demand. Check the licence permits modification/subsetting.

## Gotchas
- Same family name installed as OTF and TTF = duplicates in menus and mismatched metrics; keep one.
- Fonts from Adobe Fonts or Google Fonts APIs are delivered in optimised formats automatically.
- PDF embedding uses the outline flavour; PDF/X requires embeddable fonts (fsType permissions).

## Verify
- [ ] No Type 1 fonts in active projects; one format per family installed.
- [ ] Web fonts served as WOFF2, subset appropriately, with features intact.
