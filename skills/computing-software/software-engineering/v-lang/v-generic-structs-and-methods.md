---
id: computing-software.software-engineering.v-lang.v-generic-structs-and-methods
name: v-generic-structs-and-methods
category: computing-software
field: software-engineering
product: v-lang
tags: [v-generic-structs-and-methods, generics, generic struct, stackt, generic methods, instantiate, container, v-lang]
level: practitioner
status: docs-checked
description: "Define generic structs like Repo[T] or Box[T], attach methods whose receiver repeats the parameter, and instantiate them with explicit type arguments."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic structs and methods

Goal: build typed containers.

```v
struct Box[T] {
	value T
}

fn (b Box[T]) get() T {
	return b.value
}
```
- Declare with square brackets: `struct Repo[T] { db DB }`. Instantiate explicitly: `Repo[T]{db: db}` inside `new_repo[User](db)`, or `Expect[[]int]{value: [1, 2, 3]}`.
- Struct literals can infer omitted type arguments from field values; omitted fields use their declared defaults, including in nested generic structs.
- Method receivers name the parameter: `fn (r Repo[T]) find_by_id(id int) ?T`. Calls such as `users_repo.find_by_id(1)` need no `[T]` because it is inferred from the receiver.
- A receiver may constrain the wrapped type to a shape: `fn (e Expect[[]T]) first_or(value T) T` only applies when the wrapped type is a dynamic array, and binds `T` to the element type.
- A function can infer `U` from field shorthand: for `struct Box[T] { value T }` and `fn wrap[U](box Box[U]) Box[U]`, `wrap(value: 42)` infers `int`.
- Recursive types use references: `struct Node[T] { val T; left &Node[T]; right &Node[T] }`.
- A generic struct can be returned as a generic interface and keeps its concrete methods.

Verify: create `Box[int]` and `Box[string]` values and call `get()` on each.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Generics", "Structured generic receiver patterns", "References" for `Node[T]`). Removed: the `Stack[T]` example using `s.items.pop()` returning `?T` (vlib/builtin/array.v declares `pop` as returning `voidptr` and says nothing about options), nested instantiation claims (`Stack[Stack[int]]`), the "generic interfaces confirm" hedge and the panic-on-empty remark.

Method: documentation only; no commands were run.
