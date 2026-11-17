---
id: computing-software.firmware-embedded-development.bare-metal-programming.struct-packing-and-alignment
name: struct-packing-and-alignment
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [struct-packing, embedded-c-coding-standard, padding, packed-attribute, wire-format, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Control struct layout in firmware: AAPCS padding rules, ordering members to save RAM, when __attribute__((packed)) is safe, and serialising wire formats without packed structs."
sources:
  - https://github.com/ARM-software/abi-aa/blob/main/aapcs32/aapcs32.rst
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Common-Type-Attributes.html
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Common-Variable-Attributes.html
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Warning-Options.html
  - https://gcc.gnu.org/onlinedocs/gcc/ARM-Options.html
  - https://wiki.sei.cmu.edu/confluence/display/c/EXP42-C.+Do+not+compare+padding+data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Struct packing and alignment

## AAPCS rules (32-bit Arm)
Each fundamental type is aligned to its own size: byte 1, half-word 2, word 4, double-word 8
(`uint64_t`/`double`), single-precision float 4, data pointer 4 (AAPCS32 table of fundamental
types). The alignment of an aggregate is the alignment of its most-aligned component, and its
size is the smallest multiple of that alignment that holds all members laid out by those rules.
```c
struct bad  { uint8_t a; uint32_t b; uint8_t c; uint64_t d; };  /* 1+3pad+4+1+7pad+8 = 24 bytes */
struct good { uint64_t d; uint32_t b; uint8_t a; uint8_t c; };  /* 8+4+1+1+2pad   = 16 bytes */
```
The byte counts are worked out from those rules. Sort members largest-first to minimise padding.
GCC's `-Wpadded` warns whenever padding is added to align a member or the whole structure, and
notes that rearranging fields can often shrink the struct.

## Packed structs: when and how
In GCC, `packed` on a member gives it the smallest possible alignment (one byte, unless a larger
`aligned` value is given); on a struct, union or class definition it applies to every member.
- GCC's `-munaligned-access` documentation: unaligned access is off by default for ARMv6-M and
  ARMv8-M Baseline (and pre-ARMv6), on for other architectures. When it is off, words in packed
  structures are accessed a byte at a time. Correct, but slower.
- **Taking the address of a packed member** usually yields an unaligned pointer value. GCC warns
  about it by default (`-Waddress-of-packed-member`; `-Wno-address-of-packed-member` turns it off).
- Never overlay packed structs on peripheral registers (wrong access widths).
- Packing applies to the struct being declared, not to nested structs: GCC's example shows the
  inner struct must be packed too.
- `-Wpacked` warns when `packed` has no effect on layout or size.

## Wire formats without packed structs
Explicit serialisation does not depend on how the compiler lays out the struct or on the host
byte order:
```c
static inline void put_u16le(uint8_t *p, uint16_t v) { p[0] = (uint8_t)v; p[1] = (uint8_t)(v >> 8); }
static inline uint32_t get_u32le(const uint8_t *p) {
    return (uint32_t)p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}
size_t encode_hdr(uint8_t *out, const hdr_t *h) {
    out[0] = h->type; put_u16le(&out[1], h->len); put_u32le(&out[3], h->seq); return 7;
}
```

## Padding data
SEI CERT EXP42-C: unnamed padding may sit inside a structure or at its end, and unnamed members
have indeterminate representation even after initialisation (padding is zeroed only for objects
with static or thread storage duration that are default-initialised). So a byte-by-byte
`memcmp` of two structs can give wrong answers. CERT's compliant solution compares field by
field; serialise field by field for the same reason. Its exception: a struct with no padding
(aligned members or packed) and members without padding bits of their own may be compared with
`memcmp`, though this often fails for `_Bool` and floating-point types.

## Verify
- [ ] `_Static_assert(sizeof(struct good) == 16, "layout")` for every struct stored in flash or sent on a bus.
- [ ] `-Wpadded` and the default `-Waddress-of-packed-member` warning reviewed.
- [ ] Wire encoder round-trip unit test on host and target gives identical bytes.

## Checked
Checked 2026-11-08 against the AAPCS32 document (fundamental-type sizes and alignments, aggregate
alignment and size rules), GCC 14.2 Common Type Attributes, Common Variable Attributes and
Warning Options pages (`packed`, `-Wpadded`, `-Wpacked`, `-Wno-address-of-packed-member`), the GCC
ARM Options page (`-munaligned-access`), and SEI CERT EXP42-C. Removed because no readable page
states them: the `pahole` tip, the claim that misaligned pointers fault with LDRD/LDM or on M0,
the claim that GCC turns the shifted-byte read into a single LDR, and the `memset` advice (the CERT page
recommends field-by-field comparison instead). The 24 and 16 byte sizes are computed from the
AAPCS rules, not quoted. The `_Static_assert` line and the encoder code are examples, not
claims.
Method: documentation only; no commands were run.
