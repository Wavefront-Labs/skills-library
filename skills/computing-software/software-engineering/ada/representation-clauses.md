---
id: computing-software.software-engineering.ada.representation-clauses
name: representation-clauses
category: computing-software
field: software-engineering
product: ada
tags: [ada, representation-clauses]
level: advanced
status: draft
description: "Control layout with Size, Alignment, record representation clauses (at/range), enumeration representation and bit order."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/Ada_For_The_Embedded_C_Developer/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Representation clauses and attribute definition
```ada
type Reg is record A : Boolean; N : Natural range 0 .. 15; end record;
for Reg use record
   A at 0 range 0 .. 0;
   N at 0 range 1 .. 4;
end record;
for Reg'Size use 8;
for Color use (Red => 1, Green => 2, Blue => 4);
```
- `pragma Pack` / `Bit_Order` and `Scalar_Storage_Order` (GNAT) select endianness.
- Compiler rejects overlapping or out-of-range components.
## Gotchas
- Check with `-gnatR` to print the final layout.
## Self-check
Compile with `-gnatR2` and verify bit positions.
