---
id: computing-software.software-engineering.ada.package-spec-body-private
name: package-spec-body-private
category: computing-software
field: software-engineering
product: ada
tags: [ada, package-spec-body-private, ada-packages]
level: practitioner
status: draft
description: "Split an Ada package into spec and body, hide representation with a private type and limited private."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Package specification, body and private part
```ada
package Stacks is
   type Stack is private;
   procedure Push (S : in out Stack; X : Integer);
private
   type Stack is record Top : Natural := 0; Data : Integer_Array (1 .. 100); end record;
end Stacks;
```
- Files: `stacks.ads` (spec), `stacks.adb` (body); GNAT requires lowercase name = unit name.
- `limited private` forbids copy and `=`; use for handles.
- Client code sees only the visible part; private part is for the compiler.
## Gotchas
- Changing the private part forces recompilation of clients.
## Self-check
Try to read S.Top from a client and confirm it is rejected.
