---
id: computing-software.ux-hci-design.wcag-accessibility.colour-contrast-thresholds
name: colour-contrast-thresholds
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [colour-contrast, contrast-ratio, wcag-distinguishable]
level: practitioner
status: docs-checked
description: "Apply 4.5:1 (3:1 large text) for text and 3:1 for UI components, and compute ratios correctly."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
  - https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Contrast (SC 1.4.3 and 1.4.11)
- 1.4.3 (AA): text and images of text need at least 4.5:1. Large text (at least 18 point, or 14 point bold) needs at least 3:1; 14pt and 18pt are about 18.5px and 24px.
- 1.4.11 Non-text Contrast: visual information needed to identify user interface components and states needs at least 3:1 against adjacent colour(s). The input's adjacent colour is the colour outside the component.
- Exempt from 1.4.3: text in inactive components, pure decoration, text not visible to anyone, and logos or logotypes. Inactive components are also exempt from 1.4.11.
- Ratio = (L1 + 0.05) / (L2 + 0.05) with relative luminance per WCAG definition.

## Gotchas
- Placeholder text and text shown on hover or keyboard focus must also meet 1.4.3.
- The focus indicator must have 3:1 contrast against the adjacent background (1.4.11 with 2.4.7).
- Do not round: 4.499:1 does not meet 4.5:1.
- Brand guidelines do not exempt text beyond logos and logotypes.
- Background images with insufficient contrast behind text are a failure (F83).

## Verify
- [ ] Contrast measured for text and for component boundaries and states (hover, focus, error) using the relative luminance formula (L1 + 0.05) / (L2 + 0.05).

## Checked

- Date: 2026-11-09.
- Confirmed against Understanding SC 1.4.3 Contrast (Minimum) and Understanding SC 1.4.11 Non-text Contrast: thresholds, large-text sizes and pixel equivalents, exemptions, placeholder text, no rounding, F83, the luminance formula. Pages were searched for these claims rather than read line by line.
- Removed: the 1.4.6 (AAA) 7:1 figures and 18.66px (not on the cited pages), "test the worst area", the DevTools/axe line, and the unsupported claim that graphical objects are covered (only the UI component and state bullet was confirmed).

Method: documentation only; no commands were run.
