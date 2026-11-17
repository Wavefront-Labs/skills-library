---
id: creative-arts.design-for-form-and-experience.interaction-design.sizing-touch-targets
name: sizing-touch-targets
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [touch-target-size, touch-targets, tap-target-size, wcag-target-size, mobile-usability, target-spacing]
level: practitioner
status: docs-checked
description: "Size and space touch targets: WCAG 2.2 minimum 24 by 24 CSS pixels and 44 by 44 enhanced, spacing, and the extended hit area technique."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
  - https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Touch target sizing

Related: `...interaction-design.applying-fitts-law`.

## Numbers
- **WCAG 2.2 SC 2.5.8 Target Size (Minimum), level AA:** pointer targets at least 24 by 24 CSS pixels, with exceptions (spacing so a 24 CSS pixel circle centred on an undersized target does not intersect another target; inline targets in a sentence or block of text; an equivalent control elsewhere; user-agent default size; essential).
- **WCAG SC 2.5.5 Target Size (Enhanced), level AAA:** at least 44 by 44 CSS pixels, with equivalent, inline, user-agent and essential exceptions.
- Platform guidelines (Apple, Material) set their own minimum sizes; read the current version of each before quoting a figure.

## Practice
1. Make the **hit area** larger than the visible icon with padding or a pseudo-element; do not rely on tiny icons alone.
2. **Space targets:** more room between destructive and safe actions; avoid close adjacent small targets, in lists and toolbars.
3. **Place controls for thumbs:** frequent actions in the lower area; avoid tiny controls near screen edges where system gestures act.
4. **Text links:** line height and padding increase hit area; set the size of icon-only buttons.
5. **Test** on real devices with large and small hands, and with users with motor impairments or tremor.

## Verify
- [ ] Each interactive element has a hit area of at least 24 CSS px (target 44).
- [ ] Adjacent targets are separated or enlarged.
- [ ] Hit areas do not overlap.

## Checked
2026-11-01. Confirmed against the W3C Understanding pages for SC 2.5.8 (level AA) and SC 2.5.5 (level AAA): the 24 and 44 CSS pixel sizes, the level of each, and the exception list. Removed: the Apple 44 point and Material 48 dp figures (those sites could not be read).
Method: documentation only; no commands were run.
