---
id: computing-software.qa-testing-engineering.vitest.test-options-timeout-retry
name: test-options-timeout-retry
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [test-timeout, test-retry, test-repeats, test-fails]
level: practitioner
status: docs-checked
description: "Set per-test Vitest options timeout, retry (number or object with delay and condition), repeats, meta and fails, and avoid the timeout-plus-options argument clash."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/test.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/vi.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { test } from 'vitest'

test('flaky network call', { timeout: 10_000, retry: 2 }, async () => {})

test('retry with a delay', {
  retry: { count: 3, delay: 500 }, // object form since 4.1
}, async () => {})

test('stable under repeats', { repeats: 5 }, () => {})

test('known bug', { fails: true }, () => { expect(1).toBe(2) })
```

Options: `timeout`, `retry`, `repeats`, `tags`, `meta`, `concurrent`, `skip`, `only`, `todo`, `fails`.

- The default test timeout is 5 seconds (`testTimeout`). Hooks default to 10 seconds (`hookTimeout`).
- `retry` is a number, or an object `{ count, delay, condition }`.
- `fails: true` means the test is expected to fail: if it does, the test passes, otherwise it fails.
- A timeout passed as the last positional argument cannot be combined with an options object. Put `timeout` inside the options instead.

Timeout can also be changed at runtime with `vi.setConfig({ testTimeout: 5_000 })`.

## Checked

2026-11-04. Confirmed against api/test.md, api/vi.md and api/hooks.md: the options list, the 5 second test timeout and `testTimeout`, the 10 second hook timeout, the retry type with count, delay and condition (object form since 4.1), repeats, `fails`, the timeout-plus-options warning, and `vi.setConfig` with `testTimeout`.

Method: documentation only; no commands were run.
