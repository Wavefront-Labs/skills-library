---
id: computing-software.qa-testing-engineering.vitest.mock-classes
name: mock-classes
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [mock-class, vi-fn-class, class-fields, prototype-methods]
level: practitioner
status: docs-checked
description: "Mock a whole class with vi.fn(class {...}) in Vitest, define methods as class fields for per-instance mocks, and understand prototype-chain pitfalls."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/mocking/classes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Mock an entire class with one `vi.fn` call that receives a class:

```ts
const Dog = vi.fn(class {
  name: string
  constructor(name: string) { this.name = name }
  speak = vi.fn(() => 'woof')
  feed = vi.fn()
})

const cooper = new Dog('Cooper')
expect(Dog).toHaveBeenCalledWith('Cooper')
expect(cooper.speak).not.toHaveBeenCalled()
```

- Methods defined as class fields (`speak = vi.fn()`) give each instance its own mock, so you can assert on one instance.
- Prototype methods are shared on the class prototype; instances keep the prototype chain of the class you pass, so prototype methods stay available and `instanceof` passes. Nothing is mocked for them unless you spy.
- Mock one instance's method with `vi.spyOn(instance, 'method')`; a non-function property with `vi.spyOn(dog, 'name', 'get')`.
- If the class is re-exported from another module, recreate it inside the `vi.mock` factory.
- Prefer the `class` syntax over `function` in the implementation.
- Passing a class to `vi.fn` was introduced in Vitest 4; earlier versions needed `function` and `prototype` inheritance.
- Assigning `MockedDog.prototype.speak = vi.fn(...)` mocks the method for every instance, including earlier ones, but they then share one call history.

Pitfalls:
- If a constructor returns a non-primitive, that value becomes the result of `new` and the prototype may be unbound.
- The mock's `prototype` follows the current implementation; instances made by an earlier implementation lose prototype methods after a new one is set.

## Checked

2026-11-04. Confirmed against guide/mocking/classes.md: the `vi.fn(class {...})` form, class fields versus prototype methods, `instanceof` and prototype chain behaviour, `vi.spyOn` on one instance and on a getter, the re-export tip, the non-primitive constructor warning, the prototype re-pointing warning, and the Vitest 4 note.

Method: documentation only; no commands were run.
