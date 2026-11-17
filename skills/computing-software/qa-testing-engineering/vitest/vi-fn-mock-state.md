---
id: computing-software.qa-testing-engineering.vitest.vi-fn-mock-state
name: vi-fn-mock-state
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [vi-fn, mock-calls, mock-results, invocation-call-order]
level: intro
status: docs-checked
description: "Create a mock function with vi.fn and inspect its history through mock.calls, lastCall, results, settledResults, instances and invocationCallOrder."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/vi.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/mock.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/migration/jest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { expect, vi } from 'vitest'

const fn = vi.fn((x: number) => x * 2)
fn(1)
fn(2)

fn.mock.calls // [[1], [2]]
fn.mock.lastCall // [2]
fn.mock.results // [{ type: 'return', value: 2 }, { type: 'return', value: 4 }]
```

`vi.fn(impl?)` also accepts a class. State on `fn.mock`:
- `calls`: arguments of each call.
- `lastCall`: arguments of the last call, or `undefined`.
- `results`: `{ type: 'return' | 'throw' | 'incomplete', value }`. A function returning a rejected promise is still `'return'`.
- `settledResults`: `fulfilled`, `rejected` or `incomplete`, for awaited values.
- `instances`, `contexts`: `this` values.
- `invocationCallOrder`: global call counters, useful for ordering across mocks.

Helpers: `vi.isMockFunction(fn)`, `fn.mockName('label')` and `getMockName()` to label output.

- Objects are stored by reference in all of `mock`'s properties.
- Unlike Jest, Vitest holds a persistent reference to the mock state, so `const state = fn.mock; fn.mockClear()` leaves `state` equal to `fn.mock`.

## Checked

2026-11-04. Confirmed against api/vi.md, api/mock.md and guide/migration/jest.md: `vi.fn` with an implementation or class, the `mock` properties and result types, `vi.isMockFunction`, `mockName`, reference storage, and the persistent state difference from Jest.

Method: documentation only; no commands were run.
