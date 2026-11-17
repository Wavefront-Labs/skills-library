---
id: creative-arts.graphic-design.lettering-and-calligraphy.drawing-glyphs-in-a-font-editor
name: drawing-glyphs-in-a-font-editor
category: creative-arts
field: graphic-design
product: lettering-and-calligraphy
tags: [graphic-design, lettering-and-calligraphy, glyphs-app, fontforge, type-design-basics, font-metrics, font-editor, extrema, glyph-drawing]
level: advanced
status: draft
description: "Draw glyphs in a font editor (Glyphs or FontForge): set units per em and metrics, draw with few nodes at extrema, handle overshoot and components, and check outlines."
sources:
  - https://glyphsapp.com/
  - https://fontforge.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Drawing glyphs in a font editor

**Tools:** **Glyphs** (a commercial macOS app) and **FontForge** (free, open-source, cross-platform). The workflow is similar in either; consult the product manual for menus.

## 1. Set up the font
- **Units per em:** 1000 is a common choice for PostScript-flavoured fonts (FontForge defaults to 1000 for PostScript outlines and 2048 for TrueType); choose one and keep it.
- **Vertical metrics:** baseline (0), x-height, cap height, ascender, descender; set guidelines and alignment zones for them.
- Set family and style names early; they affect export.

## 2. Draw a few key letters first
- Start with a **control set** (for lower case: n, o, then h, u, e; for caps: H, O) and decide stem widths, contrast, curve style, terminals, serifs.
- Draw on-curve points at **extrema** (the horizontal and vertical extremes of curves) with handles horizontal or vertical; use as few points as possible. In FontForge: **Element > Add Extrema**; Glyphs has an equivalent command.
- **Overshoot:** round letters (o, c, e) extend slightly above and below the baseline and x-height or cap height lines so they look the same height as flat letters; set the alignment zones to handle it.
- Keep the stroke weight uniform: vertical stems and horizontal strokes differ in thickness on purpose (horizontals usually slightly thinner).

## 3. Use components
Build accented letters from base letters and accent components (so changes propagate); keep consistent anchor names for accent placement.

## 4. Clean outlines
- Remove overlaps (FontForge: **Element > Overlap > Remove Overlap**) for final TrueType output (some editors remove overlaps at export).
- Check path direction (TrueType and PostScript expect opposite conventions; the editor corrects on export), no tiny segments, no open contours, and no extremely sharp nodes.
- Run the application's validation or outline checks (FontForge: **Element > Find Problems**; Glyphs has its own validation and preview tools).

## 5. Test early
Use a text preview with sample words (for example "nonsense", "handgloves") to evaluate shapes together, not letter by letter.

## Failure modes
- Points not at extrema causing uneven curves and bad hinting or rendering.
- Different overshoots between letters.
- Late changes to metrics.
