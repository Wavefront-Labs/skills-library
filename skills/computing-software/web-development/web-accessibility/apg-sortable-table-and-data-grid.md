---
id: computing-software.web-development.web-accessibility.apg-sortable-table-and-data-grid
name: apg-sortable-table-and-data-grid
category: computing-software
field: web-development
product: web-accessibility
tags: [aria-patterns, sortable-table, data-grid-pattern, aria-sort, wai-aria-apg]
level: practitioner
status: docs-checked
description: "Making sortable tables accessible with buttons in headers and aria-sort, and knowing when an interactive data grid (role=grid) is warranted and how its keyboard model works."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/table/examples/sortable-table/
  - https://www.w3.org/WAI/ARIA/apg/patterns/grid/
  - https://www.w3.org/TR/wai-aria-1.2/#aria-sort
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sortable tables and data grids

## 1. Sortable table (most cases)
Keep a native `<table>`; put a **button** in each sortable header; reflect state with `aria-sort` on the `<th>`.
```html
<th scope="col" aria-sort="ascending">
  <button type="button">Date <svg aria-hidden="true" class="sort-icon">…</svg></button>
</th>
<th scope="col"><button type="button">Amount</button></th>
```
- `aria-sort` values: `ascending`, `descending`, `none`, `other` (ARIA 1.2 token list). Authors should apply it to only one header at a time.
- The button's name is the column name; state comes from `aria-sort` (don't put "sorted ascending" in the label too).
- After sorting, optionally announce "Sorted by Date, ascending" via a polite live region; test whether your target screen readers announce the aria-sort change on the focused button.
- Keep focus on the activated header button.
- Visual indicator must not rely on colour; show direction arrows.
- A caption can say that column headers with buttons are sortable, for discoverability.

## 2. When to use `role="grid"`
Only for interactive, spreadsheet-like widgets where cells contain controls or are editable and users navigate cell by cell: data grids with inline editing, selection of rows/cells, calendars. Grid turns the table into a single Tab stop with arrow-key navigation - a static data table made into a grid becomes harder to read for screen reader users (they lose table-reading shortcuts in browse mode).

## 3. Grid keyboard model (APG)
- Arrow keys move between cells; Home/End go to the first/last cell in the row; Ctrl+Home/End go to the first/last cell in the grid; Page Up/Down move by a page of rows (see the APG grid pattern for the full table).
- Enter (and F2 in editable grids) enters a cell to interact with its widget; Escape returns to cell navigation.
- Roving tabindex or `aria-activedescendant` for the active cell; `aria-rowcount`/`aria-rowindex` for virtualised rows; `aria-selected` for selection; `aria-readonly`.

## 4. Libraries
Whatever library you choose, test virtualised grids carefully: rows that are not rendered do not exist in the DOM, so set `aria-rowcount` and `aria-rowindex`.

## Verify
Screen reader announces the column header with its button and sort state; table navigation commands still work for sortable tables; grids pass APG keyboard checks.

## Checked

2026-10-26, against WCAG 2.2 / APG as of 2026-10-26 (w3c repos). Confirmed: ARIA 1.2 aria-sort tokens (ascending, descending, none, other) and the advice to apply it to one header at a time; the APG table page recommends native table elements, aria-sort on the sorted header and states that a table's widgets are separate Tab stops while a grid is a composite widget. The APG grid pattern confirms arrows, Home/End, Ctrl+Home/End (optional), Page Up/Down (optional), Enter and F2 entering a cell, Escape restoring grid navigation, and a single Tab stop for the grid. Removed library names and the NVDA shortcut.

Method: documentation only; no commands were run.
