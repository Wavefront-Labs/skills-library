---
id: computing-software.qa-testing-engineering.vitest.vi-spyon
name: vi-spyon
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [vi-spyon, spy-on-method, spy-on-getter, spy-on-class]
level: practitioner
status: docs-checked
description: "Spy on object methods and accessors with vi.spyOn, mock class constructors correctly, and know why spying on module exports fails in browser mode."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/vi.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/mocking/classes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
const cart = { getApples: () => 42 }
const spy = vi.spyOn(cart, 'getApples').mockReturnValue(1)

expect(cart.getApples()).toBe(1)
expect(spy).toHaveBeenCalledTimes(1)

spy.mockRestore() // puts the original back
```

- Accessors: `vi.spyOn(obj, 'prop', 'get')` or `'set'`.
- `vi.restoreAllMocks()` (or the `restoreMocks` option) restores every spy.

To mock one method of a single class instance, spy on that instance; it shadows the prototype method for it only:

```ts
vi.spyOn(cooper, 'speak').mockReturnValue('meow!')
```

An implementation used with `new` must use the `function` or `class` keyword, not an arrow function (see the mock-classes skill).

In Browser Mode you cannot spy on ES module exports. Use `vi.mock('./module', { spy: true })` instead, which mocks every export but keeps its implementation.

After `vi.restoreAllMocks()` the original descriptor is restored, so a later `spy.mockReturnValue(...)` has no effect unless you spy again.

## Checked

2026-11-04. Confirmed against api/vi.md and guide/mocking/classes.md: `vi.spyOn` with the `get` and `set` accessor argument, `mockRestore`, `vi.restoreAllMocks` and `test.restoreMocks`, the restored-descriptor tip, the function or class keyword requirement and arrow-function constructor error, per-instance spying shadowing the prototype method, and the Browser Mode limitation. Removed: a claim that every spy calls through by default, which the spyOn section does not state.

Method: documentation only; no commands were run.
