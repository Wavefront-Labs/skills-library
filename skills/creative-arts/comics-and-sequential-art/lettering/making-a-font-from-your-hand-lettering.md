---
id: creative-arts.comics-and-sequential-art.lettering.making-a-font-from-your-hand-lettering
name: making-a-font-from-your-hand-lettering
category: creative-arts
field: comics-and-sequential-art
product: lettering
tags: [lettering, lettering-fonts, comic-fonts, custom-lettering-font, handwriting-font, fontforge, glyphs-app, calligraphr, opentype-features]
level: advanced
status: draft
description: "Turn your hand lettering into a comic font: template sheets, scanning and vectorising, spacing and kerning, crossbar I mapping, bold italic, alternates, and testing in balloons."
sources:
  - https://fontforge.org/en-US/documentation/
  - https://www.calligraphr.com/en/
  - https://blambot.com/pages/comic-book-grammar-tradition
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Making a font from your hand lettering

**Goal:** a personal comic font that keeps your hand-lettered look with digital
speed.

## Tools
- Template services (e.g. Calligraphr) for quick handwriting fonts from scanned sheets.
- Full font editors: FontForge (free), Glyphs (macOS), FontLab, for control over
  spacing, kerning and OpenType features.

## Steps
1. **Letter a glyph set** on guidelines at a consistent size (e.g. cap height ~1 cm on
   paper): A-Z, crossbar I and plain I, 0-9, punctuation (. , ! ? ' " - -- ... ( ) : ;
   & @ #), accented letters if needed. Do 2-3 versions of common letters for
   alternates.
2. Scan at 600-1200 dpi, threshold to clean black and white.
3. Import/vectorise (auto-trace in the editor or Illustrator, then clean nodes).
4. **Metrics**: consistent cap height, baseline; set sidebearings so spacing reads even
   in all caps.
5. **Kerning**: fix common pairs (AV, LT, TA, WA, quotes after letters).
6. **Crossbar I mapping**: put crossbar I on uppercase I and plain I on lowercase i,
   or use contextual alternates (see the crossbar I skill).
7. **Bold italic**: letter a separate set with a bolder pen and slant, or derive and
   correct; auto-emboldening usually looks wrong.
8. **Alternates**: add contextual alternates (calt) cycling letter versions so doubles
   vary.
9. Export OTF; install; test.

## Testing
Letter a full page of dialogue at print size; look for uneven spacing, letters that
stand out, missing glyphs.

## Verify
- [ ] Full glyph set incl. bold italic and punctuation.
- [ ] Spacing even in a test page; key kern pairs fixed.
- [ ] Crossbar I behaviour correct.
