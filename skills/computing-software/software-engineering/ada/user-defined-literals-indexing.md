---
id: computing-software.software-engineering.ada.user-defined-literals-indexing
name: user-defined-literals-indexing
category: computing-software
field: software-engineering
product: ada
tags: [ada, user-defined-literals-indexing]
level: sme
status: draft
description: "Ada 2012/2022 Variable_Indexing, Implicit_Dereference and Ada 2022 user-defined literals (Integer_Literal, String_Literal)."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Variable_Indexing, reference types and literals
```ada
type Ref (E : access Integer) is null record with Implicit_Dereference => E;
type Big is private with Integer_Literal => From_Univ;   -- Ada 2022
```
- `Variable_Indexing => Ref_At` returns a reference type so `Obj (I) := X` works.
- Ada 2022 literal aspects: `Integer_Literal`, `Real_Literal`, `String_Literal`.
- GNAT support for Ada 2022 aspects needs a recent compiler (version unconfirmed).
## Gotchas
- Reference discriminants are accessibility-checked.
## Self-check
Assign through `Container (3) := 5` using Variable_Indexing.
