---
id: creative-arts.graphic-design.typography.type-families-weights-widths-optical-sizes
name: type-families-weights-widths-optical-sizes
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, type-family, optical-sizes, font-weights, font-widths, condensed, italic, opsz, variable-fonts, caption-text-display, style-linking]
level: practitioner
status: draft
description: "Choose within a type family: weights and the 100-900 scale, widths, true italics, and optical sizes (caption, text, display, opsz axis) matched to the setting size."
sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/os2
  - https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxistag_opsz
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type families: weights, widths and optical sizes

**Goal:** pick the right member of a family for each job instead of faking bold, italic or condensed.

## Weights
- Standard numeric scale (OpenType usWeightClass, CSS `font-weight`): 100 Thin, 200 ExtraLight, 300 Light,
  400 Regular, 500 Medium, 600 SemiBold, 700 Bold, 800 ExtraBold, 900 Black.
- Body text: Regular (sometimes Book, 350-450). Reversed text and small sizes on screen: a step heavier.
- Hierarchy: skip at least two steps (400 with 700) for a visible difference; adjacent weights look like
  a mistake.

## Widths
- Condensed and compressed widths fit long headlines and narrow columns; extended for short display words.
- Never horizontally scale type (InDesign horizontal scale, CSS transform): strokes distort. Use a real width.

## Italics and obliques
- True italic: redrawn letterforms (single-storey a, cursive f); oblique: slanted roman (common in sans).
- Synthetic italic and bold (style buttons without a font file) are fakes; browsers do it when the face is
  missing, so load the real files (style linking).

## Optical sizes
- Small sizes need larger x-height, wider spacing, lower contrast and sturdier hairlines; display sizes
  need tighter spacing and more contrast. Families ship **Caption** (6-8 pt), **Text** (9-13 pt),
  **Subhead** and **Display** (24 pt+) cuts, e.g. Minion, Arno, Garamond Premier, Sabon Next.
- Variable fonts with an **opsz** axis adjust automatically. CSS: `font-optical-sizing: auto` (default)
  maps opsz to font size; InDesign applies opsz automatically at the point size.
- Using a display cut for body text makes it look spindly and cramped; using a caption cut large looks
  clumsy and loose.

## Choosing a family for a system
- Check the family has the weights, italics, widths, small caps, figures and languages you need before
  committing (see text-vs-display-type-and-language-support and using-superfamilies skills).

## Gotchas
- Weight names are not standard across foundries (one foundry's Medium is another's Regular); compare visually.
- Licensing may differ per style; budget for the whole family needed.

## Verify
- [ ] No synthetic bold or italic in the output (InDesign: Find Font shows only real styles).
- [ ] Optical size or cut matches setting size for body, captions and display.
