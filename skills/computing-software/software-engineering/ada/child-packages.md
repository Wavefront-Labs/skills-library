---
id: computing-software.software-engineering.ada.child-packages
name: child-packages
category: computing-software
field: software-engineering
product: ada
tags: [ada, child-packages]
level: practitioner
status: draft
description: "Ada child packages (Parent.Child), private children, with/use rules and gnat file naming Parent-child.ads."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Child packages and hierarchical units
```ada
package Parent.Child is ... end Parent.Child;       -- file parent-child.ads
private package Parent.Impl is ... end Parent.Impl; -- only visible inside Parent
```
- A child sees the parent's private part; no `with` of the parent needed.
- Private children are withable only by the parent body and sibling children's private parts.
- `with Parent.Child;` implicitly brings in `Parent`.
## Gotchas
- GNAT files use `-` for the dot: `parent-child.adb`.
## Self-check
Add a private child and confirm a client outside the hierarchy cannot with it.
