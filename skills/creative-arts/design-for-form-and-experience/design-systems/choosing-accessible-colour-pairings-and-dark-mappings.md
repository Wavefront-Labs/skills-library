---
id: creative-arts.design-for-form-and-experience.design-systems.choosing-accessible-colour-pairings-and-dark-mappings
name: choosing-accessible-colour-pairings-and-dark-mappings
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [accessible-color-pairs, dark-theme-mapping, contrast-pairs, semantic-color-tokens, theme-mapping, color-system, dark-mode]
level: practitioner
status: docs-checked
description: "Define accessible colour pairings (foreground on background) and map semantic tokens between light and dark themes by role, verified with WCAG contrast tests."
sources:
  - "https://www.w3.org/TR/WCAG22/"
  - "https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html"
  - "https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme"
  - "https://web.dev/articles/prefers-color-scheme"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accessible colour pairings and dark-theme mapping

## Pairings
1. **Define roles in pairs:** every background role has an `on-` foreground (for example `surface` / `on-surface`, `primary` / `on-primary`). Only ship combinations that are in the matrix.
2. **Contrast targets (WCAG 2.2):** text at least 4.5:1 (AA, SC 1.4.3); large text 3:1; text at least 7:1 for AAA (SC 1.4.6); user interface components and states 3:1 against adjacent colours (SC 1.4.11). Treat the thresholds as exact: 2.999:1 does not meet 3:1.
3. **Make the matrix:** rows backgrounds, columns foregrounds, cells the ratio with pass/fail. Fail cells are banned in docs.
4. **State layers** (hover, pressed, focus) must keep the contrast of the base state; test the worst state.
5. Inactive (disabled) components are exempt from SC 1.4.11, but keep them distinguishable.

## Light to dark mapping
- Do not simply invert: map each role to a suitable value in the opposite theme, then re-test every pair.
- Keep a semantic token layer: a role such as text-default points to one primitive in light and another in dark; components reference only semantic tokens (`creative-arts.design-for-form-and-experience.design-systems.design-tokens-and-a-modular-type-scale`).
- Saturated accents often need lowering in chroma in dark themes; verify by eye and by the matrix.
- In CSS, `color-scheme` tells the browser which colour schemes an element supports, and the `prefers-color-scheme` media query follows the user's system setting.

## Automate
Run the matrix test on the generated tokens for each theme and fail the build on contrast regressions.

## Verify
- [ ] Every foreground/background pair in docs passes its target.
- [ ] Dark values chosen by role (not by inversion); both themes tested.

## Checked
2026-11-01. Confirmed: SC 1.4.3 (4.5:1 and 3:1), SC 1.4.6 (7:1) and SC 1.4.11 (3:1, inactive exemption, no rounding) in WCAG 2.2 and its Understanding page; `color-scheme` and `prefers-color-scheme` on MDN and web.dev. Removed as unconfirmed: the Material 3 tone numbers, library and plugin names, Figma modes and per-mode DTCG values, and the CI claim.
Method: documentation only; no commands were run.
