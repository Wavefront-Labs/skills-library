---
id: computing-software.software-engineering.c.designated-initializers-and-compound-literals
name: designated-initializers-and-compound-literals
category: computing-software
field: software-engineering
product: c
tags: [c, designated-initializers, compound-literal, zero-initialization, c99]
level: practitioner
status: docs-checked
description: "Initialise structs and arrays with C99 designated initialisers and compound literals."
sources: ["https://en.cppreference.com/w/c/language/struct_initialization", "https://en.cppreference.com/w/c/language/compound_literal", "https://en.cppreference.com/w/c/language/storage_duration", "https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Designated initializers and compound literals

Goal: readable, safe initialisation that zero-fills the rest.

- `struct cfg c = { .port = 8080, .name = "x" };` unnamed members are zero-initialised. `int a[8] = { [3] = 1, [7] = 2 };` sets elements by index.
- `T x = {0};` zero-fills the members; `T x = {};` is valid from C23 (a GNU extension earlier).
- Compound literal: `(struct point){ .x = 1, .y = 2 }` creates an lvalue; at block scope it has automatic storage for the enclosing block, so do not return its address. Use it to pass temporaries: `draw(&(struct rect){ .w = 10, .h = 5 });`
- Options-struct pattern: pass a config struct with designated initialisers instead of many positional parameters; new fields default to zero.
- `static` or global objects are zero-initialised without an initialiser.

Verify: compile with `-std=c11 -Wall -Wextra -Wmissing-field-initializers` and print values.

## Checked

- Date: 2026-11-02
- Confirmed on cppreference: `{}` valid from C23, `{0}` otherwise; compound literal has automatic storage at block scope and static at file scope; static-duration objects are initialised before `main`; GCC manual `-Wmissing-field-initializers`. Removed: the padding-zeroing remark and the claim that C++ requires initialiser order (not on the pages read).
Method: documentation only; no commands were run.
