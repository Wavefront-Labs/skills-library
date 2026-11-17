---
id: computing-software.web-development.frontend-development.css-subgrid
name: css-subgrid
category: computing-software
field: web-development
product: frontend-development
tags: [css-grid, subgrid, card-alignment, forms-layout, css]
level: practitioner
status: docs-checked
description: "Aligning nested content across siblings with CSS subgrid: card headings and footers that line up, form label columns, gap inheritance, and fallback for old browsers."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Subgrid
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/grid-template-columns
  - https://www.w3.org/TR/css-grid-2/#subgrids
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subgrid

A grid item can adopt its parent's tracks with `grid-template-rows: subgrid` and/or `grid-template-columns: subgrid`, so grandchildren align across siblings. Baseline since 2023.

## 1. Aligned cards
```css
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(18rem, 100%), 1fr)); gap: 1.5rem; }
.card {
  display: grid;
  grid-row: span 4;                 /* image, title, body, actions */
  grid-template-rows: subgrid;
  row-gap: .75rem;                  /* override the inherited gap if needed */
}
```
Each card's title row is as tall as the tallest title in that row of cards; actions line up at the same height - without fixed heights or JS.

## 2. Form alignment
```css
form { display: grid; grid-template-columns: max-content 1fr; gap: .75rem 1rem; }
.field { display: grid; grid-column: span 2; grid-template-columns: subgrid; }
```
Labels in all fields share one column width, even when each field is its own component wrapper.

## 3. Rules
- The subgridded item must span the number of tracks it needs (`grid-row: span 4`); its children then place into those tracks.
- Gaps inherit from the parent; override with `row-gap`/`column-gap` on the subgrid.
- Line names from the parent are available inside; you can add more: `grid-template-columns: subgrid [a] [b]`.
- Match the span to the content structure: the subgrid has exactly as many tracks as it spans.

## 4. Fallback
```css
@supports not (grid-template-rows: subgrid) { .card { display: flex; flex-direction: column; } .card .actions { margin-top: auto; } }
```

## Verify
DevTools grid overlay shows the "subgrid" badge; cards with different title lengths still align titles, bodies and buttons per row.

## Checked

Checked 2026-10-26 against current documentation. MDN subgrid guide (subgrid takes the tracks it spans, inherited gaps can be overridden, line names pass in and extra names can be declared) and browser-compat-data (Chrome 117, Firefox 71, Safari 16; Baseline 2023). Removed the unconfirmed implicit-track claim.

Method: documentation only; no commands were run.
