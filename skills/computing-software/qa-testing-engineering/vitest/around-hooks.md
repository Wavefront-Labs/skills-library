---
id: computing-software.qa-testing-engineering.vitest.around-hooks
name: around-hooks
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [around-each, around-all, async-local-storage, db-transaction]
level: advanced
status: docs-checked
description: "Wrap tests or suites with aroundEach and aroundAll, which must call the run function, for transactions and AsyncLocalStorage, and know their nesting order."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/hooks.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/lifecycle.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`aroundEach(runTest)` wraps every test; `aroundAll(runSuite)` wraps all tests in the suite. The callback must call the function it is given.

```ts
import { aroundEach, test } from 'vitest'

aroundEach(async (runTest) => {
  await db.transaction(runTest)
})
```

`runTest()` runs the `beforeEach` hooks, the test, fixtures accessed in the test, and the `afterEach` hooks. Use these hooks when the test must run inside a context that wraps it: AsyncLocalStorage context, tracing spans, database transactions. For plain before/after code, prefer `beforeEach` / `beforeAll` returning a cleanup function.

Rules from the docs:
- If `runTest()` is not called, the test fails with an error. If `runSuite()` is not called, the hook fails and all tests in the suite are skipped.
- Several `aroundEach` (or `aroundAll`) hooks nest; the first registered is the outermost.
- A parent suite's `aroundAll` wraps the child suite's execution.
- Order within a file: `aroundAll`, `beforeAll`, then per test `aroundEach`, `beforeEach`, the test, `afterEach`, then `afterAll`.
- The optional timeout (default 10 seconds, `hookTimeout`) applies separately to the setup phase (before the run call) and the teardown phase (after it).
- The callback receives the test context as its second argument, so fixtures can be used: `test.aroundEach(async (runTest, { db }) => { await db.transaction(runTest) })` on a test created with `test.extend`.

## Checked

2026-11-04. Confirmed against api/hooks.md and guide/lifecycle.md: the signatures, must-call rule and failure behaviour, nesting order, lifecycle order, timeout behaviour, fixture access. Removed: a rollback call inside the transaction and a reference to a "db-transaction recipe" that the pages do not contain.

Method: documentation only; no commands were run.
