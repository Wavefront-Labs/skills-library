---
id: computing-software.qa-testing-engineering.vitest.mock-clear-reset-restore
name: mock-clear-reset-restore
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [mock-clear, mock-reset, mock-restore, restore-all-mocks]
level: practitioner
status: docs-checked
description: "Tell mockClear, mockReset and mockRestore apart in Vitest, use vi.clearAllMocks, resetAllMocks and restoreAllMocks, and automate them with config options."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/mock.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/vi.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/migration/jest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `mockClear()`: clears all call information; properties on `.mock` return to their initial state. Implementations stay.
- `mockReset()`: does what `mockClear` does and resets the implementation, including "once" implementations. A mock from `vi.fn()` becomes an empty function returning `undefined`; one from `vi.fn(impl)` goes back to `impl` (Jest always uses the empty function).
- `mockRestore()`: does what `mockReset` does, and also restores the original descriptors of spied-on objects if the mock came from `vi.spyOn`. On a `vi.fn()` mock it is identical to `mockReset`.

Global versions: `vi.clearAllMocks()` and `vi.resetAllMocks()` call `mockClear` and `mockReset` on all spies. `vi.restoreAllMocks()` restores the original implementations of `vi.spyOn` spies but, unlike `mockRestore`, does not clear history or reset implementations.

Config options `clearMocks`, `mockReset` and `restoreMocks` automate these (the docs say `mockReset` runs before each test, and suggest `restoreMocks` or `vi.restoreAllMocks()` in `afterEach`):

```ts
export default defineConfig({
  test: {
    clearMocks: true,
    // or mockReset: true
    // or restoreMocks: true
  },
})
```

Related: `vi.unstubAllEnvs()` and `vi.unstubAllGlobals()` undo stubs made with `vi.stubEnv` and `vi.stubGlobal`.

When migrating from Jest, code relying on `mockReset` to produce `undefined` returns now gets the original `vi.fn(impl)` implementation.

## Checked

2026-11-04. Confirmed against api/mock.md (`mockClear`, `mockReset`, `mockRestore`), api/vi.md (`clearAllMocks`, `resetAllMocks`, `restoreAllMocks` and its difference from `mockRestore`, `unstubAllEnvs`, `unstubAllGlobals`) and guide/migration/jest.md (`mockReset` difference). Removed claims that the pages do not state: one mode per project, all three options running before each test, and `unstubEnvs` and `unstubGlobals` config options.

Method: documentation only; no commands were run.
