---
id: computing-software.software-engineering.ada.unbounded-strings
name: unbounded-strings
category: computing-software
field: software-engineering
product: ada
tags: [ada, unbounded-strings]
level: practitioner
status: docs-checked
description: "Use Ada.Strings.Unbounded for growable strings: To_Unbounded_String, Append, To_String, plus Bounded as alternative."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unbounded and bounded strings
```ada
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;
U : Unbounded_String := To_Unbounded_String ("abc");
Append (U, "def");
Put_Line (To_String (U));
```
- Bounded alternative: instantiate `Ada.Strings.Bounded.Generic_Bounded_Length` with a maximum length; `To_Bounded_String` raises an exception if the input is longer unless you give a truncation parameter.
- `Unbounded_String` is not generic (no instantiation) and has `Null_Unbounded_String`; `&` works for both kinds.
## Gotchas
- Unbounded strings need no truncation; bounded strings do.
## Self-check
Append in a loop 1000 times and print the result's length.

## Checked
2026-11-03. Confirmed in Introduction to Ada, Standard Library: Strings: `To_Unbounded_String`, `To_String`, `Append`, `Null_Unbounded_String`, `Generic_Bounded_Length`, truncation. Removed `Length`/`Element`, the Unbounded.Text_IO claim and the heap/SPARK/real-time gotcha (not on the pages read).
Method: documentation only; no commands were run.
