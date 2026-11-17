---
id: computing-software.software-engineering.v-lang.v-interface-fields-and-embedding
name: v-interface-fields-and-embedding
category: computing-software
field: software-engineering
product: v-lang
tags: [v-interface-fields-and-embedding, interfaces, interface fields, embedded interface, is, as, type assertion, smartcast interface, v-lang]
level: advanced
status: docs-checked
description: "Use fields in interfaces, embed interfaces in others, define interface methods, and test or convert interface values with is and as."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interface fields, embedding and type checks

Goal: model richer contracts.

- Fields: `interface Named { name string }` is satisfied by a struct with a matching `name` field; the docs' `Speaker` interface mixes `breed string` and `speak() string`.
- Embed: interfaces embed like structs, `pub interface ReaderWriter { Reader Writer }`; the effect is copy-pasting the embedded methods and fields.
- Narrow with `if s is Dog { ... }`; `s` is smart-cast inside the branch (to a pointer `&Dog`). `a as IBar` panics when the stored value does not implement the interface; an `is` test against another interface checks the runtime type and may always be false.
- Interfaces can have their own methods, a convenience for writing `i.some_function()`. They are not default implementations: called through the interface they win over the struct's method of the same name, except inside an `is` branch that narrows to the struct.
- A `mut:` section marks methods that require a `mut` receiver.
- Generic constraints may name an interface: `fn longest[T Named](a T, b T) T`.

Verify: store two implementers in a slice and iterate calling the method.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Interfaces", "Casting an interface", "Interface method definitions", "Embedded interface", "Constraints"). Removed or corrected: "interface default methods are not supported" (interface methods exist but are not defaults), the `match s { Dog {...} }` form, `io.Reader` with `read([]u8) !int` (the docs show `read(mut buf []u8) ?int`), `==` comparison remarks and the older-versions generics caveat.

Method: documentation only; no commands were run.
