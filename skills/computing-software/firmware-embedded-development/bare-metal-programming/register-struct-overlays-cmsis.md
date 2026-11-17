---
id: computing-software.firmware-embedded-development.bare-metal-programming.register-struct-overlays-cmsis
name: register-struct-overlays-cmsis
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [register-struct-overlay, mmio, cmsis-io-qualifiers, peripheral-struct, svd, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Model a peripheral as a CMSIS-style register struct with __IO/__IM/__OM qualifiers, reserved padding and offset static asserts, or generate it from an SVD file."
sources:
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__peripheral__gr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Register struct overlays and CMSIS IO qualifiers

## Pattern
```c
/* CMSIS-Core defines these struct member qualifiers; shown for illustration */
#define __IM  volatile const   /* 'read only' */
#define __OM  volatile         /* 'write only' */
#define __IOM volatile         /* 'read / write' */

typedef struct {
    __IOM uint32_t CTRL;       /* 0x00 */
    __IM  uint32_t STATUS;     /* 0x04 */
    __OM  uint32_t TXDATA;     /* 0x08 */
    __IM  uint32_t RXDATA;     /* 0x0C */
          uint32_t RESERVED0[4];/* 0x10-0x1C */
    __IOM uint32_t BAUD;       /* 0x20 */
} MYUART_TypeDef;

_Static_assert(offsetof(MYUART_TypeDef, BAUD) == 0x20, "MYUART layout");
#define MYUART0 ((MYUART_TypeDef *)0x40011000UL)

MYUART0->BAUD = div;
while (!(MYUART0->STATUS & MYUART_STATUS_TXE_Msk)) {}
```
Define fields as position/mask macro pairs rather than C bit-fields, e.g.
`#define MYUART_CTRL_EN_Pos 0U` / `#define MYUART_CTRL_EN_Msk (1UL << MYUART_CTRL_EN_Pos)`.

## Rules
- Every member is `volatile`: the compiler must not cache, merge or drop accesses.
- Match the member width to the access width the reference manual allows for that register
  (CMSIS-Core's own example mixes `uint8_t` and `uint32_t` members).
- Pad gaps explicitly with `RESERVED` members (as the CMSIS-Core example does); never rely on the compiler to pad.
- Static-assert key offsets: one off-by-four in a 60-register struct otherwise writes the wrong
  register silently.
- Multiple instances share the type, and drivers take a `MYUART_TypeDef *` parameter.
- `const` on read-only members makes accidental writes a compile error.

## Generating from SVD
Vendor SVD files describe the registers and fields of a device, and tools can generate the
header from them. When the vendor header and the reference manual disagree, check the errata and
the SVD version.

## Gotchas
- A `__OM` (write-only) member must not be updated with `|=`: that reads it first.
- Copying a whole register struct reads every register; check the manual for read side effects first.

## Verify
- [ ] `_Static_assert` offsets match the reference manual's register map table.
- [ ] Disassembly shows accesses of the expected width at the expected offsets.

## Checked
2026-10-31. Confirmed in the CMSIS-Core 6 peripheral access page: `__IM`, `__OM`, `__IOM` meanings, `RESERVED` padding members, mixed `uint8_t`/`uint32_t` members.
Removed: the `svdconv` command and flags, `svd2rust`, `cmsis-svd`, the claim that `uint8_t` members break some peripherals, the `_Pos`/`_Msk` "CMSIS convention" attribution, the read-back and clear-on-read claims, the DMA channel array example, the STR/LDR claim.
Method: documentation only; no commands were run.
