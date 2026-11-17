---
id: computing-software.qa-testing-engineering.vitest.vi-when-conditional-mocks
name: vi-when-conditional-mocks
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [vi-when, called-with-matcher, then-return, on-unmatched]
level: advanced
status: docs-checked
description: "Make a mock answer differently by arguments with vi.when (5.0+): calledWith, thenReturn, thenResolve, thenThrow, times, LIFO matching and onUnmatched."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/vi.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vi.when(spy)` (Vitest 5.0.0) builds argument-dependent behaviour on a mock or spy.

```ts
const getUser = vi.fn()

vi.when(getUser)
  .calledWith(1)
  .thenReturn({ id: 1, name: 'Ann' })
  .calledWith(2)
  .thenResolve({ id: 2 })
  .calledWith(3)
  .thenThrow(new Error('not found'))
  .calledWith(expect.any(String))
  .thenReturn(null)
```

`vi.when` replaces the spy's implementation for the duration of the chain. Terminators: `thenReturn`, `thenReturnOnce`, `thenThrow`, `thenResolve`, `thenReject`. The `times` option on the non-`Once` forms limits how many times a behavior applies.

Rules from the docs:
- Behaviors for the same arguments are consumed last-in, first-out: the newest is tried first and, once exhausted, earlier ones act as fallbacks.
- Arguments support asymmetric matchers such as `expect.any()`.
- `thenThrowOnce`, `thenResolveOnce` and `thenRejectOnce` also exist.
- `onUnmatched` decides what happens when no rule fits: `'passthrough'` (call the original), `'throw'`, or a function.
- `vi.isWhenChain(x)` tests whether a value is a chain.

The `When` object supports `expect(w).toHaveBeenExhausted()`, which passes once every registered behavior has been consumed. Arguments use `toEqual` deep equality. With `using`, the spy's original implementation is restored when the block exits.

## Checked

2026-11-04. Confirmed against api/vi.md (vi.when and vi.isWhenChain, both 5.0.0): the chain form, all `then*` methods, `times`, last-in-first-out ordering, asymmetric matchers, the three `onUnmatched` options with `passthrough` as default, `toHaveBeenExhausted`, and `using`. The dead recipes/conditional-mocking.md source (404) was dropped and the example rewritten as one chain as the page shows.

Method: documentation only; no commands were run.
