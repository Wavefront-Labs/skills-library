---
id: computing-software.web-development.web-accessibility.text-contrast-minimum
name: text-contrast-minimum
category: computing-software
field: web-development
product: web-accessibility
tags: [distinguishable, contrast-ratio, contrast-minimum, wcag-1-4-3, color-contrast, design-tokens, contrast-checker]
level: practitioner
status: verified
description: "Meeting WCAG 1.4.3 text contrast: 4.5:1 and 3:1 thresholds, what counts as large text, measuring over images and gradients, tools, and building compliant colour tokens."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
  - https://webaim.org/resources/contrastchecker/
  - https://developer.chrome.com/docs/devtools/accessibility/contrast
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Text contrast minimum

## 1. Thresholds (1.4.3 AA)
- Normal text: **4.5:1** against its background.
- Large text: **3:1** - large = at least 18pt (about 24 CSS px) regular, or 14pt (about 18.5 CSS px) bold (WCAG defines it in points; the Understanding page converts at 1pt = 1.333px).
- AAA (1.4.6): 7:1 and 4.5:1.
- Exempt: disabled controls, pure decoration, logotypes, text in incidental images.
Ratio = (L1 + 0.05) / (L2 + 0.05) with L1 the lighter and L2 the darker relative luminance; it ranges 1:1 to 21:1. Don't round up: 4.48:1 fails.

## 2. Reference points
On white: `#767676` is the lightest grey passing 4.5:1 (4.54); `#949494` passes 3:1. On black: `#767676` gives 4.62 (computed with the WCAG formula; `#777777` on white is 4.48 and fails). Brand colours often fail as text - darken for text use, keep the brand shade for large display or decoration.

## 3. Measure correctly
- Use the actual rendered colours, including opacity: `color: rgb(0 0 0 / .5)` on white renders as `#808080`, about 3.95:1 (axe reports 3.94).
- Text over images/gradients/video: test against the lightest (or darkest) area behind the text; add a scrim (`linear-gradient(rgb(0 0 0 / .6), transparent)`) or solid backing.
- Placeholder text must meet 4.5:1 if it conveys information (better: don't use placeholders as labels).
- Check every state: hover, focus, visited, selected, error, dark mode.
- Thin/light font weights render lighter than measured - be conservative.

## 4. Tools
DevTools color picker shows ratio with AA/AAA lines and suggests passing colours; Lighthouse/axe `color-contrast` (automated but misses text over images); WebAIM checker; Stark/Figma plugins at design time. APCA (WCAG 3 draft) is useful for research but WCAG 2.x ratio is the legal standard.

## 5. Tokens
Define text/background pairs in the design system and test them in CI (e.g. a script computing ratios for each `--text-*` on each `--surface-*` token); document "allowed on" combinations.

## Verify
axe zero `color-contrast` violations; manual check of text on images and all interactive states in light and dark themes.
