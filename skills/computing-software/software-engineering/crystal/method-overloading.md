---
id: computing-software.software-engineering.crystal.method-overloading
name: method-overloading
category: computing-software
field: software-engineering
product: crystal
tags: [method-overloading, overloading, overload, arity, block-overload, type-overload, multiple-dispatch, crystal]
level: practitioner
status: docs-checked
description: "Overload Crystal methods by arity, type restriction, required named parameter names and block; ordering and known bugs."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/overloading.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/methods_and_instance_variables.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overloading by arity, type and block

Goal: define families of methods.

- Methods overload by the number of parameters, the type restrictions on parameters, the names of required named parameters, and whether the method accepts a block (detected from `yield`; a dummy `&block` makes it explicit).
- With the same parameter count, the compiler orders the less restrictive ones last (`become_older(age : String)` is tried before `become_older(age)`), but cannot always find a total order; put less restrictive methods at the end.
- Redefining a method with the same signature: the last definition wins (`previous_def` calls the earlier one).

Gotchas:
- Known ordering bugs exist; `-Dpreview_overload_order` (since Crystal 1.6.0) fixes some, e.g. overloads without a parameter overriding ones with a default value, and ordering that depends on the definition order of types in restrictions (workaround: define the subclass before the `def`).

Verify: call each variant in a spec.

## Checked
Checked 2026-11-02 against the crystal-book Overloading and Methods pages. Removed: return-type-per-overload, ambiguity-at-call and default-argument implicit overload claims, `def each` / iterator example.

Method: documentation only; no commands were run.
