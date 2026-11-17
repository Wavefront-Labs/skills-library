---
id: computing-software.software-engineering.crystal.struct-value-semantics
name: struct-value-semantics
category: computing-software
field: software-engineering
product: crystal
tags: [struct-value-semantics, structs-vs-classes, struct, value-type, stack-allocation, copy-semantics, record, immutable, crystal]
level: practitioner
status: docs-checked
description: "Choose Crystal structs: value semantics, copies on pass, record macro, inheritance limits."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/structs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structs: value semantics

Goal: pick struct when appropriate.

- Structs inherit from `Value`, are allocated on the stack and are passed by value: passing, returning or assigning copies them. Classes inherit from `Reference` and live on the heap.
- Mostly useful for immutable data types and stateless wrappers; they avoid many small allocations. Mutable structs are allowed but surprising.
- A struct is always passed by value, even when a method returns `self`: `counter.plus.plus` modifies the variable only once because the second call works on a discarded copy.
- Reference-type fields are shared with the copy: `object.array << "foo"` shows in the original, but `object.array = ["new"]` replaces the reference only in the copy.
- A struct cannot inherit from a non-abstract struct (its memory layout must be fixed, so array elements stay the same size); it can inherit from an abstract struct, include modules and be generic.
- `record Point, x : Int32, y : Int32` (stdlib macro) expands to a struct with getters, an initializer, `copy_with` and `clone`.

Verify: spec that mutating a copy leaves the original unchanged.

## Checked
Checked 2026-11-02 against the crystal-book Structs page. Real error fixed: the skill said `record` generates `==`; the documented expansion has getters, `initialize`, `copy_with` and `clone` only. Removed: the 64-byte rule of thumb, union-bloat and hashing remarks, the `arr[i].with(...)` idiom.

Method: documentation only; no commands were run.
