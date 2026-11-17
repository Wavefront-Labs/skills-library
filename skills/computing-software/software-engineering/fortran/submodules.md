---
id: computing-software.software-engineering.fortran.submodules
name: submodules
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, submodules, fortran-modules]
level: advanced
status: docs-checked
description: "Split module interface from implementation with separate module procedures and submodules to cut recompilation cascades."
sources:
  - https://fortran-lang.org/learn/best_practices/modules_programs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Submodules
**Goal:** reduce rebuild times.
```fortran
module m
  interface
    module function f(x) result(y)
      real, intent(in) :: x
      real :: y
    end function
  end interface
end module
submodule (m) m_impl
contains
  module function f(x) result(y)
    real, intent(in) :: x
    real :: y
    y = 2.0 * x
  end function
end submodule
```
- Submodules break long dependency chains and shorten recompilation cascades, and can give specialised implementations without a preprocessor.
- The module holds only interfaces (`module function` declarations); the implementation goes in `submodule (m) name`.
- Module procedures need not all be implemented in the same submodule; several submodules can reduce the compilation load of a huge module.
## Gotchas
- The implementation repeats the interface of the `module function` it implements, as in the `stdlib_quadrature` example.
## Self-check
Split a module into an interface module and a submodule and confirm the program using it still builds.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn page Modules and Programs (section on submodules, with the `stdlib_quadrature` interface module and `submodule (stdlib_quadrature) stdlib_quadrature_trapz`). Removed: the `.smod` file claims, `module procedure` implementation form, build ordering and compiler-bug notes, and the self-check about rebuilds, which no page read covers.
Method: documentation only; no commands were run.
