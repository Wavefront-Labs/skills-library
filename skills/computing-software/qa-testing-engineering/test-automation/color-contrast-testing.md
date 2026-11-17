---
id: computing-software.qa-testing-engineering.test-automation.color-contrast-testing
name: color-contrast-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [contrast-ratio-testing, color-contrast, wcag, accessibility, a11y, axe-core]
level: practitioner
status: docs-checked
description: "Test colour contrast against WCAG 2.2: 4.5:1 text, 3:1 large text and UI components, tools for measuring, states (hover, focus, disabled) and colour-only cues."
sources:
  - https://www.w3.org/WAI/WCAG22/quickref/
  - https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
  - https://webaim.org/resources/contrastchecker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Colour contrast testing

**Goal:** text and essential UI meet WCAG 2.2 contrast so low-vision users can read and operate it.

## Thresholds (WCAG 2.2)
- 1.4.3 Contrast (Minimum), AA: 4.5:1 normal text, 3:1 large text (18 point regular, or 14 point bold).
- 1.4.6 Contrast (Enhanced), AAA: 7:1 and 4.5:1.
- 1.4.11 Non-text Contrast, AA: 3:1 for UI component boundaries (input borders, checkboxes), focus indicators and meaningful graphics against adjacent colours.
- 1.4.1 Use of Colour: colour cannot be the only cue (a red error border also needs an icon or text).
- Exempt: disabled controls, logos, pure decoration.

## Measure
- Automated: axe-core rule `color-contrast` (Playwright `@axe-core/playwright`, Lighthouse). Text over images or gradients is hard for automation to judge; check it manually.
- Manual: WebAIM Contrast Checker or the Colour Contrast Analyser eyedropper; the Chrome DevTools colour picker shows the ratio with AA/AAA ticks.
- Check every state: default, hover, focus, visited, error, placeholder text (often fails), dark mode.
- Text on images: sample the lightest region behind the text.

```js
const results = await new AxeBuilder({ page }).withTags(['wcag2aa']).analyze();
expect(results.violations).toEqual([]);
```

## Gotchas
- Opacity and overlays change the effective colour; measure rendered pixels.
- Brand palette failures are design decisions: report with the measured ratio and a passing alternative hex.

## Verify
axe shows zero contrast violations on key pages, and a manual sample of hover/focus/error states and text-on-image areas meets the ratios.

## Checked
2026-10-28. Confirmed: 4.5:1 and 3:1 thresholds and rule ID `color-contrast` (Deque axe rule page); Contrast (Minimum) large-text definition (WCAG 2.2 Understanding page); Contrast (Enhanced), Non-text Contrast and Use of Color pages exist and match the criteria named; `AxeBuilder`, `withTags` and `@axe-core/playwright` (Playwright accessibility testing page). Removed: pixel conversions for large text, the "needs review" wording, and `withRules` (not in the fetched pages; `withTags` used instead). The WCAG quickref page returned only a stub.
Method: documentation only; no commands were run.
