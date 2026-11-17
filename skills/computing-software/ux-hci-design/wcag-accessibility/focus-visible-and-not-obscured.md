---
id: computing-software.ux-hci-design.wcag-accessibility.focus-visible-and-not-obscured
name: focus-visible-and-not-obscured
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [focus-visible, focus-not-obscured]
level: practitioner
status: docs-checked
description: "Provide a visible focus indicator (2.4.7) and ensure sticky headers do not cover the focused element (2.4.11 in WCAG 2.2)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
  - https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Focus visibility
- 2.4.7 Focus Visible (Level AA): the keyboard focus indicator must be visible. Removing or hiding the indicator with styling or script is a failure (F55, F78).
- 2.4.11 Focus Not Obscured (Minimum) (Level AA): a focused component must not be entirely hidden by author-created content such as sticky content. CSS `scroll-padding` can un-obscure content (technique C43).
- 2.4.13 Focus Appearance is Level AAA and covers size and shape of a consistent, visible indicator.
```css
:focus-visible { outline: 3px solid #1a56db; outline-offset: 2px; }
html { scroll-padding-top: 4rem; }
```

## Verify
- [ ] Tab through the page with a sticky header; each focused item is visible.

## Checked

- Date: 2026-11-09.
- Confirmed against Understanding SC 2.4.7 Focus Visible and Understanding SC 2.4.11 Focus Not Obscured (Minimum): levels, "entirely hidden", sticky content, C43 scroll-padding, F55/F78, the AAA level of 2.4.13. Pages were searched for these claims rather than read line by line.
- Removed: "new in 2.2" wording, the 3:1 and minimum-area detail for 2.4.13, the claim that cookie banners are named, and the instruction to set scroll-padding equal to header height (the CSS below is only an example).

Method: documentation only; no commands were run.
