---
id: computing-software.qa-testing-engineering.playwright.screenshot-masking-and-thresholds
name: screenshot-masking-and-thresholds
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [screenshot-mask, maxdiffpixels, tohavescreenshot, visual-regression]
level: practitioner
status: docs-checked
description: "Stabilise Playwright toHaveScreenshot with mask, maskColor, maxDiffPixels, maxDiffPixelRatio, threshold and animations/caret options for dynamic content."
sources:
  - https://playwright.dev/docs/test-snapshots
  - https://playwright.dev/docs/api/class-pageassertions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Masking dynamic content and diff thresholds

**Goal:** visual tests that fail on real visual regressions, not timestamps and anti-aliasing.

## Mask dynamic regions
```ts
await expect(page).toHaveScreenshot('dashboard.png', {
  mask: [page.getByTestId('clock'), page.locator('.avatar'), page.getByRole('img', { name: /chart/ })],
  maskColor: '#FF00FF',
});
```
Masked elements are overlaid with a box (pink `#FF00FF` by default, set with `maskColor`) that covers their bounding box; the mask also applies to invisible elements.

## Tolerances
| Option | Meaning |
|---|---|
| `threshold` | acceptable perceived colour difference per pixel, 0 (strict) to 1 (lax), YIQ colour space, default 0.2 |
| `maxDiffPixels` | acceptable number of differing pixels (unset by default) |
| `maxDiffPixelRatio` | acceptable ratio 0..1 of differing pixels to total pixels (unset by default) |

Set defaults in config:
```ts
expect: { toHaveScreenshot: { maxDiffPixelRatio: 0.01, animations: 'disabled', caret: 'hide', scale: 'css' } },
```

## Stabilisers
- `animations: 'disabled'` (default for toHaveScreenshot): finite animations are fast-forwarded to completion, infinite ones are reset to their initial state.
- `caret: 'hide'` (default).
- Freeze time with `page.clock.setFixedTime(...)`; stub dynamic data with `route`.
- When creating a missing baseline, Playwright takes screenshots until two consecutive ones match and saves the last.

## Gotchas
- Raising thresholds to pass a flaky test hides real regressions; prefer masking or stabilising.
- Masking a large area makes the test meaningless; screenshot a component instead (`locator.toHaveScreenshot`).
- Screenshots differ between browsers and platforms because of rendering and fonts: generate baselines in the same Docker image as CI.

## Verify
Change a button colour: test fails with a diff image; change the clock: test passes.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: mask and maskColor behaviour (pink #FF00FF default, applies to invisible elements), threshold (0 to 1, YIQ, default 0.2), maxDiffPixels and maxDiffPixelRatio being unset by default, setting them under expect.toHaveScreenshot in the config, animations default disabled and caret default hide, page.clock.setFixedTime, and the two-consecutive-screenshots behaviour when creating a baseline. Removed: the document.fonts.ready claim, which the docs do not state.

Method: documentation only; no commands were run.
