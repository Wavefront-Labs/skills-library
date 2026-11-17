---
id: computing-software.software-engineering.fortran.intent-attributes
name: intent-attributes
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, intent-attributes, fortran-declarations]
level: intro
status: docs-checked
description: "Declare intent(in), intent(out) or intent(inout) on every dummy argument to document direction and let the compiler catch misuse."
sources:
  - https://fortran-lang.org/learn/quickstart/organising_code
  - https://fortran-lang.org/learn/best_practices/allocatable_arrays
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# intent in, out and inout
**Goal:** make argument direction explicit.
- `intent(in)`: read only. `intent(out)`: write only (an `allocatable` dummy with `intent(out)` is deallocated on entry). `intent(inout)`: read and write.
```fortran
subroutine scale(x, factor)
  real, intent(inout) :: x(:)
  real, intent(in)    :: factor
  x = x * factor
end subroutine
```
- Functions: arguments should be `intent(in)`; such functions are known as `pure`.
- Always specify intent: it lets the compiler check for unintentional errors and documents the code.
## Gotchas
- `intent(out)` is write-only: assign the argument before using it.
## Self-check
Assign to an `intent(in)` argument on purpose and confirm the compiler complains.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn pages Organising code structure (intent meanings, good practice, pure functions) and Allocatable Arrays (`allocatable` with `intent(out)` deallocates on entry). Removed: pointer-dummy intent rule, derived-type default initialisation on entry, `-Wuninitialized` and literal-argument claims, which no page read covers.
Method: documentation only; no commands were run.
