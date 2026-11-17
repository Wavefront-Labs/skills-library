---
id: computing-software.software-engineering.ada.maps-sets
name: maps-sets
category: computing-software
field: software-engineering
product: ada
tags: [ada, maps-sets]
level: practitioner
status: docs-checked
description: "Ada.Containers Hashed_Maps, Ordered_Maps, Hashed_Sets, Ordered_Sets: instantiate, Insert, Find, Element and iteration."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hashed/ordered maps and sets
```ada
package M is new Ada.Containers.Indefinite_Hashed_Maps
  (Key_Type => String, Element_Type => Integer,
   Hash => Ada.Strings.Hash, Equivalent_Keys => "=");
Tbl : M.Map;
Tbl.Include ("a", 1);
if Tbl.Contains ("a") then Put_Line (Tbl ("a")'Image); end if;
```
- For sets, `Insert` of a duplicate raises `Constraint_Error`, while `Include` silently ignores it.
- Ordered variants need a `"<"` ordering function (no hash) and iterate in order; hashed output is usually unordered.
- `Contains` returns a Boolean; `Find` returns a cursor or `No_Element`.
## Gotchas
- `Tbl (K)` raises an exception when K is missing; test with `Contains` first.
## Self-check
Insert a duplicate element into a set and observe Constraint_Error; swap to Include.

## Checked
2026-11-03. Confirmed in Introduction to Ada, Standard Library: Containers: `Indefinite_Hashed_Maps` generic parameters (`Key_Type`, `Element_Type`, `Hash`, `Equivalent_Keys`), `Ada.Strings.Hash`, `Include`/`Insert`/`Contains`/`Find`, ordered-map `<`. Removed the Bounded_* claim and the map-overwrite claim for Include (not on the pages read); Constraint_Error is scoped to sets.
Method: documentation only; no commands were run.
