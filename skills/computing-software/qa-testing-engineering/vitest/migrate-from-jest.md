---
id: computing-software.qa-testing-engineering.vitest.migrate-from-jest
name: migrate-from-jest
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [migrate-from-jest, jest-differences, globals-config, jest-compat]
level: practitioner
status: docs-checked
description: "Move a Jest suite to Vitest: enable globals or import from vitest, rewrite default-export mock factories, replace requireActual, fix hook returns and test name separators."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/migration/jest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Checklist of documented differences:
- Globals are off by default. Enable the `globals` option or import from `vitest`. With globals off, libraries like testing-library skip automatic DOM cleanup.
- Module factory: return an object with explicit exports, e.g. `vi.mock('./some-path', () => ({ default: 'hello' }))`.
- `jest.requireActual` becomes `await vi.importActual(...)`.
- `__mocks__` modules load only when `vi.mock()` is called; to mock everywhere, do it in `setupFiles`.
- To mock a module used by third-party libraries too, add them to `server.deps.inline`.
- `mockReset` restores the original `vi.fn(impl)` rather than emptying it.
- `mock.mock` is a persistent reference.
- Hooks may return cleanup functions: change `beforeEach(() => setActivePinia(...))` to a braced body. Hooks run as a stack; set `sequence.hooks: 'list'` for Jest behaviour.
- Test names join with `>`, so `-t 'math adds'` becomes `-t 'math > adds'`.
- No `done` callback; use async/await or promises.
- No legacy timers. `jest.setTimeout(n)` becomes `vi.setConfig({ testTimeout: n })`.
- Types: import `Mock` from `vitest`, not a `jest` namespace.
- Env: `VITEST_POOL_ID` replaces `JEST_WORKER_ID`; `VITEST_WORKER_ID` is a unique worker id.
- Custom snapshot matchers use the `Snapshots` export from `vitest` instead of `jest-snapshot` (experimental, 4.1.3).

## Checked

2026-11-04. Confirmed against guide/migration/jest.md: every item in the checklist, including the `-t` example, `VITEST_POOL_ID` and `VITEST_WORKER_ID`, `sequence.hooks: 'list'`, `vi.setConfig`, and the `Snapshots` export.

Method: documentation only; no commands were run.
