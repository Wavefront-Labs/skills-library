---
id: computing-software.firmware-embedded-development.bare-metal-programming.bit-manipulation-idioms
name: bit-manipulation-idioms
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [bit-manipulation, bitmask, bit-fields, read-modify-write, set-clear-registers, bit-banding, clz, popcount, embedded-c, embedded-c-coding-standard, firmware-embedded-development]
level: intro
status: docs-checked
description: "Firmware bit manipulation: set/clear/toggle/test masks, multi-bit field insert/extract, branch-free conditional set and mask merge from Bit Twiddling Hacks, and CMSIS intrinsics."
sources:
  - https://graphics.stanford.edu/~seander/bithacks.html
  - https://arm-software.github.io/CMSIS_5/Core/html/group__intrinsic__CPU__gr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bit manipulation idioms

**Goal:** readable bit operations on registers and packed data using unsigned types.

## Single bits
```c
#define BIT(n)        (1UL << (n))
reg |=  BIT(5);              /* set */
reg &= ~BIT(5);              /* clear */
reg ^=  BIT(5);              /* toggle */
if ((reg & BIT(5)) != 0U)    /* test: compare explicitly */
```
Use unsigned constants (`1UL`, `1U`). The bit hacks page notes that signed right shift is
implementation-defined in the 1989 ANSI C specification, so keep bit work on unsigned types.

## Multi-bit fields
```c
#define FIELD_MSK(pos, w)   (((1UL << (w)) - 1UL) << (pos))
#define FIELD_PREP(pos, w, v) (((uint32_t)(v) << (pos)) & FIELD_MSK(pos, w))
#define FIELD_GET(pos, w, r)  (((r) & FIELD_MSK(pos, w)) >> (pos))

/* set a 3-bit prescaler at bits [10:8] without touching the rest */
uint32_t v = TIM->CR;
v = (v & ~FIELD_MSK(8, 3)) | FIELD_PREP(8, 3, psc);
TIM->CR = v;
```
Prefer the vendor header's `_Pos` / `_Msk` macros where they exist rather than magic numbers.

## Branch-free forms (Bit Twiddling Hacks)
- Conditionally set or clear bits without branching: `w ^= (-f ^ w) & m;` (set the bits in mask
  `m` if flag `f` is true, clear them otherwise), or the superscalar form
  `w = (w & ~m) | (-f & m);`. The page says that on some architectures the lack of branching can
  more than make up for what appears to be twice as many operations.
- Merge bits from two values according to a mask: `r = a ^ ((a ^ b) & mask);`. The page notes
  there may be no benefit if the mask is a constant.
- Counting bits set: the page covers the naive loop, Kernighan's method, lookup tables and
  multiply/parallel variants. The snippets are public domain unless noted; the collection and
  descriptions are copyrighted by the author.

## Intrinsics (CMSIS-Core)
| Intrinsic | Purpose |
|---|---|
| `__CLZ(uint32_t)` | count leading zeros; implemented in software on Armv6-M (Cortex-M0, M0+, SC000) |
| `__RBIT(uint32_t)` | reverse bit order |
| `__REV(uint32_t)` | reverse bytes of a 32-bit value (0x12345678 becomes 0x78563412) |
| `__REV16(uint32_t)` | reverse bytes within each halfword (0x12345678 becomes 0x34127856) |
| `__ROR(uint32_t, uint32_t)` | rotate right; shift in the range 1..31 |

The exclusive-access intrinsics (`__LDREXW`, `__STREXW`) are not available on Cortex-M0, M0+ and
SC000.

## Verify
- [ ] Unit test the macros on the host with boundary positions and widths.
- [ ] Compare a branch-free expression against the obvious `if` version over all inputs of a small width.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against Bit Twiddling Hacks (conditional set/clear, mask merge, bit counting, licence note, signed right shift) and the CMSIS-Core CPU intrinsics page (signatures, `__CLZ` software on Armv6-M, `__REV`/`__REV16` examples, exclusive access availability). Removed because no cited page states them: `1 << 31` being undefined behaviour, read-modify-write ISR race advice, STM32 BSRR, nRF OUTSET/OUTCLR and RP2040 alias registers, bit-banding core support, write-1-to-clear guidance, C bit-field implementation notes (C11 6.7.2.1, `-fstrict-volatile-bitfields`), CMSIS `_VAL2FLD`, and the `__builtin_*` functions. The Barr Group page is a book landing page with no checkable rules, so it was dropped from sources.
