---
id: computing-software.firmware-embedded-development.bare-metal-programming.system-reset-via-aircr
name: system-reset-via-aircr
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [sysresetreq, nvic-systemreset, aircr, software-reset, reset-cause, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Trigger a clean software reset on Cortex-M with AIRCR.SYSRESETREQ (NVIC_SystemReset), what CMSIS says it resets, and how to tag the reason for the next boot."
sources:
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__NVIC__gr.html
  - https://github.com/ARM-software/CMSIS_6/blob/main/CMSIS/Core/Include/core_cm4.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System reset via AIRCR SYSRESETREQ

## The call
```c
__NO_RETURN void NVIC_SystemReset(void);   /* CMSIS */
/* what the CMSIS Cortex-M4 header does: */
__DSB();                                                    /* finish outstanding writes */
SCB->AIRCR = (0x5FAUL << SCB_AIRCR_VECTKEY_Pos)            /* VECTKEY value for a write */
           | (SCB->AIRCR & SCB_AIRCR_PRIGROUP_Msk)          /* keep priority grouping */
           | SCB_AIRCR_SYSRESETREQ_Msk;
__DSB();
for (;;) { __NOP(); }                                       /* wait until reset */
```
The CMSIS documentation says `NVIC_SystemReset` requests a system reset by setting the SYSRESETREQ
flag in the AIRCR register. Copy the 0x5FA key and the `PRIGROUP` preservation if you open-code it,
as the header does.

## What gets reset
CMSIS notes that in most microcontroller designs setting SYSRESETREQ resets the processor and most
parts of the system, but should not affect the debug system. The exact scope is chosen by the
SoC vendor: read the vendor reference manual for which peripherals, backup domain and RAM survive,
and for the reset-cause register that reports a software reset.

## Passing a reason across the reset
```c
__attribute__((section(".noinit"))) volatile uint32_t g_reset_reason;
void reboot(uint32_t why) { g_reset_reason = why; NVIC_SystemReset(); }
```
On boot read the vendor reset-cause register first, then `g_reset_reason`. Protect the value with a
magic number or checksum so stale RAM is not mistaken for a reason, and clear it after reading.
Whether RAM contents survive a given reset is vendor-specific.

## Gotchas
- Before reset, flush log buffers, finish any flash erase or program in progress, and put external
  devices (radios, motor drivers) in a safe state: the MCU resets but they may not.
- `NVIC_SystemReset` never returns, so code after it is unreachable.

## Verify
- [ ] The vendor reset-cause register reports a software reset after the call.
- [ ] The no-init reason survives (if your part keeps RAM) and is cleared after reading.

## Checked
Method: docs-checked 2026-11-09 against the CMSIS_6 NVIC functions page (`NVIC_SystemReset` description and its remark about SYSRESETREQ) read in full, and `core_cm4.h` (the `__NVIC_SystemReset` body, `SCB_AIRCR_*` macro names) read by search.
Removed as unconfirmed: VECTRESET behaviour, the TrustZone SYSRESETREQS statement, per-vendor reset-cause register names (`RCC_CSR`, `RESETREAS`), which resources survive reset, and the debugger vector-catch note. The Arm architecture manual and user guide sources were unreadable and were dropped.
