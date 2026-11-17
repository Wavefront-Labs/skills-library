---
id: computing-software.qa-testing-engineering.vitest.fixtures-test-extend
name: fixtures-test-extend
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [test-extend, fixtures, fixture-cleanup, auto-fixture]
level: practitioner
status: docs-checked
description: "Create reusable Vitest fixtures with test.extend in the builder form (4.1+) or the object form with use(), with cleanup, lazy init and auto fixtures."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/test-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Builder form (Vitest 4.1+): each `.extend(name, value | fn)` adds one fixture. The function gets the context first and `{ onCleanup }` second.

```ts
import { test as baseTest } from 'vitest'

export const test = baseTest
  .extend('config', { port: 3000, host: 'localhost' })
  .extend('server', async ({ config }) => `http://${config.host}:${config.port}`)
  .extend('tempFile', async ({}, { onCleanup }) => {
    const file = await createTempFile()
    onCleanup(async () => { await removeFile(file) })
    return file
  })
  .extend('metrics', { auto: true }, () => startMetrics())
```

Object form (Playwright style) uses `use()`:

```ts
const test = baseTest.extend({
  todos: async ({}, use) => {
    await use([1, 2, 3])
  },
})
```

Rules:
- Fixtures are lazy: created only when a test or another fixture destructures them.
- `auto: true` runs the fixture even when no test asks for it.
- `onCleanup` can be called only once per fixture; split into several fixtures for more.
- Suite-level hooks needing fixtures must be called on the extended test (`test.beforeAll`).

Always use object destructuring (`{ database }`) to read fixtures, in fixtures and in tests; reading `context.database` from an undestructured argument does not work.

## Checked

2026-11-04. Confirmed against guide/test-context.md: builder form (4.1.0) and `onCleanup`, object form with `use()`, `auto`, lazy initialisation by usage, the once-per-fixture `onCleanup` warning, the destructuring warning, and suite-level hooks on the extended test.

Method: documentation only; no commands were run.
