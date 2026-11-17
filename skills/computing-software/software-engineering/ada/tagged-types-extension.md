---
id: computing-software.software-engineering.ada.tagged-types-extension
name: tagged-types-extension
category: computing-software
field: software-engineering
product: ada
tags: [ada, tagged-types-extension, ada-oop]
level: practitioner
status: docs-checked
description: "Ada tagged records: extension, dot notation, class-wide types 'Class, and primitive operations."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tagged types and type extension
```ada
type Animal is tagged record Name : String (1 .. 10); end record;
procedure Speak (A : Animal);
type Dog is new Animal with record Tricks : Natural; end record;
overriding procedure Speak (D : Dog);
Pet : Animal'Class := Dog'(...);
Pet.Speak;       -- dispatches (object.method notation)
```
- A subprogram is a primitive only if it is declared in the same scope as the type (and meets the further conditions the page lists).
- The `overriding` qualifier is optional, but if present it must be valid, so it catches mistakes.
- When the dispatching parameter is first you can use dot notation `Obj.Op (...)`.
## Gotchas
- A dispatching call needs an object of a class-wide type (`T'Class`); a variable of the specific type always holds exactly that type.
## Self-check
Call Speak on Animal'Class holding a Dog and see the Dog version run.

## Checked
2026-11-03. Confirmed in Introduction to Ada, Object-Oriented Programming: primitives and scope, `overriding` qualifier, class-wide `'Class` dispatching, dot notation. Removed the "before it is frozen" and `not overriding` claims (not on the pages read).
Method: documentation only; no commands were run.
