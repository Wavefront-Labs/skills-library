---
id: computing-software.qa-testing-engineering.jest-pytest.jest-setup-and-teardown
name: jest-setup-and-teardown
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [jest-setup-teardown, beforeeach, afterall, describe-scoping, jest]
level: practitioner
status: verified
description: "Use Jest beforeEach/afterEach/beforeAll/afterAll with correct describe scoping and order, async setup, and the collection-vs-execution phase gotcha."
sources:
  - https://jestjs.io/docs/setup-teardown
  - https://jestjs.io/docs/api#beforeallfn-timeout
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setup and teardown hooks and describe scoping

```js
beforeAll(async () => { await db.connect(); });      // once per file (top level)
afterAll(async () => { await db.disconnect(); });
beforeEach(() => { jest.useFakeTimers(); });
afterEach(() => { jest.useRealTimers(); jest.restoreAllMocks(); });

describe('orders', () => {
  beforeEach(async () => { await db.seed('orders'); });   // only for tests in this block
  test('lists', async () => { ... });
});
```

## Order of execution
For nested describes: all outer `beforeEach` run before inner `beforeEach`; `afterEach` run inner first, then outer. `beforeAll` of a describe runs before any of its tests.

## Collection vs execution phase
Jest runs **all describe bodies first** (collection), then the tests. Code directly inside `describe` (not in a hook or test) runs at collection time:
```js
describe('x', () => {
  const user = createUser();     // runs during collection, before any beforeAll!
  beforeAll(() => db.connect());
});
```
Put setup in hooks.

## Async hooks
Return a promise or use `async`; a `done` callback also works but don't mix both. Mixing `async` with a `done` parameter fails the hook ("Test functions cannot both take a 'done' callback and return something"; ran). Hook timeout: second argument (`beforeAll(fn, 30_000)`) or `testTimeout` config.

## Global setup
- `setupFiles`: run before the test framework is installed (polyfills, env vars).
- `setupFilesAfterEnv`: run after framework install in each test file (custom matchers, `jest-dom`, global hooks).
- `globalSetup` / `globalTeardown`: once per run in a separate context (start DB containers); values pass via `process.env` or files, not globals.

## Gotchas
- If `beforeAll` throws, Jest (circus) skips the tests, marks them failed and still runs `afterAll` (ran), so put cleanup in `afterAll` rather than at the end of the failing hook. Handles that are never closed make Jest report that it "did not exit one second after the test run"; `--detectOpenHandles` prints where the timer or socket was created (ran: it named the `setInterval` line).
- `test.concurrent` tests share `beforeEach` timing differently; avoid shared mutable state.

## Verify
`npx jest --detectOpenHandles` exits cleanly; running a single test with `-t` passes alone.
