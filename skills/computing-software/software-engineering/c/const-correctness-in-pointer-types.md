---
id: computing-software.software-engineering.c.const-correctness-in-pointer-types
name: const-correctness-in-pointer-types
category: computing-software
field: software-engineering
product: c
tags: [c, const-correctness, pointer-to-const, const-pointer, restrict]
level: practitioner
status: docs-checked
description: "Read and write const and restrict qualified pointer declarations and keep APIs const-correct."
sources: ["https://en.cppreference.com/w/c/language/restrict", "https://en.cppreference.com/w/c/language/string_literal", "https://en.cppreference.com/w/c/string/byte/strchr", "https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Const correctness in pointer types

Goal: express read-only intent so the compiler enforces it.

- Read declarations right to left: `const char *p` is pointer to const char (cannot modify `*p`); `char *const p` is a const pointer (cannot reassign `p`); `const char *const p` is both.
- Take `const T *` for input parameters; return non-const only when the caller owns the object. `strchr` and friends return `char *` from a `const char *` argument in C before C23 (C23 adds a qualifier-preserving form); wrap in your own API if needed.
- Converting `char **` to `const char **` is not implicit (it would break const-safety); use `const char *const *`.
- Modifying a string literal is undefined behaviour. Prefer `const char *s = "..."`.
- `restrict` promises no aliasing between objects accessed through different restrict pointers; violating it is UB. Use it only when true.

Verify: compile with `-Wcast-qual` and fix each warning rather than casting.

## Checked

- Date: 2026-11-02
- Confirmed: cppreference strchr declarations (`char *strchr(const char *, int)`; qualifier-generic form since C23), string literals are not modifiable (UB), `restrict` violations are UB; GCC manual `-Wcast-qual` (warns on removing a qualifier and on `char **` to `const char **` casts). Removed: the claim about casting away const on a const-defined object and the `-Wwrite-strings` recommendation (not verified on the fetched page).
Method: documentation only; no commands were run.
