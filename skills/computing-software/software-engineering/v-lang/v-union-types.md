---
id: computing-software.software-engineering.v-lang.v-union-types
name: v-union-types
category: computing-software
field: software-engineering
product: v-lang
tags: [v-union-types, unions-and-type-aliases, union, c union, overlay, unsafe, bit casting, memory layout, v-lang]
level: advanced
status: docs-checked
description: "Declare C-style unions that overlay fields in the same memory, read them under unsafe and use them for binary conversion."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unions

Goal: reinterpret bytes without casts.

```v
union ThirtyTwo {
	a u32
	b [4]u8
}
```
- A union is a special type of struct that stores different data types in the same memory location. All members share it, so modifying one modifies the rest; the largest member defines the size of the union.
- Only one member holds a valid value at any time. Union member access must be performed in an `unsafe` block.
- Uses named in the docs: lower memory usage, and direct access to the bytes of an integer without shifts and masks (`b[byte_offset]` for `a`).
- Unions support embedding like structs: `union Rgba32 { Rgba32_Component  value u32 }`, initialized with `value: 0x008811FF` or `Rgba32_Component: Rgba32_Component{ a: 128 }`; `sizeof(Rgba32)` is 4 bytes in the docs example.
- Embedded struct arguments are not necessarily stored in the order listed.
- When a union holds interface storage, V clears the entire storage before initializing the selected member; an inactive interface member formats as `unknown interface value`.

Verify: reproduce the Rgba32 example and check `sizeof` is 4.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Unions"). Removed as not stated there: `math.f32_bits`/`f32_from_bits` alternatives, the f32/u32 `0x3f800000` check, endianness and padding remarks, C interop and protocol header uses, sum-type advice.

Method: documentation only; no commands were run.
