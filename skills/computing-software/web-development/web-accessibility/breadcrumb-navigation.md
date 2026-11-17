---
id: computing-software.web-development.web-accessibility.breadcrumb-navigation
name: breadcrumb-navigation
category: computing-software
field: web-development
product: web-accessibility
tags: [breadcrumb-navigation, aria-current, wcag-2-4-8, nav-landmark, breadcrumbs, navigation]
level: practitioner
status: docs-checked
description: "Accessible breadcrumbs: nav landmark with label, ordered list, aria-current for the current page, CSS separators, mobile truncation, structured data and WCAG 2.4.8."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/
  - https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/examples/breadcrumb/
  - https://www.w3.org/WAI/WCAG22/Understanding/location.html
  - https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
  - https://developer.mozilla.org/en-US/docs/Web/CSS/content
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Breadcrumb navigation

## 1. Markup
```html
<nav aria-label="Breadcrumb" class="breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/guides/">Guides</a></li>
    <li><a href="/guides/billing/" aria-current="page">Billing</a></li>
  </ol>
</nav>
```
```css
.breadcrumb ol { display: flex; flex-wrap: wrap; gap: .25rem; list-style: none; padding: 0; }
.breadcrumb li + li::before { content: "/"; margin-inline-end: .25rem; color: #6b7280; }
```
- `nav` with `aria-label="Breadcrumb"` makes a labelled navigation landmark; the label names the type of navigation (APG).
- An ordered list conveys the hierarchical order of the trail.
- `aria-current="page"` on the link to the current page; if the current item is not a link, `aria-current` is optional (APG).
- Separators via CSS (or `aria-hidden` spans) so screen readers do not read "slash" between items. Note: CSS generated content can be read by some screen readers; a pure-CSS border/chevron or `content: "/" / ""` (alt text syntax) avoids it.

## 2. Responsive
Long trails wrap; on small screens show only the parent as "Back to Guides" link, keeping the full trail available in a disclosure if useful.

## 3. Structured data
Google Search reads `BreadcrumbList` structured data (JSON-LD) to categorize page information in results. Use a trail that represents a typical user path to the page rather than mirroring the URL structure.

## 4. WCAG
Breadcrumbs are a listed example for 2.4.8 Location (AAA); they supplement, not replace, primary navigation.

## Verify
- [ ] Screen reader landmark list shows the "Breadcrumb" navigation landmark; current item announced as current page; separators silent.

## Checked

- Date: 2026-10-26. Documentation: ARIA APG breadcrumb pattern and example, WCAG 2.2 Understanding Location, Google breadcrumb structured data page, MDN `content`.
- Confirmed: nav landmark labelled via `aria-label`; ordered list in the APG example; `aria-current="page"` on the current link (optional when not a link); 2.4.8 Location is AAA and names breadcrumb trails; `content: "/" / ""` alternative-text syntax exists; Google uses BreadcrumbList markup and recommends a typical user path.
- Removed or corrected: the "do not include the word navigation" rule, the "list, 3 items" announcement, the Multiple Ways link and the "must match the visible trail" statement.
Method: documentation only; no commands were run.