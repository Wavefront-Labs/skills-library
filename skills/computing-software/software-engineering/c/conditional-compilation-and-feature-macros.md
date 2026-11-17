---
id: computing-software.software-engineering.c.conditional-compilation-and-feature-macros
name: conditional-compilation-and-feature-macros
category: computing-software
field: software-engineering
product: c
tags: [c, conditional-compilation, ifdef, predefined-macros, has-include, platform-detection]
level: practitioner
status: docs-checked
description: "Use #if/#ifdef, predefined macros and __has_include for portable platform and feature selection."
sources: ["https://en.cppreference.com/w/c/preprocessor/conditional", "https://en.cppreference.com/w/c/preprocessor/replace", "https://en.cppreference.com/w/c/language/function_definition", "https://gcc.gnu.org/onlinedocs/cpp/Standard-Predefined-Macros.html", "https://gcc.gnu.org/onlinedocs/cpp/Common-Predefined-Macros.html", "https://gcc.gnu.org/onlinedocs/cpp/Invocation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional compilation and feature macros

Goal: platform branches that stay small, testable and correct.

- Prefer `#if defined(X) && ...` over nested `#ifdef`; an undefined macro in `#if` evaluates to 0.
- Standard predefined: `__STDC_VERSION__` (e.g. 199901L, 201112L, 201710L), `__STDC_HOSTED__`, `__FILE__`, `__LINE__`, `__func__` (a variable, not a macro).
- Compiler and OS macros are not standard (GCC defines `__GNUC__`); read your compiler's documentation for the others. List what a GCC-compatible compiler defines with `gcc -dM -E - < /dev/null`.
- `__has_include(<header>)` is standard from C23; check your compiler's documentation before relying on it, or on `__has_attribute`/`__has_builtin`, in earlier modes.
- Concentrate `#if` blocks in one compat header; keep application code free of them.
- Test each configuration in CI; untested branches rot.

Verify: build with each `-D` option combination in a matrix and run `gcc -E` to confirm the intended branch is selected.

## Checked

- Date: 2026-11-02
- Confirmed: cppreference (an identifier that is not a constant is replaced with 0 in `#if`; `__STDC_VERSION__` values 199901L, 201112L, 201710L; `__STDC_HOSTED__`; `__has_include` listed as C23; `__func__` is a predefined variable); GCC cpp manual (`__GNUC__`, `__STDC_HOSTED__`, `-dM` lists macros). Removed: `__clang__`, `_MSC_VER`, `_WIN32`, `__linux__`, `__APPLE__` and the claim that `__has_include`/`__has_attribute`/`__has_builtin` are widely supported extensions (not stated on the pages read).
Method: documentation only; no commands were run.
