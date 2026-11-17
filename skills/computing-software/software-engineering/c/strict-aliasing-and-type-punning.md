---
id: computing-software.software-engineering.c.strict-aliasing-and-type-punning
name: strict-aliasing-and-type-punning
category: computing-software
field: software-engineering
product: c
tags: [c, c-undefined-behavior, strict-aliasing, type-punning, union-punning, memcpy-punning, fno-strict-aliasing]
level: advanced
status: docs-checked
description: "Avoid strict-aliasing violations and pun types safely with memcpy or unions."
sources: ["https://en.cppreference.com/w/c/language/object", "https://en.cppreference.com/w/c/language/union", "https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html", "https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html", "https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strict aliasing and type punning

Goal: reinterpret bytes without miscompilation at -O2.

- Accessing an object through an lvalue of an incompatible type is undefined; the optimiser may reorder or cache loads and stores on that assumption. Character types (`char`, `unsigned char`) may alias anything.
- Broken: `float f; uint32_t u = *(uint32_t *)&f;`
- Safe: `uint32_t u; memcpy(&u, &f, sizeof u);` (compilers optimise it to a register move).
- Reading a different member of a union than last written is allowed for type punning in C (implementation-defined representation).
- `-Wstrict-aliasing` (GCC, included in `-Wall`) warns on some cases; `-fstrict-aliasing` is enabled at `-O2`, `-O3` and `-Os`, and `-fno-strict-aliasing` disables the assumption but costs optimisation and hides bugs.
- Alignment also matters; `memcpy` avoids alignment problems as well.

Verify: compare behaviour at `-O0` and `-O2`; diverging output is a red flag. Run with `-fsanitize=undefined` (alignment checks).

## Checked

- Date: 2026-11-02
- Confirmed: cppreference object page (accessing an object through an incompatible lvalue is UB; character types are exempt; type punning through an inactive union member); union page (type punning, TC3); GCC manual `-fstrict-aliasing` (enabled at -O2, -O3, -Os), `-Wstrict-aliasing` (in `-Wall`), `-fsanitize=alignment`. Removed: the 'unlike C++' comparison, the Linux kernel remark and the odd-address UB claim.
Method: documentation only; no commands were run.
