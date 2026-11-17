---
id: computing-software.web-development.frontend-development.visual-regression-testing
name: visual-regression-testing
category: computing-software
field: web-development
product: frontend-development
tags: [frontend-testing, visual-regression, screenshot-testing, playwright, storybook, chromatic]
level: practitioner
status: docs-checked
description: "Catching unintended UI changes with screenshot tests: Playwright toHaveScreenshot, Storybook/Chromatic, controlling fonts/animations/data, thresholds and baseline workflow."
sources:
  - https://playwright.dev/docs/test-snapshots
  - https://storybook.js.org/docs/writing-tests/visual-testing
  - https://storybook.js.org/docs/writing-tests/integrations/test-runner
  - https://github.com/lost-pixel/lost-pixel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Visual regression testing

## 1. Playwright built-in
```ts
test("pricing page", async ({ page }) => {
  await page.goto("/pricing");
  await page.evaluate(() => document.fonts.ready);
  await expect(page).toHaveScreenshot("pricing.png", {
    fullPage: true,
    mask: [page.getByTestId("live-chat"), page.locator("time")],   // dynamic regions
    animations: "disabled",                                         // default for toHaveScreenshot
    maxDiffPixelRatio: 0.01,
  });
});
```
- First run writes baselines into `*-snapshots/`; update deliberately with `npx playwright test --update-snapshots`.
- Baselines are per browser + OS (`pricing-chromium-linux.png`). Font rendering differs between macOS and Linux - **generate and compare baselines in the same Docker image** as CI (`mcr.microsoft.com/playwright:<version>`), never on laptops.
- Component-level: screenshot a locator (`expect(card).toHaveScreenshot()`) - smaller, fewer false positives.

## 2. Storybook-based
Storybook's documented route is Chromatic (a cloud service by the Storybook team; the `@chromatic-com/storybook` addon takes snapshots of every story, compared against baselines, with cross-browser support). Lost Pixel is an open-source alternative that runs against Storybook builds or application pages. `@storybook/test-runner` (Jest and Playwright) is being replaced by the Storybook Vitest addon.

## 3. Determinism checklist
- Freeze time (`page.clock.setFixedTime`), seed random data, stub API responses with fixtures.
- Wait for fonts and images (Playwright marks `networkidle` as DISCOURAGED; wait for specific elements/fonts).
- Disable animations (the default for `toHaveScreenshot`), hide the text caret (`caret` option), and stabilise scrollbars where inconsistent.
- Fixed viewport sizes per breakpoint you care about.

## 4. Workflow
- Treat a diff as a question: intended (update baseline in the same PR) or regression (fix).
- Keep the suite focused: key pages x 2-3 viewports and design-system components. Thousands of full-page shots become noise nobody reviews.
- Store baselines in git (Playwright) or in the service (Chromatic); large PNG churn may need Git LFS.

## Verify
A deliberate 1px padding change fails the test with a readable diff image in the HTML report; rerun without changes passes 10/10.

## Checked

Checked 2026-10-26 against the Playwright docs source (microsoft/playwright `docs/src`, main, last commit 2026-10-25: test snapshots, PageAssertions.toHaveScreenshot, Clock, Docker, params), the Storybook docs (visual testing, test runner) and the Lost Pixel README.

- Confirmed: first run writes baselines into `<spec>-snapshots` and `--update-snapshots` updates them; snapshot names include browser and platform because rendering differs; `toHaveScreenshot` accepts `animations` (default `"disabled"`), `caret`, `fullPage`, `mask` and `maxDiffPixelRatio`; `page.clock.setFixedTime`; Chromatic and `@chromatic-com/storybook` for Storybook visual tests; Lost Pixel is open source and supports Storybook.
- Changed: the Storybook test runner is described as being replaced by the Vitest addon.
- Removed: Percy and Applitools, and the Chromatic documentation link, which could not be checked.

Method: documentation only; no commands were run.
