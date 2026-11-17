---
id: computing-software.software-engineering.ada.derived-types-conversion
name: derived-types-conversion
category: computing-software
field: software-engineering
product: ada
tags: [ada, derived-types-conversion]
level: practitioner
status: draft
description: "Create a distinct type with 'type T is new U', inherited operations, explicit conversions and why Ada avoids implicit mixing."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Derived types and type conversion
```ada
type Meters is new Float;
type Feet   is new Float;
M : Meters := 3.0;
F : Feet   := Feet (M * 3.28);   -- explicit conversion required
```
- Derived types inherit the parent's primitive operations.
- Numeric and closely related types convert with `T (X)`; unrelated types need your own function.
## Gotchas
- Use `Unchecked_Conversion` only for representation-level reinterpretation.
## Self-check
Try `M + F`: expect a compile error naming the type mismatch.
