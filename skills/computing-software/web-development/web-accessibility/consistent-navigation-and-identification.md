---
id: computing-software.web-development.web-accessibility.consistent-navigation-and-identification
name: consistent-navigation-and-identification
category: computing-software
field: web-development
product: web-accessibility
tags: [readable, predictable, consistent-navigation, consistent-identification, wcag-3-2-3, wcag-3-2-4, design-system, icon-labels]
level: practitioner
status: docs-checked
description: "Meeting WCAG 3.2.3 and 3.2.4: navigation in the same relative order across pages and components with the same function labelled consistently."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/consistent-navigation.html
  - https://www.w3.org/WAI/WCAG22/Understanding/consistent-identification.html
  - https://www.w3.org/WAI/WCAG22/Understanding/consistent-help.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consistent navigation and identification

**Goal:** users (especially with cognitive or visual disabilities) learn the site once - navigation stays where it was and the same things have the same names.

## 1. Consistent navigation (3.2.3, AA)
Navigation mechanisms repeated on multiple pages (header nav, footer links, sidebar, search, skip link) appear in the **same relative order** each time.
- Adding items is fine (a sub-nav for a section); reordering existing ones per page is not.
- Users may change the order themselves (adaptive user agents or preferences); the criterion concerns the order the author provides.
- Use shared layout components (one header component) so it can't drift.

## 2. Consistent identification (3.2.4, AA)
Components with the same function across the site are identified consistently:
- The criterion covers components repeated across a set of pages that provide the same functionality.
- The Understanding document encourages the same label or text alternative for the same function (a magnifier named "Search" everywhere), but says identical labels are not strictly required as long as users can still recognise the function.
- Same function doesn't mean identical text in every context: "Download report (PDF)" vs "Download invoice (PDF)" is fine - consistent pattern.

## 3. Practical controls
- A design system with labelled icon components (`<Icon name="search" label="Search" />` defaults) and content guidelines (a terminology list).
- Lint/scan: crawl the site and compare accessible names of controls with the same icon/function (axe doesn't test this; manual or custom scripts).

## 4. Related
3.2.6 Consistent Help (Level A, new in WCAG 2.2) is the same idea for help mechanisms.

## Verify
- [ ] Header/footer nav items in the same order on all templates (visual diff of nav across pages).
- [ ] Same-function icons share the same accessible name (Accessibility pane spot checks).
- [ ] Terminology list exists and copy follows it.

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 success criteria and Understanding pages.
- Confirmed: 3.2.3 and 3.2.4 are Level AA; 3.2.6 Consistent Help is Level A and new in 2.2; sub-navigation may be added without breaking "same order"; skip links are an example of a repeated mechanism; users may reorder via their own preferences.
- Corrected: consistent identification does not require identical labels (the skill said identical labels and same link text were required); the same-destination link rule was removed.
Method: documentation only; no commands were run.