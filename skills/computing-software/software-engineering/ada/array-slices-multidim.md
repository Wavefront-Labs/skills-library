---
id: computing-software.software-engineering.ada.array-slices-multidim
name: array-slices-multidim
category: computing-software
field: software-engineering
product: ada
tags: [ada, array-slices-multidim]
level: practitioner
status: draft
description: "Array slices A (2 .. 4), the & operator, multidimensional arrays and assigning overlapping slices."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Slices, concatenation and multidimensional arrays
```ada
S : Vec := (others => 1);
T : Seq := (1.0, 2.0, 3.0) & (4.0, 5.0);   -- concatenation
S (2 .. 4) := S (6 .. 8);                  -- slice assignment
type Grid is array (1 .. 3, 1 .. 3) of Integer;
G : Grid := (others => (others => 0));
G (2, 3) := 7;
```
- Multidimensional: `G'Length (1)`, `G'Range (2)`.
## Gotchas
- Large local arrays blow the stack; allocate with `new` or enlarge the stack.
## Self-check
Concatenate two arrays and assert the length equals the sum of the parts.
