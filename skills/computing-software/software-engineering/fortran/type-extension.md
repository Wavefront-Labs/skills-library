---
id: computing-software.software-engineering.fortran.type-extension
name: type-extension
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, type-extension, fortran-oop]
level: practitioner
status: docs-checked
description: "Extend a derived type with extends(parent) and use the inherited components directly."
sources:
  - https://fortran-lang.org/learn/quickstart/derived_types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type extension and inheritance
**Goal:** model is-a relationships.
```fortran
type :: shape
  character(len=:), allocatable :: name
end type
type, extends(shape) :: circle
  real :: r = 1.0
end type
```
- `extends(parent)` makes the child inherit all members of the parent; use them directly, e.g. `c%name`.
- Extensions can be chained: each type inherits everything above it.
- A `class(shape)` dummy accepts a `circle`, because `class` allows any type that extends `shape`.
## Gotchas
- A type with `bind(c)` or `sequence` cannot have `extends`.
## Self-check
Set `c%name` and `c%r` on a `circle` and pass it to a `class(shape)` dummy.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn quickstart page Derived types: `extends`, inherited member access through a chain of extensions, `class(t)` accepting extensions, the `bind(c)`/`sequence` restriction. Removed: overriding rules, single-inheritance, the parent-component and constructor forms, and the generics comparison, which no page read covers.
Method: documentation only; no commands were run.
