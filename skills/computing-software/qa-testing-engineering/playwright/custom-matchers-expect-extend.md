---
id: computing-software.qa-testing-engineering.playwright.custom-matchers-expect-extend
name: custom-matchers-expect-extend
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [expect-extend, custom-matchers, playwright-assertions, typescript, test-readability]
level: practitioner
status: docs-checked
description: "Add custom Playwright matchers with expect.extend: async locator matchers with retries via expect().toPass or polling, messages, isNot handling and TypeScript typing."
sources:
  - https://playwright.dev/docs/test-assertions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom matchers with expect.extend (Playwright)

**Goal:** domain assertions (`toHaveAmount`, `toBeSortedBy`) with good failure messages, reused across specs.

## Define
```ts
// fixtures.ts
import { expect as baseExpect, type Locator } from '@playwright/test';

export const expect = baseExpect.extend({
  async toHaveAmount(locator: Locator, expected: number, options?: { timeout?: number }) {
    const assertionName = 'toHaveAmount';
    let pass: boolean;
    let matcherResult: any;
    try {
      const expectation = this.isNot ? baseExpect(locator).not : baseExpect(locator);
      await expectation.toHaveAttribute('data-amount', String(expected), options);
      pass = true;
    } catch (e: any) {
      matcherResult = e.matcherResult;
      pass = false;
    }
    if (this.isNot) pass = !pass;
    const message = pass
      ? () => this.utils.matcherHint(assertionName, undefined, undefined, { isNot: this.isNot }) +
          `\n\nExpected: not ${expected}\nReceived: ${matcherResult?.actual}`
      : () => this.utils.matcherHint(assertionName, undefined, undefined, { isNot: this.isNot }) +
          `\n\nExpected: ${expected}\nReceived: ${matcherResult?.actual}`;
    return { message, pass, name: assertionName, expected, actual: matcherResult?.actual };
  },
});
```
Building on a built-in web-first assertion inherits auto-retry. For computed values, wrap the computation in `expect.poll(...)` or `expect(...).toPass()` in the test instead.

## Use
```ts
import { test } from '@playwright/test';
import { expect } from './fixtures';
await expect(page.getByTestId('total')).toHaveAmount(36);
await expect(page.getByTestId('total')).not.toHaveAmount(40);
```
Combine multiple extended expects: `mergeExpects(expectA, expectB)`; combine fixtures with `mergeTests`.

## Gotchas
- Matchers that read once (`await locator.textContent()` then compare) do not retry and become flaky.
- Forgetting `this.isNot` inverts `.not` usage silently.

## Verify
Matcher retries until timeout (test with a delayed DOM update), and failure output shows expected vs received.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: expect.extend on the imported expect, the this.isNot handling, this.utils.matcherHint in messages, building on web-first assertions for auto-retry, mergeExpects and mergeTests, expect.poll, and that non-retrying assertions do not auto-retry. Removed: the PlaywrightTest.Matchers typing note.

Method: documentation only; no commands were run.
