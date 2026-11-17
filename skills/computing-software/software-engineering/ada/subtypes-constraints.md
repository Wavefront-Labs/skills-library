---
id: computing-software.software-engineering.ada.subtypes-constraints
name: subtypes-constraints
category: computing-software
field: software-engineering
product: ada
tags: [ada, subtypes-constraints, ada-subtypes]
level: intro
status: draft
description: "Ada subtypes narrow a base type without a new type: range subtypes, Natural/Positive, constraint checks."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/chapters/strongly_typed_language.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Subtypes and constraints
```ada
subtype Small_Int is Integer range -10 .. 10;
subtype Name_Str  is String (1 .. 20);
X : Small_Int := 5;
I : Integer := X;       -- same type, no conversion
```
- Predefined: `Natural`, `Positive`.
## Gotchas
- A subtype is not a new type; overloading on subtype alone is illegal.
- Out-of-range assignment raises `Constraint_Error` at run time.
## Self-check
Assign 11 to a Small_Int via a variable and confirm Constraint_Error.
