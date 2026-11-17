---
id: computing-software.software-engineering.ada.literals-numeric-char
name: literals-numeric-char
category: computing-software
field: software-engineering
product: ada
tags: [ada, literals-numeric-char]
level: intro
status: draft
description: "Ada literals: based numbers (16#FF#), underscores in numbers, character and string literals, exponent forms."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Numeric, character and string literals
```ada
N1 : constant := 1_000_000;      -- underscores allowed
H  : constant := 16#FF#;         -- based literal, base 2..16
B  : constant := 2#1010_1010#;
F  : constant := 1.5E-3;
C  : Character := 'A';
S  : String := "say ""hi"" now";  -- double the quote to embed it
```
- No `.` means universal_integer, with `.` universal_real; `1` is never a Float.
- Wide_Character / Wide_Wide_String for Unicode; UTF-8 source needs `-gnatW8`.
## Gotchas
- `1.` and `.5` are illegal; write `1.0`, `0.5`.
- Named numbers (`constant := ...`) have no type until used.
## Self-check
Print `16#FF#` as Integer and confirm 255; confirm `Float := 1` fails to compile.
