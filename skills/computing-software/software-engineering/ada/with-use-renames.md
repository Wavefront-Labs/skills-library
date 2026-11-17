---
id: computing-software.software-engineering.ada.with-use-renames
name: with-use-renames
category: computing-software
field: software-engineering
product: ada
tags: [ada, with-use-renames, ada-visibility]
level: intro
status: draft
description: "Ada context clauses: with, use, use type, use all type, renames, and package aliases to avoid namespace pollution."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# with, use, use type and renames
```ada
with Ada.Text_IO;
use  type Ada.Calendar.Time;       -- only operators
package TIO renames Ada.Text_IO;
function Sq (X : Integer) return Integer renames Math.Square;
```
- `with` makes a unit visible; `use` makes its contents directly visible.
- Prefer `use type` over `use` for operators; `use all type` also gives primitives.
## Gotchas
- Wildcard `use` can cause ambiguous overloads.
## Self-check
Replace `use Ada.Text_IO` with a renames alias and compile.
