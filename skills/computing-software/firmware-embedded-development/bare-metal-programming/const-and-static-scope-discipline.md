---
id: computing-software.firmware-embedded-development.bare-metal-programming.const-and-static-scope-discipline
name: const-and-static-scope-discipline
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [const-correctness, static-scope, internal-linkage, encapsulation, flash-placement, rodata, volatile-const, barr-c, embedded-c, embedded-c-coding-standard, firmware-embedded-development]
level: practitioner
status: draft
description: "Use const and static deliberately in embedded C: tables in flash via .rodata, const pointer forms, file-scope static for encapsulation, volatile const registers, and avoiding globals."
sources:
  - https://barrgroup.com/embedded-systems/books/embedded-c-coding-standard
  - https://wiki.sei.cmu.edu/confluence/display/c/DCL00-C.+Const-qualify+immutable+objects
  - https://www.misra.org.uk/misra-c/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Const and static scope discipline

**Goal:** the compiler enforces what may change and who may see it; read-only data lives
in flash, not scarce RAM.

## const puts data in flash
```c
static const uint16_t sine_table[256] = { ... };   /* .rodata -> flash, 512 B of RAM saved */
static uint16_t sine_table[256] = { ... };         /* .data: copied to RAM at boot, costs flash AND RAM */
```
On Harvard AVR, `const` alone still copies to RAM; use `PROGMEM`/`__flash` and `pgm_read_*`.
Check placement in the map file.

## Pointer forms
| Declaration | Meaning |
|---|---|
| `const uint8_t *p` | data read-only through p |
| `uint8_t * const p` | pointer fixed, data writable |
| `const uint8_t * const p` | both fixed |
| `volatile const uint32_t *sr` | read-only register that changes under you (status/input) |
Make function parameters `const T *` whenever the callee does not modify the data
(MISRA Rule 8.13); it documents intent and lets callers pass flash tables.

## static for scope
- File-scope `static` functions and variables have internal linkage: the module's public
  API is exactly what is in its header (MISRA Rule 8.7/8.8; BARR-C 8.x).
- Function-local `static` gives persistent state with minimum scope - but it is shared
  across calls and contexts, so it is not reentrant; never in code called from ISR and
  main both without protection.
- No `extern` declarations in `.c` files; one header per module declares the public items.

## Avoiding globals
Replace writable globals with a module-private struct plus accessor functions, or pass a
context pointer (`uart_t *dev`) - enables multiple instances and host testing.
```c
/* uart.c */
static struct { ringbuf_t rx; uint32_t errors; } s_uart;
uint32_t uart_error_count(void) { return s_uart.errors; }
```

## Gotchas
- Casting away const to write to a flash-placed object faults (or silently does nothing).
- `const` objects in C are not compile-time constants: cannot size a file-scope array with
  them; use `enum` or `#define`, or C23 `constexpr`.
- Large `const` structs with function pointers (driver ops tables) belong in flash too -
  keeps them safe from stray writes.

## Verify
- [ ] Map file: lookup tables appear in `.rodata`, not `.data`.
- [ ] `nm -g` on each object lists only intended public symbols.
