---
id: computing-software.software-engineering.c.goto-cleanup-pattern
name: goto-cleanup-pattern
category: computing-software
field: software-engineering
product: c
tags: [c, goto-cleanup, single-exit, resource-cleanup, error-unwinding]
level: practitioner
status: docs-checked
description: "Use goto-based cleanup labels to release resources in reverse order on every error path."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://wiki.sei.cmu.edu/confluence/display/c/", "https://pubs.opengroup.org/onlinepubs/9799919799/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Goto cleanup pattern

Goal: leak-free functions with several acquisitions.

- Declare resources initialised to invalid values (`NULL`, `-1`), acquire in order, and on failure `goto` a label that releases in reverse order.
- Pattern: `int rc = -1; FILE *f = NULL; char *buf = NULL; f = fopen(...); if (!f) goto out; buf = malloc(n); if (!buf) goto out_close; ... rc = 0; out_close: fclose(f); out: return rc;` with labels in reverse acquisition order.
- Or use a single label and null-check everything (`free(NULL)` is safe; guard `fclose` and `close(fd >= 0)`).
- A `goto` may not enter the scope of a variable-length array or other variably modified type; jumping past an ordinary declaration is allowed but leaves the variable uninitialised, so declare and initialise variables at the top.
- Label names describe what is freed or the stage, not "err1".
- Keep it local to one function (the label must be in the same function as the `goto`); avoid `setjmp/longjmp` for error handling.

Verify: run each early-exit under Valgrind (`--leak-check=full`) or a leak-checking sanitizer build.

## Checked

2026-11-02. Confirmed: label must be in the same function, jumping into the scope of a variably modified type is not allowed while entering a non-VM variable's scope is (cppreference goto); `free(NULL)` does nothing (cppreference free); Valgrind `--leak-check=full` (Memcheck manual). Removed: Linux kernel idiom claim, the cleanup attribute bullet and the ASAN_OPTIONS detail (not confirmed from a fetched page).

Method: documentation only; no commands were run.
