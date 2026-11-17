---
id: computing-software.qa-testing-engineering.playwright.custom-test-and-worker-fixtures
name: custom-test-and-worker-fixtures
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, playwright-fixtures, worker-fixtures, test-extend, fixture-scope, typescript, auto-fixtures]
level: practitioner
status: verified
description: "Build custom Playwright fixtures with test.extend: test- and worker-scoped fixtures, setup/teardown around use(), automatic fixtures, option fixtures and composition."
sources:
  - https://playwright.dev/docs/test-fixtures
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playwright custom test and worker fixtures

**Goal:** encapsulate setup/teardown (page objects, seeded data, accounts, servers) as fixtures that tests request by name.

## Test-scoped fixtures
```ts
// fixtures.ts
import { test as base, expect } from '@playwright/test'
import { TodoPage } from './pages/todo-page'

type Fixtures = { todoPage: TodoPage; apiUser: { id: string; token: string } }

export const test = base.extend<Fixtures>({
  apiUser: async ({ request }, use) => {
    const res = await request.post('/api/test-users')       // setup
    const user = await res.json()
    await use(user)                                          // test runs here
    await request.delete(`/api/test-users/${user.id}`)       // teardown, runs even if test fails
  },
  todoPage: async ({ page, apiUser }, use) => {             // fixtures can depend on fixtures
    const todo = new TodoPage(page)
    await todo.goto()
    await use(todo)
  },
})
export { expect }
```
Tests import `test` from `./fixtures` and declare what they need: `test('adds', async ({ todoPage }) => ...)`. Unused fixtures are never set up (lazy).

## Worker-scoped fixtures
Shared by all tests in a worker process (expensive resources: one account per worker, a DB schema per worker):
```ts
export const test = base.extend<{}, { workerAccount: Account }>({
  workerAccount: [async ({}, use, workerInfo) => {
    const acc = await createAccount(`w${workerInfo.workerIndex}`)
    await use(acc)
    await deleteAccount(acc)
  }, { scope: 'worker' }],
})
```

## Automatic and option fixtures
- `{ auto: true }`: runs for every test without being requested (e.g. attach console logs on failure via `testInfo.attach`).
- Option fixtures: `[ 'default', { option: true } ]`, overridden per project in config `use: { locale: 'de-DE', myOption: 'x' }`.
- `{ timeout: 60_000 }` gives a slow fixture its own timeout.

## Gotchas
- Code after `await use()` is teardown; forgetting to `await use` breaks the test.
- Worker fixtures cannot depend on test fixtures (`page`): run here `worker fixture "wpage" cannot depend on a test fixture "page" defined in <builtin>.`; they can use `browser`. Run here: an unused fixture was never set up, and a fixture's teardown after `use()` ran although the test failed.
- Use `mergeTests` to combine fixture sets from different modules (run here: an option fixture merged with another extended `test` kept both, and the option read `standard` and `gold` under two projects).
- `workerIndex` grows after worker restarts; for a fixed pool of accounts use `parallelIndex` (see `workers-and-parallel-index-isolation`).

## Verify
`npx playwright test --list` works; deliberately fail a test and confirm teardown still cleaned the data.
