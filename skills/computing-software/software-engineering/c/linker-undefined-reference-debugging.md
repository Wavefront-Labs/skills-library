---
id: computing-software.software-engineering.c.linker-undefined-reference-debugging
name: linker-undefined-reference-debugging
category: computing-software
field: software-engineering
product: c
tags: [c, undefined-reference, link-order, multiple-definition, nm, ld-errors]
level: practitioner
status: docs-checked
description: "Diagnose undefined reference and multiple definition link errors with nm, link order and symbol checks."
sources: ["https://gcc.gnu.org/onlinedocs/gcc/Code-Gen-Options.html", "https://gcc.gnu.org/gcc-10/porting_to.html", "https://sourceware.org/binutils/docs/ld/Options.html", "https://sourceware.org/binutils/docs/binutils/nm.html", "https://man7.org/linux/man-pages/man3/sqrt.3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linker undefined reference debugging

Goal: turn a wall of `ld` errors into a one-line fix.

- "undefined reference to `foo`": declared but no definition linked. Check the object/library providing it: `nm -C libx.a | grep foo` (nm marks undefined symbols `U`; uppercase letters are global symbols).
- With static libraries, order matters for GNU ld: put libraries after the objects that use them (`gcc main.o -lm -lfoo`); dependent libs go later. `-Wl,--start-group libs -Wl,--end-group` resolves cycles.
- Forgotten libraries are classic; math functions like `sqrt` need `-lm` (the man page says to link with the math library).
- "multiple definition of `x`": a variable defined (not `extern`) in a header included twice; also `-fcommon` vs `-fno-common` (GCC 10 defaults to `-fno-common`, exposing tentative definitions in headers).
- C name vs C++ mangling: C++ code must wrap C headers in `extern "C"`; check with `nm` (mangled `_Z...` names).
- Show the actual link command with `gcc -v` or `make V=1`; `-Wl,--trace-symbol=foo` shows where a symbol is resolved.

Verify: after the fix, `ldd ./prog` (shared) lists expected libs and the binary runs.

## Checked

- Date: 2026-11-02
- Confirmed: GCC manual (`-fcommon`/`-fno-common` and that `-fno-common` is the default); GCC 10 porting notes (default changed to `-fno-common`, exposing definitions without `extern` in headers); ld manual (`-Wl,` prefix, `--start-group`/`--end-group`, `--trace-symbol`); nm manual (symbol type letters, uppercase = global); sqrt(3) (link with `-lm`). Removed: `-lpthread (older glibc)`, `-ldl`, the `__stack_chk_fail`/`main` bullet.
Method: documentation only; no commands were run.
