---
id: computing-software.software-engineering.ada.float-fixed-types
name: float-fixed-types
category: computing-software
field: software-engineering
product: ada
tags: [ada, float-fixed-types]
level: practitioner
status: draft
description: "Float, digits-based floating types, ordinary and decimal fixed point (delta/small) in Ada and their attributes."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/chapters/more_about_types.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Floating point and fixed point types
```ada
type Real is digits 15;                     -- floating, >=15 decimal digits
type Volt is delta 0.01 range 0.0 .. 100.0; -- ordinary fixed
type Money is delta 0.01 digits 12;         -- decimal fixed
for Volt'Small use 0.01;                    -- exact decimal small
```
- Ordinary fixed `small` defaults to a power of two <= delta, not 0.01, unless you give the clause.
- Mixed fixed multiply/divide needs conversion to a type.
## Gotchas
- Float equality: compare with a tolerance.
## Self-check
Print `Volt'Small` before and after the clause; the value changes.
