---
id: computing-software.software-engineering.c.ownership-and-free-conventions
name: ownership-and-free-conventions
category: computing-software
field: software-engineering
product: c
tags: [c, ownership-conventions, double-free, use-after-free, free-null, memory-leak-prevention]
level: practitioner
status: docs-checked
description: "Define who frees what, avoid double free and use-after-free, and document ownership in C APIs."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://www.gnu.org/software/libc/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ownership and free conventions

Goal: a single, documented owner for every allocation.

- `free(NULL)` is a no-op; `free` on anything not from the allocator, or twice, is undefined.
- Set the pointer to NULL after free when it stays in scope; this turns many double frees into harmless no-ops, though it does not fix aliases.
- API convention: `foo_create()`/`foo_destroy()` pair; document whether returned buffers are caller-owned ("caller frees with free()") or borrowed. Free with the matching deallocator.
- Make destroy functions accept NULL, like `free`.
- Prefer caller-supplied buffers (`size_t foo(char *buf, size_t cap)`) to avoid ownership transfers.
- Arena/pool allocators (allocate many, free all at once) remove per-object ownership for request-scoped data.
- Never `free` a pointer into the middle of an allocation or one you advanced.

Verify: `valgrind --leak-check=full --show-leak-kinds=all ./prog` should report that all heap blocks were freed.

## Checked

2026-11-02. Confirmed: `free(NULL)` does nothing; freeing a pointer not returned by an allocation function, or twice, is undefined (cppreference free); Valgrind `--leak-check=full` and `--show-leak-kinds` (Memcheck manual). Removed: the Windows DLL claim. Not checked: ownership conventions (design advice).

Method: documentation only; no commands were run.
