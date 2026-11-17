---
id: computing-software.qa-testing-engineering.playwright.topass-and-assertion-timeouts
name: topass-and-assertion-timeouts
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [topass, expect-timeout, web-first-assertions, assertion-negation, expect-configure]
level: practitioner
status: verified
description: "Tune Playwright assertion timeouts, use negated web-first assertions correctly, and retry multi-step blocks with expect().toPass() and intervals."
sources:
  - https://playwright.dev/docs/test-assertions
  - https://playwright.dev/docs/test-timeouts
  - https://playwright.dev/docs/test-assertions#expecttopass
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assertion timeouts, negation and toPass retries

**Goal:** assertions that wait just long enough and retry the right unit of work.

## Timeouts
```ts
// playwright.config.ts
export default defineConfig({ expect: { timeout: 10_000 } }); // default 5000ms
await expect(page.getByText('Report ready')).toBeVisible({ timeout: 60_000 }); // one slow step (a miss at the default failed after 5008 ms with `Timeout: 5000ms`)
const slowExpect = expect.configure({ timeout: 30_000 });
await slowExpect(page.getByRole('status')).toHaveText('Done');
```

## Negation
```ts
await expect(page.getByRole('progressbar')).not.toBeVisible(); // waits until it disappears
await expect(page.getByRole('progressbar')).toBeHidden();      // equivalent, reads better
```
Web-first negations retry until true. **Do not** write `expect(await loc.isVisible()).toBe(false)`; that checks once, often before the spinner even appears.

## toPass: retry a block
For checks that need actions between attempts (refresh, re-fetch an API):
```ts
await expect(async () => {
  const res = await page.request.get('/api/job/42');
  expect(res.status()).toBe(200);
  expect((await res.json()).state).toBe('complete');
}).toPass({ intervals: [1_000, 2_000, 5_000], timeout: 60_000 });
```
- `toPass` default timeout is 0 (docs: it also ignores the expect timeout), so it retries until the test timeout; always set `timeout`. Run here with `{ timeout: 2000, intervals: [100] }` it succeeded on attempt 7 once the condition held.
- Inner `expect`s should be generic matchers or short-timeout web-first ones.

## expect.poll for a single value
```ts
await expect.poll(async () => (await page.request.get('/api/count')).json(), { timeout: 30_000 }).toEqual({ n: 3 });
```

## Gotchas
- Assertion timeout counts inside the test timeout (30s default): raising one without the other just moves the failure.
- Avoid `page.waitForTimeout` before assertions; the assertion already waits.
- Don't wrap UI actions in `toPass` that are not idempotent (double submit).

## Verify
Search for `isVisible()` / `textContent()` used inside `expect(...)`; replace with web-first matchers.
