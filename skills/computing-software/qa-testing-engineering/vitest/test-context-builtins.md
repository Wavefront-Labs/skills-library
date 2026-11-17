---
id: computing-software.qa-testing-engineering.vitest.test-context-builtins
name: test-context-builtins
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [test-context, context-skip, annotate, abort-signal]
level: practitioner
status: docs-checked
description: "Use the built-in Vitest test context: task, expect, skip, annotate, signal, bench, onTestFailed and onTestFinished, passed as the first test argument."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/test-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every test callback receives a context object as its first argument.

```ts
import { test } from 'vitest'

test('uses context', async ({ task, expect, skip, signal }) => {
  skip(process.platform === 'win32', 'unix only')
  const res = await fetch('http://localhost:3000', { signal })
  expect(res.ok).toBe(true)
})
```

Built-ins:
- `task`: the test's task metadata.
- `expect`: assertion bound to this test (use it in concurrent tests and snapshots).
- `skip(note?)` always skips; `skip(condition, note?)` skips conditionally (since 3.1).
- `annotate`: add a test annotation (3.2.0).
- `signal`: an `AbortSignal` aborted on timeout, Ctrl+C or bail (3.2.0).
- `bench`: benchmark fixture (5.0.0).
- `onTestFailed`, `onTestFinished`: per-test callbacks.

When using `test.extend()` fixtures, use object destructuring (`({ database }) => ...`) to access the context, in both the fixture function and the test function.

## Checked

2026-11-04. Confirmed against guide/test-context.md: the first-argument context, each built-in with its version tag (`skip` condition 3.1, `annotate` and `signal` 3.2.0, `bench` 5.0.0), the signal abort conditions, concurrent snapshot use of `expect`, and the destructuring rule. Removed: a lazy-initialisation claim the page does not state.

Method: documentation only; no commands were run.
