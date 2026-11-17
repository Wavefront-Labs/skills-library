---
id: computing-software.software-engineering.ada.record-types-aggregates
name: record-types-aggregates
category: computing-software
field: software-engineering
product: ada
tags: [ada, record-types-aggregates, ada-records]
level: intro
status: draft
description: "Declare Ada records with default component values, aggregates (positional and named), selection and the Ada 2022 delta aggregate."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/chapters/more_about_types.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Record types and aggregates
```ada
type Point is record
   X, Y : Float := 0.0;
end record;
P : Point := (X => 1.0, Y => 2.0);
Q : Point := (P with delta Y => 5.0);   -- Ada 2022
```
- Select with `P.X`; whole-record assignment copies.
- `(others => <>)` uses the defaults.
## Gotchas
- Prefer named association for long records.
## Self-check
Build P, update one field with a delta aggregate, confirm the others are unchanged.
