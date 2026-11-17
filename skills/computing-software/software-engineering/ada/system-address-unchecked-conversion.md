---
id: computing-software.software-engineering.ada.system-address-unchecked-conversion
name: system-address-unchecked-conversion
category: computing-software
field: software-engineering
product: ada
tags: [ada, system-address-unchecked-conversion, ada-low-level]
level: advanced
status: draft
description: "Low-level Ada: System.Address, Address aspect, To_Address, Ada.Unchecked_Conversion and System.Storage_Elements."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/Ada_For_The_Embedded_C_Developer/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# System.Address and Unchecked_Conversion
```ada
with System; with System.Storage_Elements; with Ada.Unchecked_Conversion;
type Word is mod 2**32;
Reg : Word with Volatile, Address => System'To_Address (16#4000_0000#);
function To_F is new Ada.Unchecked_Conversion (Word, Float);
```
- Sizes of source and target should match; the compiler warns otherwise.
- `System.Storage_Elements.To_Integer / To_Address` for address arithmetic.
## Gotchas
- Overlaying with `Address` suppresses initialisation only if you use `Import`.
## Self-check
Convert 16#3F800000# to Float and confirm 1.0.
