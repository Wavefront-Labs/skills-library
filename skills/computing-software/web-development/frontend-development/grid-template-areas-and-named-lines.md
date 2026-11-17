---
id: computing-software.web-development.frontend-development.grid-template-areas-and-named-lines
name: grid-template-areas-and-named-lines
category: computing-software
field: web-development
product: frontend-development
tags: [css-grid, grid-template-areas, named-lines, page-layout, css]
level: practitioner
status: docs-checked
description: "Laying out pages with grid-template-areas and named lines: readable ASCII layouts, responsive area rearrangement, implicit line names, and accessibility of visual reordering."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/grid-template-areas
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Grid_template_areas
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Named_grid_lines
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/reading-flow
  - https://www.w3.org/TR/css-grid-2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# grid-template-areas and named lines

## 1. Areas
```css
.layout {
  display: grid;
  grid-template-columns: 16rem minmax(0, 1fr);
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header"
    "nav    main"
    "footer footer";
  min-height: 100svh;
  gap: 1rem;
}
.header { grid-area: header; } .nav { grid-area: nav; } .main { grid-area: main; } .footer { grid-area: footer; }

@media (width < 48rem) {
  .layout { grid-template-columns: 1fr; grid-template-areas: "header" "main" "nav" "footer"; }
}
```
- Areas must be rectangles; a `.` marks an empty cell. Each row string needs the same number of cells or the declaration is invalid.

## 2. Named lines
```css
.article {
  display: grid;
  grid-template-columns: [full-start] minmax(1rem, 1fr) [content-start] minmax(0, 65ch) [content-end] minmax(1rem, 1fr) [full-end];
}
.article > * { grid-column: content; }
.article > .bleed { grid-column: full; }      /* full-width images */
```
`content-start`/`content-end` lines create an implicit `content` area name; areas likewise create `header-start`/`header-end` line names.

## 3. Accessibility of reordering
Grid can place items anywhere, but screen readers and keyboard focus follow DOM order. Moving `nav` after `main` visually while it comes first in DOM is fine if reading order still makes sense; moving interactive items so Tab jumps around the screen fails WCAG 1.3.2 / 2.4.3. Reorder the DOM when the logical order changes. (`reading-flow` is supported only from Chrome 137 per browser-compat-data.)

## 4. Pitfalls
- `1fr` columns have `min-width: auto` - wide content blows them out; use `minmax(0, 1fr)`.
- Items without an area auto-place into remaining cells, often creating unexpected implicit rows.

## Verify
DevTools grid overlay with "Show area names" and "Show line names"; Tab through at each breakpoint.

## Checked

Checked 2026-10-26 against current documentation. MDN grid-template-areas guide (same cell count per row, `.` for empty cells, rectangular areas), named-grid-lines guide (`-start`/`-end` implicit names) and `reading-flow` support (Chrome 137 only).

Method: documentation only; no commands were run.
