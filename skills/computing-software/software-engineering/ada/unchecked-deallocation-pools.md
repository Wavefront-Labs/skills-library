---
id: computing-software.software-engineering.ada.unchecked-deallocation-pools
name: unchecked-deallocation-pools
category: computing-software
field: software-engineering
product: ada
tags: [ada, unchecked-deallocation-pools, ada-memory-management]
level: advanced
status: draft
description: "Free heap objects with Ada.Unchecked_Deallocation, set Storage_Size, define user storage pools."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unchecked_Deallocation and storage pools
```ada
procedure Free is new Ada.Unchecked_Deallocation (Node, Node_Ptr);
Free (P);                  -- P := null afterwards
type Ptr is access Node with Storage_Size => 10_000;   -- pool limit
```
- Custom pools: derive from `System.Storage_Pools.Root_Storage_Pool` and set `Storage_Pool`.
- Subpools in Ada 2012 (`System.Storage_Pools.Subpools`).
## Gotchas
- Freeing a copy leaves dangling pointers (no automatic tracking).
- Exceeding Storage_Size raises `Storage_Error`.
## Self-check
Allocate until Storage_Error with a small Storage_Size.
