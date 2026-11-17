---
id: computing-software.software-engineering.nim.generic-procs-and-types
name: generic-procs-and-types
category: computing-software
field: software-engineering
product: nim
tags: [generic-procs-and-types, generics, generic, type-parameter, monomorphisation, instantiation, stack, nim]
level: practitioner
status: docs-checked
description: "Write procs and types parameterised by type, instantiate explicitly, and understand compile-time monomorphisation."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic procs and generic types

Goal: reuse code across types.

```nim
type Stack[T] = object
  data: seq[T]
proc push[T](s: var Stack[T], x: T) = s.data.add x
proc pop[T](s: var Stack[T]): T = s.data.pop
```
- Generics parametrise procs, iterators or types with type parameters (type variables). Brackets either introduce parameters (at the definition) or instantiate a generic (at the use site).
- Using a generic resolves the formal definition into an instance bound to concrete types; this is "instantiation". At the use site, brackets can supply the concrete types in the order the parameters are declared, or the compiler may infer the bindings: `add(root, newNode("hello"))` instantiates `newNode` and `add`.
- Several parameters and constraints: `proc p[H; T: Foo[H]](param: T): H`; separate independent definitions with `;`.
- To pass a type, use a `typedesc` parameter. A `typedesc` parameter is also usable as a type, so `proc p(a: typedesc; b: a)` accepts `p(int, 4)`.
- `var T` and `typedesc[T]` cannot be inferred in a generic instantiation, and `g[var int](v, i)` is rejected as well.
- The same generic type name creates a type class that matches any instantiation (`Table` matches every `Table[K, V]`).

Gotchas:
- Test generic code with several concrete types; the constraint (`[T: ...]`) is what limits which types are accepted.

Verify: `Stack[int]` and `Stack[string]` both compile and behave.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository), Generics chapter from its start through Generic inference restrictions (read in full): generic types and procs, the anatomy of a generic proc, instantiation, type classes, implicit generics and `typedesc`. Removed because the chapter does not state them: specialised code per instantiation and its binary-size and compile-time costs, "type-checked on instantiation", and static parameters (`Matrix[N: static int]`). tut1 and lib were not read and were dropped from sources.
Method: documentation only; no commands were run.
