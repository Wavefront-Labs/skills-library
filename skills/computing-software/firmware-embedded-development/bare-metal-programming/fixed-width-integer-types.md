---
id: computing-software.firmware-embedded-development.bare-metal-programming.fixed-width-integer-types
name: fixed-width-integer-types
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [stdint-fixed-width, stdint-h, uint32-t, inttypes-h, printf-format-macros, portability, barr-c, embedded-c, embedded-c-coding-standard, firmware-embedded-development]
level: intro
status: docs-checked
description: "Use <stdint.h> types correctly in firmware: exact-width vs least/fast, uintptr_t, PRIu32 printf macros, data-model differences, and portable register/protocol layouts."
sources:
  - https://en.cppreference.com/w/c/types/integer
  - https://wiki.sei.cmu.edu/confluence/display/c/INT00-C.+Understand+the+data+model+used+by+your+implementation%28s%29
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixed-width integer types

**Goal:** integer sizes that are the same on an 8-bit AVR, a 32-bit Cortex-M and the 64-bit
host running unit tests.

## Why
Data models differ (SEI CERT INT00-C table): `int` is 16 bits on iAPX86 and 32 bits on
IA-32 and ARM-32; `long` is 32 bits on ARM-32 and 64 on 64-bit Linux and BSDs. Code using
bare `int` for a 20-bit counter or a protocol field silently changes behaviour when ported
or host-tested. If you must assume sizes, add static assertions.

## Which type
| Type | Use |
|---|---|
| `uint8_t`..`uint64_t`, `int8_t`.. | registers, protocol fields, stored data, anything with a defined width |
| `uint_fast16_t` etc. | local counters where speed matters and at-least-N bits suffices (32-bit on ARM) |
| `uint_least8_t` | smallest type with at least that many bits |
| `uintptr_t` | integer holding an address (MMIO base arithmetic) |

## printf and literals
```c
#include <inttypes.h>
printf("t=%" PRIu32 " id=%" PRIx16 "\n", t, id);   /* never %d / %lu for uint32_t */
```
`PRIu32`, `PRIx16` and the other PRI macros (in `<inttypes.h>`) exist for each fixed-width,
least, fast, max and pointer type, so the format matches the type on every target. The
UINTN_C macros build constants of the matching least type (for example `UINT64_C(0x123)`
might expand to `0x123ULL` or `0x123UL`). The exact-width types are optional: an
implementation defines them only if it has a matching type, with no padding bits.

## Layout of wire/flash formats
Fixed-width types do not fix **endianness** or **padding**: serialise field by field
(`buf[0] = v & 0xFF; buf[1] = v >> 8;`) or use packed structs with explicit byte-order
helpers, and `_Static_assert(sizeof(hdr_t) == 12, "layout")`.

## Gotchas
- `uint8_t i; for (i = 0; i < 300; i++)` never terminates; `-Wtype-limits` catches it.
- `int` is still fine for return codes and small loop counters where width is irrelevant,
  if your standard allows it.

## Verify
- [ ] Build on target and host with format and conversion warnings enabled: none remain
      (compilers can warn when a format string does not match its arguments).
- [ ] Static asserts on every on-wire/on-flash struct size.

## Checked

2026-11-08. Confirmed on the cppreference fixed-width integer page: exact/fast/least/max/pointer type definitions, optional exact-width types without padding bits, PRI macros in inttypes.h, UINTN_C example. Confirmed on SEI CERT INT00-C: data-model table (int and long sizes), static assertions advice, uintptr_t and fast/least descriptions. Removed (not on pages read): AVR/MSP430 sizes, BARR-C and MISRA Dir 4.6 requirements (the Barr page fetched only a downloads page), char signedness on ARM GCC, newlib uint32_t mapping, Cortex-M0 64-bit helper cost, specific warning flags, and the size_t and bool table rows.

Method: documentation only; no commands were run.
