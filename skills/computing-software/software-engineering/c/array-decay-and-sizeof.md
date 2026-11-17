---
id: computing-software.software-engineering.c.array-decay-and-sizeof
name: array-decay-and-sizeof
category: computing-software
field: software-engineering
product: c
tags: [c, c-pointers-arrays, array-decay, sizeof-array, pointer-arithmetic, function-parameter-arrays]
level: practitioner
status: docs-checked
description: "Understand array-to-pointer decay, why sizeof fails on array parameters, and pointer arithmetic rules."
sources: ["https://en.cppreference.com/w/c/language/conversion", "https://en.cppreference.com/w/c/language/operator_arithmetic", "https://en.cppreference.com/w/c/language/array", "https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html", "https://en.cppreference.com/w/c/11"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array decay and sizeof

Goal: stop the `sizeof(arr)` and off-by-one pointer bugs.

- In most expressions an array decays to a pointer to its first element. Exceptions: operand of `sizeof`, unary `&`, and string-literal array initialisers.
- A function parameter written `int a[10]` is really `int *a`; `sizeof(a)` inside gives pointer size. Pass the length separately: `void f(const int *a, size_t n)`.
- Element count idiom (only for true arrays in scope): `#define COUNT(a) (sizeof(a) / sizeof((a)[0]))`. GCC's `-Wsizeof-pointer-div` helps catch misuse.
- Pointer arithmetic scales by element size and is defined only within an array object or one past its end; subtraction likewise needs two pointers into the same array.
- `int (*p)[10]` is a pointer to array of 10 ints; use it for 2-D arrays: `int (*m)[cols] = malloc(rows * sizeof *m);` (variably modified type, C99+, optional in C11 and later).

Verify: compile with `-Wall -Wextra` and run under `-fsanitize=address` to catch out-of-bounds from bad length handling.

## Checked

- Date: 2026-11-02
- Confirmed on cppreference: array-to-pointer conversion and its exceptions (operand of `&`, `sizeof`, string-literal initialiser); array parameters are transformed to pointers; pointer arithmetic defined only within an array or one past its end; VLAs optional in C11 (`__STDC_NO_VLA__`). Confirmed in the GCC manual: `-Wsizeof-pointer-div` and that it is enabled by `-Wall`. Removed: the claim that dereferencing one-past is invalid (not stated on the pages read).
Method: documentation only; no commands were run.
