---
id: computing-software.qa-testing-engineering.vitest.wait-for-and-wait-until
name: wait-for-and-wait-until
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [vi-wait-for, vi-wait-until, retry-callback, wait-options]
level: practitioner
status: docs-checked
description: "Retry a callback until it stops throwing with vi.waitFor, or until it returns a truthy value with vi.waitUntil, and set timeout, interval and message."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/vi.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
await vi.waitFor(() => {
  expect(server.isReady).toBe(true) // retried while it throws
}, { timeout: 2000, interval: 100 })

const element = await vi.waitUntil(() => document.querySelector('#ready'), {
  timeout: 2000,
  message: 'element never appeared',
})
```

- `vi.waitFor(cb, options)` waits for `cb` to succeed: while it throws or returns a rejected promise it keeps waiting, until it succeeds or times out. It returns a Promise of the callback's result.
- `vi.waitUntil(cb, options)` waits until `cb` returns a truthy value and returns it; a falsy return keeps polling, but if `cb` throws, waiting stops immediately with an error.
- A number as options means `{ timeout: n }`.
- Defaults: timeout 1000 ms, interval 50 ms.
- `message` describes what is awaited; on failure Vitest prefixes it to the error (for example `Error: user saved: Timed out in waitUntil!`).
- With `vi.useFakeTimers`, `vi.waitFor` automatically calls `vi.advanceTimersByTime(interval)` in every check callback.

Both return Promises, so await them.

## Checked

2026-11-04. Confirmed against api/vi.md (vi.waitFor and vi.waitUntil): behaviour on throw and falsy returns, the numeric options shorthand, the 1000 ms timeout and 50 ms interval defaults, the `message` option, and the fake-timers advance for `vi.waitFor`. Removed: a rethrow-the-last-error gotcha, a side-effect warning and an `expect.poll` recommendation that the page does not state, and the claim that `vi.waitUntil` also advances fake timers. The dead recipes/wait-for.md source (404) was dropped.

Method: documentation only; no commands were run.
