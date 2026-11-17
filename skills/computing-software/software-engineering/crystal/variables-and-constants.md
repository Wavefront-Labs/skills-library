---
id: computing-software.software-engineering.crystal.variables-and-constants
name: variables-and-constants
category: computing-software
field: software-engineering
product: crystal
tags: [variables-and-constants, syntax-basics, variables, constants, assignment, multiple-assignment, scope, type-declaration, crystal]
level: intro
status: draft
description: "Declare locals, multiple assignment, constants, type declarations and understand scope and the uninitialized rules."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Local variables, constants and assignment

Goal: know scoping rules.

- Locals are lowercase and scoped to the method or block; blocks can see outer locals, `def` cannot.
- Declare type without value: `x : Int32 = 1` or `x = uninitialized Int32` (unsafe, no zeroing).
- Multiple assignment: `a, b = b, a`; splat on left: `first, *rest = arr`.
- Constants start uppercase (`MAX = 10`), evaluated lazily at first access in order of use; namespaced `Foo::MAX`.
- Operator-assign: `x ||= 5`, `x &&= y`, `x += 1`.

Gotchas:
- Reassigning a constant is a compile error; constants may hold mutable objects though.
- A variable assigned inside an `if` branch only is nilable afterwards.
- Complex constant initialisers run lazily or at startup depending on the form; avoid side effects there.

Verify: compile a snippet that reads a variable assigned in only one branch and check it is typed `(Int32 | Nil)`.
