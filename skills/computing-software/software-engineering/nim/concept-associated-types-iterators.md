---
id: computing-software.software-engineering.nim.concept-associated-types-iterators
name: concept-associated-types-iterators
category: computing-software
field: software-engineering
product: nim
tags: [concept-associated-types-iterators, concepts, concept, associated-type, container, iterator-concept, generic-concept, nim]
level: sme
status: docs-checked
description: "Describe container-like concepts using associated types, iterator requirements and generic type parameters."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Concepts with generic parameters (container concepts)

Goal: model containers and algorithms generically.

```nim
type
  Comparable = concept
    proc cmp(a, b: Self): int
  Indexable[I, T] = concept
    proc `[]`(x: Self; at: I): T
    proc `[]=`(x: var Self; at: I; newVal: T)
    proc len(x: Self): I
  Index = concept
    proc inc(x: var Self)
    proc `<`(a, b: Self): bool
proc sort*[I: Index; T: Comparable](x: var Indexable[I, T])
```
- `Self` inside a concept body is the type being matched (the "implementation"). A concept is a generic match, never a concrete type, so `typeof(x)` in a proc taking `Indexable[I, T]` is the implementation type.
- A concept with only concrete types in its body is "atomic" (`Comparable`); one with generic variables (`Indexable[I, T]`) is a "container" concept, and matching relates the element type `T` through the required procs.
- A "gray" concept uses generic procs in its body (`proc process[T](s: Self; data: T)`) without declaring the variable; it can hamper generic type checking but helps overload resolution.
- Matching substitutes the operand type for `Self` and runs overload resolution on every body definition, so an implementation need not match exactly: `proc p(x: Implementation; y: SomeInteger)` satisfies a concept requiring `proc p(s: Self; x: int)`.
- The first acceptable candidate for each binding wins, even if other candidates would bind different generic parameters.
- For simple unions prefer a type class built with `or` or `|`.

Gotchas:
- Comparing concepts in overloads: a concept is more specific than `T` or `auto`; against another concept the subset rule applies; otherwise a concept is less specific. If neither concept is a subset of the other, the one with more definitions wins; no clear winner is a compile-time ambiguity error.

Verify: an algorithm taking an `Indexable[int, T]` works for a `seq` and for a user type that defines `[]`, `[]=` and `len`.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository, the Concepts chapter at lines 3108-3243 read in full and the Generics chapter read): Self, atomic/container/gray concepts, overload resolution of body definitions, first-candidate binding, specificity rules, subset matching and the ambiguity error. Removed: the `for e in x` and `x.len is int` requirements, the "v1 limits" remark, the compile-time cost claim and the `openArray[T]` advice, none of which the chapter states. The rest of the manual, tut1 and lib were not read for this skill; those two pages were dropped from sources.
Method: documentation only; no commands were run.
