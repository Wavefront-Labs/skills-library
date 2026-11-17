---
id: computing-software.web-development.responsive-design.responsive-data-tables
name: responsive-data-tables
category: computing-software
field: web-development
product: responsive-design
tags: [responsive-components, responsive-tables, data-tables, overflow, accessibility]
level: practitioner
status: verified
description: "Making data tables usable on small screens: scrollable wrappers with accessible focus, sticky first columns, priority columns, stacked card layouts that keep semantics."
sources:
  - https://adrianroselli.com/2020/11/under-engineered-responsive-tables.html
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Element/table
  - https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responsive data tables

WCAG 1.4.10 Reflow exempts content that needs two-dimensional layout (the Understanding page lists data tables, not individual cells), and says a table in its own scrollable container lets the rest of the page reflow, but users still need to read them at 320px.

## 1. Default: scroll the table, not the page
```html
<div class="table-scroll" role="region" aria-labelledby="cap-orders" tabindex="0">
  <table><caption id="cap-orders">Recent orders</caption>…</table>
</div>
```
```css
.table-scroll { overflow-x: auto; max-inline-size: 100%; }
.table-scroll:focus-visible { outline: 3px solid var(--focus); }
th:first-child, td:first-child { position: sticky; inset-inline-start: 0; background: var(--surface); }
```
- `tabindex="0"` + `role="region"` + a name makes the scroller keyboard-reachable and announced (run in Chromium 156: aria snapshot `region "Recent orders"`, and ArrowRight scrolled the focused wrapper by 40px).
- A sticky first column keeps row context while scrolling horizontally (run: after `scrollLeft = 200` the first `th` stayed at x=8, the body margin).

## 2. Reduce columns
- Hide low-priority columns at narrow widths behind a "Columns" toggle - never silently drop data users need.
- Combine columns (date + status in one cell) on small screens.

## 3. Stacked "card" layout
```css
@media (width < 40rem) {
  .stack table, .stack tbody, .stack tr, .stack td { display: block; }
  .stack thead { position: absolute; clip-path: inset(50%); width: 1px; height: 1px; overflow: hidden; }
  .stack td::before { content: attr(data-label) ": "; font-weight: 600; }
}
```
**Caveat:** changing `display` on table elements can remove table semantics in some browser and version combinations (Chromium 156 kept `table`, `rowgroup`, `row`, `cell` and `columnheader` in its accessibility tree after the `display: block` rules above; other browsers not run, so test with a screen reader). Re-add ARIA roles (`role="table"`, `rowgroup`, `row`, `cell`, `columnheader`) on the elements when you do this, or render a separate list markup for mobile. Stacked layouts suit record lists (orders, contacts), not comparison tables.

## 4. Alternatives
Summary table + drill-down detail page; charts for trends; let users download CSV.

## Verify
At 320px CSS width (or 400% zoom of 1280), no page-level horizontal scroll; screen reader still announces headers per cell; keyboard can scroll the region.
