---
id: computing-software.firmware-embedded-development.bare-metal-programming.static-assertions-in-firmware
name: static-assertions-in-firmware
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [static-assert, embedded-c-coding-standard, compile-time-checks, struct-layout, config-validation, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use _Static_assert to catch layout, size, configuration and register-map errors at compile time in firmware, with useful patterns and C99 fallbacks."
sources:
  - https://en.cppreference.com/w/c/language/_Static_assert
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static assertions

A failed `_Static_assert` stops the build with your message. Every assumption that a constant
expression can express belongs in one: zero runtime cost.

## Syntax
```c
_Static_assert(sizeof(fw_header_t) == 64, "fw_header_t must stay 64 bytes (bootloader ABI)");
static_assert(...);        /* convenience macro from <assert.h> until C23; keyword since C23 */
```
`_Static_assert` exists since C11. The expression must be an integer constant expression and the
message a string literal; if it compares equal to zero the compiler must display the message in
the error (C23 also allows omitting the message).

## High-value patterns in firmware
```c
/* 1. Layouts shared with a bootloader, another core, flash records, or a wire protocol */
_Static_assert(offsetof(shared_t, magic) == 0, "magic first");
_Static_assert(sizeof(settings_rec_t) % 8 == 0, "flash double-word programming granularity");

/* 2. Register map overlays match the reference manual */
_Static_assert(offsetof(MYUART_TypeDef, BAUD) == 0x20, "BAUD at 0x20");

/* 3. Configuration sanity */
_Static_assert((RX_BUF_SIZE & (RX_BUF_SIZE - 1)) == 0, "ring buffer size must be a power of two");
_Static_assert(SYSCLK_HZ / BAUD >= 16, "baud too high for oversampling by 16");
_Static_assert(TASK_COUNT <= 32, "event bitmask is 32 bits");

/* 4. Table completeness against an enum */
static const char *const k_state_names[] = { "idle", "run", "fault" };
_Static_assert(sizeof k_state_names / sizeof k_state_names[0] == STATE_COUNT, "names out of sync");

/* 5. Type assumptions */
_Static_assert(sizeof(void *) == 4, "32-bit target assumed by the IPC format");
```

## Limits
- Only integer constant expressions: a plain `const int` variable is not one in C (cppreference's
  example shows the error). Use `enum` or `#define` for values you want to check.
- Linker-determined values (section sizes, symbol addresses) cannot be checked by the compiler;
  check them in the linker script or a post-build step.

## Pre-C11 fallback
```c
#define STATIC_ASSERT(c, m) typedef char static_assert_##m[(c) ? 1 : -1]
```
Negative array size fails compilation; message is the typedef name.

## Verify
- [ ] Change a struct member size deliberately: the build fails with your message.
- [ ] Every struct written to flash or sent between images has a size assert.

## Checked
2026-10-31. Confirmed on cppreference (Static assertion): `_Static_assert`/`static_assert` syntax, integer constant expression requirement, message display, `<assert.h>` macro until C23, `const` variable rejected.
Removed: placement in struct definitions, linker-script `ASSERT()`, `ATOMIC_INT_LOCK_FREE`, the Barr Group and GCC source links.
Method: documentation only; no commands were run.
