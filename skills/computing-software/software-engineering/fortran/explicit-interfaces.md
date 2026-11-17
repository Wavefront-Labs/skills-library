---
id: computing-software.software-engineering.fortran.explicit-interfaces
name: explicit-interfaces
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, explicit-interfaces, fortran-interfaces]
level: practitioner
status: docs-checked
description: "Put procedures in modules to get explicit interfaces, and use -Wimplicit-interface to find calls without one."
sources:
  - https://fortran-lang.org/learn/quickstart/organising_code
  - https://gcc.gnu.org/onlinedocs/gfortran/Error-and-Warning-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Explicit interfaces and why modules supply them
**Goal:** avoid undetected argument mismatches.
- Procedures placed in a module get an explicit interface automatically; the quickstart recommends always placing functions and subroutines in modules.
- Assumed-shape arguments rely on that interface. Outside a module you must pass the dimensions and declare explicit-shape arguments instead.
- gfortran `-Wimplicit-interface` warns when a procedure is called without an explicit interface; it only checks that one is present, not that the declared interfaces agree across program units.
- gfortran `-Waliasing` warns when the same actual argument is associated with an `intent(in)` and an `intent(out)` dummy in a call with an explicit interface.
## Gotchas
- Consistency of interfaces between program units is not checked by `-Wimplicit-interface`.
## Self-check
Call an external routine that is not in a module and confirm `-Wimplicit-interface` warns.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn page Organising code structure (modules generate explicit interfaces, assumed-shape versus explicit-shape) and the gfortran Error and Warning Options page (`-Wimplicit-interface`, `-Waliasing`). Removed: the list of features that require an interface, the interface-block example, the `-Wall` mismatch claim and the `import` and link-time notes, which no page read covers.
Method: documentation only; no commands were run.
