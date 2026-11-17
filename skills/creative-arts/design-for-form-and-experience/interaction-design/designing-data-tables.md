---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-data-tables
name: designing-data-tables
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [data-table-design, data-tables, table-design, dashboard-design, sortable-tables, filtering-and-sorting, tabular-data]
level: practitioner
status: draft
description: "Design data tables: align by type, sensible columns, sortable headers, density, sticky headers, selection and row actions, pagination or virtualisation, with accessible markup."
sources:
  - "Nielsen Norman Group - Data Tables: Four Major User Tasks (nngroup.com/articles/data-tables)"
  - "Pencil and Paper - Data Table Design UX Patterns and Best Practices (pencilandpaper.io/articles/ux-pattern-analysis-enterprise-data-tables)"
  - "W3C WAI Tables Tutorial (w3.org/WAI/tutorials/tables)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data table design

**Goal:** users can find, compare, sort and act on rows quickly.

## Tasks to support (NN/g)
Find a specific row, **compare** rows, **view/edit** a row's details, and **act** on rows (bulk). Design for the dominant task.

## Columns and cells
- Order columns by importance; the identifier (name) first; fewer columns beats horizontal scroll (hide or allow column chooser).
- **Alignment:** text left; numbers right with tabular figures (`creative-arts.design-for-form-and-experience.interaction-design.using-tabular-figures-for-numbers`); headers align with data; dates and statuses consistent in format and width.
- **Truncate** long text with a tooltip or expand (`creative-arts.design-for-form-and-experience.interaction-design.handling-text-truncation-and-overflow`); show units in headers.
- Status as badge with text and icon, not colour alone.

## Rows and density
Compact 32-40 px for experts, default 48 px, comfortable 56 px; zebra stripes or row dividers (not both heavy); row hover highlight; sticky header, and sticky first column when scrolling horizontally.

## Interaction
- **Sort** by clicking header (arrow indicator, `aria-sort`); default sort meaningful; multi-sort for experts.
- **Filter and search** (`creative-arts.design-for-form-and-experience.interaction-design.designing-filtering-and-sorting`).
- **Selection:** checkbox column, select all with "select all N" for paged data, bulk action bar appears with count.
- **Row actions:** primary action by clicking the row or name; secondary in an overflow menu at row end; destructive confirmations.
- **Pagination vs infinite scroll vs virtualisation:** pagination (10-100 per page) when users compare or return to position; virtualise rows for thousands.
- Empty, loading, error states designed.

## Accessibility
Real `<table>`, `<th scope="col">`, `<caption>`; keyboard access to sort buttons; avoid `div` tables; for grid editing use ARIA grid pattern carefully.

## Verify
- [ ] Alignment, sorting, and sticky header correct; selection and bulk actions work.
- [ ] Semantic markup with captions and sort state exposed.
