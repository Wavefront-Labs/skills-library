---
id: computing-software.qa-testing-engineering.playwright.axe-accessibility-scans-in-playwright
name: axe-accessibility-scans-in-playwright
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [axe-playwright, axe-core, accessibility-testing, wcag, playwright-accessibility]
level: practitioner
status: docs-checked
description: "Run axe-core scans in Playwright with @axe-core/playwright: WCAG tag filters, scoping include/exclude, scanning states, fixtures, and baselining known violations."
sources:
  - https://playwright.dev/docs/accessibility-testing
  - https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accessibility scans with @axe-core/playwright

**Goal:** automatic WCAG checks in the same E2E tests, including states only reachable by interaction.

## Basic scan
```ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('checkout has no detectable a11y violations', async ({ page }, testInfo) => {
  await page.goto('/checkout');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .exclude('#third-party-chat')
    .analyze();
  await testInfo.attach('axe-results', { body: JSON.stringify(results, null, 2), contentType: 'application/json' });
  expect(results.violations).toEqual([]);
});
```

## Scan states
```ts
await page.getByRole('button', { name: 'Edit address' }).click();
await expect(page.getByRole('dialog')).toBeVisible();
const results = await new AxeBuilder({ page }).include('[role="dialog"]').analyze();
```

## Fixture for shared config
```ts
export const test = base.extend<{ makeAxeBuilder: () => AxeBuilder }>({
  makeAxeBuilder: async ({ page }, use) => {
    await use(() => new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).exclude('#cookie-banner'));
  },
});
```

## Known issues
- `.disableRules(['color-contrast'])` only with a ticket.
- Better: snapshot violation fingerprints and fail on new ones:
```ts
const ids = results.violations.flatMap(v => v.nodes.map(n => `${v.id} ${n.target}`));
expect(ids).toMatchSnapshot('a11y-known.txt');   // or compare to an allow-list
```

## Gotchas
- Scanning before content renders reports nothing; wait for a meaningful element first.
- Violations print as large objects; map to `id`, `impact`, `nodes[].target` for readable output.
- Automated scans miss keyboard traps, focus order and announcement quality; keep manual checks.

## Verify
A deliberately removed label fails the test, and attached results identify the selector and rule.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: the @axe-core/playwright import, withTags with wcag2a, wcag2aa, wcag21a and wcag21aa, include() and exclude() scoping (exclude removes all rules for the element and its descendants), disableRules(), the violation fingerprint snapshot technique (do not snapshot the whole violations array), testInfo.attach of scan results and the makeAxeBuilder fixture pattern.

Method: documentation only; no commands were run.
