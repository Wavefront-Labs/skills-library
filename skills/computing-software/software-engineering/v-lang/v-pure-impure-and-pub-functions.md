---
id: computing-software.software-engineering.v-lang.v-pure-impure-and-pub-functions
name: v-pure-impure-and-pub-functions
category: computing-software
field: software-engineering
product: v-lang
tags: [v-pure-impure-and-pub-functions, functions, pub-fn, visibility, pure-functions, module-api, private, v-lang]
level: practitioner
status: docs-checked
description: "Control a V module's API with pub, and know the documented purity story: immutable arguments, no globals by default, mut parameters, and the @[unsafe] function attribute."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function visibility, pub and purity

Goal: expose only the API you intend and know what V's docs say about pure functions.

- Functions are private (not exported) by default. Prepend `pub` to let other modules use them; the same applies to structs, constants and type declarations. `pub` can only be used from a named module.
- Function arguments are immutable by default, even when references are passed, and mutable arguments must be marked on call. Use `.clone()` for a mutable copy of an immutable array.
- The docs reason that, since V has no globals, a function's return value depends on its arguments only and evaluation has no side effects, unless the function uses I/O. They add that V is not a purely functional language, and a compiler flag `-enable-globals` exists but is intended for low-level applications such as kernels and drivers.
- A parameter declared `mut` can be modified by the callee. A method with a `mut` receiver needs a mutable receiver value; an immutable value parameter cannot call it, since changes would affect a copy and be lost.
- `@[unsafe]` on a function means calls to it must be inside `unsafe {}` blocks, while the function body is still checked unless you wrap parts in `unsafe {}`. This is useful for unsafe functions with checks before and after the unsafe operation.
- `@[inline]` makes calls to a function inlined; `@[noinline]` prevents it.
- `@[deprecated]`, `@[deprecated: 'use x']` and `@[deprecated_after: 'date']` mark deprecation.

Gotchas:
- Private struct fields are available only inside the same module, but a public function can return a private struct type; the caller reads its public fields without naming the type (docs). Exporting the type is still the clearer choice.
- Internal test files in the same module can call private functions (docs, testing section).

Verify: from another module, calling the private function fails to compile.

## Checked
2026-11-08. Checked against the V documentation (`doc/docs.md`): symbol visibility, function argument immutability, the no-globals note and `-enable-globals`, `mut` receivers, `@[unsafe]`, `@[inline]`/`@[noinline]` and deprecation attributes. Removed: the claim that calling C or using `unsafe {}` makes a function "impure" (the docs do not use that term), and the claim that a `pub fn` returning a private type is "awkward" (the docs describe it as allowed). Replaced the generic landing-page sources with the raw docs file.
Method: documentation only; no commands were run.
