---
id: computing-software.software-engineering.c.valgrind-memcheck-leaks
name: valgrind-memcheck-leaks
category: computing-software
field: software-engineering
product: c
tags: [c, valgrind-memcheck, memory-leaks, invalid-read, uninitialised-value, leak-check]
level: practitioner
status: docs-checked
description: "Run Valgrind Memcheck and interpret invalid access, uninitialised-value and leak reports."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://sourceware.org/gdb/documentation/", "https://valgrind.org/docs/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Valgrind memcheck leaks

Goal: find heap errors in code that cannot be rebuilt with sanitizers.

- Run: `valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes ./prog args` (build with `-g -O0` or `-Og` for readable traces). The quick start says to expect programs to run much slower (for example 20 to 30 times).
- "Invalid read/write of size N" shows the access plus "Address ... is N bytes after a block of size M alloc'd at" with a second stack for the allocation; "freed at" gives the free stack for use-after-free.
- "Conditional jump or move depends on uninitialised value(s)": `--track-origins=yes` adds where the value was created.
- Leak categories: definitely lost (real leak), indirectly lost, possibly lost (interior pointer only), still reachable (held at exit; often fine).
- `--error-exitcode=1` fails CI on errors; `--suppressions=file` with `--gen-suppressions=all` for third-party noise.

Verify: write a program with a deliberate leak and one off-by-one heap write, and confirm both are reported.

## Checked

2026-11-02. Confirmed in the Valgrind quick start, Memcheck manual and core manual: leak kinds (still reachable, possibly lost, definitely, indirectly), `--track-origins=yes`, `--show-leak-kinds`, `--error-exitcode`, suppressions, Helgrind. Changed the slowdown figure to the manual's wording. Removed: the stack/global limitation and the ASan combination remark (not stated).

Method: documentation only; no commands were run.
