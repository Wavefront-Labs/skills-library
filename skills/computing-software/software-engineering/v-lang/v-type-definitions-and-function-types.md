---
id: computing-software.software-engineering.v-lang.v-type-definitions-and-function-types
name: v-type-definitions-and-function-types
category: computing-software
field: software-engineering
product: v-lang
tags: [v-type-definitions-and-function-types, unions-and-type-aliases, type-alias, function-type, callback-type, duck-typing, v-lang]
level: practitioner
status: docs-checked
description: "Name function signatures with type aliases, pass them as callbacks and rely on V's duck-typing of compatible functions."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
  - https://docs.vlang.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type definitions and function types

Goal: name function signatures to clarify APIs.

- `type Filter = fn (string) string` names a signature. It works like any other type, so a function can accept one:
  `fn filter(s string, f Filter) string { return f(s) }`.
- V has duck-typing: a function does not declare compatibility with a function type, it only has to be compatible.
  `fn uppercase(s string) string { return s.to_upper() }` can be used everywhere a `Filter` is expected.
- Function signatures can include fixed-size arrays, pointers to fixed-size arrays and other function types. Optional
  and result callback return types are supported.
- A null function value must be written `unsafe { nil }` (outside `unsafe` the compiler rejects a null reference).
- Plain alias declaration: `type NewType = ExistingType`, a special case of a sum type declaration.

Gotchas:
- The page does not show methods on function-type aliases or on aliases of types from other modules; test those
  against your compiler version.

Verify: pass `uppercase` to `filter('abc', uppercase)` and assert the result is `ABC`.

## Checked

Read the Function Types and Type aliases sections of the V documentation (doc/docs.md from the vlang/v repository, the source of docs.vlang.io). Removed claims the page does not state: `type Celsius = f64` method examples, aliases of array types with methods, the struct-of-callbacks nil check idiom and the module rule for alias methods. Tags previously contained spaces and were fixed.

Method: docs-only read of cited pages, 2026-11-08
