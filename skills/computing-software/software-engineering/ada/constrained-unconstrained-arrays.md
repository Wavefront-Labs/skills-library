---
id: computing-software.software-engineering.ada.constrained-unconstrained-arrays
name: constrained-unconstrained-arrays
category: computing-software
field: software-engineering
product: ada
tags: [ada, constrained-unconstrained-arrays, ada-arrays]
level: practitioner
status: draft
description: "Ada array types: index ranges, unconstrained 'range <>', 'First/'Last/'Length/'Range attributes and array aggregates."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/chapters/more_about_types.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Constrained and unconstrained arrays
```ada
type Vec is array (1 .. 10) of Integer;
type Seq is array (Positive range <>) of Float;
A : Seq (1 .. 5) := (others => 0.0);
B : Vec := (1 | 3 => 9, others => 0);
for I in A'Range loop A (I) := Float (I); end loop;
```
- Attributes: `A'First`, `A'Last`, `A'Length`, `A'Range`.
- Aggregates: positional, named, `others` (last).
## Gotchas
- Out-of-bounds index raises `Constraint_Error` (checks on).
## Self-check
Index A (6) on a 5-element array and confirm Constraint_Error.
