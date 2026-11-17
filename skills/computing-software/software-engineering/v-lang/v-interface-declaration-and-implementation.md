---
id: computing-software.software-engineering.v-lang.v-interface-declaration-and-implementation
name: v-interface-declaration-and-implementation
category: computing-software
field: software-engineering
product: v-lang
tags: [v-interface-declaration-and-implementation, interfaces, interface, implicit implementation, polymorphism, dynamic dispatch, method set, v-lang]
level: practitioner
status: docs-checked
description: "Declare interface methods and fields, satisfy them implicitly (or with the optional implements keyword), use mut: sections, and narrow with is."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declaring interfaces and implicit implementation

Goal: write code against behaviour.

```v
interface Speaker {
	breed string
	speak() string
}
```
- A type implements an interface by implementing its methods and fields; no keyword is needed. V interfaces may define both fields and methods.
- There is an optional `implements` keyword for explicit intent on a struct: `struct PathError implements IError { ... }`.
- Collect implementers with an interface-typed array: `mut arr := []Speaker{}` then `arr << dog`.
- Mutating methods go in a `mut:` section; implementing types then need a `mut` receiver for those methods. Without `mut:`, the method is `fn (s Type) write(a string) string`, and a type implementing it only that way does not satisfy an interface whose method is in `mut:`.
- Check the underlying type with `is`: `if s is Dog { println(s.breed) }` smart-casts `s` inside the branch. `a as IBar` panics when the stored value does not implement `IBar`.
- Interface methods defined on the interface (`fn (a Adoptable) speak() string`) are called instead of the struct's method when called through the interface value; this is not a C#-style default implementation.

Verify: store two implementers in an interface array and call the method on each.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Interfaces", "Implement an interface", "Casting an interface", "Interface method definitions"). Removed or corrected: "no implements keyword" (it exists and is optional), `[Speaker(Dog{}), Cat{}]` literal form, the heap-promotion remark and the exact-signature gotcha.

Method: documentation only; no commands were run.
