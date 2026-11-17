---
id: computing-software.software-engineering.c.integer-promotions-and-conversions
name: integer-promotions-and-conversions
category: computing-software
field: software-engineering
product: c
tags: [c, c-integer-semantics, integer-promotion, usual-arithmetic-conversions, signed-unsigned-comparison]
level: practitioner
status: docs-checked
description: "Predict C integer promotions and usual arithmetic conversions and fix signed/unsigned comparison bugs."
sources: ["https://en.cppreference.com/w/c/language/conversion", "https://en.cppreference.com/w/c/string/byte/isalpha", "https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integer promotions and conversions

Goal: know what type an expression really has before it is compared, shifted or stored.

- Operands narrower than `int` (`char`, `short`, `_Bool`, bit-fields) are promoted to `int` (or `unsigned int` if `int` cannot hold all values) before arithmetic.
- Usual arithmetic conversions then bring both operands to a common type: if ranks differ, the lower-rank operand converts up; if one is unsigned with rank >= the other's, the signed operand converts to unsigned.
- Classic bug: `int i = -1; size_t n = 5; if (i < n)` is false, because `i` converts to a huge `size_t`. Compile with `-Wsign-compare` (in `-Wextra` for C) and fix by checking `i < 0 ||` first or by using one signed type.
- Plain `char` signedness is implementation-defined. Use `unsigned char` for bytes and cast before passing to `<ctype.h>` functions (their argument must be in `unsigned char` range or `EOF`).

Verify: `gcc -Wall -Wextra -Wconversion -c file.c` and read every sign-compare and conversion warning; add a small test printing the result of the suspect comparison.

## Checked

- Date: 2026-11-02
- Confirmed on cppreference: integer promotions to `int`/`unsigned int`; usual arithmetic conversions and the unsigned-rank rule; `<ctype.h>` arguments must be representable as `unsigned char` or EOF. GCC manual: `-Wsign-compare` is enabled by `-Wextra` in C; `-Wconversion`. Removed: the shift-count and negative-shift undefined behaviour bullet (not on the pages read).
Method: documentation only; no commands were run.
