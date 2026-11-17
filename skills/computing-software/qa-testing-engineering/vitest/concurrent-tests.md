---
id: computing-software.qa-testing-engineering.vitest.concurrent-tests
name: concurrent-tests
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [test-concurrent, describe-concurrent, max-concurrency, sequence-concurrent]
level: practitioner
status: docs-checked
description: "Run tests inside one file concurrently with test.concurrent, describe.concurrent or sequence.concurrent, bounded by maxConcurrency, using the context expect."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/parallelism.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/test.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tests in a file are sequential by default. Mark them concurrent:

```ts
import { describe, test } from 'vitest'

describe.concurrent('suite', () => {
  test('first', async ({ expect }) => {
    await somethingSlow()
    expect(1).toBe(1)
  })
  test('second', async ({ expect }) => {
    expect(2).toBe(2)
  })
})
```

- `test.concurrent` / `describe.concurrent` run via `Promise.all`, limited by `maxConcurrency`.
- Concurrency only helps tests that `await` something; fully synchronous tests gain nothing.
- `sequence.concurrent: true` makes every test concurrent; opt one out with `{ concurrent: false }`.
- Hook order is set by `sequence.hooks`.

In concurrent tests use `expect` from the test context argument so snapshots and assertions are attributed to the right test; use `onTestFinished` and `onTestFailed` from the context too, because Vitest does not track concurrent tests in the global hooks.

## Checked

2026-11-04. Confirmed against guide/parallelism.md (sequential default, `Promise.all`, `maxConcurrency`, await-only benefit, `sequence.concurrent`, `concurrent: false`, `sequence.hooks`), api/test.md (context `expect` for concurrent tests) and api/hooks.md (context `onTestFinished`/`onTestFailed`).

Method: documentation only; no commands were run.
