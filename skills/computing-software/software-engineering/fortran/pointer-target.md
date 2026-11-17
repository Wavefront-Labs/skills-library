---
id: computing-software.software-engineering.fortran.pointer-target
name: pointer-target
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, pointer-target, fortran-pointers]
level: practitioner
status: docs-checked
description: "Associate pointers with targets, test with associated, and prefer allocatable unless you need aliasing or linked structures."
sources:
  - https://fortran-lang.org/learn/intrinsics/ASSOCIATED
  - https://fortran-lang.org/learn/intrinsics/NULL
  - https://fortran-lang.org/learn/best_practices/allocatable_arrays
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pointer, target and association
**Goal:** use pointers only when needed.
```fortran
real, target :: x(10)
real, pointer :: p(:)
p => x(2:5)             ! pointer assignment, not copy
print *, associated(p), size(p)
```
- Pointer targets carry the `target` attribute, as in the `associated` page examples.
- `null()` returns a disassociated pointer; `associated(p)` tests whether `p` has a target, and `associated(p, t)` tests for a specific target.
- `allocatable` memory is freed automatically at scope exit, which pointers do not offer, so prefer `allocatable` where possible.
## Gotchas
- A pointer given to `associated` must not have an undefined association status, so initialise it, for example with `=> null()`.
- Use `=>` for association and `=` for value assignment; mixing them is the classic bug.
## Self-check
Change `p(1)` and confirm `x(2)` changes.

## Checked
2026-11-03. Confirmed against the fortran-lang.org intrinsic pages for `associated` and `null` and the Allocatable Arrays page (automatic deallocation versus pointers). Removed: `nullify`, the aliasing performance claim, the manual-`deallocate` rule and the non-target actual argument rule, which no page read covers.
Method: documentation only; no commands were run.
