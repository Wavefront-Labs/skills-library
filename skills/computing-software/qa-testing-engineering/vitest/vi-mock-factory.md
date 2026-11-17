---
id: computing-software.qa-testing-engineering.vitest.vi-mock-factory
name: vi-mock-factory
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [vi-mock, mock-factory, import-original, partial-mock]
level: practitioner
status: docs-checked
description: "Replace a module with vi.mock and a factory in Vitest, keep part of the original via importOriginal, type it with import(), and mock default exports correctly."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/mocking/modules.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/vi.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/migration/jest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { expect, vi } from 'vitest'
import { answer } from './example.js'

vi.mock(import('./example.js'), async (importOriginal) => {
  const original = await importOriginal()
  return {
    answer: vi.fn(original.answer), // tracked, still calls the real one
    variable: 'mock',
  }
})

expect(answer()).toBe(42)
expect(answer).toHaveBeenCalled()
```

- `vi.mock` is hoisted above imports; Vitest turns static imports into dynamic ones so the mock registers first.
- The factory may be async. `importOriginal` is async and must be awaited.
- `vi.mock(import('./x'))` (a module promise) lets TypeScript type `importOriginal`; Vitest strips the `import()`.
- A method the factory does not return throws a helpful error on access. Use `vi.fn()` for exports you want to track.
- Default export: return `{ default: ... }`. This differs from Jest, where the factory result is the default export.
- Call `vi.mock` in a `setupFiles` file to mock in every test file.

- The `vi` import must come from `vitest`, or `globals` must be enabled, for hoisting to work.
- Calls between functions inside the same file cannot be mocked from outside, because they reference each other directly; this affects only calls from other modules.

## Checked

2026-11-04. Confirmed against guide/mocking/modules.md, api/vi.md and guide/migration/jest.md: the factory example with `importOriginal`, hoisting and the static-to-dynamic import transform, the async factory and awaited `importOriginal`, `import()` typing, the helpful error for unreturned exports, `{ default }` versus Jest, `setupFiles`, the `vi` import requirement, and the same-file call pitfall. Removed: a "split code or inject the dependency" suggestion the pages do not make.

Method: documentation only; no commands were run.
