---
id: computing-software.software-engineering.crystal.type-restrictions
name: type-restrictions
category: computing-software
field: software-engineering
product: crystal
tags: [type-restrictions, types-and-methods, type-restriction, parameter-types, underscore, class-restriction, self-restriction, crystal]
level: practitioner
status: docs-checked
description: "Control what a Crystal method accepts with type restrictions: self, .class, splat and block restrictions, and when to skip them."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/type_restrictions.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/blocks_and_procs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type restrictions on arguments

Goal: control what a method accepts.

- `def add(x : Number, y : Number)`: a wrong type gives `no overload matches 'add' with types Bool, Bool`.
- Without restrictions a method is still checked: every call with a new type combination is a separate instantiation, so the error is just less clear. Prefer no restriction unless defining overloads; unrestricted code also accepts duck-typed non-`Number` types (`Six` with a `+` method).
- `x : self` is the type that will own the method; it always matches an instance, even in class methods (`self.class` for the type).
- `x : Int32.class` accepts the type itself, not instances; use it for overloads by type.
- Splats: `*args : Int32` or `*args : _`; with `*x : *{Int32, String}` the restriction names a Tuple.
- When an instance variable is assigned from a parameter, the compiler inserts that restriction (`Foo.new "hi"` fails with `Foo.new(x : ::Int64)`).
- Free variables: `x : T forall T` (see generic-methods-restrictions).
- Block restriction: `&block : Int32 -> Int32`; a block returning another type is a compile error.
- Restrictions do not apply to variables inside the method.

Verify: call with a wrong type and read the `no overload matches` message listing the candidates.

## Checked
Checked 2026-11-02 against the crystal-book Type restrictions and Blocks and Procs pages. Removed: `Enumerable(Int32)`, plain `Class`, `Proc(_, Int32)`, per-member union dispatch, and the advice to prefer `Comparable`/`Enumerable` interfaces.

Method: documentation only; no commands were run.
