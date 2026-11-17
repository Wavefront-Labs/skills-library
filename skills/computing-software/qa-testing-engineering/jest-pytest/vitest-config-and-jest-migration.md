---
id: computing-software.qa-testing-engineering.jest-pytest.vitest-config-and-jest-migration
name: vitest-config-and-jest-migration
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [vitest-config, vitest, jest-migration, vi-mock]
level: practitioner
status: verified
description: "Configure Vitest (environment, globals, setupFiles, coverage, workspace) and migrate from Jest: jest to vi API mapping, mock hoisting, timers and snapshot differences."
sources:
  - https://vitest.dev/config/
  - https://vitest.dev/guide/migration.html
  - https://vitest.dev/guide/mocking.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vitest configuration and migrating from Jest

## Config
```ts
// vitest.config.ts (or the `test` key in vite.config.ts)
import { defineConfig } from 'vitest/config';
export default defineConfig({
  test: {
    environment: 'jsdom',          // 'node' default; also 'happy-dom'
    globals: true,                 // describe/it/expect without imports (add "vitest/globals" to tsconfig types)
    setupFiles: ['./test/setup.ts'],
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
    restoreMocks: true,
    coverage: { provider: 'v8', reporter: ['text', 'lcov'], thresholds: { lines: 85, branches: 80 } },
    pool: 'forks',                 // default; or 'threads' / 'vmThreads' / 'vmForks'
  },
});
```
Multiple configs: `projects` (`workspace` is deprecated since Vitest 3.2 and replaced by `projects`). Per-file environment: `// @vitest-environment jsdom`.

## API mapping
| Jest | Vitest |
|---|---|
| `jest.fn()`, `jest.spyOn` | `vi.fn()`, `vi.spyOn` |
| `jest.mock(path, factory)` | `vi.mock(path, factory)` (hoisted; factory may be async; use `vi.importActual`) |
| `jest.requireActual` | `await vi.importActual()` |
| `jest.useFakeTimers()` | `vi.useFakeTimers()` |
| `jest.setTimeout` | `vi.setConfig({ testTimeout })` or per-test timeout arg |
| `done` callbacks | not supported: return a promise (ran on Vitest 4.1: the test passed in 2 ms and the late `done()` surfaced as an unhandled error; the migration guide says the callback style is unsupported) |
| `jest.mock('x', () => 'hello')` | `vi.mock('x', () => ({ default: 'hello' }))` |

`vi.mock` is hoisted; factories can't reference outer variables unless they're created with `vi.hoisted(() => ...)` (ran, with `vi.importActual` in an async factory).

## Migration steps
1. Install `vitest`, coverage provider, environment package.
2. Rename `jest.` to `vi.`; switch `jest.config` options to `test:` options.
3. `globals: true` to minimise import churn, or add `import { describe, it, expect, vi } from 'vitest'`.
4. Re-record snapshots if the serializer differs (header comment and some formatting differ).
5. Remove Babel/ts-jest transforms: Vite handles TS/ESM natively.

## Gotchas
- Module mocks of default exports need `{ default: ... }` in the factory (the factory must return every export explicitly).
- Vitest only uses `<root>/__mocks__` after `vi.mock()` is called; Jest loads root mocks for node_modules automatically.
- `mockReset` replaces the implementation with `undefined` in Jest (30) but restores the original in Vitest (ran: `vi.fn(() => 1)` still returned 1 after `mockReset`; a spy returned the real value).
- Hooks run as a stack by default in Vitest; Jest runs them in definition order (`sequence.hooks` controls it).
- Vitest runs files in isolated workers; global state leaks are less common but `isolate: false` (speed) brings them back.

## Verify
`npx vitest run --coverage` matches the Jest pass count and coverage within a point or two; with `thresholds` set below the measured value it exits non-zero (ran with `@vitest/coverage-v8`, which must match the Vitest version).
