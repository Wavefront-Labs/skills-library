---
id: computing-software.software-engineering.ada.interfaces-abstract-types
name: interfaces-abstract-types
category: computing-software
field: software-engineering
product: ada
tags: [ada, interfaces-abstract-types]
level: advanced
status: draft
description: "Ada interface types, abstract tagged types and subprograms, multiple inheritance of interfaces, 'Class dispatch."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interfaces and abstract types
```ada
type Printable is interface;
procedure Print (X : Printable) is abstract;
type Doc is new Base and Printable with null record;
type Shape is abstract tagged null record;
function Area (S : Shape) return Float is abstract;
```
- An interface has no components; a type can implement many.
- Abstract types cannot be instantiated.
- Null procedure default: `procedure Reset (X : T) is null;`
## Gotchas
- Every abstract primitive must be overridden in a concrete extension.
## Self-check
Try to declare an object of an abstract type and read the error.
