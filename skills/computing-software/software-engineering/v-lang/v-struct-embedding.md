---
id: computing-software.software-engineering.v-lang.v-struct-embedding
name: v-struct-embedding
category: computing-software
field: software-engineering
product: v-lang
tags: [v-struct-embedding, structs, embedded struct, embedding, composition, inheritance, promoted fields, v-lang]
level: practitioner
status: docs-checked
description: "Embed one struct in another to promote fields and methods, name collisions, and initialise embedded values."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Struct embedding and composition

Goal: reuse fields and methods without inheritance.

```v
struct Size {
mut:
	width  int
	height int
}

fn (s &Size) area() int {
	return s.width * s.height
}

struct Button {
	Size
	title string
}
```
- `Button` automatically gets all the fields and methods of `Size`: `button.width = 3`, `button.area()`.
- Reach the embedded struct explicitly with `button.Size` or `button.Size.area()`.
- Initialize the embedded part by its type name: `Button{ Size: Size{ width: 3, height: 2 } }`, or promoted fields directly (`height: 2`). Assign with `button.Size = Size{...}`.
- If embedded structs or the outer struct have a method or field with the same name, `button.Size.area()` targets the embedded one; without the embedded name, the outermost struct's member is used.
- Unlike inheritance, you cannot type cast between structs and embedded structs. Conceptually embedded structs are like mixins, not base classes.
- A struct can embed multiple structs, and unions support embedding too.
- Omitted embedded structs keep their declared field defaults.

Verify: call promoted and shadowed methods and assert results.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Embedded structs", "Unions"). Removed as not stated there: embedding `&Animal` as a pointer, satisfying interfaces through promoted methods, the Animal/Dog example.

Method: documentation only; no commands were run.
