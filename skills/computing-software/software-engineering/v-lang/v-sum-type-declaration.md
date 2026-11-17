---
id: computing-software.software-engineering.v-lang.v-sum-type-declaration
name: v-sum-type-declaration
category: computing-software
field: software-engineering
product: v-lang
tags: [v-sum-type-declaration, sum-types, sum type, type a  b  c, union type, variant, tagged union, v-lang]
level: practitioner
status: docs-checked
description: "Declare a sum type with type A = B | C, mix structs, primitives and other sum types, and construct values."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declaring sum types

Goal: model a value that is one of several types.

- Declare with the `type` keyword: `struct Moon {}  struct Mars {}  struct Venus {}  type World = Mars | Moon | Venus`. A sum type instance can hold a value of several different types.
- Construct by wrapping a value: `sum := World(Moon{})`. Primitives work as variants too: `type Entry = int | string`, `Entry('v')`.
- The built-in method `type_name()` returns the name of the currently held type (`sum.type_name() == 'Moon'`).
- Copying a sum type copies its held value; reference variants still refer to the same object.
- Recursive fields need indirection: a binary tree uses `left &Tree` and `right &Tree` in `struct Node` with `type Tree = Empty | Node`. A fixed layout cycle (`child Tree`) is an error; use `&Tree` or `[]Tree`. `?Tree` does not break a cycle, `?&Tree` does.
- Named variants: once one variant is written `Name(Type)`, all variants are `Name(Type)` or a bare `Name`: `type Expr = IntLit(int) | Count(int) | Str(string) | Void`. Create with `Expr.Count(3)` and `Expr.Void`. Generic form: `type Opt[T] = Some(T) | Nothing`, used as `Opt[int].Some(3)`.
- A variant must be named with its declared type in `is`, `as` and `match`.

Verify: build a small tree like the docs example and `println` the result.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Sum types", "Named variants"). Removed as not stated there: methods declared on a sum type, nesting sum types in sum types, `type Any = int | string | []Any`, returning a bare variant from a function declared to return the sum, the "use interfaces for open polymorphism" advice.

Method: documentation only; no commands were run.
