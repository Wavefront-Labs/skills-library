---
id: computing-software.ux-hci-design.wcag-accessibility.skip-links-and-bypass-blocks
name: skip-links-and-bypass-blocks
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [skip-link, bypass-blocks]
level: practitioner
status: docs-checked
description: "Provide a skip-to-main-content link or landmarks and headings to bypass repeated blocks (SC 2.4.1)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Skip link
SC 2.4.1 Bypass Blocks (Level A): a mechanism is available to bypass blocks of content that are repeated on multiple web pages.
```html
<a href="#main">Skip to main content</a>
...
<main id="main">
```
- Sufficient techniques include a link at the top of each page that goes directly to the main content area (G1), a link at the start of a repeated block to go to its end (G123), and links at the top to each area of the content (G124).
- Grouping repeated blocks so they can be skipped also works: ARIA landmarks (ARIA11), headings at the start of each section (H69), an expandable and collapsible menu (SCR28).
- A skip link may be unnecessary where navigation links sit at the bottom of the page, since browsers provide keyboard shortcuts to move focus to the top.
- Example from the page: a link above a long list of filters that skips to the product results.

## Verify
- [ ] Keyboard users can reach the skip link or the landmark/heading structure and move past the repeated block in one step.

## Checked

2026-11-09. Confirmed on the Understanding SC 2.4.1 page: the criterion text and Level A, the techniques G1, G123, G124, ARIA11, H69, SCR28, the note about browser shortcuts and the filter example. Removed: the CSS for hiding the link, the "must be first focusable and visible on focus" rule, the tabindex on main, and the claim that landmarks satisfy bypass for all screen reader users, none of which the page states in those terms.

Method: documentation only; no commands were run.
