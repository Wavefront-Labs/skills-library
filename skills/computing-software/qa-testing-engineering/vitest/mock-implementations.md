---
id: computing-software.qa-testing-engineering.vitest.mock-implementations
name: mock-implementations
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [mock-implementation, mock-return-value, mock-resolved-value, mock-throw]
level: intro
status: docs-checked
description: "Program Vitest mocks with mockImplementation, mockReturnValue, mockResolvedValue, mockRejectedValue, mockThrow and their Once variants, and withImplementation."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/mock.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
const fn = vi
  .fn()
  .mockReturnValue('default')
  .mockReturnValueOnce('first call')
  .mockReturnValueOnce('second call')
// 'first call', 'second call', 'default', 'default'

const api = vi.fn().mockResolvedValue({ ok: true })
const bad = vi.fn().mockRejectedValueOnce(new Error('down'))
const thrower = vi.fn().mockThrow(new Error('boom')) // 4.1.0
```

Methods: `mockImplementation(fn)`, `mockImplementationOnce(fn)`, `mockReturnValue(v)`, `mockReturnValueOnce(v)`, `mockResolvedValue(v)`, `mockResolvedValueOnce(v)`, `mockRejectedValue(e)`, `mockRejectedValueOnce(e)`, `mockThrow(v)` and `mockThrowOnce(v)` (4.1.0), `mockReturnThis()`.

`withImplementation(impl, callback)` swaps the implementation only while the callback runs.

`getMockImplementation()` returns the current implementation.

Gotchas:
- Chained `Once` values are consumed in order, then the default applies.
- Return-value helpers cannot be used when the mock is called with `new`; give it a class implementation instead.
- Spies inherit `length` from the original function when initialized, but a later `mockImplementation` does not change it.

## Checked

2026-11-04. Confirmed against api/mock.md: every method listed, the 4.1.0 version tag on `mockThrow` and `mockThrowOnce`, the chained-Once example, the class-support warning, withImplementation, getMockImplementation and the length note.

Method: documentation only; no commands were run.
