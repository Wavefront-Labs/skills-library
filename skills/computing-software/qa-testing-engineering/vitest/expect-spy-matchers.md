---
id: computing-software.qa-testing-engineering.vitest.expect-spy-matchers
name: expect-spy-matchers
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [to-have-been-called, called-with, nth-called-with, chai-spy-assertions]
level: practitioner
status: docs-checked
description: "Assert on Vitest mock calls with toHaveBeenCalledWith, Times, NthCalledWith, LastCalledWith, return and resolved variants, plus the Chai-style calledOnce family."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/expect.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/mock.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
const fn = vi.fn()
fn('a', 1)

expect(fn).toHaveBeenCalled()
expect(fn).toHaveBeenCalledTimes(1)
expect(fn).toHaveBeenCalledWith('a', 1)
expect(fn).toHaveBeenLastCalledWith('a', 1)
expect(fn).toHaveBeenNthCalledWith(1, 'a', 1)
expect(fn).toHaveBeenCalledExactlyOnceWith('a', 1)
```

Jest-style set: `toHaveBeenCalled`, `toHaveBeenCalledTimes`, `toHaveBeenCalledWith`, `toHaveBeenLastCalledWith`, `toHaveBeenNthCalledWith`, `toHaveBeenCalledExactlyOnceWith`, `toHaveBeenCalledBefore` / `After`, `toHaveReturned*` and `toHaveResolved*` families, and `toHaveBeenExhausted` (5.0.0).

Chai-style (4.1.0): `called`, `callCount`, `calledWith`, `calledOnce`, `calledOnceWith`, `calledTwice`, `calledThrice`, `lastCalledWith`, `nthCalledWith`, `returned*`, `calledBefore`, `calledAfter`, e.g. `expect(fn).to.have.been.calledOnce`.

Mock state stores objects by reference. If your code mutates an object after the call, `toHaveBeenCalledWith` compares against the mutated object. Clone the argument inside the mock implementation (`structuredClone`) when you need the value at call time.

## Checked

2026-11-04. Confirmed against api/expect.md (every matcher name, the 4.1.0 Chai-style family, `toHaveBeenExhausted` 5.0.0) and api/mock.md (objects stored by reference, clone with `structuredClone`).

Method: documentation only; no commands were run.
