---
id: computing-software.software-engineering.nim.concept-definition-matching
name: concept-definition-matching
category: computing-software
field: software-engineering
product: nim
tags: [concept-definition-matching, concepts, concept, type-class, structural-typing, generic-constraint, container-concept, nim]
level: advanced
status: docs-checked
description: "Declare a concept as a structural type constraint, list required procs, and use it in generic signatures."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining and matching concepts

Goal: constrain generics by required operations.

```nim
type
  Comparable = concept
    proc cmp(a, b: Self): int
proc smallest[T: Comparable](a, b: T): T =
  if cmp(a, b) <= 0: a else: b
```
- A concept is a user-defined type class that matches other types based on a set of bindings: each definition in its body must be satisfiable with `Self` replaced by the candidate type. Matching is structural; there is no explicit "implements".
- `Self` is the type being matched. Concepts are generic matches, not concrete types.
- Use a concept as a generic constraint (`[T: Comparable]`) or directly as a parameter type (`proc f(x: Comparable)`).
- A concept can be a boolean expression over a named value: `Primitive = concept x` with body `x is PrimitiveBase or distinctBase(x) is Primitive`. Such concepts can be recursive (for example to see through `distinct` types) and mutually recursive; the compiler uses cycle detection.
- Test a type at compile time with `is`: `assert int is Primitive`.
- The manual says generic type checking of concept-constrained bodies is forthcoming, so concepts currently mainly serve overload resolution.

Gotchas:
- Matching is by overload resolution, so an implementation with a looser signature still matches.
- The first acceptable candidate for each binding is used.

Verify: passing a type with no `cmp` to `smallest` gives a type mismatch against the concept.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository, Concepts chapter read in full): the definition, `Self`, matching by overload resolution, recursive and mutually recursive concepts, `is` assertions, and the forthcoming generic type checking. Removed because the chapter does not describe them: `concept x, y`, `concept x of Other`, `Comparable and Printable`, the `{.experimental: "conceptsv2".}` remark and the claim about error message contents. The old example `$x is string` was replaced by one taken from the chapter. Other sources (tut1, lib) and the rest of the manual were not read; they were dropped.
Method: documentation only; no commands were run.
