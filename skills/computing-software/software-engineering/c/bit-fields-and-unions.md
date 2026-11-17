---
id: computing-software.software-engineering.c.bit-fields-and-unions
name: bit-fields-and-unions
category: computing-software
field: software-engineering
product: c
tags: [c, bit-fields, union, tagged-union, bitmask-flags]
level: advanced
status: docs-checked
description: "Use unions as tagged variants and prefer explicit masks over bit-fields for portable bit layouts."
sources: ["https://en.cppreference.com/w/c/language/bit_field", "https://en.cppreference.com/w/c/language/union", "https://en.cppreference.com/w/c/11", "https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bit fields and unions

Goal: compact data without non-portable layout assumptions.

- Adjacent bit-fields may be packed to share and straddle bytes, and the signedness of a plain `int` bit-field is implementation-defined; do not use them for hardware registers or wire formats you share across compilers. Use shifts and masks with `uint32_t`.
- Flags: `#define F_READ (1u << 0)`; set `|=`, clear `&= ~F_READ`, test `&`. Use unsigned constants (`1u << 31` not `1 << 31`).
- Tagged union (variant): `struct val { enum { V_INT, V_STR } tag; union { long i; char *s; } u; };` always switch on `tag`; the union is as large as its biggest member.
- Reading an inactive member reinterprets the stored bytes as the new type (type punning, defined since C99 TC3); if the new type is larger, the excess bytes are unspecified and may be a trap representation.
- Anonymous unions/structs are standard from C11.
- Only the active member's lifetime matters for pointers: free `s` only when the tag says string.

Verify: unit-test each tag; compile with `-Wswitch-enum` so adding a tag flags unhandled switches.

## Checked

- Date: 2026-11-02
- Confirmed on cppreference: bit-field types and implementation-defined signedness of plain `int`, packing/straddling of adjacent bit-fields, union type punning wording (TC3, excess bytes unspecified, trap representation), anonymous struct and union members listed under C11. GCC manual: `-Wswitch-enum`. Removed: the unqualified claims about bit-field order and the wire-format advice was kept as advice only.
Method: documentation only; no commands were run.
