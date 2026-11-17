---
id: computing-software.software-engineering.v-lang.v-struct-declaration-and-init
name: v-struct-declaration-and-init
category: computing-software
field: software-engineering
product: v-lang
tags: [v-struct-declaration-and-init, structs, struct, struct init, fields, pointer to struct, zero value, struct literal, v-lang]
level: intro
status: docs-checked
description: "Declare structs, initialise with field names, zero values, shorthand and pointers with &, and use the update syntax."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Struct declaration and initialisation

Goal: define and create data types.

- `struct Point { x int  y int }`; fields accessed with a dot.
- Init with names: `mut p := Point{ x: 10, y: 20 }`. Short (positional) syntax follows field declaration order: `Point{10, 20}` is the same as `Point{x: 10, y: 20}`. Omitted fields are zeroed; array and map fields are allocated.
- When the expected type is already known, the struct name can be omitted when returning a literal or passing one as a function argument.
- Heap: `p := &Point{10, 10}` has type `&Point`; references use the same field syntax.
- Anonymous structs: a field can have an inline `struct { name string  age int }` type and is initialized with `struct { name: '...' age: 24 }`.
- Update syntax: `User{ ...u  is_registered: true }` returns a modified copy; it can also spread a different struct type that supplies compatible fields.
- Fields can reuse reserved keywords (`type string`).
- Printing: `println(p)` prints the struct with its fields; `println(&Foo{...})` shows a leading `&`.
- Methods: `fn (u User) can_register() bool { return u.age > 16 }`; receiver in its own list after `fn`; methods must be in the same module as the type; the convention is a short, preferably one-letter receiver name, not `self` or `this`.

Gotcha: fields are immutable unless the variable is `mut` and the field is under a `mut:` section; assigning to a copy (`mut a := fa`) does not change the original.

Verify: `assert Point{30, 4} == Point{x: 30, y: 4}`.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Structs", "Heap structs", "Short struct literal syntax", "Struct update syntax", "Anonymous structs", "Methods"). Removed as not stated there: "positional init is fragile", `'${p}'` interpolation output, the `struct Line { a Point b Point }` example, the "@[heap] semantic care" remark.

Method: documentation only; no commands were run.
