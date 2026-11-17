---
id: computing-software.firmware-embedded-development.bare-metal-programming.trustzone-nsc-veneers
name: trustzone-nsc-veneers
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [nsc-veneer, trustzone-m, sg-instruction, cmse-implib, sgstubs, secure-gateway, import-library, armv8-m, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Expose Secure services to Non-secure code through NSC veneers: cmse_nonsecure_entry, .gnu.sgstubs placement, the import library, stable veneer addresses, and API design."
sources:
  - https://github.com/ARM-software/acle/blob/main/cmse/cmse.md
  - https://sourceware.org/binutils/docs/ld/ARM.html
  - https://gcc.gnu.org/onlinedocs/gcc/ARM-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Non-secure callable veneers

**Goal:** a narrow, stable, verified set of entry points from the Non-secure application into
Secure firmware.

## Mechanism
Non-secure code may only enter Secure state by branching to an `SG` (secure gateway)
instruction located in **NSC** memory. The toolchain generates a small veneer per entry
function: `SG; B.W __acle_se_<fn>`. The linker (GNU ld) places all SG veneers in the special output
section `.gnu.sgstubs`; its start address must be set, with `--section-start` or in the linker
script, so that it lands in the SAU region marked NSC (see `trustzone-sau-configuration`). The
real function body stays in plain Secure memory.

## Secure side
```c
#include <arm_cmse.h>
int32_t __attribute__((cmse_nonsecure_entry)) sec_sign(const uint8_t *msg, uint32_t len, uint8_t *sig) {
    if (cmse_check_address_range((void *)msg, len, CMSE_NONSECURE | CMSE_MPU_READ) == NULL) return -1;
    if (cmse_check_address_range(sig, 64, CMSE_NONSECURE | CMSE_MPU_READWRITE) == NULL) return -1;
    return do_sign(msg, len, sig);
}
```
Compile with `-mcmse` (GCC option for the Armv8-M Security Extensions). Link flags to also
produce the import library: `-Wl,--cmse-implib -Wl,--out-implib=secure_nsclib.o`.

## Non-secure side
Link the NS image against `secure_nsclib.o`: a relocatable file containing only copies of the
(absolute) symbols of the veneers. Include the shared header; calls look like ordinary function
calls.

## Stable addresses
If the Secure image is updated independently, veneer addresses must not move.
`-Wl,--in-implib=<old import library>` (with `--cmse-implib`) tells ld that the symbols in it must
keep the same address; new symbols are added to the `--out-implib` library, and ld warns if
symbols of the input library disappear. Version the import library with the Secure image.

## API design rules
- Few, coarse-grained entry points; every one is attack surface. Validate every pointer and
  length with `cmse_check_address_range` and copy data in before use (time-of-check vs
  time-of-use: NS can modify its buffer concurrently from an interrupt).
- Prefer arguments and results that fit in registers: stack-based ones are copied from the
  non-secure stack by the entry function's prologue, so pass a pointer to a struct and validate it.
- Return status codes, never Secure pointers.
- Guard shared Secure state yourself if NS interrupts can re-enter an entry function.

## Verify
- [ ] The list of `__acle_se_` symbols in the Secure ELF (`nm`) is exactly the intended entries.
- [ ] Veneer addresses identical between two Secure builds using `--in-implib`.
- [ ] Passing a Secure address from NS returns an error instead of leaking data.

## Checked
2026-10-31. Confirmed in the Arm CMSE specification (ARM-software/acle `cmse/cmse.md`): `__acle_se_`
veneer symbols, `cmse_check_address_range` and its flags, import library contents, stack-based
arguments of entry functions. Confirmed in the GNU ld ARM page: `.gnu.sgstubs` placement,
`--cmse-implib`, `--out-implib`, `--in-implib` and its warnings. Confirmed in the GCC ARM Options page: `-mcmse`.
Removed: the claimed `ALIGN(32)` linker script, "ld checks for stray SG encodings", the claim that
more than four argument words are rejected by GCC, the no-variadic rule, and the `nm | grep` command.
Method: documentation only; no commands were run.
