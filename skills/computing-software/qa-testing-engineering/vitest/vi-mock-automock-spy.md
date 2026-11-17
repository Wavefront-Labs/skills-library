---
id: computing-software.qa-testing-engineering.vitest.vi-mock-automock-spy
name: vi-mock-automock-spy
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [automock, mocks-folder, mock-spy-true, spied-module]
level: practitioner
status: docs-checked
description: "Automock a module with vi.mock(path), know the automocking algorithm, use __mocks__ folders, and keep original behaviour with vi.mock(path, { spy: true })."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/mocking/modules.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/vi.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/migration/jest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vi.mock(import('./example.js'))` with no factory automocks. If `./__mocks__/example.js` exists, it is loaded instead. For packages, the `__mocks__` folder lives at the project root. Otherwise Vitest loads the original and replaces recursively:
- arrays become empty
- primitives stay
- getters return `undefined`
- methods return `undefined`
- objects are deeply cloned
- class instances and prototypes are cloned

Keep the real behaviour but track calls:

```ts
import { expect, vi } from 'vitest'
import * as exampleObject from './example.js'
import { answer } from './example.js'

vi.mock(import('./example.js'), { spy: true })

expect(answer()).toBe(42) // original runs
expect(answer).toHaveBeenCalled()
vi.mocked(exampleObject.answer).mockReturnValue(0)
```

Spying a class module also tracks instances: `Answer.prototype.value` accumulates calls from every instance while each instance has its own state.

- `{ spy: true }` modifies exported objects and prototypes in place, not copies. For `vi.mock(import('node:events'), { spy: true })` every emitter in the worker is affected.
- Modules in `<root>/__mocks__` are not used unless `vi.mock()` is called (unlike Jest); do it in `setupFiles` to mock everywhere.
## Checked

2026-11-04. Confirmed against guide/mocking/modules.md, api/vi.md and guide/migration/jest.md: automocking without a factory, the `__mocks__` lookup (project root for package names), the automocking algorithm list, `spy: true` with call-through and tracking, instance and prototype state sharing, the in-place modification warning with the `node:events` example, and the `__mocks__` not-loaded-by-default difference from Jest. Removed: a `server.deps.inline` tip that none of the cited pages state.

Method: documentation only; no commands were run.
