---
id: computing-software.web-development.frontend-development.multi-column-layout-and-floats
name: multi-column-layout-and-floats
category: computing-software
field: web-development
product: frontend-development
tags: [multi-column-layout, css-floats, css-columns, shape-outside, css-layout]
level: practitioner
status: docs-checked
description: "Using CSS multi-column layout for flowing text and card lists, and floats for text wrap: column-width, break-inside, column-span, clearing with flow-root, and shape-outside."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Multicol_layout
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/column-fill
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/float
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/shape-outside
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-column layout and floats

Grid and flexbox handle page layout; multicol and floats remain the right tools for two jobs: flowing content into columns and wrapping text around an object.

## 1. Multi-column
```css
.article { columns: 22rem 3; column-gap: 2rem; column-rule: 1px solid #ddd; }  /* width-based, max 3 */
.article h2 { column-span: all; }                     /* full-width heading across columns */
.article figure, .card { break-inside: avoid; }       /* don't split items across columns */
```
- Prefer `column-width` (via `columns: <width> <max-count>`): it is responsive without media queries.
- Content reads top-to-bottom then next column, so for long text on screens it forces scrolling back up. Use for short blocks: footer link lists, tag clouds, glossary terms, print.
- Card lists with `break-inside: avoid` give a cheap masonry look, but order goes down columns, not across rows - wrong when order matters (newest first).
- `column-fill: balance` (the default) evens out column heights; `column-fill: auto` fills columns in sequence and matters when the container has a block size.

## 2. Floats for wrapping
```css
.pullquote { float: inline-start; width: min(40%, 18rem); margin-inline-end: 1.5rem; }
.avatar { float: left; shape-outside: circle(50%); clip-path: circle(50%); margin-right: 1rem; }
```
- Use logical `inline-start/inline-end` so RTL layouts flip.
- `shape-outside` (with an image's alpha: `shape-outside: url(cutout.png); shape-image-threshold: .5`) wraps text around non-rectangular shapes; requires CORS for cross-origin images.

## 3. Containing floats
```css
.media { display: flow-root; }   /* new block formatting context: contains floats, no clearfix hack */
.after { clear: both; }
```
`overflow` other than visible also contains floats but is meant for overflowing content and can add unwanted scrollbars; `flow-root` has no such side effect.

## 4. Do not
Build grids or sidebars with floats (fragile widths, no equal heights) - use grid/flex. Floated items inside a flex/grid container lose their float.

## Verify
- [ ] Columns collapse to one on narrow screens without media queries; no figure split across columns; floats contained without clipping; RTL check flips wrap side.

## Checked
2026-10-26. MDN multicol, column-fill, float, shape-outside and block formatting context pages (main, 2026-10-26): confirmed column-fill auto/balance, break-inside: avoid, float inline-start/inline-end, shape-outside images need CORS headers and use shape-image-threshold, flow-root contains floats without side effects, and overflow-based BFCs can cause unwanted scrollbars. Removed the unconfirmed focus-ring remark.
Method: documentation only; no commands were run.
