---
id: computing-software.software-engineering.v-lang.v-struct-field-visibility-and-heap
name: v-struct-field-visibility-and-heap
category: computing-software
field: software-engineering
product: v-lang
tags: [v-struct-field-visibility-and-heap, structs, pub mut, mut fields, visibility, heap, struct sections, private fields, v-lang]
level: practitioner
status: docs-checked
description: "Control field visibility and mutability with pub, mut and pub mut sections, and mark structs @[heap] for reference semantics."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Field access modifiers and @[heap]

Goal: encapsulate struct state.

```v
struct Foo {
	a int // private immutable (default)
mut:
	b int // private mutable
pub:
	d int // public immutable (readonly)
pub mut:
	e int // public, but mutable only in parent module
__global:
	f int // public and mutable both inside and outside parent module
}
```
- Struct fields are private and immutable by default. There are 5 options: default, `mut:`, `pub:`, `pub mut:` and `__global:` (not recommended).
- Modifiers can also be written before individual fields (`mut b int`, `pub c int`, `pub mut d int`); an inline modifier overrides the current section for that declaration only.
- Private fields are available only inside the same module; accessing them from another module is a compile error. Public immutable fields are readonly everywhere.
- `&Point{...}` allocates a struct on the heap and gives a reference; structs are otherwise allocated on the stack.
- `@[heap]` on a struct declaration instructs the compiler to always allocate its objects on the heap, so references to them (for example stored in another struct) stay valid after the function returns. The docs note the attribute can cost performance and may suit very large structures.
- Mutable references need a mutable variable: `mut c := &fc`; `&fb` of an immutable `fb` is an error.

Verify: access a private field from another module and expect a compile error.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Access modifiers", "Heap structs", "Structs with reference fields", "Stack and Heap"). Removed as not stated there: the `-enable-globals` requirement, getter-method advice, `[]&T` shared identity advice, the "compiler auto-heaps in many cases" remark.

Method: documentation only; no commands were run.
