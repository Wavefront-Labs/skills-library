---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-filtering-and-sorting
name: designing-filtering-and-sorting
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [filtering-and-sorting, faceted-filters, faceted-search, filters, sort-order, product-listing, data-display]
level: practitioner
status: draft
description: "Design filtering and sorting: facets by user attributes, immediate vs apply updates, applied-filter chips with counts, clear-all, sorting defaults and mobile filter sheets."
sources:
  - "Nielsen Norman Group - Filters vs Facets: Definitions and Design (nngroup.com/articles/filter-categories-values)"
  - "Baymard Institute - Product List Filtering and Sorting UX (baymard.com/blog/ecommerce-product-lists)"
  - "Material Design 3 - Chips: filter chips (m3.material.io/components/chips)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Filtering and sorting

**Goal:** users narrow a large set to what they need and understand the result.

## Filters
- **Choose facets** from user attributes and top tasks (price, size, brand, status, date), ordered by usefulness; show counts for options when cheap, and **hide or disable zero-result options**.
- **Control types:** checkboxes (multi-select within a facet = OR), radio or segmented (single), range sliders with number inputs (price), search within long lists, date range pickers; keep facet groups collapsible.
- **Across facets AND, within a facet OR,** and state that clearly.
- **Immediate vs apply:** desktop sidebars update results immediately; on mobile use a filter sheet with an **Apply (shows result count)** button; for expensive queries, use apply.
- **Applied filters visible** above results as removable chips, with **Clear all**; persist across navigation and in the URL (shareable, Back-button safe).
- Show result count and update announcements (`aria-live`).

## Sorting
- Meaningful **default** (relevance for search, newest for feeds, name for lists); common options: relevance, price low to high and reverse, rating, date; label the current sort; sort and filters should be independent controls.
- Table sorting by column (`creative-arts.design-for-form-and-experience.interaction-design.designing-data-tables`).

## Edge cases
Zero results: show which filters caused it with one-click removal; avoid dead-end combinations; mobile: sticky filter and sort button with active-filter count badge; remember last settings for app lists.

## Verify
- [ ] Facets match user needs; applied filters visible, removable, in URL.
- [ ] Results count and zero-result handling work.
- [ ] Mobile filter sheet has apply and clear.
