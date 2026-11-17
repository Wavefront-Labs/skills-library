---
id: computing-software.ux-hci-design.wcag-accessibility.use-of-colour-and-text-resize
name: use-of-colour-and-text-resize
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [use-of-colour, reflow-320px]
level: practitioner
status: docs-checked
description: "Pair colour with another cue, allow 200% text resize and reflow at 320 CSS px without two-dimensional scrolling."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
  - https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
  - https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 1.4.1, 1.4.4, 1.4.10
- 1.4.1 (A): colour is not the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element.
- 1.4.4 (AA): text can be resized without assistive technology up to 200 percent without loss of content or functionality.
- 1.4.10 (AA): vertically scrolling content works at a width equivalent to 320 CSS pixels (1280 CSS pixels wide at 400% zoom) without requiring two-dimensional scrolling, except for parts that need two-dimensional layout for usage or meaning, such as maps or data tables. The exception applies only to that section of content.

## Verify
- [ ] Zoom to 400% on a 1280px viewport; no two-dimensional scrolling or loss of content.

## Checked

- Date: 2026-11-09.
- Confirmed against Understanding SC 1.4.1 Use of Color (Level A), SC 1.4.4 Resize Text (Level AA) and SC 1.4.10 Reflow (Level AA): the criterion wording, 200 percent, 320 CSS pixels, the 1280 px at 400% equivalence and the two-dimensional layout exception. Pages were searched for these claims rather than read line by line.
- Removed: the link underline / 3:1 rule, relative-unit advice and `user-scalable=no` (not stated on the cited pages).

Method: documentation only; no commands were run.
