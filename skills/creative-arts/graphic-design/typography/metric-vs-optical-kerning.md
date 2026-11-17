---
id: creative-arts.graphic-design.typography.metric-vs-optical-kerning
name: metric-vs-optical-kerning
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, kerning, tracking, metric-kerning, optical-kerning, kerning-pairs, font-kerning, css-font-kerning, mixed-fonts]
level: practitioner
status: draft
description: "Choose metric or optical kerning: when the font's kern pairs are best, when optical rescues poor or mixed fonts, and how to set it in Adobe apps and CSS."
sources:
  - https://helpx.adobe.com/indesign/using/kerning-tracking.html
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-kerning
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Metric vs optical kerning

**Goal:** the right automatic kerning for the font, so manual kerning is only needed in display type.

## What they are
- **Metric** (also "Auto"): uses the font's built-in **kerning pairs** (GPOS `kern`), drawn by the type designer
  for combinations like AV, To, Yo, LT, f.. A well-made font has thousands of pairs.
- **Optical:** the app ignores the font's pairs and calculates spacing from glyph shapes. Adobe apps offer it in
  the Character panel kerning menu.
- **0 / None:** no kerning - only sidebearings. Almost never right except for monospaced or some UI tests.

## When to use which
| Situation | Use |
|---|---|
| Professionally made text font (most commercial and good open-source fonts) | **Metric** |
| Free/amateur font with poor or missing kerning (AV gaps visible) | Optical, then check |
| **Mixed fonts or sizes in one line** (e.g. a symbol font next to text, different fonts in a logo) | Optical (metric pairs exist only within one font) |
| Large display type | Either as a start, then **manual kerning** (see display kerning skill) |
| Script fonts with connecting letters | Metric (optical can break joins) |

Test: set `AVATAR Toyota "Wy` in both and compare at large size.

## Setting
- **InDesign/Illustrator:** Character panel > Kerning: Metrics / Optical / 0. Put it in paragraph styles. Text with
  manual kern values shows the number in parentheses.
- **Photoshop:** same menu in Character panel.
- **CSS:** `font-kerning: normal` (uses the font's kerning, default `auto` usually equals normal for larger text);
  kerning is on by default in modern browsers. There is no optical kerning in CSS.

## Gotchas
- Optical kerning can loosen or tighten overall spacing compared to metric - check line breaks after switching.
- Kerning tables in variable fonts may vary along axes - test at the weight used.
- PDF/print output preserves the kern values chosen in the layout app.

## Verify
- [ ] Problem pairs (AV, To, LT, quotes) look even at final size.
- [ ] Kerning method set in styles, not ad hoc.
