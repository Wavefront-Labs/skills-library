---
id: computing-software.software-engineering.ada.overloading-expression-functions
name: overloading-expression-functions
category: computing-software
field: software-engineering
product: ada
tags: [ada, overloading-expression-functions]
level: practitioner
status: draft
description: "Overload Ada subprograms by profile, define operators with quoted names, and write expression functions."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Overloading, operators and expression functions
```ada
function "+" (L, R : Vec2) return Vec2 is (X => L.X + R.X, Y => L.Y + R.Y);
function Max (A, B : Integer) return Integer is (if A > B then A else B);
procedure Put (X : Integer);  procedure Put (X : Float);
```
- Overload resolution uses parameter types and the result type; ambiguity is a compile error.
- Expression functions are inlined candidates and usable in contracts and in a package spec.
- Operators: `"="`, `"<"`, `"abs"`, `"mod"` etc.; `/=` follows `=`.
## Gotchas
- Declaring `"="` for a record changes predefined equality only for that type.
## Self-check
Add two Vec2 values with `+` and print the result.
