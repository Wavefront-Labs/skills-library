---
id: computing-software.web-development.web-accessibility.multiple-ways-headings-and-labels
name: multiple-ways-headings-and-labels
category: computing-software
field: web-development
product: web-accessibility
tags: [navigable, wcag-navigable, multiple-ways, headings-and-labels, wcag-2-4-5, wcag-2-4-6, site-search, sitemap, breadcrumbs, heading-structure]
level: practitioner
status: docs-checked
description: "Meeting WCAG 2.4.5 Multiple Ways and 2.4.6 Headings and Labels: search, sitemap, nav and breadcrumbs, and descriptive headings/labels people can scan."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/multiple-ways.html
  - https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html
  - https://www.w3.org/WAI/tutorials/page-structure/headings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple ways, headings and labels

**Goal:** users can find pages more than one way, and headings/labels describe their content well enough to navigate by them.

## 1. Multiple ways (2.4.5, AA)
Provide at least two ways to reach the same content (for example navigation, search, a sitemap). Exception: a page that is the result of, or a step in, a process (checkout step 3).

Breadcrumb markup:
```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/docs">Docs</a></li>
    <li><a href="/docs/forms" aria-current="page">Forms</a></li>
  </ol>
</nav>
```
Search: a search landmark containing a labelled input.

## 2. Headings (2.4.6, AA)
- Headings describe the section ("Shipping address", not "Section 2"); one `<h1>` describing the page is the common convention.
- Don't skip levels for visual size (`h2` -> `h4`); style with classes. Skipped levels confuse navigation.
- Visual headings should be real heading elements; don't use headings for non-heading text that just needs to be big.
- Screen reader users navigate by headings.

## 3. Labels
Form labels and button text describe purpose: "Search products", "Add to basket", not "Submit"/"Go"/"OK" repeated. Unique labels for repeated controls ("Remove Blue T-shirt" via hidden text or `aria-label` that starts with the visible "Remove").

## Verify
- [ ] The headings outline reads like a table of contents.
- [ ] At least two ways to reach each content page.
- [ ] No duplicate generic button labels in one view.

## Checked
2026-10-28 Confirmed on W3C Understanding SC 2.4.5 (at least two options for reaching content; exception for a page that is the result of or a step in a process) and SC 2.4.6 (headings and labels describe topic or purpose). Removed: the WebAIM percentage, the list of ways, SC 1.3.1 reference, search element claim, named heading-outline tooling.
Method: documentation only; no commands were run.
