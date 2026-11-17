---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-visible-focus-indicators
name: designing-visible-focus-indicators
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [focus-indicator, focus-visible, focus-ring, wcag-focus-appearance, keyboard-focus-style, focus-not-obscured]
level: practitioner
status: docs-checked
description: "Design visible focus indicators: WCAG 2.2 focus criteria, high-contrast outlines, not obscured by sticky UI, and consistent styling."
sources:
  - "https://www.w3.org/TR/WCAG22/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Visible focus indicators

## Requirements
- **SC 2.4.7 Focus Visible (AA):** any keyboard-operable interface has a mode of operation where the keyboard focus indicator is visible.
- **SC 2.4.11 Focus Not Obscured (Minimum) (AA, new in WCAG 2.2):** a focused component is not entirely hidden by author-created content such as sticky headers or cookie banners.
- **SC 2.4.12 Focus Not Obscured (Enhanced) (AAA)** requires that no part is hidden.
- **SC 2.4.13 Focus Appearance (AAA, new in WCAG 2.2):** the indicator area is at least that of a 2 CSS pixel thick perimeter of the unfocused component and has at least 3:1 contrast between the same pixels in focused and unfocused states; read the exceptions in the criterion before claiming conformance.
- **SC 1.4.11 Non-text Contrast (AA)** also applies: visual information needed to identify UI components and states has at least 3:1 contrast against adjacent colours.

## Design
1. **Do not remove default outlines** without a replacement.
2. Use a solid outline of at least 2 px with an offset in a colour that has at least 3:1 against both the component and the background; a two-colour (inner and outer) ring works on any background.
3. Show focus for keyboard users; avoid rings on mouse clicks only where the platform's keyboard-only focus styling allows.
4. Make focus style **consistent across components** and a **design token** (see `...design-systems.tokens-tiers-primitive-semantic-component`).
5. Check **sticky elements** so focused items are not hidden under sticky headers.
6. Show focus on custom components including dark mode and on images.
7. In Figma, add a focus variant to each interactive component (see `...figma.auto-layout-components-and-variants`).

## Verify
- [ ] Tabbing through shows an obvious indicator on every control.
- [ ] Indicator contrast is at least 3:1 on every background used.
- [ ] No sticky UI covers the focused element.

## Checked
2026-11-01. Confirmed in WCAG 2.2 (w3.org/TR/WCAG22): SC 2.4.7, 2.4.11, 2.4.12, 2.4.13 (levels, new-in-2.2 flags, the 2 CSS pixel perimeter and 3:1 test) and SC 1.4.11. Removed: CSS-specific names (`:focus-visible`, `scroll-padding-top`, `outline`) and the "offset" wording as unconfirmed by WCAG; the 2 px outline and two-colour ring are design guidance, not WCAG text.
Method: documentation only; no commands were run.
