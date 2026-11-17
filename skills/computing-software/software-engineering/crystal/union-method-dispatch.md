---
id: computing-software.software-engineering.crystal.union-method-dispatch
name: union-method-dispatch
category: computing-software
field: software-engineering
product: crystal
tags: [union-method-dispatch, union-types, virtual-type, dynamic-dispatch, abstract-class, type-id-dispatch, performance, crystal]
level: advanced
status: draft
description: "Explain how calls on union and abstract-class typed values dispatch at runtime and how that affects performance."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Virtual types and dispatch on unions

Goal: see where runtime dispatch happens.

- A value typed as a base class with subclasses is a virtual type `Base+`; calls dispatch on the type id.
- A union call such as `(Int32 | String).to_s` expands into a `case` on the type id; overload resolution happens per member at compile time.
- Concrete, single-type receivers are statically bound and often inlined.
- Prefer abstract classes or modules with abstract defs when you want polymorphism; prefer generics when each use has one type.

Gotchas:
- Passing a union into a hot loop multiplies the code and cost; hoist the dispatch out of the loop.
- Structs in a union are copied around; large structs make the union big.
- Adding a subclass can change types printed in errors to `Base+`.

Verify: inspect LLVM IR via `crystal build --emit llvm-ir` and look for the type-id switch.
