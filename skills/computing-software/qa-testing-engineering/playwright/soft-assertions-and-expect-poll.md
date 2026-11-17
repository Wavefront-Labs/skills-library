---
id: computing-software.qa-testing-engineering.playwright.soft-assertions-and-expect-poll
name: soft-assertions-and-expect-poll
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [soft-assertions, expect-poll, expect-topass, playwright-assertions, web-first-assertions]
level: practitioner
status: verified
description: "Use Playwright soft assertions to collect multiple failures, expect.poll for non-DOM values, and expect.toPass for retrying blocks, with timeouts and intervals."
sources:
  - https://playwright.dev/docs/test-assertions#soft-assertions
  - https://playwright.dev/docs/test-assertions#expectpoll
  - https://playwright.dev/docs/test-assertions#expecttopass
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Soft assertions and expect.poll

**Goal:** check several things without stopping at the first failure, and wait on values that are not locators.

## Soft assertions
```ts
await expect.soft(page.getByTestId('status')).toHaveText('Paid');
await expect.soft(page.getByTestId('eta')).toHaveText(/\d+ days/);
await page.getByRole('link', { name: 'Invoice' }).click();   // test continues
expect(test.info().errors).toHaveLength(0);                  // optional: stop here if any soft failed
```
The test is marked failed at the end with all soft failures listed (run here: two failed soft assertions gave `test.info().errors.length` of 2). Configure all expects as soft: `const softExpect = expect.configure({ soft: true })`.

## expect.poll (retry a function until the matcher passes)
```ts
await expect.poll(async () => {
  const res = await page.request.get('/api/orders/42');
  return (await res.json()).status;
}, {
  message: 'order should be shipped',
  timeout: 30_000,
  intervals: [1_000, 2_000, 5_000],      // default [100, 250, 500, 1000]
}).toBe('SHIPPED');
```
`expect.poll` timeout defaults to 5 s (a miss reported `Timeout 5000ms exceeded while waiting on the predicate` after about 4.9 s); `expect.soft.poll(...)` also exists. Use for API state, emails in a test inbox, files, DB rows: anything not covered by web-first locator assertions.

## expect().toPass (retry a block)
```ts
await expect(async () => {
  const res = await page.request.get('/api/health');
  expect(res.status()).toBe(200);
  expect((await res.json()).queue).toBe('drained');
}).toPass({ timeout: 60_000, intervals: [1_000, 5_000] });
```
Default `toPass` timeout is 0 (docs; it ignores the expect timeout), so it retries until the test timeout; run here with a 4 s test timeout the failure was the inner `Expected: 2 Received: 1` plus `Test timeout of 4000ms exceeded`. Set one explicitly.

## Gotchas
- Soft assertions after a navigation failure produce cascades; keep hard assertions for preconditions.
- `expect.poll` on a locator is unnecessary; web-first assertions already retry.
- Do not wrap actions with side effects (create order) in `toPass`; retries repeat them.

## Verify
Report lists every soft failure, and polling assertions have explicit timeouts shorter than the test timeout.
