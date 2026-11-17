---
id: creative-arts.graphic-design.lettering-and-calligraphy.font-spacing-and-kerning
name: font-spacing-and-kerning
category: creative-arts
field: graphic-design
product: lettering-and-calligraphy
tags: [graphic-design, lettering-and-calligraphy, font-spacing, kerning, sidebearings, spacing-strings, kerning-classes, font-metrics-spacing]
level: advanced
status: draft
description: "Space and kern a font: set sidebearings with control strings, space lowercase before caps, judge optical space, then add kerning pairs and classes sparingly."
sources:
  - https://glyphsapp.com/
  - https://fontforge.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spacing and kerning a font

**Goal:** even typographic colour in running text, with spacing set before kerning.

## 1. Spacing before kerning
- **Spacing** sets the left and right **sidebearings** of each glyph. Do it before adding kerning; kerning corrects exceptions, not a poor spacing system.
- Start with a few reference letters: for lower case, **n** (stems) and **o** (rounds); work out sidebearings of n, then o, then others by their shapes: straight sides take n-like bearings, rounds take o-like bearings, diagonals less.
- Use **control strings** to compare: for example `nnnonnonoooo` and `HHOHOOHH`, repeated in each glyph pair context, then real words.

## 2. Compose and link
- Use **metrics keys or linked sidebearings** (in Glyphs: for example `=n` for the left sidebearing of another glyph) so related glyphs, such as accented or similar shapes, inherit values; in FontForge use the Metrics window.
- Accented glyphs inherit spacing from base letters.

## 3. Judge optically
- Aim for even white area between letters, not equal gaps; round-round tighter than straight-straight (the pairs "oo" versus "nn").
- View at text and display sizes, in black on white and white on black; print a proof.

## 4. Kerning
1. Identify problem pairs: caps with diagonals (AV, AT, LT, TA, VA, Yo), punctuation after caps, and lower-case pairs like "ry", "r." and "f-".
2. Prefer **kerning classes (groups)** so that a pair value applies to families of glyphs (A and its accented forms), with exceptions for single pairs; build groups on the left and right sides consistently.
3. Check negative and positive kerns; keep values modest, and test in sentences of real text.
4. Add kerning to the font's **kern** feature (in OpenType); in complex fonts GPOS handles it.

## 5. Test
Use a text editor and a browser at real sizes; check with a set of test words and the alphabet in pairs; compare with fonts you admire.

## Failure modes
- Spacing patched with pair kerns for everything.
- Kerning applied before the glyph shapes are final.
- Too many one-off pairs.
