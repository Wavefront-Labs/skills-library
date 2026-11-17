---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-search-and-autocomplete
name: designing-search-and-autocomplete
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [search-ux, autocomplete, search-suggestions, typeahead, site-search, zero-results, query-suggestions]
level: practitioner
status: draft
description: "Design search UX: a visible wide search box, autocomplete suggestions with keyboard support, forgiving matching, useful results pages, filters and zero-results recovery."
sources:
  - "Nielsen Norman Group - Search topic (nngroup.com/topic/search)"
  - "Baymard Institute - Autocomplete Suggestions and Search UX (baymard.com/blog/autocomplete-design)"
  - "W3C WAI-ARIA Authoring Practices - Combobox pattern (w3.org/WAI/ARIA/apg/patterns/combobox)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Search and autocomplete

**Goal:** people find items quickly, even with typos, vague queries and no matches.

## Search box
- **Visible,** as an open field with a magnifier button (not an icon only), at top centre or top right, wide enough for about 27 characters (NN/g); same on every page; Enter submits; keep the query in the box on results.

## Autocomplete (typeahead)
1. Start at **2-3 characters;** debounce 100-250 ms; show **5-10** suggestions (about 8 on desktop, fewer on mobile).
2. Suggestions: popular queries, recent searches, matching categories and products with thumbnails where scanning helps; **bold the completion** (not the typed text); show category scopes ("in Shoes").
3. **Keyboard:** Up/Down moves highlight, Enter selects, Esc closes; Tab/Right arrow accepts a completion; the typed text remains editable.
4. **Accessibility:** ARIA combobox pattern: `role="combobox"`, `aria-expanded`, `aria-controls`, `aria-activedescendant`, results in a `listbox`, announce result count politely.
5. Do not auto-submit or replace what the user typed; handle IME composition.

## Matching
Typo tolerance (edit distance), stemming, synonyms, plural and unit handling, and diacritics; rank by popularity and relevance; let users search by SKU or exact phrases.

## Results page
Query echoed, result count, relevant filters and sorting (`creative-arts.design-for-form-and-experience.interaction-design.designing-filtering-and-sorting`), spelling suggestion ("Showing results for ..."), good snippets.

## Zero results
Never a dead end: suggest corrections, broader queries, popular items, contact help; log zero-result queries and review monthly.

## Verify
- [ ] Wide visible search box; keyboard-operable autocomplete with ARIA.
- [ ] Typos and synonyms handled; zero-result queries tracked.
