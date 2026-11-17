---
id: computing-software.ux-hci-design.wcag-accessibility.target-size-and-pointer-gestures
name: target-size-and-pointer-gestures
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [target-size-minimum, pointer-gestures, wcag-input-modalities]
level: practitioner
status: docs-checked
description: "Make targets at least 24x24 CSS px (2.5.8) and give single-pointer alternatives to path or multipoint gestures."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
  - https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pointer criteria
- 2.5.8 Target Size (Minimum) (Level AA): targets are at least 24 by 24 CSS pixels, or have enough spacing that a 24 CSS pixel circle centred on each undersized target does not intersect another target or another undersized target's circle. Exceptions: an equivalent control elsewhere, inline links in text, size determined by the user agent, and essential presentation.
- 2.5.1 Pointer Gestures (Level A): functionality that uses multipoint or path-based gestures must also work with a single pointer without a path-based gesture, unless the gesture is essential. The single-pointer alternative cannot rely only on dragging (see 2.5.7 Dragging Movements).

## Verify
- [ ] Measure target sizes and spacing; every multipoint or path-based gesture has a single-pointer alternative that is not a drag.

## Checked

- Date: 2026-11-09.
- Confirmed against Understanding SC 2.5.8 Target Size (Minimum) (Level AA) and Understanding SC 2.5.1 Pointer Gestures (Level A): 24 by 24 CSS pixels, the circle spacing test, the four exceptions, the essential exception and the link to 2.5.7. Pages were searched for these claims rather than read line by line.
- Removed: 2.5.5 (44x44), 2.5.2 and the 2.5.7 detail (not covered by the cited pages), "new in 2.2" wording and DevTools.

Method: documentation only; no commands were run.
