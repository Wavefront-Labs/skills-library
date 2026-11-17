---
id: computing-software.software-engineering.c.struct-padding-and-layout
name: struct-padding-and-layout
category: computing-software
field: software-engineering
product: c
tags: [c, c-structs-unions, struct-padding, alignment, offsetof, sizeof-struct, packed-struct]
level: advanced
status: docs-checked
description: "Predict struct padding, order members to shrink it, and avoid packed-struct traps."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://gcc.gnu.org/onlinedocs/gcc/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Struct padding and layout

Goal: know exactly what sizeof and offsetof will say, and why.

- The compiler may insert unnamed padding between members and after the last member, never before the first; the exact layout comes from the platform ABI, so print `sizeof` and `offsetof` rather than assuming.
- Reordering members from largest to smallest alignment usually removes padding. Inspect with `offsetof(type, member)` from `<stddef.h>`.
- Never write whole structs to files or sockets: padding may be present and layout differs by ABI. Serialise field by field.
- `__attribute__((packed))` or GCC's `#pragma pack(n)` (which sets the maximum member alignment) removes padding; GCC warns that the two interfere when used together. Avoid taking the address of packed members; copy with `memcpy`.
- Use `_Static_assert(sizeof(struct hdr) == 16, "hdr size")` to freeze layouts you rely on.
- `memcmp` on structs is unreliable because of padding.

Verify: compile a tiny program printing `sizeof` and `offsetof` per member on each target ABI.

## Checked

2026-11-02. Confirmed: unnamed padding between members and after the last, never before the first (cppreference struct); `offsetof` in `<stddef.h>` (cppreference offsetof); `_Static_assert` (cppreference); `#pragma pack` semantics and the packed/pragma interference warning (GCC Structure-Layout Pragmas). Removed: natural-alignment rule wording, pahole, and the fault claim about packed members (not confirmed).

Method: documentation only; no commands were run.
