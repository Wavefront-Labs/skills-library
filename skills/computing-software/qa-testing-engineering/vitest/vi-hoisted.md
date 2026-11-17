---
id: computing-software.qa-testing-engineering.vitest.vi-hoisted
name: vi-hoisted
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [vi-hoisted, hoisting, mock-factory-variables, vi-mock-hoisting]
level: practitioner
status: docs-checked
description: "Share variables with a hoisted vi.mock factory using vi.hoisted, and understand why referencing top-level variables from the factory otherwise fails."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/vi.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/mocking/modules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vi.mock` calls are moved above all imports, and Vitest converts static imports into dynamic ones when a file contains `vi.mock`. A factory therefore runs before your top-level `const` declarations exist. Wrap the values in `vi.hoisted`, which runs its callback before the imports and returns the callback's value.

```ts
import { expect, vi } from 'vitest'
import { fetchUser } from './api.js'

const mocks = vi.hoisted(() => ({
  fetchUser: vi.fn(),
}))

vi.mock(import('./api.js'), () => ({
  fetchUser: mocks.fetchUser,
}))

mocks.fetchUser.mockResolvedValue({ id: 1 })
expect(await fetchUser()).toEqual({ id: 1 })
```

- The callback may be async (`await vi.hoisted(async () => ...)`), even where top-level await is not supported.
- Use it for mock functions or locally defined variables a `vi.mock` factory needs.
- Imported variables are not available inside the callback (it fails with `Cannot access '__vi_import_0__' before initialization`). Use `await import(...)` inside an async callback if you must, though the page discourages importing there.
- `vi` must be imported directly from `vitest` (not via a utility file), or `globals` enabled, so Vitest can find and hoist `vi.mock`.

## Checked

2026-11-04. Confirmed against api/vi.md (vi.hoisted section and the vi.mock hoisting warning) and guide/mocking/modules.md (the static-to-dynamic import transform when `vi.mock` is present). Removed: advice to use `importOriginal` instead of hoisting, which the pages do not state.

Method: documentation only; no commands were run.
