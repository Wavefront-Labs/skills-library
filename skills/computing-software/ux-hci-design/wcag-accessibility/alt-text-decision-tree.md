---
id: computing-software.ux-hci-design.wcag-accessibility.alt-text-decision-tree
name: alt-text-decision-tree
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [alt-text-decision-tree, img-alt-attribute, wcag-text-alternatives]
level: practitioner
status: docs-checked
description: "Decide between informative, decorative, functional and complex images and write the matching alt text."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html
  - https://www.w3.org/WAI/tutorials/images/decision-tree/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alt text by image purpose (SC 1.1.1, Level A)
- **Informative**: short alt conveying the same information.
- **Decorative**: `alt=""` (empty, not missing) so screen readers skip it; or CSS background.
- **Functional** (link/button image): alt describes the action/destination ("Search"), not the picture.
- **Text in image**: alt repeats the text.
- **Complex** (chart, diagram): short alt naming it, plus long description nearby or linked.

## Gotchas
- Use an empty `alt` attribute for decorative images and for images whose content is redundant to nearby text; follow the W3C decision tree.

## Verify
- [ ] Each `<img>` has an `alt` attribute; decorative ones have an empty `alt`.

## Checked

- Date: 2026-11-02.
- Confirmed against the W3C WAI images decision tree and Understanding SC 1.1.1 Non-text Content (Level A): empty `alt` for decorative images, CSS backgrounds as an alternative, text in images, functional images, charts with a short alternative plus a description.
- Removed: screen reader file-name behaviour, the "image of" advice and the SVG role/aria-hidden specifics (not stated on those pages).

Method: documentation only; no commands were run.
