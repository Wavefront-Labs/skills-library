---
id: computing-software.software-engineering.ada.aspect-specifications
name: aspect-specifications
category: computing-software
field: software-engineering
product: ada
tags: [ada, aspect-specifications, ada-aspects-pragmas]
level: practitioner
status: draft
description: "Ada 2012 'with' aspect syntax vs legacy pragmas: Inline, Pack, Size, Convention, Import, Export, Volatile, Atomic."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Aspect specifications
```ada
function F (X : Integer) return Integer with Inline;
type R is record ... end record with Pack, Size => 24, Volatile;
Count : Integer with Atomic, Address => System'To_Address (16#4000#);
```
- Aspects are scoped to the declaration; pragmas are located separately.
- GNAT-defined aspects/pragmas listed in the GNAT Reference Manual.
## Gotchas
- Aspects on a completion vs spec: some must be on the first declaration.
## Self-check
Rewrite a `pragma Inline` as an aspect and compile.
