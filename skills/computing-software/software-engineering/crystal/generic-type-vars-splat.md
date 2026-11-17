---
id: computing-software.software-engineering.crystal.generic-type-vars-splat
name: generic-type-vars-splat
category: computing-software
field: software-engineering
product: crystal
tags: [generic-type-vars-splat, generics, type-var, tuple-generic, proc-generic, namedtuple-generic, splat-generics, instance-type, crystal]
level: advanced
status: docs-checked
description: "Use splat type variables in Crystal generics: class Foo(*T), *x : *T, **x : **T and Proc(*T, R) restrictions."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/generics.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/type_restrictions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type variable helpers: typeof, T.new and splat generics

Goal: manipulate type variables in method bodies.

- A generic with a splat type variable: `class Foo(*T)` with `def initialize(*@content : *T)`. `Foo(Int32, String)` or inferred from `Foo.new("Hello", ["Crystal", "!"], 140)` gives `Foo(String, Array(String), Int32)`.
- Subclass with concrete arguments: `class Int32StringChild < Parent(Int32, String)`.
- Zero arguments is `Parent().new` (type `Parent()`); `Parent.new` with no arguments cannot infer `T` and `class Foo < Parent` is an error.
- In a method, `*x : *T` forall T gives `T` as a `Tuple(...)`, `**x : **T` gives a `NamedTuple(...)`, and `x : Proc(*T, Int32)` gives `T` as a `Tuple` of the proc's argument types.
- Inside a generic's class methods, `T` is bound only if inferred from arguments; otherwise give it explicitly (`Foo(Int32).foo(1)`).

Verify: print `T` inside a method for several instantiations.

## Checked
Checked 2026-11-02 against the crystal-book Generics and Type restrictions pages. Removed: `Proc(Int32, String, Bool)` T/R split, `T.zero`, `T.size`, class-var annotation remark, forward-reference alias remark, compile-time cost remark, `from(x : U) : self`.

Method: documentation only; no commands were run.
