---
id: computing-software.qa-testing-engineering.vitest.stub-env-and-globals
name: stub-env-and-globals
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [stub-env, stub-global, unstub-all-envs, unstub-globals]
level: practitioner
status: docs-checked
description: "Change process.env and global values for one test with vi.stubEnv and vi.stubGlobal, and undo them with the unstub functions or config options."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/vi.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/mocking/globals.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/migration/jest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { afterEach, expect, test, vi } from 'vitest'

afterEach(() => {
  vi.unstubAllEnvs()
  vi.unstubAllGlobals()
})

test('uses env', () => {
  vi.stubEnv('API_URL', 'http://localhost:3000')
  expect(process.env.API_URL).toBe('http://localhost:3000')
})

test('uses a fake global', () => {
  vi.stubGlobal('innerWidth', 500)
  expect(innerWidth).toBe(500)
})
```

- `vi.stubEnv(name, value)` sets a value on `process.env` and `import.meta.env`.
- `vi.stubGlobal(name, value)` sets a property on `globalThis`.
- `vi.unstubAllEnvs()` and `vi.unstubAllGlobals()` restore the originals.
- By default Vitest does not reset stubbed globals; turn on the `unstubGlobals` config option to restore them after each test, or call `vi.unstubAllGlobals()` manually.
- Assigning to `globalThis` or `import.meta.env` directly also works, but `vi.unstubAllGlobals` / `vi.unstubAllEnvs` cannot restore those values.

Vitest sets `NODE_ENV` to `test` if it was not already set.

## Checked

2026-11-04. Confirmed against api/vi.md, guide/mocking/globals.md and guide/migration/jest.md: stubEnv on `process.env` and `import.meta.env`, stubGlobal on `globalThis`, both unstub functions, the `unstubGlobals` option, the manual-assignment caveat, and the NODE_ENV default. Removed: the `unstubEnvs` config option, which none of the pages mention, and a generic persistence gotcha.

Method: documentation only; no commands were run.
