---
id: computing-software.software-engineering.cpp.c-memory-management
name: c-memory-management
category: computing-software
field: software-engineering
product: cpp
tags: [c, c-memory-management, malloc, free, realloc, ownership-conventions, goto-cleanup, double-free, integer-overflow, sei-cert-c, cpp-cert]
level: practitioner
status: docs-checked
description: "Manage memory in C safely: malloc/calloc/realloc idioms, overflow-checked sizes, ownership conventions in APIs, goto-cleanup error paths, and leak/double-free prevention."
sources: ["https://en.cppreference.com/w/c/memory", "https://wiki.sei.cmu.edu/confluence/display/c/MEM31-C.+Free+dynamically+allocated+memory+when+no+longer+needed", "https://wiki.sei.cmu.edu/confluence/display/c/MEM04-C.+Beware+of+zero-length+allocations", "https://wiki.sei.cmu.edu/confluence/display/c/INT30-C.+Ensure+that+unsigned+integer+operations+do+not+wrap"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Memory management in C

**Goal:** C code with no leaks, double frees or overflowed allocations, using explicit
ownership rules since there is no RAII.

## Allocation idioms
```c
struct item *items = calloc(n, sizeof *items);    // zeroed
if (!items) return -ENOMEM;

// realloc: never assign directly to the original pointer
struct item *tmp = realloc(items, new_n * sizeof *items);
if (!tmp) { /* items still valid */ goto fail; }
items = tmp;
```
- `sizeof *ptr` instead of `sizeof(struct item)` stays correct if the type changes.
- `n * size` can wrap (CERT INT30-C): check `if (n > SIZE_MAX / size)` before `malloc(n * size)`.
- `malloc(0)` may return NULL or a unique pointer; don't treat NULL as failure there
  (CERT MEM04-C).

## Ownership conventions (document them in the header)
- Function that returns allocated memory: name says so and states how to free
  (`char *foo_strdup(...)  /* caller frees with free() */`, or provide `foo_free()`).
- Pair constructors/destructors: `widget_new()` / `widget_free(w)`; `widget_free(NULL)`
  is a no-op like `free(NULL)`.
- Borrowed pointers (`const char *name`) are never freed by the callee; if it needs to
  keep the data, it copies.

## Single-exit cleanup
```c
int process(const char *path) {
    int rc = -1;
    FILE *f = NULL; char *buf = NULL;
    if (!(f = fopen(path, "rb"))) goto out;
    if (!(buf = malloc(BUF_SZ))) goto out;
    /* ... */
    rc = 0;
out:
    free(buf);
    if (f) fclose(f);
    return rc;
}
```

## Preventing double free / use-after-free
Set pointers to NULL after free when the variable outlives the call
(`free(p); p = NULL;`). Never free memory you did not allocate (string literals, stack).

## Tooling
Run tests under a memory checker (address and leak sanitizers or Valgrind), and enable compiler warnings and a static analyser for allocation errors.

## Verify
- [ ] Every allocating function's header documents ownership and the matching free.
- [ ] Test suite under a memory checker reports no leaks and no invalid frees.

## Checked

- Date: 2026-10-28
- Confirmed on cppreference (C memory, calloc, realloc pages) and SEI CERT (MEM04-C zero-length allocations, INT30-C unsigned wrap): realloc must not overwrite the original pointer, zero-size allocation may return NULL or a unique pointer, check multiplication before allocating.
- Removed: calloc overflow-check claim, reallocarray, malloc-cast note, Windows CRT heap note, cleanup attribute remark, sanitizer and analyzer flags.
Method: documentation only; no commands were run.
