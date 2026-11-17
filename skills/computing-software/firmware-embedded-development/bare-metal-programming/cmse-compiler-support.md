---
id: computing-software.firmware-embedded-development.bare-metal-programming.cmse-compiler-support
name: cmse-compiler-support
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [cmse, mcmse, arm-cmse-h, cmse-nonsecure-call, cmse-nonsecure-entry, bxns, blxns, trustzone-m, armv8-m, firmware-embedded-development]
level: advanced
status: draft
description: "Use ARMv8-M CMSE compiler support in GCC/Clang: -mcmse, arm_cmse.h intrinsics, nonsecure entry and call attributes, register clearing, function pointer tagging, TT checks."
sources:
  - https://developer.arm.com/documentation/100720/latest
  - https://gcc.gnu.org/onlinedocs/gcc/ARM-Function-Attributes.html
  - https://gcc.gnu.org/onlinedocs/gcc/ARM-Options.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CMSE compiler support

**Goal:** let the compiler generate correct Secure/Non-secure transitions and checks
instead of hand-written assembly.

## Flags and header
- Compile Secure code with `-mcpu=cortex-m33 -mcmse` (Clang: `--target=arm-none-eabi
  -mcmse`). Without `-mcmse`, the attributes are errors and `arm_cmse.h` is unusable.
- `#include <arm_cmse.h>`; feature macro `__ARM_FEATURE_CMSE` (3 when building Secure code
  with CMSE).
- Non-secure code does not need `-mcmse`.

## The two attributes
| Attribute | On | Compiler does |
|---|---|---|
| `cmse_nonsecure_entry` | Secure function callable from NS | emits `__acle_se_` symbol for a veneer, clears caller-saved and unused argument registers and flags on return, returns with `BXNS` |
| `cmse_nonsecure_call` | type of a pointer to an NS function | saves Secure callee-saved state, clears all other registers (incl. FP), calls with `BLXNS` |
```c
typedef void __attribute__((cmse_nonsecure_call)) ns_cb_t(uint32_t evt);
static ns_cb_t *g_cb;
void __attribute__((cmse_nonsecure_entry)) sec_register_cb(ns_cb_t *cb) {
    g_cb = cmse_nsfptr_create(cb);    /* clear LSB to mark as NS pointer */
}
void sec_notify(uint32_t e) { if (g_cb && cmse_is_nsfptr(g_cb)) g_cb(e); }
```
Calling an NS function through a normal pointer would leave Secure data in registers and
execute it as Secure - a direct vulnerability.

## Pointer checking intrinsics
- `cmse_check_address_range(p, size, flags)` uses the `TT` instruction family over the
  range; returns `p` or NULL. Flags: `CMSE_NONSECURE`, `CMSE_MPU_READ`,
  `CMSE_MPU_READWRITE`, `CMSE_MPU_UNPRIV`, `CMSE_AU_NONSECURE`.
- `cmse_check_pointed_object(p, flags)` for a typed object.
- `cmse_TT(p)`, `cmse_TTT`, `cmse_TTA` return raw attribution info (region numbers,
  readable/writable, secure).
- `cmse_nonsecure_caller()` tells whether the current entry came from NS.

## Gotchas
- Entry functions may not take arguments on the stack or be variadic; GCC errors.
- Return of large structs (via hidden pointer) from entry functions is not supported.
- Floating-point: with NS FPU use enabled, the compiler clears FP registers too; lazy FP
  state preservation settings (`FPCCR.TS`, `CLRONRET`) must match the security policy.
- Toolchain bugs exist in older GCC (pre-8) for register clearing; use a current
  Arm GNU Toolchain and review disassembly of entry functions once.
- Inline asm inside entry functions bypasses the compiler's clearing guarantees.

## Verify
- [ ] `objdump -d` of an entry function ends with register clears and `bxns lr`.
- [ ] NS callback invocation disassembles to `blxns`.
