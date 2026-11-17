---
id: creative-arts.graphic-design.typography.letterform-anatomy
name: letterform-anatomy
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, type-anatomy, letterform-anatomy, x-height, cap-height, ascender, descender, baseline, counter, aperture, terminal, serif, stroke-contrast, stress, overshoot]
level: intro
status: draft
description: "Read letterforms by their anatomy (x-height, counters, apertures, terminals, stress, contrast) and use those features to predict legibility, apparent size and fit for a job."
sources:
  - https://learn.microsoft.com/en-us/typography/develop/character-design-standards/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Letterform anatomy

**Goal:** look at a typeface and know, from its parts, how it will behave at text size,
at a distance, on screen and in print.

## The vertical metrics
- **Baseline** - where letters sit. **x-height** - height of lowercase without ascenders.
- **Cap height** - height of flat capitals (H). **Ascender** (b, d, h) usually rises above cap height.
- **Descender** (p, g, y) - below baseline.
- **Overshoot** - round letters (o, O) and pointed ones (A, V apex) extend slightly past the
  baseline/x-height so they *look* the same size as flat letters.

**Why it matters:** a typeface with a large x-height (Verdana, Helvetica) looks bigger at the
same point size than a small x-height face (Garamond). Compare by x-height, not point size.

## Counters and apertures
- **Counter** - enclosed or partly enclosed space (o, e, a). Big counters survive small sizes,
  low-res screens and ink spread.
- **Aperture** - the opening of c, e, a, s. **Open apertures** (Frutiger, Source Sans) keep
  letters distinct at distance and small size; closed apertures (Helvetica) look tidy at
  display size but c/e/o blur together. Signage and UI favour open apertures.

## Strokes
- **Contrast** - difference between thick and thin strokes. High contrast (Didot, Bodoni) is
  elegant large, but thin strokes break up small, in low-res, or reversed out of colour.
- **Stress / axis** - angle of the thinnest parts of round letters: diagonal (humanist,
  calligraphic origin) or vertical (rational/modern).
- **Serif** types: bracketed, unbracketed (hairline), slab. **Terminal** - end of a stroke without
  a serif (ball, teardrop, flat, angled).
- **Spine** (S), **bowl** (b, p), **shoulder** (n, h), **ear** (g), **link/loop** (two-storey g),
  **crossbar**, **stem**, **tail**, **spur**.

## Distinguishing similar glyphs
Check **Il1**, **O0**, **rn vs m**, **a vs o** at small size: important for codes, UI, signage, forms.

## Use it
- Body text at small size / on screen: moderate x-height, open apertures, low-to-medium contrast.
- Reversed text (white on dark): increase weight slightly, avoid hairline serifs.
- Display: high contrast and tight apertures are fine and can add character.

## Verify
- [ ] You can name x-height, aperture and contrast for the candidate typefaces.
- [ ] Il1 / O0 / rn tests done when the text contains codes or the context needs it.
