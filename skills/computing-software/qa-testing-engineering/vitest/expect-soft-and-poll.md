---
id: computing-software.qa-testing-engineering.vitest.expect-soft-and-poll
name: expect-soft-and-poll
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [expect-soft, expect-poll, expect-assert, poll-interval]
level: practitioner
status: docs-checked
description: "Use expect.soft to keep a test running after a failed assertion, expect.poll to retry an async value until it passes, and expect.assert to narrow types."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/expect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`expect.soft` records a failure but continues the test; the test still fails at the end. Use it only inside a test.

```ts
test('form', () => {
  expect.soft(form.title).toBe('Hello')
  expect.soft(form.count).toBe(3)
})
```

`expect.poll` retries a function until the assertion passes or the timeout is hit. It must be awaited.

```ts
await expect.poll(() => fetchStatus(), { interval: 50, timeout: 1000, message: 'status never ready' }).toBe('ready')
```

Options: `interval`, `timeout`, `message`. Not supported with poll: snapshot matchers, `resolves`, `rejects` and `toThrow`. With fake timers it advances them automatically.

`expect.assert(cond)` is a Chai-style assertion that narrows types for TypeScript.

Other helpers: `expect.assertions(n)`, `expect.hasAssertions()`, `expect.fail(msg)` and `expect.unreachable()`.

`expect.poll` makes every assertion asynchronous. Since Vitest 3, forgetting to await it fails the test with a warning. The docs suggest `vi.waitFor` to resolve a flaky value first when you need a snapshot matcher.

## Checked

2026-11-04. Confirmed against api/expect.md: `expect.soft` behaviour and test-only warning, `expect.poll` options, message, fake timer advance, unsupported matchers, `expect.assert` type narrowing, the other helpers. Replaced a claim that an un-awaited poll silently never asserts; the page says the test fails with a warning.

Method: documentation only; no commands were run.
