---
id: computing-software.software-engineering.crystal.class-reference-semantics
name: class-reference-semantics
category: computing-software
field: software-engineering
product: crystal
tags: [class-reference-semantics, structs-vs-classes, class, reference-type, heap-allocation, object-id, equality, hash-method, clone, dup, crystal]
level: practitioner
status: draft
description: "Use classes for entities with identity, heap allocation, equality via == and object_id, hash and cloning."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Classes: reference semantics and identity

Goal: manage identity and equality.

- Class instances are heap-allocated, passed by reference; variables point to the same object.
- Default `==` is identity; override `==(other)` and `hash(hasher)` together (or `def_equals_and_hash x, y`) to use as Hash keys or in Set.
- `dup` is shallow, `clone` is deep for stdlib collections where implemented.
- Finalisers: `def finalize` runs on GC, not deterministic; never rely on it for resources, use `ensure` or block-form APIs.

Gotchas:
- Overriding `==` without `hash` breaks Hash and Set lookups.
- `same?(other)` tests identity.
- Strings and arrays are mutable objects; dup them before modifying received arguments.

Verify: spec equal-valued instances as hash keys.
