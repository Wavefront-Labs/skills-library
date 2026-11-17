---
id: creative-arts.design-for-form-and-experience.design-systems.visual-regression-testing-for-components
name: visual-regression-testing-for-components
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [visual-regression-testing, visual-testing, chromatic, percy, playwright-screenshots, storybook-testing, ui-regression]
level: practitioner
status: draft
description: "Set up visual regression testing for components: snapshot stories in a controlled browser, handle flakiness, review diffs in PRs, and gate merges with baselines."
sources:
  - "Chromatic documentation - visual testing for Storybook (chromatic.com/docs)"
  - "Playwright docs - Visual comparisons: toHaveScreenshot (playwright.dev/docs/test-snapshots)"
  - "Percy by BrowserStack - Visual testing docs (docs.percy.io)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Visual regression testing for components

**Goal:** catch unintended visual changes in the system before they reach products.

## Options
- **Chromatic** (Storybook cloud): captures every story across browsers, shows diffs in the PR, UI review workflow, TurboSnap to test only changed stories.
- **Playwright** `toHaveScreenshot()` against a Storybook or test page: self-hosted, baselines in Git (or LFS).
- **Percy / Applitools / Loki / reg-suit** as alternatives.

## Playwright example
```ts
import { test, expect } from '@playwright/test'
test('Button/Primary', async ({ page }) => {
  await page.goto('http://localhost:6006/iframe.html?id=components-button--primary&viewMode=story')
  await page.waitForLoadState('networkidle')
  await expect(page.locator('#storybook-root')).toHaveScreenshot('button-primary.png', { maxDiffPixelRatio: 0.001 })
})
```
Run in a **fixed Docker image** (`mcr.microsoft.com/playwright`) so fonts and anti-aliasing match across machines; update baselines with `--update-snapshots` and review them.

## Reduce flakiness
- Disable animations (`animations: 'disabled'`, or `prefers-reduced-motion`), freeze time and random data, mask dynamic regions (`mask: [locator]`), wait for fonts (`document.fonts.ready`), load images deterministically, set a fixed viewport and device scale factor.
- Snapshot **states** (hover, focus, error via play functions) and **themes** (light, dark), plus a few viewports.

## Workflow
1. Each PR runs the visual tests; diffs appear as checks.
2. Designers and engineers approve intentional changes (baseline update), reject accidents.
3. Block merges on unreviewed diffs; keep baselines on main.
4. Track flaky stories and fix or quarantine.

## Verify
- [ ] Stories cover variants, states and themes; rendered in a pinned environment.
- [ ] Animation, time and data are deterministic.
- [ ] PR checks require diff review before merge.
