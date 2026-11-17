---
id: computing-software.web-development.web-accessibility.non-text-contrast-ui-components
name: non-text-contrast-ui-components
category: computing-software
field: web-development
product: web-accessibility
tags: [distinguishable, non-text-contrast, wcag-1-4-11, focus-indicators, form-controls, icons]
level: practitioner
status: verified
description: "Meeting WCAG 1.4.11 Non-text Contrast: 3:1 for input borders, focus indicators, icons, checkbox states and chart graphics, with what is exempt and how to measure."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
  - https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html
  - https://www.sarasoueidan.com/blog/focus-indicators/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Non-text contrast

**1.4.11 (AA):** visual information required to identify UI components and their states, and meaningful parts of graphics, need **3:1** against adjacent colours.

## 1. What must reach 3:1
- Input and select boundaries when the boundary is the only way to identify the control (a light grey `#ddd` border on white is 1.36:1 - fails). `#949494` on white is 3.03:1 (computed).
- Checkbox/radio/toggle outlines and their checked state indicator.
- Focus indicators against the background they appear on.
- Icons that convey meaning without text (icon-only buttons).
- Chart lines, bars, pie segments (against background and each other where adjacent and required to understand).
- Custom slider tracks/thumbs, progress bar fill.

## 2. Exempt
- Inactive/disabled components.
- Components where appearance is browser default (not modified by author).
- Buttons with visible text labels don't need the button background to contrast with the page (the text identifies it) - but the text itself needs 4.5:1 against the button.
- Logos, decorative graphics, things where a text alternative carries the info and the graphic isn't required.

## 3. Focus indicator design
```css
:focus-visible { outline: 3px solid #1a5fd0; outline-offset: 2px; }
/* two-tone ring works on any background */
:focus-visible { outline: 2px solid #fff; box-shadow: 0 0 0 4px #0b0b0b; }
```
Measure the indicator colour against the adjacent background (and against the component if the indicator is inside it). WCAG 2.4.13 Focus Appearance (AAA) requires an indicator at least as large as the area of a 2 CSS px thick perimeter of the unfocused component, with 3:1 between focused and unfocused pixels; 2.4.7 Focus Visible (AA) only requires it to be visible.

## 4. State changes
Selected vs unselected (tabs, toggles) should differ by more than colour hue, or the indicator must itself be 3:1 against the unselected state.

## 5. Measure
Use the DevTools colour picker on borders/icons; a contrast checker with eyedropper (Colour Contrast Analyser by TPGi) for graphics. axe-core has no non-text-contrast rule (its contrast rules are `color-contrast` and `color-contrast-enhanced`, both for text), so check manually. Colour Contrast Analyser is from TPGi.

## Verify
Walk all form controls, icon buttons, focus states and charts with an eyedropper; record ratios for design tokens (`--border-control`, `--focus-ring`).
