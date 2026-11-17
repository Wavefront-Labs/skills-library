---
id: computing-software.software-engineering.fortran.gfortran-warnings
name: gfortran-warnings
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, gfortran-warnings, fortran-gfortran]
level: practitioner
status: docs-checked
description: "Enable a strong warning set with -Wall -Wextra and targeted flags such as -Wconversion, -Wimplicit-interface, -Wunused and -pedantic."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Warning flags
**Goal:** let the compiler find bugs.
```bash
gfortran -Wall -Wextra -pedantic -std=f2018 -Wconversion-extra -Wimplicit-interface \
         -Wimplicit-procedure -Warray-temporaries -c module.f90
```
- `-Wall` currently includes `-Waliasing`, `-Wampersand`, `-Wconversion`, `-Wsurprising`, `-Wc-binding-type`, `-Wintrinsics-std`, `-Wtabs`, `-Wintrinsic-shadow`, `-Wline-truncation`, `-Wtarget-lifetime`, `-Winteger-division`, `-Wreal-q-constant`, `-Wunused`, `-Wundefined-do-loop` and `-Wundefined-vars`.
- `-Wextra` implies `-Wcompare-reals` (warns when real or complex values are compared for equality or inequality).
- `-Wconversion-extra` warns about implicit conversions between different types and kinds; it does not imply `-Wconversion`.
- `-Wimplicit-interface` and `-Wimplicit-procedure` flag calls to procedures without an explicit interface.
- `-Wunused-parameter`, `-Wcharacter-truncation` and `-Warray-temporaries` are separate options.
- `-Werror` turns warnings into errors.
## Gotchas
- The lists above are from the current manual; the contents of `-Wall` vary by GCC version, so check the manual for your version.
## Self-check
Compile code with an unused variable and a real `==` comparison and confirm each warning appears.

## Checked
2026-11-02. Confirmed in the GNU Fortran manual (invoke): the -Wall expansion, -Wextra implies -Wcompare-reals, -Wconversion/-Wconversion-extra, -Wimplicit-interface/-procedure, -Warray-temporaries, -Wunused-parameter, -Wcharacter-truncation; -Werror in the GCC manual. Removed: -Wsurprising/-Wintrinsics-std placement (now listed under -Wall), -Wmaybe-uninitialized note and CI version-pinning advice (not stated).
Method: documentation only; no commands were run.
