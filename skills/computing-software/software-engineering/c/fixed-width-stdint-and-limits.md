---
id: computing-software.software-engineering.c.fixed-width-stdint-and-limits
name: fixed-width-stdint-and-limits
category: computing-software
field: software-engineering
product: c
tags: [c, stdint-limits, stdint-h, limits-h, intmax-t, inttypes-h]
level: practitioner
status: docs-checked
description: "Use stdint.h fixed-width types, limits macros and inttypes.h format macros correctly in portable C."
sources: ["https://en.cppreference.com/w/c/types/integer", "https://en.cppreference.com/w/c/types/limits", "https://en.cppreference.com/w/c/io/fprintf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixed width stdint and limits

Goal: pick the right integer type for sizes, wire formats and counters.

- `<stdint.h>`: `int32_t`, `uint8_t` etc. are optional exact-width types (absent if the platform lacks them); `int_least8_t` to `int_least64_t` and `int_fast8_t` to `int_fast64_t` are not marked optional. `intptr_t`/`uintptr_t` are optional but round-trip a `void *` when present.
- Use `size_t` for object sizes and indexes, `ptrdiff_t` for pointer differences, `off_t` (POSIX) for file offsets.
- Limits: `INT_MAX`, `UINT_MAX` and friends in `<limits.h>`.
- Printing: use `<inttypes.h>` macros, e.g. `printf("%" PRIu64 "\n", v);` for `uint64_t`; `%zu` for `size_t`, `%td` for `ptrdiff_t`, `%jd` for `intmax_t`.
- Do not assume `long` is 32 or 64 bits; its width depends on the platform ABI.
- Wire formats: use exact-width types plus explicit serialisation, never `struct` overlays.

Verify: add `_Static_assert(sizeof(uint32_t) == 4, "uint32_t size")`-style checks for assumptions and compile for two targets.

## Checked

- Date: 2026-11-02
- Confirmed on cppreference: exact-width, `int_fast`/`int_least` and `intptr_t` families and which are optional; `<inttypes.h>` `PRI*` macros; `%zu`, `%td`, `%jd` conversions; `<limits.h>` `INT_MAX`/`UINT_MAX`. Removed: the `INT32_MAX`/`SIZE_MAX` header attribution, the LP64/Windows `long` widths and the `-m32` suggestion (not stated on the pages read).
Method: documentation only; no commands were run.
