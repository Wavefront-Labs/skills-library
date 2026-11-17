---
id: creative-arts.design-for-form-and-experience.design-systems.setting-a-baseline-grid-and-vertical-rhythm
name: setting-a-baseline-grid-and-vertical-rhythm
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [baseline-grid, vertical-rhythm, line-height-grid, baseline-rhythm, typographic-grid, spacing-rhythm]
level: practitioner
status: draft
description: "Set a baseline grid and vertical rhythm: choose a base unit, snap line heights and spacing to multiples, and know when a strict baseline is not worth it on the web."
sources:
  - "Robert Bringhurst, The Elements of Typographic Style"
  - "MDN Web Docs (developer.mozilla.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Baseline grid and vertical rhythm

A baseline grid is a set of equally spaced horizontal lines that text sits on. Vertical rhythm is the consistent spacing of lines and blocks along the vertical axis.

## Steps
1. **Choose a base unit,** commonly 4 or 8 px for UI, or a body line height (such as 24 px for 16 px text) for editorial layouts.
2. **Set line heights as multiples:** body 16/24, small 14/20, h3 20/28, h2 24/32 (UI scales usually use 4 px steps).
3. **Spacing between blocks** as multiples of the unit (see `...design-systems.defining-a-spacing-scale`).
4. **Use unitless `line-height`** in CSS so it scales with font size; for rhythm, set values per style token instead.
5. **Align images and components** to the grid by heights that are multiples.
6. **Check optical alignment:** fonts have differing metrics, so cap-height and baseline may not sit on grid lines without adjusting.
7. **Tools:** a grid overlay in Figma (layout grid with rows) or a CSS background gradient overlay in dev.

## Practical note
On dynamic web content (variable text length, user font-size changes, images) a strict baseline grid is hard to maintain; most teams keep a consistent spacing scale and line-height tokens, and use a strict baseline only in print-like or fixed layouts. Newer CSS features for trimming font leading (text-box-trim) have uneven browser support, so verify before relying on them.

## Verify
- [ ] All line heights and spacings are multiples of the base unit.
- [ ] Two columns of text align across rows where intended.
- [ ] The scheme still works at 200 percent zoom.
