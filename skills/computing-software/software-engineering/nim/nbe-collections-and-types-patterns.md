---
id: computing-software.software-engineering.nim.nbe-collections-and-types-patterns
name: nbe-collections-and-types-patterns
category: computing-software
field: software-engineering
product: nim
tags: [nbe-collections-and-types-patterns, learning-resources-nim-by-example, nim-by-example, objects, inheritance, tuples, templates, macros, generics, examples, nim]
level: practitioner
status: draft
description: "Practise the intermediate examples on seqs, tables, tuples, objects, inheritance, generics, templates and macros."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
  - https://nim-lang.org/docs/lib.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nim by Example: collections, objects, generics and macros

Goal: cover the mid-level examples.

- Sequences/arrays, Tables, Sets, Tuples, Objects (value vs ref), Inheritance and methods, Generics, Iterators, Operator overloading, Templates, Macros, Exceptions, Concurrency basics.
- Exercises: implement a `Stack[T]`, a shape hierarchy with `method area`, a custom `+` for vectors, an `iterator` for fibonacci, a template `benchmark`, a macro `assertNotNil`.
- Use `toTable`, `mapIt`, `sorted`, `join` to keep code idiomatic.
- Compare object variant (`case kind`) with inheritance for an expression tree evaluator.
- Review compile errors carefully; Nim's messages name the expected types.

Gotchas:
- `method` requires `ref object of RootObj` and `-d:` multimethods settings in older Nim versions.
- Generic code surfaces errors at instantiation.

Verify: all exercises compile and pass simple asserts.
