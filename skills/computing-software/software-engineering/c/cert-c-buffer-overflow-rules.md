---
id: computing-software.software-engineering.c.cert-c-buffer-overflow-rules
name: cert-c-buffer-overflow-rules
category: computing-software
field: software-engineering
product: c
tags: [c, c-secure-coding, buffer-overflow, cert-c, bounds-checking, off-by-one, stack-smashing]
level: advanced
status: gated
description: "Prevent buffer overflows with length-carrying APIs, off-by-one reviews and checked allocation sizes."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://wiki.sei.cmu.edu/confluence/display/c/", "https://gcc.gnu.org/onlinedocs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cert c buffer overflow rules

Goal: remove the classic memory-corruption bugs by construction.

- Sources of overflows: unbounded copies (`gets` (removed in C11), `strcpy`, `sprintf`), off-by-one (forgetting the NUL), integer overflow in size computations, trusting lengths from input, and `memcpy` with a signed negative length converted to huge `size_t`.
- Rules of thumb (SEI CERT C rule themes for arrays, strings, integers and memory; the CERT wiki is blocked here, so no individual rule ids are cited) (gated: unconfirmed, source is paywalled or blocked): pass buffer + capacity together; validate every external length against both a maximum and the destination size; compute `n * size` with overflow checks; prefer `snprintf`, `memcpy` with checked sizes, and `fgets` over `scanf("%s")` (or use `scanf("%99s")` width limits).
- Use types that cannot be negative (`size_t`) and keep arithmetic on lengths in one place.
- Design: small fixed-capacity buffer structs with append functions that check remaining space.
- Detect during development with AddressSanitizer, fuzzing and `-D_FORTIFY_SOURCE=2` (or 3, which needs gcc 12+ or clang 9+ with glibc 2.33+); see the hardening skill.

Verify: fuzz the parser entry point for 10 minutes with an ASan build and confirm no crashes; add every crash input as a regression test.

## Checked

2026-11-02. Confirmed: `gets` removed in C11 (cppreference gets); `_FORTIFY_SOURCE` levels 1/2/3 and the gcc 12 / clang 9 / glibc 2.33 requirement for level 3 (Linux man-pages feature_test_macros(7)). Removed: fuzzer tool names. Gated: the SEI CERT rule themes (wiki blocked). Not checked: general bounds-checking advice (judgement).

Method: documentation only; no commands were run.
