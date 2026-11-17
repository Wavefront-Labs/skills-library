---
id: computing-software.software-engineering.fortran.ieee-exceptions
name: ieee-exceptions
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, ieee-exceptions, fortran-ieee]
level: advanced
status: docs-checked
description: "Enable floating-point traps with gfortran -ffpe-trap and print exception summaries with -ffpe-summary."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Floating-point exceptions and traps
**Goal:** detect numerical failures.
- `-ffpe-trap=<list>` enables traps; the list is comma separated from `invalid`, `zero`, `overflow`, `underflow`, `inexact`, `denormal` (or `none` to clear). A trapped exception sends `SIGFPE`, aborting the program with a core file useful for debugging.
- The manual suggests that trapping `invalid`, `zero` and `overflow` is probably a good idea unless the program handles these exceptions; `inexact` is likely uninteresting. By default no traps are enabled. Once enabled a trap cannot be disabled except by `-ffpe-trap=none`.
- `-ffpe-summary=<list>` (`none`, `all` or exceptions) prints the flag status to `ERROR_UNIT` at `STOP` and `ERROR STOP`; by default all but `inexact` are shown.
```bash
gfortran -g -ffpe-trap=invalid,zero,overflow -o app main.f90
```
- Querying and setting exception flags from code is done with the `IEEE_EXCEPTIONS` module of the Fortran standard (procedure names not on the pages checked).
## Gotchas
- `-ffpe-trap` takes effect at run time through signals; use `-g` so the core file or debugger shows the source line.
## Self-check
Build with `-ffpe-trap=zero` and divide by a variable holding zero to confirm the program aborts with SIGFPE.

## Checked
2026-11-02. Confirmed in invoke.texi: -ffpe-trap list, SIGFPE behaviour, recommended traps, default none, -ffpe-trap=none, -ffpe-summary semantics and default. Removed: ieee_set_flag/ieee_get_flag example and flag names, reordering and speculative-trap claims, backtrace claim (not on pages read).
Method: documentation only; no commands were run.
