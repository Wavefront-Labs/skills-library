---
id: computing-software.software-engineering.v-lang.v-unsafe-blocks
name: v-unsafe-blocks
category: computing-software
field: software-engineering
product: v-lang
tags: [v-unsafe-blocks, pointers-and-unsafe, unsafe, unsafe block, pointer arithmetic, nil, raw pointer, memory safety, v-lang]
level: advanced
status: docs-checked
description: "Wrap pointer arithmetic, pointer indexing, nil, union fields and goto in unsafe {}; mark risky functions with @[unsafe] and keep blocks small."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# unsafe blocks and @[unsafe]

Goal: confine risk to small audited regions.

- V requires potentially memory-unsafe operations to be marked. The docs list: pointer arithmetic, pointer indexing, conversion to a pointer from an incompatible type, and calling certain C functions such as `free`, `strlen` and `strncmp`.
- Example: `mut p := unsafe { malloc(2) }`; `p[0] = `h`` is an error outside `unsafe`, as is `p++`. Also `unsafe { p - &values[0] }` and `unsafe { &values[0] + 2 }` on fixed arrays (they do not decay to pointers).
- Other operations needing `unsafe`: reading union members, `goto`, calling `@[unsafe]` functions, and writing a null reference as `unsafe { nil }`.
- Mark risky functions `@[unsafe]`; their callers must use `unsafe`. The function body is still checked unless you also wrap code in `unsafe {}`.
- Keep memory-safe expressions out of the block so the reason for `unsafe` stays clear.
- Slices can share memory with their parent only inside `unsafe { a[2..4] }`.

Gotchas:
- The docs mark this section as work in progress.
- `@[direct_array_access]` removes bounds checks of array operations in a function; use it only where bounds are verified.

Verify: remove `unsafe` and confirm the compiler error naming the unsafe operation.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Memory-unsafe code", "Goto", "Union", attributes section showing `@[unsafe]`, "Structs with reference fields", "Array Slices", `@[direct_array_access]`). Removed as not stated: `charptr` and `byteptr` casts, raw-pointer dereference needing `unsafe` as a blanket rule, and the claim that only listed operations are unchecked.

Method: documentation only; no commands were run.
