---
id: computing-software.qa-testing-engineering.vitest.vi-domock-unmock-reset
name: vi-domock-unmock-reset
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [vi-domock, vi-unmock, vi-reset-modules, vi-import-actual]
level: advanced
status: docs-checked
description: "Mock per test with non-hoisted vi.doMock, undo with vi.unmock and doUnmock, load originals with vi.importActual, and reset the module cache with vi.resetModules."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/vi.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/migration/jest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vi.doMock` is the non-hoisted twin of `vi.mock`. It affects only imports made after it runs, so use dynamic `import()`.

```ts
test('per-test mock', async () => {
  vi.doMock('./config.js', () => ({ mode: 'test' }))
  const { run } = await import('./app.js')
  expect(run()).toBe('test')
})
```

It returns a Disposable, so `using _ = vi.doMock(...)` works.

- `vi.unmock(path)` (hoisted) and `vi.doUnmock(path)` remove a mock.
- `vi.importActual(path)` loads the real module even when mocked. It replaces Jest's `requireActual`.
- `vi.importMock(path)` loads the automocked version.
- `vi.resetModules()` clears the module cache so the next import re-evaluates the module. It does not reset the mock registry.
- `vi.dynamicImportSettled()` waits for pending dynamic imports.
- `vi.mocked(obj, { partial, deep })` is a type helper only.

- `vi.mock` does not work with `require`.
- Modules imported inside setup files are not mocked.

## Checked

2026-11-04. Confirmed against api/vi.md and guide/migration/jest.md: `vi.doMock` and its Disposable return, `vi.unmock` and `vi.doUnmock`, `vi.importActual` replacing `requireActual`, `vi.importMock`, `vi.resetModules` not resetting the mock registry, `vi.dynamicImportSettled`, `vi.mocked` options, and the `require` and setup-file limitations.

Method: documentation only; no commands were run.
