---
id: creative-arts.graphic-design.typography.opentype-features
name: opentype-features
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, opentype, opentype-features, stylistic-sets, contextual-alternates, fractions, ordinals, swashes, case-sensitive-forms, font-feature-settings, indesign, css]
level: practitioner
status: draft
description: "Use OpenType features (stylistic sets, alternates, fractions, ordinals, swashes, case forms) in InDesign, Illustrator and CSS, and check font support."
sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/featurelist
  - https://helpx.adobe.com/indesign/using/using-fonts.html
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OpenType features

**Goal:** use the typographic extras a professional font already contains instead of faking them.

## Common features (tag - what it does)
| Tag | Feature | Use |
|---|---|---|
| `liga` | standard ligatures (fi, fl) | on by default for text |
| `dlig` | discretionary ligatures (ct, st) | display only, period flavour |
| `calt` | contextual alternates | script fonts connecting naturally |
| `ss01`-`ss20` | stylistic sets | e.g. single-storey a, alternate R; brand looks |
| `salt` | stylistic alternates | one-off glyph swaps |
| `swsh` | swashes | display initials/terminals |
| `frac` | fractions | 1/2 -> proper fraction |
| `ordn` | ordinals | 1st, 2nd, No |
| `sups`/`subs` | true superscript/subscript | footnote refs, chemistry |
| `case` | case-sensitive forms | hyphens, brackets raised for ALL CAPS |
| `smcp`/`c2sc` | small caps / caps to small caps | see small caps skill |
| `lnum`/`onum`/`tnum`/`pnum` | figure styles | see figures skill |
| `zero` | slashed zero | codes, data |

## Find what a font supports
- InDesign/Illustrator: select text, Character panel menu > **OpenType** - unsupported
  features are in brackets. The **Glyphs panel** (Show: Alternates for Selection) shows
  alternates per glyph; a small triangle on a glyph means alternates exist.
- Web: wakamaifondue.com or the font's specimen; `fc-query` / FontDrop for desktop files.

## Applying
- **InDesign:** Character panel > OpenType menu; or select a word and pick from the on-canvas
  alternates widget. Put features in **character/paragraph styles** (Basic Character Formats
  > OpenType Features) so they are consistent and survive edits.
- **Illustrator:** Window > Type > OpenType panel; on-canvas alternates on selection.
- **CSS:** prefer high-level properties: `font-variant-numeric: tabular-nums;`,
  `font-variant-caps: small-caps;`, `font-variant-ligatures: discretionary-ligatures;`. Use
  `font-feature-settings: "ss01" 1, "zero" 1;` for the rest (it overrides earlier declarations
  entirely, so repeat all features in one declaration).

## Gotchas
- Stylistic set numbers mean different things in each font - read the specimen.
- Fonts subset for the web may drop features; check the subset includes the GSUB features you use.
- `case` matters in all-caps headings: hyphens and parentheses otherwise sit too low.

## Verify
- [ ] Fractions, ordinals, all-caps punctuation use real glyphs (zoom in to check).
- [ ] Features applied via styles (InDesign) or CSS classes, not one-off overrides.
