---
id: computing-software.qa-testing-engineering.vitest.expect-resolves-rejects-throw
name: expect-resolves-rejects-throw
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [expect-resolves, expect-rejects, to-throw, expect-assertions]
level: intro
status: docs-checked
description: "Assert promises and errors in Vitest with resolves, rejects and toThrow, always awaiting the assertion, and guard async tests with expect.assertions."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/expect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
await expect(Promise.resolve('ok')).resolves.toBe('ok')
await expect(Promise.reject(new Error('boom'))).rejects.toThrow('boom')

expect(() => parse('')).toThrow()
expect(() => parse('')).toThrow('empty input')
expect(() => parse('')).toThrow(/empty/)
```

- `resolves` and `rejects` unwrap the promise, then chain any matcher. They must be awaited: an assertion that is not awaited marks the test as failed at the end of the test.
- `toThrow` needs the throwing code wrapped in a function, otherwise the error escapes before `expect` sees it.
- `toThrow` takes an optional argument: a `RegExp` (message matches), a `string` (message includes it), or any other value, compared with the thrown value by deep equality.

Guard callbacks that might never run:

```ts
test('calls back', async () => {
  expect.assertions(1)
  await run((v) => expect(v).toBe(1))
})
```

`expect.assertions(n)` is checked after the test has passed or failed; `expect.hasAssertions()` only requires at least one assertion. Snapshot variants for errors: `toThrowErrorMatchingSnapshot` and `toThrowErrorMatchingInlineSnapshot`.

`expect.poll` does not support `resolves`, `rejects` or `toThrow`.

## Checked

2026-11-04. Confirmed against api/expect.md: `resolves`, `rejects` and the not-awaited warning, `toThrow` argument forms and function-wrapping tip, `expect.assertions`, `expect.hasAssertions`, snapshot error matchers, `expect.poll` limits. Replaced the claim that `toThrow` accepts an error class, which the page does not state.

Method: documentation only; no commands were run.
