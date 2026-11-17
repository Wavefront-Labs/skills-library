---
id: computing-software.firmware-embedded-development.bare-metal-programming.function-like-macros-vs-inline
name: function-like-macros-vs-inline
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [function-like-macros, embedded-c-coding-standard, static-inline, macro-pitfalls, gcc-inline, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Replace function-like macros with static inline functions where possible, write the macros you keep safely, and know where macros remain necessary."
sources:
  - https://gcc.gnu.org/onlinedocs/cpp/Macro-Pitfalls.html
  - https://gcc.gnu.org/onlinedocs/cpp/Operator-Precedence-Problems.html
  - https://gcc.gnu.org/onlinedocs/cpp/Swallowing-the-Semicolon.html
  - https://gcc.gnu.org/onlinedocs/cpp/Duplication-of-Side-Effects.html
  - https://gcc.gnu.org/onlinedocs/cpp/Stringizing.html
  - https://gcc.gnu.org/onlinedocs/cpp/Concatenation.html
  - https://gcc.gnu.org/onlinedocs/cpp/Standard-Predefined-Macros.html
  - https://gcc.gnu.org/onlinedocs/gcc/Inline.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function-like macros vs inline functions

## Prefer `static inline`
```c
#define MAX(a, b) ((a) > (b) ? (a) : (b))          /* MAX(i++, j) increments twice */
static inline uint32_t max_u32(uint32_t a, uint32_t b) { return a > b ? a : b; }
```
A `static inline` function evaluates each argument once and is type checked. GCC can integrate it
into its callers, removing call overhead, and when all calls are integrated and its address is never
used, no assembler code is emitted for it. Put them in headers as `static inline`. Inlining is not
guaranteed: GCC does not inline any function when not optimizing unless it has the
`always_inline` attribute, and `-Winline` warns when a function marked inline could not be
substituted. Variadic functions, `alloca`, computed `goto`, nested functions and `setjmp` make a
function unsuitable for inlining. The effect on code size is less predictable: it can grow or shrink.

## Classic macro pitfalls
| Pitfall | Example | Fix |
|---|---|---|
| Missing parentheses | `#define SQ(x) x*x` -> `SQ(a+1)` = `a+1*a+1` | parenthesise each argument and the whole expansion |
| Double evaluation | `MAX(read_reg(), 0)` may read twice | inline function (the GCC manual calls such a macro unsafe) |
| Multi-statement macros | `#define RST() a(); b()` in `if (x) RST();` | `do { a(); b(); } while (0)` |
| Semicolon before `else` | `if (x) M(); else ...` with a `{ }` macro is invalid C | `do { } while (0)` (one statement; most compilers add no code) |
| Name capture | a statement-expression macro's local `tmp` can clash with the caller's | trailing-underscore names reduce the risk but do not remove it; prefer an inline function |

## Where macros are still the right tool
- **Stringification (`#`) and token pasting (`##`):** `#define REG(name) { #name, &PERIPH->name }`,
  X-macros to keep enum and string tables in sync.
- **`__FILE__`/`__LINE__` capture** in logging and assert macros: they expand where the macro is
  used, which a function cannot do.
- **Conditional compilation** of code that must vanish entirely (log levels).
- **Bit masks for registers**: `#define USART_CR1_UE (1UL << 0)` (constants, not functions).

## X-macro example
```c
#define ERROR_LIST(X) X(OK, 0) X(TIMEOUT, -110) X(NACK, -6)
typedef enum {
#define X(name, val) ERR_##name = val,
    ERROR_LIST(X)
#undef X
} err_t;
```

## Verify
- [ ] No function-like macro in the code evaluates an argument more than once (code review).
- [ ] Release disassembly shows small inline functions inlined (no `bl max_u32`).

## Checked
2026-11-08. Confirmed in the GCC preprocessor manual (Macro Pitfalls: operator precedence, swallowing the
semicolon, duplication of side effects; Stringizing; Concatenation; Standard Predefined Macros for `__FILE__` and
`__LINE__`) and the GCC manual (An Inline Function is As Fast As a Macro). Removed: the MISRA C:2012 Directive 4.9
claim (the MISRA page is a paywalled order form), the claim that `-O1` or `-Os` inline trivial functions, the
`_Generic` and constant-expression bullets, and the cppcheck remark. The disassembly check was not checked
against a manual.
Method: documentation only; no commands were run.
