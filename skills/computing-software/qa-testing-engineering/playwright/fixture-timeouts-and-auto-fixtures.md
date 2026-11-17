---
id: computing-software.qa-testing-engineering.playwright.fixture-timeouts-and-auto-fixtures
name: fixture-timeouts-and-auto-fixtures
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [fixture-timeout, auto-fixtures, playwright-fixtures, box-fixtures]
level: practitioner
status: verified
description: "Configure Playwright automatic fixtures ({ auto: true }) for per-test logging or checks, give slow fixtures their own timeout, and box fixtures out of reports."
sources:
  - https://playwright.dev/docs/test-fixtures#automatic-fixtures
  - https://playwright.dev/docs/test-fixtures#fixture-timeout
  - https://playwright.dev/docs/test-fixtures#box-fixtures
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic fixtures and fixture timeouts

**Goal:** cross-cutting setup that runs for every test, and slow setup that does not eat the test budget.

## Automatic fixture
```ts
export const test = base.extend<{ consoleGuard: void }>({
  consoleGuard: [async ({ page }, use, testInfo) => {
    const errors: string[] = [];
    page.on('pageerror', e => errors.push(e.message));
    await use();
    if (errors.length) {
      await testInfo.attach('page-errors', { body: errors.join('\n'), contentType: 'text/plain' });
      throw new Error(`Uncaught page errors:\n${errors.join('\n')}`);
    }
  }, { auto: true }],
});
```
Runs for every test using this `test`, even without being named in the test signature.

Worker-scoped auto fixture (e.g. start a mock server once per worker):
```ts
mockServer: [async ({}, use) => { const s = await start(); await use(s); await s.stop(); }, { scope: 'worker', auto: true }],
```

## Fixture timeout
```ts
seededDb: [async ({}, use) => { await seed(); await use(); }, { timeout: 120_000 }],
```
Without it, fixture setup counts toward the test timeout; worker-scoped fixtures get their own timeout equal to the test timeout (docs). Run here: `{ timeout: 500 }` on a fixture that waited 3 s failed with `Fixture "db" timeout of 500ms exceeded during setup.`

## box and title
```ts
helper: [async ({}, use) => { await use(x); }, { box: true }],          // hidden from steps
apiClient: [async ({}, use) => { await use(c); }, { title: 'API client' }],
```

## Gotchas
- Auto fixtures that depend on `page` force a page for every test, including API-only tests; scope them to a separate `test` export if that matters.
- Throwing after `use()` marks the test failed even though its body passed (run here: the page error `boom` was attached as `page-errors` and the test reported `Uncaught page errors:`): intended for guards, surprising otherwise; document it.
- `box` and `title` are accepted fixture options (1.64 typings: `box?: boolean | 'self'`, `title?: string`).

## Verify
A test that triggers a page error fails with the attached error list; slow seeding no longer causes "Test timeout" failures.
