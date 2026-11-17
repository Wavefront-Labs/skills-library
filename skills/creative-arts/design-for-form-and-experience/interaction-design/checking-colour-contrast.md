---
id: creative-arts.design-for-form-and-experience.interaction-design.checking-colour-contrast
name: checking-colour-contrast
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [contrast-ratio, colour-contrast, color-contrast, wcag-contrast, text-contrast, non-text-contrast]
level: practitioner
status: docs-checked
description: "Check colour contrast in designs: WCAG ratios for text and UI components, how the ratio is computed, states and images, and fix strategies."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
  - https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html
  - https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
  - https://www.w3.org/TR/WCAG22/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Colour contrast checking

## Requirements
- **SC 1.4.3 Contrast (Minimum), AA:** text at least 4.5:1 against its background; large text (at least 18 point, or 14 point bold) at least 3:1. Inactive components, pure decoration, text not visible to anyone, and logos or logotypes are exempt.
- **SC 1.4.6 Contrast (Enhanced), AAA:** 7:1 for normal text, 4.5:1 for large text.
- **SC 1.4.11 Non-text Contrast, AA:** visual information needed to identify user interface components and their states (such as selected or focused), and parts of graphics needed to understand content, at least 3:1 against adjacent colours. Inactive components are exempt.

## How the ratio works
Ratio = (L1 + 0.05) / (L2 + 0.05), where L1 is the relative luminance of the lighter colour and L2 of the darker, with relative luminance as defined in WCAG. Ratios run from 1:1 to 21:1. The thresholds are not rounded: 4.499:1 does not meet 4.5:1.

## Check
1. Use a contrast checker (browser dev tools or a design-tool plugin) on every text and background pair, in **all states**: default, hover, focus, error, selected. Disabled (inactive) controls are exempt from the text rule but should still be understandable.
2. **Text on images or gradients:** test the worst-case area; add an overlay or solid pill behind text.
3. **Icons and graphics** that carry information need 3:1 (SC 1.4.11).
4. **Dark mode:** check the dark palette independently (see `...design-systems.choosing-accessible-colour-pairings-and-dark-mappings`).
5. **Transparency:** compute against the resulting blended colour.

## Fix
Darken or lighten the foreground first; change the pairing; increase the weight and size if text is large; add a border to separate boundaries.

## Verify
- [ ] Every pair has a recorded ratio.
- [ ] States and dark mode were checked.
- [ ] Information is not conveyed by colour alone (see `...interaction-design.designing-for-colour-vision-deficiency`).

## Checked
2026-11-01. Confirmed against the W3C Understanding pages for SC 1.4.3, 1.4.6 and 1.4.11 and the WCAG 2.2 text: the ratios, the large-text size, the exemptions, the ratio formula and range, and the no-rounding rule. Removed: named checker tools and the placeholder-text claim (no page states them).
Method: documentation only; no commands were run.
