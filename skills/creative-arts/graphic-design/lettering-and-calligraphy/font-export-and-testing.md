---
id: creative-arts.graphic-design.lettering-and-calligraphy.font-export-and-testing
name: font-export-and-testing
category: creative-arts
field: graphic-design
product: lettering-and-calligraphy
tags: [graphic-design, lettering-and-calligraphy, font-export, font-testing, otf-ttf, woff2, font-validation, fontbakery, font-licence]
level: advanced
status: draft
description: "Export and test a font: generate OTF or TTF, set name and embedding fields, validate with checkers, test in apps and browsers, make WOFF2, and pick a licence."
sources:
  - https://glyphsapp.com/
  - https://fontforge.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Font export and testing

**Goal:** a font file that installs everywhere, shows the right names and works in print and on the web.

## 1. Pre-export checklist
- Final outlines (overlaps removed, correct direction, extremes added), spacing and kerning finished, glyph set complete for target languages (Latin diacritics, punctuation, numerals).
- Names: family name, style name, version, copyright and licence strings, designer, and unique ID set correctly. Style linking (Regular, Italic, Bold, Bold Italic) must follow the usual convention so apps group styles properly.
- Vertical metrics set, line gap decided, so line spacing is consistent across operating systems.

## 2. Export
- **Glyphs:** **File > Export** (or the Export dialog), choose OTF (PostScript outlines) or TTF (TrueType outlines) and Web fonts as needed; the exported fonts are written to the folder you choose.
- **FontForge:** **File > Generate Fonts**, choose OpenType (CFF) or TrueType, and review the generation options; check validation messages.
- Interpolated families export from masters with consistent names.
- Variable fonts need a separate variable export setup (Glyphs and fontmake or similar can generate them).

## 3. Validate
- Run a font QA tool such as **Font Bakery** (open source, used by Google Fonts) or the validators in your editor, and fix reported errors.
- Check naming and OS/2 table fields (including embedding permissions, `fsType`).
- Check outlines for overlaps, missing extremes, and curves.

## 4. Test in context
- Install the font; test in a design application, a word processor, and several browsers on more than one OS. Check ligatures, kerning, accents and line spacing.
- Compare text at 10-12 px, 16 px and display sizes; at small sizes light hinting or autohinting may show problems.
- Print a proof sheet.

## 5. Web versions
- Make **WOFF2** (compressed) for the web: fontTools can save a font with flavor woff2 (requires the brotli module), or use the WOFF2 tools. Provide WOFF as legacy fallback only if needed.
- Subset to needed characters for performance; keep the licence text.

## 6. Licence
Choose and document a licence: proprietary EULA, or an open licence such as the SIL Open Font License. Licensing a typeface and protecting its name has legal aspects; seek legal advice before distribution or sale.

## Self-check
Fresh install on a clean system, no errors in the validator, correct names in font menus, and text displays correctly in at least three applications.
