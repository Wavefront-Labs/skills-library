---
id: creative-arts.design-for-form-and-experience.interaction-design.balancing-whitespace-and-information-density
name: balancing-whitespace-and-information-density
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [information-density, whitespace, negative-space, density, visual-hierarchy, ui-layout, data-density]
level: practitioner
status: draft
description: "Balance whitespace and information density: choose density per audience and task, use space to group and focus, and keep expert screens compact without clutter."
sources:
  - "Edward Tufte, The Visual Display of Quantitative Information (Graphics Press, 1983), data-ink ratio"
  - "Material Design 3 - Density (m3.material.io/foundations/layout/understanding-layout/density)"
  - "Nielsen Norman Group - Whitespace and Visual Design articles (nngroup.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Whitespace and information density

**Goal:** the right amount of content per screen for the user and task: not sparse for experts, not cluttered for novices.

## Decide density
- **Task and audience:** experts in dense tools (trading, admin, IDEs) scan many items and want compact rows; consumer or occasional tasks want fewer items with more air.
- **Context:** dense on desktop, with larger touch targets on touch (minimum 44x44 pt iOS, 48x48 dp Android), so density modes are limited by input type.

## Use space as structure
- **Macro whitespace** (margins, between sections) separates groups and gives focus; **micro whitespace** (line height 1.4-1.6 for body, padding inside controls) governs legibility.
- Remove borders and fills before adding space; grouping by proximity does the work (see `creative-arts.design-for-form-and-experience.interaction-design.grouping-with-gestalt-principles`).
- Do not delete content to look clean if users need it to decide; use **progressive disclosure** instead.

## Density modes
Offer **comfortable / compact** (list rows 48 vs 36 px, table rows 52 vs 36 vs 28). Implement as tokens (spacing, row height, icon size) that switch by mode; persist the choice.

## Check
- Squint test for clear hierarchy; zoom to 200 percent for reflow.
- Time-to-find tests on a dense screen vs a spacious one for real tasks.
- Measure scroll depth and error rate; sparse pages that force excess scrolling can hurt.

## Verify
- [ ] Density chosen from user and task evidence.
- [ ] Touch targets meet minimums at every density.
- [ ] Hierarchy remains clear when blurred.
