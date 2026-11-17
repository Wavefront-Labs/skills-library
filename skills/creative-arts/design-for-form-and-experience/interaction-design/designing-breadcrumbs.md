---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-breadcrumbs
name: designing-breadcrumbs
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [breadcrumbs, breadcrumb-navigation, location-indicator, navigation-design, site-hierarchy, wayfinding-digital]
level: practitioner
status: draft
description: "Design breadcrumbs: location-based trails for hierarchical sites, correct separators and truncation, current page not linked, mobile treatment and accessible markup."
sources:
  - "Nielsen Norman Group - Breadcrumbs: 11 Design Guidelines for Desktop and Mobile (nngroup.com/articles/breadcrumbs)"
  - "W3C WAI-ARIA Authoring Practices - Breadcrumb pattern (w3.org/WAI/ARIA/apg/patterns/breadcrumb)"
  - "GOV.UK Design System - Breadcrumbs (design-system.service.gov.uk/components/breadcrumbs)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Breadcrumbs

**Goal:** show where the page sits in the hierarchy and give a one-click path to ancestors. They supplement, never replace, primary navigation.

## When to use
Deep hierarchies (e-commerce categories, docs, large content sites) and users arriving from search. Not needed for flat sites or linear flows (wizards use steppers).

## Types
**Location** (hierarchy path, the default and best), attribute (shared attributes of a product), and history-based (avoid; the browser Back covers it).

## Design rules
1. Place **above the page title, top left,** below the global navigation, in small text.
2. Order from top-level to current: `Home > Shoes > Running shoes > Model X`.
3. **Separator** a chevron or ">" (visual only, not read out by screen readers).
4. Every ancestor is a **link;** the current page is plain text (optionally `aria-current="page"`).
5. **Use the real hierarchy** with the same names as page titles and nav labels; products in multiple categories follow the path the user came by or the primary category.
6. **Mobile:** show only the parent link ("< Running shoes") or truncate middle items with an ellipsis menu; keep targets at least 44 px high.
7. Do not add the current page title twice; keep all on one line where possible.

## Markup
```html
<nav aria-label="Breadcrumb"><ol>
  <li><a href="/">Home</a></li>
  <li><a href="/shoes">Shoes</a></li>
  <li aria-current="page">Model X</li>
</ol></nav>
```
Add `BreadcrumbList` JSON-LD for search results.

## Verify
- [ ] Trail matches the real hierarchy and nav labels.
- [ ] Ancestors link, current page does not; accessible nav markup.
- [ ] Mobile variant tested for target size.
