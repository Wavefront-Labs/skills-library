---
id: computing-software.qa-testing-engineering.vitest.setup-teardown-hooks
name: setup-teardown-hooks
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [before-each, after-each, before-all, hook-timeout]
level: intro
status: docs-checked
description: "Use beforeEach, afterEach, beforeAll and afterAll in Vitest, return cleanup functions from the before hooks, and set the per-hook timeout."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/hooks.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/test-context.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/migration/jest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { afterAll, beforeAll, beforeEach } from 'vitest'

beforeAll(async () => {
  await startServer()
  return async () => { await stopServer() } // cleanup, runs after the suite
})

beforeEach(async () => {
  await resetState()
  return () => clearTimers() // cleanup, runs after each test
})

afterAll(async () => {
  await closeConnections()
}, 20_000) // optional timeout
```

- Each hook accepts an optional timeout as the last argument; the default is 10 seconds (`hookTimeout`).
- `beforeEach` and `beforeAll` may return a cleanup function; it runs after all other `afterEach` (or `afterAll`) hooks.
- The `test.beforeEach` style (called on an extended `test`) gives hooks typed access to fixtures.
- Hooks do not run when Vitest is used as a type checker.

Because `beforeEach` and `beforeAll` may return a teardown function, a hook declared as `beforeEach(() => setActivePinia(createTestingPinia()))` that returns something other than `undefined` or `null` must be rewritten with braces: `beforeEach(() => { setActivePinia(createTestingPinia()) })` (Jest migration note).

## Checked

2026-11-04. Confirmed against api/hooks.md, guide/test-context.md and guide/migration/jest.md: the four hooks, the 10 second default and `hookTimeout`, returned cleanup functions and their order, `test.beforeEach` and friends for fixtures, the type-checker note, and the Jest migration rewrite.

Method: documentation only; no commands were run.
