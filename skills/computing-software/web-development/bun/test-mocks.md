---
id: computing-software.web-development.bun.test-mocks
name: test-mocks
category: computing-software
field: web-development
product: bun
tags: [mock-module, spy-on, mock-restore, jest-fn]
level: practitioner
status: docs-checked
description: "Mock in bun:test with mock(), spyOn and mock.module: implementations, restoring versus clearing, preload mocks, hoisting rules and package-scope differences."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/test/mocks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { mock, spyOn, jest } from "bun:test";
const random = mock((m: number) => m * Math.random());   // jest.fn behaves identically
random(2); random.mock.calls;                              // [[2]]
const spy = spyOn(service, "fetch").mockResolvedValue({ ok: true });
spy.mockRestore();                                         // put the original back
mock.module("./db", () => ({ query: mock(async () => []) }));
afterEach(() => { mock.restore(); mock.clearAllMocks(); });
```

Mocks: `mockImplementation`, `mockImplementationOnce`, `mockReturnValue`, `mockResolvedValue`, `mockRejectedValue`. `spyOn(obj, "prop", "get")` spies on accessors.

Reset semantics:
- `mock.restore()` restores spies but not `mock.module()` overrides.
- `mock.clearAllMocks()` clears history only; `jest.resetAllMocks()` also removes implementations.

Gotchas:
- `mock.module()` runs where written; `vi.mock()`/`jest.mock()` are hoisted above imports, and hoisted factories cannot use top-level variables (use `vi.hoisted()`).
- Mocking an already-imported module does not undo its side effects; use a preload (`bun test --preload ./my-preload` or `[test] preload`).
- Module mocks are removed after each test file; preload mocks apply to every file.
- `vi.mock()` affects only your own code, not packages in `node_modules`; `mock.module()` affects all importers.
- Calling a mock with `new` runs its implementation; check `mock.instances`.

## Checked

2026-11-04. Confirmed against the Bun docs page test/mocks: mock() and jest.fn, mock.calls, the mockImplementation family, spyOn accessor form with get/set, mock.restore not resetting mock.module, clearAllMocks versus resetAllMocks, hoisting rules and vi.hoisted, preload usage with --preload and bunfig, module mocks removed after each test file, the package-scope difference between vi.mock and mock.module, and new on a mock. Nothing removed.
Method: documentation only; no commands were run.
