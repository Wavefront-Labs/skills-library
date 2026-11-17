---
id: computing-software.software-engineering.c.uninitialized-and-dangling-pointer-ub
name: uninitialized-and-dangling-pointer-ub
category: computing-software
field: software-engineering
product: c
tags: [c, dangling-pointer, uninitialized-variable, use-after-scope, returning-local-address]
level: practitioner
status: docs-checked
description: "Spot uninitialised reads, dangling pointers and returned stack addresses before they become heisenbugs."
sources: ["https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html", "https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html", "https://github.com/google/sanitizers/wiki/AddressSanitizerFlags", "https://valgrind.org/docs/manual/mc-manual.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uninitialized and dangling pointer ub

Goal: eliminate lifetime errors with tooling and conventions.

- Locals with automatic storage are uninitialised; reading them is undefined (indeterminate values may be trap representations). Initialise at declaration: `T x = {0};`
- Returning `&local` or storing it in a longer-lived struct creates a dangling pointer; compilers warn on the direct case (check your compiler's warning list).
- Pointers become invalid after `free`, after `realloc` moves the block, and after the enclosing block ends.
- Do not keep pointers into a growing array across an append (realloc may move it); use indexes.
- Tools: `-Wall -Wextra -Wuninitialized -Wmaybe-uninitialized`; AddressSanitizer with `-fsanitize=address` (GCC's `-fsanitize=address` enables `-fsanitize-address-use-after-scope`; set `ASAN_OPTIONS=detect_stack_use_after_return=1` for use-after-return, which defaults to false); Valgrind Memcheck for uninitialised reads.

Verify: reproduce with ASan, which prints allocation and free stack traces for the bad access.

## Checked

- Date: 2026-11-02
- Confirmed: GCC manual `-Wuninitialized`, `-Wmaybe-uninitialized` and that `-fsanitize=address` enables use-after-scope; AddressSanitizer flags wiki (`detect_stack_use_after_return`, default false); Valgrind Memcheck manual (use of uninitialised values). Removed: `-Wreturn-local-addr`/`-Wreturn-stack-address` (not in the GCC option list read), the comparison-of-invalid-pointers remark and the Clang default claim.
Method: documentation only; no commands were run.
