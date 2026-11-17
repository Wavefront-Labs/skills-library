---
id: computing-software.software-engineering.fortran.operator-overloading
name: operator-overloading
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, operator-overloading, fortran-generic]
level: advanced
status: draft
description: "Overload +, -, *, ==, assignment and define new .op. operators with interface operator blocks."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Defined operators and assignment
**Goal:** give derived types natural syntax.
```fortran
interface operator(+)
  module procedure add_vec
end interface
interface assignment(=)
  module procedure assign_from_real
end interface
interface operator(.dot.)
  module procedure dot
end interface
```
- Operator functions take one or two `intent(in)` arguments; assignment is a subroutine with `intent(out/inout)` first and `intent(in)` second.
- Type-bound form: `procedure :: add => add_vec; generic :: operator(+) => add`.
- A new operator is named `.name.`; a defined binary operator has lower precedence than all intrinsic operators and a defined unary one has higher (confirm in the standard's precedence table).
## Gotchas
- Defined operators for intrinsic types may not redefine existing intrinsic meaning (e.g. real + real).
- Operator functions must be `pure` if you want them in `do concurrent`.
## Self-check
Compile `a + b` for your type and confirm it dispatches to `add_vec`.
