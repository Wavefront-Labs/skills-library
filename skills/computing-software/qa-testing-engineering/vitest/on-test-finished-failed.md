---
id: computing-software.qa-testing-engineering.vitest.on-test-finished-failed
name: on-test-finished-failed
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [on-test-finished, on-test-failed, test-cleanup, reverse-order]
level: practitioner
status: docs-checked
description: "Register per-test cleanup with onTestFinished and failure-only diagnostics with onTestFailed inside a Vitest test body, and use the context versions in concurrent tests."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/hooks.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/test-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both hooks are valid only inside a running test body (not at file or describe level).

```ts
import { onTestFailed, onTestFinished, test } from 'vitest'

test('uses a temp resource', async () => {
  const conn = await connect()
  onTestFinished(() => conn.close()) // always runs
  onTestFailed(() => console.log(conn.diagnostics())) // only on failure
  await conn.run()
})
```

- `onTestFinished` callbacks always run, in reverse registration order, and are not affected by `sequence.hooks`.
- `onTestFailed` runs only when the test fails. Both run after the `afterEach` hooks and receive the test context.

In concurrent tests, always take them from the test context (`test.concurrent('x', ({ onTestFinished }) => {})`), because Vitest does not track concurrent tests in global hooks.

Both also exist as context properties bound to the current test.

## Checked

2026-11-04. Confirmed against api/hooks.md and guide/test-context.md: the hooks throw outside a test body, onTestFinished always runs (reverse order, unaffected by `sequence.hooks`), onTestFailed runs only after a failure, both run after afterEach, and the context versions are required for concurrent tests. Removed: an unstated advice bullet and a cross-reference to another skill.

Method: documentation only; no commands were run.
