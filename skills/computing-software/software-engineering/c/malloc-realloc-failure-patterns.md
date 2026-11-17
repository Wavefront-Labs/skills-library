---
id: computing-software.software-engineering.c.malloc-realloc-failure-patterns
name: malloc-realloc-failure-patterns
category: computing-software
field: software-engineering
product: c
tags: [c, c-dynamic-memory, realloc-pattern, malloc-null-check, calloc, sizeof-star-idiom]
level: practitioner
status: docs-checked
description: "Allocate and grow buffers correctly: check NULL, size by sizeof *p, and never lose the pointer on realloc failure."
sources: ["https://en.cppreference.com/w/c/memory/malloc", "https://en.cppreference.com/w/c/memory/realloc", "https://en.cppreference.com/w/c/memory/calloc", "https://man7.org/linux/man-pages/man3/malloc.3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Malloc realloc failure patterns

Goal: allocation code that survives failure without leaks.

- Always test the result of `malloc`/`calloc`/`realloc` for NULL.
- Size by the pointed-to object: `T *p = malloc(n * sizeof *p);` (survives type changes); use `calloc(n, sizeof *p)` for zeroed arrays with its built-in overflow check.
- `p = realloc(p, new)` leaks the original when realloc returns NULL. Use a temp: `void *t = realloc(p, new); if (!t) { /* p still valid */ } else p = t;`
- `realloc(p, 0)` has implementation-defined behaviour before C23 and is undefined in C23; do not use it to free.
- Grow geometrically (double capacity) for amortised O(1) appends; keep `len` and `cap` in a struct.
- `malloc(0)` may return NULL or a unique pointer; handle both.
- Memory from `malloc` is uninitialised.

Verify: run under Valgrind or `-fsanitize=address`; inject failures with a wrapper that returns NULL on the Nth call.

## Checked

- Date: 2026-11-02
- Confirmed: cppreference malloc (uninitialised storage, `malloc(0)` implementation-defined), realloc (on size 0: implementation-defined and deprecated since C17, undefined since C23); man7 malloc(3) (calloc reports an error if `n * size` overflows). The realloc temporary-pointer pattern and geometric growth are standard practice. Removed: the Linux overcommit remark.
Method: documentation only; no commands were run.
