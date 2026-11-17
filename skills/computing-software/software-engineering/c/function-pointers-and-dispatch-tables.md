---
id: computing-software.software-engineering.c.function-pointers-and-dispatch-tables
name: function-pointers-and-dispatch-tables
category: computing-software
field: software-engineering
product: c
tags: [c, function-pointer, dispatch-table, callback, typedef-function, qsort]
level: practitioner
status: docs-checked
description: "Declare function pointers with typedefs and build dispatch tables and qsort/bsearch comparators safely."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://c-faq.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function pointers and dispatch tables

Goal: callbacks and table-driven dispatch without unreadable declarations.

- Typedef the signature: `typedef int (*cmp_fn)(const void *, const void *);` then `cmp_fn f = cmp_int;`. Call as `f(a, b)`.
- Dispatch table: `static const struct { const char *name; int (*run)(int argc, char **argv); } cmds[] = { {"add", cmd_add}, {"del", cmd_del} };` then loop and compare names.
- `qsort(base, n, size, cmp)`: the comparator receives pointers to elements; return negative/zero/positive. Never return `a - b` for ints (overflow); use `(a > b) - (a < b)`.
- Call through a pointer of the function's real type; wrap mismatched signatures in a correctly typed shim.
- Converting between function pointers and `void *` is not defined by ISO C; POSIX requires the `dlsym` conversion to work on conforming implementations.
- Check for NULL before calling optional callbacks.

Verify: write a small test with duplicate keys and `INT_MIN` through `qsort`.

## Checked

2026-11-02. Confirmed: qsort comparator contract and the INT_MIN subtraction-overflow hazard (cppreference qsort); function-pointer/`void *` conversion statement (POSIX dlsym page). Removed: the claim that `-Wpedantic` flags it, and the 'undefined' wording on incompatible calls. Not checked: typedef/dispatch-table syntax (language usage).

Method: documentation only; no commands were run.
