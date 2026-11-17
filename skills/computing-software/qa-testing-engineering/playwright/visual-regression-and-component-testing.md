---
id: computing-software.qa-testing-engineering.playwright.visual-regression-and-component-testing
name: visual-regression-and-component-testing
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, visual-regression, screenshot-testing, tohavescreenshot, component-testing, playwright-ct, cross-browser, chromium, firefox, webkit, baseline-images, diff-threshold, masking, animations-disabled, javascript, typescript]
level: practitioner
status: docs-checked
description: "Playwright's built-in toHaveScreenshot for visual regression across Chromium/Firefox/WebKit, and @playwright/test's component-testing mode for mounting components in isolation."
sources: ["https://playwright.dev/docs/test-snapshots", "https://playwright.dev/docs/test-components"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playwright: visual regression and component testing

**Goal:** catch visual regressions using Playwright's built-in screenshot
assertions (no third-party service required), and test components in isolation
without a full E2E harness.

## 1. Built-in visual regression with toHaveScreenshot
```ts
await expect(page).toHaveScreenshot('dashboard.png', { maxDiffPixels: 100, threshold: 0.1 })
await expect(page.locator('[data-testid=card]')).toHaveScreenshot('card.png')
```
First run generates the baseline (`--update-snapshots` also refreshes it); subsequent runs diff
against it. `threshold` (0 strict to 1 lax, default 0.2) says which pixels count as different;
`maxDiffPixels` (unset by default) is how many may differ.

## 2. Baselines are OS- and browser-specific — the #1 gotcha
Playwright screenshots render slightly differently per OS (font rasterization,
subpixel hinting) even for the same browser engine. A baseline captured on macOS
and compared against a Linux CI run will fail on noise, not a real regression.
**Always generate and store baselines from the same environment that will run the
comparison** — typically inside the CI container/Docker image, never from a
developer's laptop. Snapshot file names already carry the browser and platform
(for example `example-test-1-chromium-darwin.png`); the name and path can be changed with
`testConfig.snapshotPathTemplate`.

## 3. Taming non-determinism before snapshotting
- Disable animations and transitions for test runs (check the `toHaveScreenshot` options in
  the API reference for the supported way).
- Wait for a specific "ready" signal before snapshotting: a screenshot mid-render produces a
  flaky diff unrelated to any real change.
- Mask dynamic regions (see the `toHaveScreenshot` options) rather than loosening
  `threshold` or `maxDiffPixels` globally, which hides real regressions elsewhere on the same page.
- Freeze or mock the clock/`Date` the same way as any other test to avoid
  timestamp-driven diffs.

## 4. Component testing (story gallery)
Current Playwright docs describe component tests as regular end-to-end tests that run against
a small story gallery page served by your own dev server, driven by the built-in `mount`
fixture of `@playwright/test`; no extra npm packages or bundler integration:
```ts
import { test, expect } from '@playwright/test';

test('click should expand', async ({ mount }) => {
  const component = await mount('components/Expandable/Stateful');
  await component.getByRole('button').click();
  await expect(component.getByTestId('expanded')).toHaveValue('true');
});
```
Each composition is one story export; stories record effects into a hidden input the test
asserts on. Story ids are strings, so renaming a story breaks specs at runtime. The older
`@playwright/experimental-ct-*` packages (JSX in the test file) are the legacy approach; the
docs include a migration guide. Per-test variation (providers, routing) goes through
`hooksConfig`.

## 5. Cross-browser visual checks are expensive — budget them
Running visual snapshots across Chromium, Firefox, and WebKit triples the baseline
set and the maintenance burden (three sets of images to review on every
intentional UI change). Default to visual regression on Chromium only for most
pages; reserve the full three-engine matrix for layout-critical pages with known
cross-engine rendering differences (complex flexbox/grid, custom form controls).

## Verify
- [ ] Baselines generated and stored from the same OS/container that runs CI comparisons.
- [ ] Animations disabled and page settled (explicit ready signal) before snapshot.
- [ ] Dynamic regions masked explicitly, not papered over with a loose global threshold.
- [ ] Component tests follow the current story-gallery approach, or the legacy experimental packages knowingly.
- [ ] Full cross-browser visual matrix reserved for pages that justify the cost.

## Checked

2026-10-28. Confirmed in the Playwright snapshots page: `toHaveScreenshot`, `--update-snapshots`, `threshold` (0 to 1, default 0.2), `maxDiffPixels` (unset by default), browser and platform in snapshot file names, `testConfig.snapshotPathTemplate`. Confirmed in the components page: story-gallery component testing with the built-in `mount` fixture, `hooksConfig`, and the migration notice for `@playwright/experimental-ct-*`.
Removed or rewritten: the experimental-ct React example and `playwright-ct.config.ts` workflow (superseded by the gallery approach), `__screenshots__/<os>/` folders, `maxDiffPixelRatio`, the CSS-injection and `networkidle` snippets, and the `mask` snippet (option details not on the fetched pages).

Method: documentation only; no commands were run.
