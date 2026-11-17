---
id: computing-software.firmware-embedded-development.bare-metal-programming.trustzone-nonsecure-callbacks
name: trustzone-nonsecure-callbacks
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [ns-callback, trustzone-m, cmse-nonsecure-call, cmse-nsfptr-create, pointer-validation, firmware-embedded-development]
level: sme
status: docs-checked
description: "Call non-secure functions from secure code on ARMv8-M: cmse_nonsecure_call typedefs, cmse_nsfptr_create, register clearing, and validating NS pointers."
sources:
  - https://github.com/ARM-software/acle/blob/main/cmse/cmse.md
  - https://gcc.gnu.org/onlinedocs/gcc/ARM-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Non-secure callbacks (cmse_nsfptr_create)

Secure services sometimes need to notify the non-secure world (a secure timer expiring, a crypto
operation completing). Secure code must not call an NS function with a normal call: the CMSE
specification requires a call that clears the LSB of the address, clears secret registers and
branches with `BLXNS`.

## Declaring the callback type
```c
#include <arm_cmse.h>
typedef void (*ns_cb_t)(uint32_t status) __attribute__((cmse_nonsecure_call));

static ns_cb_t s_cb;

/* NS-callable entry to register the callback */
__attribute__((cmse_nonsecure_entry))
int32_t secure_register_cb(void (*cb)(uint32_t)) {
    ns_cb_t p = cmse_nsfptr_create((ns_cb_t)cb);     /* LSB cleared: marks an NS target */
    if (!cmse_is_nsfptr(p)) return -1;
    s_cb = p;
    return 0;
}

void secure_event_isr(void) {
    if (s_cb) s_cb(STATUS_DONE);                     /* compiler emits register clearing + BLXNS */
}
```
- `cmse_nsfptr_create(p)` returns `p` with its LSB cleared; `cmse_is_nsfptr(p)` is non-zero when
  the LSB is unset (both from the CMSE spec).
- A call through a `cmse_nonsecure_call` type: the toolchain clears the LSB of the address,
  clears registers that may hold secret information, and branches with `BLXNS`. Requires `-mcmse`.

## Validating NS pointers passed into secure APIs
Any pointer argument from NS code is untrusted (confused deputy attack: NS passes a pointer to
secure memory and lets the secure service overwrite it).
```c
__attribute__((cmse_nonsecure_entry))
int32_t secure_read_key_id(uint8_t *out, size_t len) {
    if (cmse_check_address_range(out, len, CMSE_NONSECURE | CMSE_MPU_READWRITE) == NULL) return -1;
    /* copy only after the check; beware TOCTOU on data NS can modify concurrently */
    ...
}
```
`CMSE_MPU_UNPRIV` sets the `T` flag of the `TT` instruction, so the check uses the unprivileged
access permissions. `cmse_nonsecure_caller()` returns non-zero if the entry function was called
from non-secure state.

## Gotchas
- If the NS callback never returns, the secure code that called it never continues. Keep
  callbacks short and treat the NS side as untrusted.
- Arguments or results that do not fit in registers use the non-secure stack (CMSE spec); prefer
  register-only callbacks.
- Float context: the spec describes clearing floating-point registers conditionally on the `TS`
  bit of `FPCCR`; read that section before relying on it.

## Verify
- [ ] Disassembly of the call site shows register clearing followed by `blxns`.
- [ ] Passing a secure address to the registration API is rejected.

## Checked
2026-10-31. Confirmed in the Arm CMSE specification (ARM-software/acle `cmse/cmse.md`):
`cmse_nonsecure_call`, `cmse_nsfptr_create`, `cmse_is_nsfptr`, `cmse_nonsecure_caller`,
`cmse_check_address_range` and the `CMSE_*` flags, `BLXNS` and register clearing, use of the
non-secure stack, `FPCCR.TS`. Confirmed in the GCC ARM Options page: `-mcmse`.
Removed: SecureFault INVTRAN wording, "secure interrupts still enabled" and the pending-NS-interrupt advice,
the NS-memory range check on the function pointer, `CLRONRET`, the stack integrity signature claim.
Method: documentation only; no commands were run.
