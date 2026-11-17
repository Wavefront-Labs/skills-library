---
id: computing-software.software-engineering.ada.big-numbers-decimal
name: big-numbers-decimal
category: computing-software
field: software-engineering
product: ada
tags: [ada, big-numbers-decimal]
level: advanced
status: draft
description: "Ada 2022 Ada.Numerics.Big_Numbers.Big_Integers and Big_Reals; decimal fixed point and Ada.Decimal."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Big numbers and decimal arithmetic
```ada
with Ada.Numerics.Big_Numbers.Big_Integers; use ...Big_Integers;
X : Big_Integer := To_Big_Integer (2) ** 100;
```
- Ada 2022 package; availability depends on GNAT version (unconfirmed).
- Money: `type Cents is delta 0.01 digits 18;` exact decimal fixed; `Ada.Decimal`.
- `Ada.Text_IO.Decimal_IO` for decimal types.
## Gotchas
- Big_Integer `**` takes a `Natural` exponent; no truncation is silent.
## Self-check
Compute 2**100 and compare against a Python-computed value.
