---
id: computing-software.software-engineering.ada.enumeration-types
name: enumeration-types
category: computing-software
field: software-engineering
product: ada
tags: [ada, enumeration-types]
level: intro
status: draft
description: "Enumeration types in Ada: literals, 'Image, 'Value, 'Pos, 'Succ, Boolean and Character as enums, overloaded literals."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enumeration types
```ada
type Color is (Red, Green, Blue);
for C in Color loop Put_Line (C'Image); end loop;
V : Color := Color'Value ("Green");
N : Natural := Color'Pos (Blue);   -- 2
```
- Literals may be overloaded across types; qualify with `Color'(Red)`.
- `Boolean` is `(False, True)`; `Character` is an enumeration too.
- Ada 2022: `Obj'Image` works on any object.
## Gotchas
- `'Value` on bad text and `'Succ` of the last literal raise `Constraint_Error`.
## Self-check
Iterate over Color printing Image; confirm Color'Succ (Blue) raises.
