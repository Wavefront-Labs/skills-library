---
id: computing-software.software-engineering.ada.fixed-strings
name: fixed-strings
category: computing-software
field: software-engineering
product: ada
tags: [ada, fixed-strings, ada-strings]
level: intro
status: docs-checked
description: "Ada String is a fixed array of Character: Ada.Strings.Fixed Index, Count and Trim, and the move to bounded or unbounded strings."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixed-length strings and Ada.Strings.Fixed
```ada
with Ada.Strings.Fixed; use Ada.Strings.Fixed;
S : String (1 .. 5) := "Hello";
I : Natural := Index ("a,b,c", ",");   -- 2
```
- `Ada.Strings.Fixed` has `Index` (position of a substring), `Count` (number of occurrences) and `Trim` (remove whitespace).
- `"Hello" & 3 * " World"` repeats a string with `*` and concatenates with `&`.
- Fixed-length strings are arrays, so bounded or unbounded strings are easier to build at run time.
## Gotchas
- Use `S'First` and `S'Last` rather than assuming bounds of 1.
## Self-check
Use Index and Count on a string with repeated words.

## Checked
2026-11-03. Confirmed in Introduction to Ada, Standard Library: Strings: `Index`, `Count`, `Trim`, `*` repetition, bounded vs fixed strings. Removed the `Head`, `Ada.Strings.Both` Trim form, 0-if-not-found, empty-string and Constraint_Error claims (not on the pages read).
Method: documentation only; no commands were run.
