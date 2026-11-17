---
id: computing-software.software-engineering.ada.separate-subunits-limited-with
name: separate-subunits-limited-with
category: computing-software
field: software-engineering
product: ada
tags: [ada, separate-subunits-limited-with]
level: advanced
status: draft
description: "Ada subunits (separate), 'limited with' for cyclic dependencies and 'private with' for private-part visibility."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Subunits and limited with
```ada
procedure Main is
   procedure Big;  -- stub
   ...
separate (Parent)
procedure Big is begin null; end Big;   -- file parent-big.adb
limited with B;     -- cyclic: only incomplete-type view
private with Util;
```
- `separate` compiles the body independently of the parent.
- `limited with` gives a limited view (incomplete types) to break circular `with`.
## Gotchas
- Subunit file name is `parent-sub.adb`.
## Self-check
Create two mutually dependent packages through limited with.
