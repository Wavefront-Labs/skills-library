---
id: computing-software.software-engineering.c.flexible-array-members-and-aligned-alloc
name: flexible-array-members-and-aligned-alloc
category: computing-software
field: software-engineering
product: c
tags: [c, flexible-array-member, aligned-alloc, alignas, struct-hack, max-align-t]
level: advanced
status: docs-checked
description: "Use C99 flexible array members for variable-size structs and aligned_alloc/alignas for alignment-sensitive memory."
sources: ["https://en.cppreference.com/w/c/language/struct", "https://en.cppreference.com/w/c/memory/aligned_alloc", "https://en.cppreference.com/w/c/memory/malloc", "https://man7.org/linux/man-pages/man3/posix_memalign.3.html", "https://en.cppreference.com/w/c/language/_Alignas"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flexible array members and aligned alloc

Goal: single-allocation variable-length objects and correct alignment.

- Flexible array member: `struct buf { size_t len; unsigned char data[]; };` allocate `malloc(sizeof(struct buf) + n)`. It must be the last member.
- `sizeof(struct buf)` excludes the flexible part (may include trailing padding); a safe size is `offsetof(struct buf, data) + n`. Check the addition for overflow.
- Prefer the C99 form to `data[1]` / `data[0]` hacks.
- `malloc` returns memory suitably aligned for any object type with fundamental alignment. For stricter alignment (SIMD, cache lines) use `aligned_alloc(alignment, size)` (C11; alignment must be one the implementation supports and size a multiple of it) or POSIX `posix_memalign`. Free with `free`.
- Declare aligned objects with `_Alignas(n)` / `alignas(n)` from `<stdalign.h>`.

Verify: print `(uintptr_t)p % alignment` and assert it is 0.

## Checked

- Date: 2026-11-02
- Confirmed: cppreference (flexible array member exists in structs; `aligned_alloc` size must be an integral multiple of alignment; `malloc` returns memory aligned for fundamental alignment; `alignas`/`_Alignas`), man7 posix_memalign (alignment a power of two and a multiple of `sizeof(void *)`). Removed: the strict-ISO restriction on arrays of such structs, the MSVC remark and the 'non-standard' label for the old hacks.
Method: documentation only; no commands were run.
