---
id: computing-software.web-development.frontend-development.css-containment-and-content-visibility
name: css-containment-and-content-visibility
category: computing-software
field: web-development
product: frontend-development
tags: [css-containment, contain-property, content-visibility, contain-intrinsic-size, rendering-performance, css]
level: advanced
status: docs-checked
description: "Using CSS containment for rendering performance: contain values and their side effects, content-visibility auto with contain-intrinsic-size, accessibility and measuring gains."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/contain
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/content-visibility
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/contain-intrinsic-size
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Using
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Display/Containing_block
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSS containment and content-visibility

## 1. contain values
| Value | Promise to the browser | Side effects |
|---|---|---|
| `layout` | inside layout does not affect outside | new formatting context, containing block for fixed/absolute, stacking context |
| `paint` | descendants never paint outside | clips overflow like `overflow: clip`, containing block, stacking context |
| `size` / `inline-size` | element size does not depend on children | collapses to 0 without explicit size (container queries use inline-size) |
| `style` | counters and quotes are scoped to the element | |
| `content` | = layout paint style | safe default for widgets |
| `strict` | = size layout paint style | needs explicit size |
```css
.widget { contain: content; }    /* changes inside do not trigger page-wide layout */
```

## 2. content-visibility: auto
```css
.feed-item, .article-section {
  content-visibility: auto;
  contain-intrinsic-size: auto 600px;    /* placeholder height; "auto" remembers the last rendered size */
}
```
Off-screen elements skip style, layout and paint until near the viewport. MDN describes this as making initial page load much faster on long pages (docs, feeds, comment threads).
Without `contain-intrinsic-size`, skipped elements are 0 tall and the scrollbar jumps as you scroll.

## 3. Behaviour to know
- With `auto`, skipped content stays available to find-in-page, tab-order navigation, focus and selection. With `hidden`, skipped contents are not accessible to those features, similar to `display: none`.
- `content-visibility: auto` also applies layout, style and paint containment, so the element becomes a containing block for absolute and fixed descendants.
- Paint containment clips box-shadows and dropdowns that extend outside; apply to sections, not to elements containing popovers.
- `contentvisibilityautostatechange` event lets you pause work in skipped sections.

## 4. Measure
Performance panel: record initial load and scroll before/after; compare "Rendering" time and long tasks.

## Verify
- [ ] Rendering time for a long page drops measurably; no scrollbar jumping; Ctrl+F finds text in off-screen sections.

## Checked

Checked 2026-10-26 against current documentation. MDN `contain`, `content-visibility`, `contain-intrinsic-size`, the containment guide and the containing-block guide: `content` and `strict` expansions, side effects of layout/paint containment, `style` containment scope, `auto` versus `hidden` accessibility, the `auto <length>` remembered size and the `contentvisibilityautostatechange` event. Removed the unconfirmed "several-fold" speed-up and the Lighthouse audit reference.

Method: documentation only; no commands were run.
