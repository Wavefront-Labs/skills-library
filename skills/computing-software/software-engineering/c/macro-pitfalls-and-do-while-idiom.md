---
id: computing-software.software-engineering.c.macro-pitfalls-and-do-while-idiom
name: macro-pitfalls-and-do-while-idiom
category: computing-software
field: software-engineering
product: c
tags: [c, c-preprocessor, macro-pitfalls, do-while-0, macro-parenthesization, multiple-evaluation, stringify-paste]
level: practitioner
status: docs-checked
description: "Write safe function-like macros: parenthesise, avoid double evaluation, wrap statements in do-while(0)."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://gcc.gnu.org/onlinedocs/cpp/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Macro pitfalls and do while idiom

Goal: macros that behave like the function they imitate.

- Parenthesise every parameter and the whole expansion: `#define SQUARE(x) ((x) * (x))`.
- Arguments with side effects evaluate multiple times: `SQUARE(i++)` evaluates `i++` twice. Prefer `static inline` functions; use macros only for types-generic needs, token pasting or `__FILE__`/`__LINE__`.
- Multi-statement macros: `#define LOG(msg) do { fprintf(stderr, "%s\n", (msg)); } while (0)` so that `if (x) LOG("a"); else ...` parses.
- `#x` stringifies, `a ## b` pastes tokens; to expand a macro before stringifying use two levels: `#define STR(x) XSTR(x)` / `#define XSTR(x) #x`.
- Variadic macros: `#define LOG(fmt, ...) fprintf(stderr, fmt, __VA_ARGS__)` needs at least one variable argument under strict conformance; GCC documents two workarounds: `__VA_OPT__(,)` (C++20, also available in GNU C) and the GNU `##__VA_ARGS__` extension that deletes the comma.
- Inspect results with `gcc -E file.c`.

Verify: run `gcc -E` on the call sites and read the expansion.

## Checked

2026-11-02. Confirmed: `__VA_OPT__` and `##__VA_ARGS__` behaviour and `__VA_ARGS__` rules (GCC CPP manual, Variadic Macros); stringizing two-level expansion (GCC CPP manual, Stringizing). Removed: 'undefined' wording on SQUARE(i++), the C23 claim and `-E -P`. Not checked: parenthesisation and do-while advice (well-known idiom, judgement).

Method: documentation only; no commands were run.
