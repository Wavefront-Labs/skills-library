---
id: computing-software.software-engineering.d.d-safe-trusted-system
name: d-safe-trusted-system
category: computing-software
field: software-engineering
product: d
tags: [d-safe-trusted-system, function-attributes, memory-safety, safe-d, trusted-wrapper, safe, trusted, system, d]
level: practitioner
status: docs-checked
description: "Apply D memory-safety attributes: @safe checks, @trusted wrappers with reviewed contracts, @system default, -preview=dip1000 and safe-by-default modules."
sources:
  - https://dlang.org/spec/function.html
  - https://dlang.org/spec/memory-safe-d.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @safe, @trusted and @system memory safety

Goal: put the unsafe parts in small, reviewed @trusted islands.

- `@safe`: no pointer arithmetic, no casting a non-pointer to a pointer, no access to union fields that overlap pointers, no `__gshared` or `@system` variables, no `.ptr` access on arrays, no calling `@system` functions, inline assembler must be `@trusted`, no unsafe casts (mutable/immutable, thread-local/shared); out-of-bounds indexing is a runtime error.
- `@trusted`: you promise the body is memory-safe for all inputs; callable from `@safe`. Keep tiny and keep the interface safe.
- `@system` is what a function is when not marked `@safe` or `@trusted` (and not inferred); safety is then verified manually. Minimise the number and size of system functions.
- `-preview=dip1000` exists as a compiler preview (`-preview=help` lists them).
- `@safe` can be inferred (function attribute inference).
- Call-checks: `@safe` code cannot call `@system` code.

Gotchas:
- A `@trusted` function is not checked by the compiler: it must have a safe interface for all inputs.

Verify: `dmd -c -preview=dip1000 m.d` with `@safe:` at the top; grep for `@trusted` and review each.

## Checked

Date 2026-11-02. Confirmed @safe restrictions, @trusted and @system meaning (Functions and Memory-Safe-D specs). Corrected the @safe restriction list and the @system default claim; removed the @trusted lambda remark.

Method: documentation only; no commands were run.
