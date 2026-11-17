---
id: computing-software.ux-hci-design.wcag-accessibility.semantic-html-structure
name: semantic-html-structure
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [semantic-html, info-and-relationships, wcag-adaptable]
level: practitioner
status: docs-checked
description: "Use headings, lists, tables, landmarks and form labels so structure is programmatically determinable."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Semantic structure (SC 1.3.1, A)
Information, structure and relationships conveyed through presentation must be programmatically determinable or available in text. Techniques the page lists as sufficient where the technology provides semantics:
- Headings with `h1` to `h6` (H42).
- Landmarks (ARIA11) and named regions: `aria-labelledby` to name regions and landmarks (ARIA13).
- Real lists with `ol`, `ul`, `dl` (H48).
- Data tables with table markup (H51), a `caption` (H39), and `scope` or `id`/`headers` to associate header cells (H63, H43).
- Labels via `label` elements (H44); related controls grouped with `fieldset` and `legend` (H71).
- Where the technology cannot express a relationship, put a text description near it, for example "all required fields are marked with an asterisk (*)".
- Colour values need not be programmatically determined; SC 1.4.1 covers colour.

## Verify
- [ ] A screen reader's headings and landmarks lists give a sensible outline; table headers and form labels are announced with their cells and controls.

## Checked

2026-11-09. Confirmed on the Understanding SC 1.3.1 page: the criterion and Level A, the sufficient techniques H42, ARIA11, ARIA13, H48, H51, H39, H63, H43, H44, H71, the text-description fallback and the colour note. Removed: the single-h1 and no-skipped-levels rules, the aria-label advice for repeated landmarks, and the first-rule-of-ARIA line, which this page does not state.

Method: documentation only; no commands were run.
