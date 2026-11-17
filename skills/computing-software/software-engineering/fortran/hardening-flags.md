---
id: computing-software.software-engineering.fortran.hardening-flags
name: hardening-flags
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, hardening-flags, fortran-security]
level: advanced
status: gated
description: "Build release binaries with GCC stack protector and PIE flags and bounds checking where affordable."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/
  - https://gcc.gnu.org/onlinedocs/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardening compiler and linker flags
**Goal:** raise the cost of exploiting memory bugs.
```bash
gfortran -O2 -fstack-protector-strong -fPIE -pie -o app *.f90
gfortran -g -fcheck=bounds -o app_checked *.f90
```
- `-fstack-protector-strong`, `-fPIE` and `-pie` are GCC options and apply to gfortran, which is a GCC front end; their exact effect is described in the GCC manual.
- Linker hardening options (such as RELRO) are passed to the linker with `-Wl,`; see the linker documentation for your platform (gated: unconfirmed, source is paywalled or blocked).
- `-fcheck=bounds` generates run-time checks for array subscripts against the declared bounds; it also checks assumed- and deferred-shape arrays against the allocated bounds.
- For C interop code, treat the C side with the same hardening.
## Gotchas
- Pure Fortran array-heavy code is mainly exposed through out-of-bounds writes and misuse of `c_f_pointer`.
- Hardening flags do not replace bounds checking.
## Self-check
Inspect the built binary with the platform tools (`readelf` on Linux) to confirm it is position independent.

## Checked
2026-11-02. Confirmed in the GCC manual: -fstack-protector-strong, -fPIE, -pie exist; GNU Fortran manual: -fcheck=bounds behaviour. Removed: _FORTIFY_SOURCE advice, checksec, performance claims. Gated: the -Wl,-z relro flags are not in the pages read.
Gated: the linker relro/now options are not in the pages read.
Method: documentation only; no commands were run.
