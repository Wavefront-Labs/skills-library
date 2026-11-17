---
id: computing-software.ux-hci-design.wcag-accessibility.multiple-ways-and-consistent-navigation
name: multiple-ways-and-consistent-navigation
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [multiple-ways]
level: practitioner
status: docs-checked
description: "Offer at least two ways to find pages and keep help mechanisms in a consistent order (SC 2.4.5, 3.2.6)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/multiple-ways.html
  - https://www.w3.org/WAI/WCAG22/Understanding/consistent-help.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Findability
- 2.4.5 Multiple Ways (Level AA): more than one way is available to locate a web page within a set of web pages, except where the page is the result of, or a step in, a process. Techniques include a site map (G63) and a search function (G161).
- 3.2.6 Consistent Help (Level A): if a page contains human contact details, a human contact mechanism, a self-help option or a fully automated contact mechanism, and these repeat across multiple pages in a set, they occur in the same order relative to other page content unless the user initiates a change.
- "Same order" is judged on the serialized page order, compared across pages in the same page variation (same zoom level and orientation). Help may be on the page or a direct link to another page.

## Verify
- [ ] Compare page templates: help mechanisms occur in the same order relative to other page content, and each page offers two ways to find it.

## Checked

- Date: 2026-11-09.
- Confirmed against Understanding SC 2.4.5 Multiple Ways (Level AA) and Understanding SC 3.2.6 Consistent Help (Level A): process exception, G63/G161, the four help mechanisms, serialized-order note. The 2.4.5 page was searched for these claims rather than read line by line; the 3.2.6 criterion and notes were read.
- Removed: SC 3.2.3 and 3.2.4 (not on the cited pages), the "new in 2.2" wording and the contact/chat/FAQ examples.

Method: documentation only; no commands were run.
