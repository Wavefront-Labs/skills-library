---
id: computing-software.software-engineering.ada.accessibility-anonymous-access
name: accessibility-anonymous-access
category: computing-software
field: software-engineering
product: ada
tags: [ada, accessibility-anonymous-access]
level: advanced
status: draft
description: "Ada accessibility levels, dangling-reference checks, anonymous access parameters and access discriminants."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Accessibility rules and anonymous access
```ada
procedure Set (R : access Integer) is begin R.all := 0; end;   -- anonymous access param
```
- A pointer may not outlive its designated object: `X'Access` is legal only if the pointer type's level is no deeper than X's.
- Static violations are compile errors; dynamic ones raise `Program_Error`.
- `'Unchecked_Access` bypasses the check; use only with proof the object outlives the pointer.
## Gotchas
- Anonymous access parameters have the level of the call; do not store them.
- Access-to-subprogram: `type Cb is access procedure (X : Integer);` obey the same rules.
## Self-check
Take 'Access of a local aliased variable into a global access object and read the compile error.
