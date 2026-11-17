---
id: computing-software.software-engineering.ada.volatile-atomic-memory-mapped
name: volatile-atomic-memory-mapped
category: computing-software
field: software-engineering
product: ada
tags: [ada, volatile-atomic-memory-mapped]
level: advanced
status: draft
description: "Model hardware registers in Ada with Volatile, Atomic, Volatile_Full_Access, Import and Address aspects."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/Ada_For_The_Embedded_C_Developer/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Volatile, Atomic and memory-mapped registers
```ada
type GPIO is record MODER : UInt32; ODR : UInt32; end record
  with Volatile, Size => 64;
Port : GPIO with Import, Address => System'To_Address (16#4002_0000#);
Port.ODR := Port.ODR or 1;   -- read-modify-write; use Volatile_Full_Access for exact width
```
- `Atomic` forces indivisible access; compiler rejects if hardware cannot.
- `Volatile_Full_Access` (GNAT) makes every access full-width.
## Gotchas
- Reading with side effects: model with `Effective_Reads` in SPARK.
## Self-check
Compile for the target and inspect the assembly for the expected single load/store.
