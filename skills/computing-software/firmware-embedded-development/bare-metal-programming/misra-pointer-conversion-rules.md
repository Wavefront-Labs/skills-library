---
id: computing-software.firmware-embedded-development.bare-metal-programming.misra-pointer-conversion-rules
name: misra-pointer-conversion-rules
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [misra-pointer-conversion, misra-c, rule-11, integer-to-pointer, register-cast-deviation, firmware-embedded-development]
level: advanced
status: draft
description: "Apply MISRA C:2012 Rule 11 (pointer type conversions) in firmware: what each rule forbids, compliant patterns, and the standard deviation for register base address casts."
sources:
  - https://misra.org.uk/product/misra-c2012-third-edition-first-revision/
  - https://www.misra.org.uk/app/uploads/2021/06/MISRA-Compliance-2020.pdf
  - https://wiki.sei.cmu.edu/confluence/display/c/EXP36-C.+Do+not+cast+pointers+into+more+strictly+aligned+pointer+types
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pointer conversion rules (Rule 11)

MISRA C:2012 Rule 11 is the group that firmware trips most, because register access, DMA and
protocol parsing all involve casts.

## The rules (paraphrased)
| Rule | Category | Forbids |
|---|---|---|
| 11.1 | Required | converting between function pointers and any other type |
| 11.2 | Required | conversions involving pointers to incomplete types |
| 11.3 | Required | casting between pointers to different object types (`uint8_t *` -> `struct hdr *`) |
| 11.4 | Advisory | converting between a pointer and an integer |
| 11.5 | Advisory | converting `void *` to a pointer to object |
| 11.6 | Required | casting between `void *` and arithmetic type |
| 11.7 | Required | casting between pointer to object and non-integer arithmetic |
| 11.8 | Required | casting away `const` or `volatile` |
| 11.9 | Required | `NULL` is the only permitted null pointer constant (no literal `0` for pointers) |

## Firmware patterns
**Peripheral base addresses** (`#define GPIOA ((GPIO_TypeDef *)0x48000000UL)`) violate 11.4.
It is advisory, so most projects record a project-wide **deviation permit** for
"conversion of an integer constant address to a pointer to a peripheral register structure,
in device header files only". Keep such casts in one place (vendor headers or a BSP file).

**Parsing byte buffers** with struct overlays violates 11.3 and risks misalignment:
```c
const struct hdr *h = (const struct hdr *)rx;      /* 11.3 + possible unaligned access */
/* compliant alternative */
struct hdr h;
(void)memcpy(&h, rx, sizeof h);                    /* copy, then use; compiler optimises small copies */
uint16_t len = (uint16_t)((uint16_t)rx[2] << 8) | rx[3];   /* or explicit byte assembly */
```
Casting to `uint8_t *`/`char *` (to inspect bytes) is permitted by an exception in 11.3.

**Callbacks with context** (`void *arg` cast back to `struct dev *`) trigger 11.5 (advisory):
generally accepted with a documented deviation, or avoided with typed callbacks.

**Casting away volatile** to pass a buffer to `memcpy` violates 11.8. Use a loop with volatile
accesses, or remove `volatile` from a buffer that only needs barriers.

**Function pointer from address** (jumping to an application's reset handler in a bootloader):
violates 11.1 and 11.4. Isolate it in one function with a deviation record; it is unavoidable.

## Verify
- [ ] Static analyser (cppcheck `--addon=misra`, PC-lint, Polyspace) reports no 11.x findings outside the deviation-permitted files.
- [ ] Each remaining cast has a deviation record ID in a comment.
