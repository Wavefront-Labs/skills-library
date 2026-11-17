---
id: computing-software.software-engineering.crystal.nilable-types
name: nilable-types
category: computing-software
field: software-engineering
product: crystal
tags: [nilable-types, nil-and-nilable, nil, nilable, optional, nil-check, nil-type, null-safety, crystal]
level: intro
status: docs-checked
description: "Treat nil as a type in Crystal: Nil, T?, compile errors on nilable calls, truthiness and narrowing."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/literals/nil.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/type_grammar.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/truthy_and_falsey_values.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/union_types.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/if_var.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nilable types and the Nil type

Goal: treat nil as a type.

- `Nil` represents the absence of a value and has the single value `nil`.
- `Int32?` is `Int32 | ::Nil` (a union type).
- Calling a method on a union requires every member to respond to it, otherwise a compile-time error; so a method that `Nil` lacks fails on a nilable value.
- The only falsey values are `nil`, `false` and null pointers; `0`, `""` and `[]` are truthy.
- `if x` removes `nil` in the branch (local variables only; see nil-safe-operators); `x.nil?` also narrows.

Gotchas:
- Narrowing does not work on instance variables, getters or method calls; assign to a local first.

Verify: compile a call on a nilable value and read the error naming `Nil`.

## Checked
Checked 2026-11-02 against the crystal-book Nil literal, Type grammar, Truthy and falsey, Union types and `if var` pages. Removed: the list of nilable-returning stdlib methods (`[]?`, `first?`, `find`, `index`), `not_nil!` advice, JSON/YAML optional keys, exact error wording.

Method: documentation only; no commands were run.
