---
id: computing-software.web-development.responsive-design.responsive-svg-and-charts
name: responsive-svg-and-charts
category: computing-software
field: web-development
product: responsive-design
tags: [responsive-svg, responsive-charts, viewbox, preserveaspectratio, data-visualisation]
level: practitioner
status: verified
description: "Making SVG graphics and charts responsive: viewBox and preserveAspectRatio, scaling vs re-rendering, readable text and strokes, mobile chart layouts and accessible fallbacks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/viewBox
  - https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/preserveAspectRatio
  - https://css-tricks.com/scale-svg/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responsive SVG and charts

## 1. viewBox scaling
```html
<svg viewBox="0 0 600 300" role="img" aria-labelledby="t">
  <title id="t">Revenue by quarter, 2025</title> ...
</svg>
```
```css
svg { inline-size: 100%; block-size: auto; }   /* height follows the viewBox ratio */
```
- Omit `width`/`height` attributes (or keep them for CLS and override with CSS) so the SVG fills its container.
- `preserveAspectRatio="xMidYMid meet"` (default) letterboxes; `slice` crops like `object-fit: cover`; `none` stretches (only for decorative backgrounds). Run (viewBox 600x300 in a 300x300 box): `meet` drew the content 300x150 at y 75, `slice` 600x300 at x -150, `none` 300x300.
- An `<svg>` with no `viewBox`, `width` or `height` falls back to 300x150 (run in Chromium 156), and one in a container with `height: 0` renders 0px tall: give the container a size or `aspect-ratio`. With a `viewBox` and `inline-size: 100%`, the height followed the 2:1 ratio in block, flex and grid parents (300x150 in a 300px parent, 200x100 in a 200px grid column).

## 2. Scaling vs re-rendering
Pure viewBox scaling shrinks everything: on a phone, 12px axis labels become 5px. For charts:
- Re-render at the real container width using `ResizeObserver`, keeping font sizes in CSS px.
- Reduce tick count with width (d3 `scale.ticks(width / 80)`; d3-scale returned 7 ticks for `ticks(4)` over 0-1200, so the count is approximate), shorten labels (`Jan` not `January`, `1.2k`), rotate or drop alternate labels.
- `vector-effect="non-scaling-stroke"` keeps line widths constant when scaled. Run: a 4-unit stroke at 4x scale measured 16px, and 4px with `non-scaling-stroke`.

## 3. Mobile chart patterns
- Swap orientation: horizontal bar charts read better on narrow screens than vertical bars with crowded labels.
- Replace legends with direct labels at line ends.
- Offer a "view as table" toggle; for very wide time series, horizontal scroll inside an `overflow-x: auto` region with a sticky y-axis.
- Touch: tooltips on tap with larger hit areas (invisible wider `<path>` or Voronoi overlay), not hover only.

## 4. Text and CSS inside SVG
Inline SVG accepts CSS and `currentColor`, so charts follow dark mode: `stroke: var(--series-1)`. `<img src="chart.svg">` can't be styled from the page and can't use page fonts.

## 5. Accessibility
`role="img"` + `<title>`/`aria-labelledby` summary for static charts; for interactive charts, a data table alternative and keyboard focus on data points.

## Verify
- [ ] At 320px width labels remain at least ~11px and legible; no horizontal page overflow; chart follows theme colours; table alternative available.
