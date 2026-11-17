---
id: computing-software.software-engineering.c.assert-and-static-assert
name: assert-and-static-assert
category: computing-software
field: software-engineering
product: c
tags: [c, static-assert, assert-h, ndebug, compile-time-checks, invariants]
level: practitioner
status: docs-checked
description: "Use assert for internal invariants and _Static_assert for compile-time checks, never for input validation."
sources: ["https://en.cppreference.com/w/c/error/assert", "https://en.cppreference.com/w/c/language/_Static_assert", "https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assert and static assert

Goal: catch programmer errors early without turning validation off in release builds.

- `assert(expr)` from `<assert.h>` prints the expression, `__FILE__`, `__LINE__` and `__func__` to standard error and calls `abort()` on failure; defining `NDEBUG` removes it entirely, so never put side effects (`assert(fclose(f) == 0)`) or runtime input checks in it.
- Use assert for impossible states and preconditions of internal functions; handle bad external input with real error returns.
- `_Static_assert(cond, "message")` (C11; `static_assert` is a convenience macro in `<assert.h>`, and a keyword from C23, where the message is optional and `_Static_assert` is deprecated) checks an integer constant expression at compile time: sizes, enum counts, alignment. Example: `_Static_assert(sizeof(void *) == 8, "64-bit only");`.
- Pair an enum with a name table and assert their lengths match: `_Static_assert(sizeof names / sizeof names[0] == N_STATES, "names table");`.
- Decide per project whether release builds keep asserts.
- `__builtin_unreachable()` after assert is a GCC/Clang optimisation promise: wrong use is undefined.

Verify: compile a deliberately false static assert to see the diagnostic; build release with `-DNDEBUG` and check behaviour stays correct.

## Checked

- Date: 2026-11-02
- Confirmed on cppreference: `assert` expands to nothing under `NDEBUG`, prints the expression, `__FILE__`, `__LINE__`, `__func__` and calls `abort()`; `_Static_assert` syntax (C11), `static_assert` keyword and optional message in C23, `_Static_assert` deprecated in C23, integer constant expression. GCC manual: `__builtin_unreachable` is undefined if reached. Removed: the claim that many security-sensitive projects keep asserts in release builds.
Method: documentation only; no commands were run.
