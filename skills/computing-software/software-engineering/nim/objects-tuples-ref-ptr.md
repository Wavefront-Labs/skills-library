---
id: computing-software.software-engineering.nim.objects-tuples-ref-ptr
name: objects-tuples-ref-ptr
category: computing-software
field: software-engineering
product: nim
tags: [objects-tuples-ref-ptr, type-system, object, tuple, ref, ptr, inheritance, rtti, nil, dereference, nim]
level: practitioner
status: docs-checked
description: "Define Nim value objects, inheritance, tuples, traced ref types and untraced ptr, and the dereference rules."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Objects, tuples, ref and ptr types

Goal: choose value vs reference types.

- An `object` is a value type: assigning it copies all components. Each object type `Foo` has a constructor `Foo(field: value, ...)`; unspecified fields get their default values and order may change.
- Fields visible from other modules must be marked `*` (`name*: string`); unmarked fields are hidden.
- Objects provide inheritance and field hiding; objects with inheritance have runtime type information so the `of` operator works (`student of Person`). Different object types are never equivalent (nominal typing). An object with no ancestor is implicitly final: `Student = ref object of Person` is an error unless Person is non-final, e.g. `object of RootObj`. The `inheritable` pragma starts new roots.
- Object variants are tagged unions discriminated via an enumerated type.
- Tuples are value types that copy each component and are structurally typed: same field types, names and order mean equivalent types. Construct with `(name: "Peter", age: 30)` or anonymous fields `("Peter", 30)`; access with `t.field` or `t[i]` (constant `i`). Unpack with parentheses `let (dir, name, ext) = splitFile(path)`; without parentheses all names get the same whole value. Tuple fields are always public.
- References: `ref` is traced (garbage-collected heap), `ptr` is untraced and unsafe, for manual memory and low-level work. `new(n)` allocates a traced object; `alloc`, `dealloc` and `realloc` deal with untraced memory. `[]` dereferences, while `.` and `[]` index operators dereference implicitly, so `n.data` needs no `n[].data` (the tutorial calls `n[].data` highly discouraged). A reference to nothing is `nil`.

Verify: copying a value object leaves the original unchanged; copying a ref aliases it.

## Checked

2026-11-08. Read the Nim tutorial Objects, Tuples and Reference and pointer types sections in full and the manual object paragraphs on inheritance, the `of` operator and finality.

Removed as unconfirmed: `NilAccessDefect` on nil dereference, the `method` dynamic dispatch remark, and the `addr x` description. Dropped the lib index source (not used).

Method: documentation only; no commands were run.
