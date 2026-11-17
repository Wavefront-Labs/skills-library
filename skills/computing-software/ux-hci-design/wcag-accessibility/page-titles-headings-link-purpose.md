---
id: computing-software.ux-hci-design.wcag-accessibility.page-titles-headings-link-purpose
name: page-titles-headings-link-purpose
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [page-titled, link-purpose, wcag-navigable]
level: practitioner
status: docs-checked
description: "Use descriptive page titles and link text whose purpose can be determined in context (SC 2.4.2, 2.4.4)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html
  - https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Titles and links
- 2.4.2 Page Titled (Level A): web pages have titles that describe topic or purpose.
- 2.4.4 Link Purpose (In Context) (Level A): the purpose of each link can be determined from the link text alone, or from the link text together with its programmatically determined link context, except where the purpose would be ambiguous to users in general.
- Techniques for adding context: `aria-labelledby` (ARIA7) or `aria-label` (ARIA8) for link purpose, and the `title` attribute to supplement link text (H33).
- Links with the same destination should use consistent text.

## Verify
- [ ] Screen reader links list is meaningful.

## Checked

- Date: 2026-11-09.
- Confirmed against Understanding SC 2.4.2 Page Titled and Understanding SC 2.4.4 Link Purpose (In Context) (both Level A): criterion wording, link context, ARIA7/ARIA8/H33, consistent text for the same destination. The pages were searched for these claims rather than read line by line.
- Removed: SC 2.4.6 and headings advice, title uniqueness and ordering advice, the example link text with file size, visually hidden text and SPA `document.title` guidance (not on the cited pages).

Method: documentation only; no commands were run.
