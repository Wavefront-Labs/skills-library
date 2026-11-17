---
id: computing-software.software-engineering.fortran.derived-type-basics
name: derived-type-basics
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, derived-type-basics, fortran-derived-types]
level: intro
status: docs-checked
description: "Define a derived type, access components with the percent sign, and use default component initialisation and private components."
sources:
  - https://fortran-lang.org/learn/quickstart/derived_types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining and using derived types
**Goal:** group related data in a type.
```fortran
type :: point
  real :: x = 0.0, y = 0.0     ! default initialisation
end type point
type(point) :: p
p%x = 1.5
```
- Components are accessed with `%`.
- `private` inside the type hides components outside the module; `public`/`private` statements go before components.
- Components may be `allocatable` or `pointer`.
- Construct a value with the type name: `point(1.5, 2.0)` or `point(y=2.0)`; keyword arguments may come in any order.
- `sequence` keeps components in the declared order; `bind(c)` matches a C struct but cannot be combined with `extends`, `sequence`, or `pointer` and `allocatable` components.
## Gotchas
- A derived type and its members are public by default; with a module-level `private` statement the type must be declared `public` to be used outside the module.
## Self-check
Create a point with the constructor, set `p%x`, and print both components.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn quickstart page Derived types: type syntax, `%` access, default initialisation, constructors with keywords, `private`/`public`, `sequence`, `bind(c)`, allocatable and pointer members. Removed: the linked-list claim, layout-guarantee wording, and the intrinsic assignment and `==` claims, which no page read states.
Method: documentation only; no commands were run.
