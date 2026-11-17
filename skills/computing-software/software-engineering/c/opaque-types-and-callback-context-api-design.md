---
id: computing-software.software-engineering.c.opaque-types-and-callback-context-api-design
name: opaque-types-and-callback-context-api-design
category: computing-software
field: software-engineering
product: c
tags: [c, opaque-pointer, callback-context, abi-stability, api-versioning, library-design]
level: advanced
status: docs-checked
description: "Design C library APIs with opaque handles, void* callback contexts and stable ABIs."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://gcc.gnu.org/onlinedocs/", "https://man7.org/linux/man-pages/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Opaque types and callback context api design

Goal: a C library interface that can evolve without recompiling users.

- Opaque handle: header declares `typedef struct foo foo_t;` and functions `foo_t *foo_new(const foo_opts *o); void foo_free(foo_t *); int foo_do(foo_t *, ...);` while the struct body stays in the `.c` file, so fields can change without breaking ABI.
- Callbacks always take a user context: `typedef void (*foo_cb)(const foo_event *ev, void *user);` registered with `(cb, user)`; without it callers need globals. Document threading and lifetime (which thread calls, may it call back into the API).
- Options structs: add a `size_t struct_size` first field or reserved fields so new members can be appended compatibly.
- Export only intended symbols: `-fvisibility=hidden` plus `__attribute__((visibility("default")))`; prefix all public names (`foo_`).
- Use fixed-width types and explicit enums in public headers; do not expose `struct` layouts or `bool` on ABI boundaries if C++ or other languages call in.
- Check ABI compatibility between two builds with `abidiff` (libabigail), which compares the ABIs of two ELF shared libraries.
- Document error semantics and ownership per function.

Verify: build a tiny consumer against the headers only, then swap in a newer library build and run without recompiling.

## Checked

2026-11-02. Confirmed: `-fvisibility=hidden` plus `__attribute__((visibility("default")))` on public declarations (GCC wiki Visibility); `abidiff` compares two ELF shared libraries' ABIs (libabigail manual). Removed: version script/.def file and soname claims (not confirmed). Not checked: API design advice (judgement).

Method: documentation only; no commands were run.
