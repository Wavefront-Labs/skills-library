---
id: computing-software.software-engineering.ada.access-types-allocators
name: access-types-allocators
category: computing-software
field: software-engineering
product: ada
tags: [ada, access-types-allocators, ada-access-types]
level: practitioner
status: draft
description: "Ada access types: new allocators, null, .all, .all dereference, access-to-constant and general access (all) types."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Access types and allocators
```ada
type Node;
type Node_Ptr is access Node;
type Node is record Val : Integer; Next : Node_Ptr; end record;
P : Node_Ptr := new Node'(Val => 1, Next => null);
P.Val := 2;            -- implicit dereference
V : Node := P.all;
type Int_Ref is access all Integer;   -- may point at 'Access of aliased objects
type Cst     is access constant Integer;
```
- Objects pointed to by `'Access` must be `aliased`.
- `not null access T` excludes null; checked at conversion.
## Gotchas
- Dereferencing null raises `Constraint_Error`.
- Heap memory is not freed automatically; see unchecked-deallocation.
## Self-check
Build a 3-node list, walk it to null, then dereference a null pointer and see the exception.
