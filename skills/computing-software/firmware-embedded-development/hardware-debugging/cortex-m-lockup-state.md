---
id: computing-software.firmware-embedded-development.hardware-debugging.cortex-m-lockup-state
name: cortex-m-lockup-state
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [lockup, cortex-m, double-fault, hardfault-in-hardfault, vector-catch, lockup-reset, hardware-debugging, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Diagnose Cortex-M lockup: a fault at HardFault priority or above, the 0xFFFFFFFE fetch loop, lockup-to-reset behaviour, and catching the first fault with OpenOCD vector catch."
sources:
  - https://interrupt.memfault.com/blog/cortex-m-hardfault-debug
  - https://openocd.org/doc/html/Architecture-and-Core-Commands.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cortex-M lockup state

Lockup is the core's response to an unrecoverable fault. It is not a HardFault; your handler does
not run to completion.

## What it is
- In the HardFault handler the core runs at a non-configurable priority of -1. At that level or
  above, another fault puts the processor in an unrecoverable state where a reset is expected.
  That state is lockup.
- The processor typically resets automatically on lockup, but the specification does not require
  it; on some parts you must enable a hardware watchdog for a reset to happen. Check the MCU's
  reference manual.
- With a debugger attached, lockup often behaves differently. Example from the Memfault post: on
  the nRF52840 "Reset from CPU lockup is disabled if the device is in debug interface mode".
- In lockup the core repeatedly fetches the same fixed instruction, `0xFFFFFFFE` (or the
  instruction that triggered the lockup), until a reset occurs. A debugger showing the PC stuck
  there with a core that does not progress is the usual sign.

## Debug procedure
1. Connect under reset and set a vector catch on the faults so the core halts on the first fault,
   before it escalates into lockup. OpenOCD: `cortex_m vector_catch [all|none|list]` or a list
   of `hard_err`, `mm_err`, `bus_err`, `irq_err`, `state_err`, `chk_err`, `nocp_err` and `reset`.
   Without NVIC setup enabling them, MemManage, BusFault and UsageFault are mapped to HardFault.
2. Run. The core halts on the first fault; inspect CFSR, HFSR, MMFAR/BFAR and the stacked frame
   as in the HardFault workflow.
3. If it locks up straight after reset, dump the vector table (the initial stack pointer word and
   reset vector word) and check the stack pointer points into RAM and the reset vector is valid.

## Make HardFault robust
- Keep the handler small and do not call printf, malloc or RTOS APIs from it: record and reset.
- A fault inside the handler (for example from a bad stack pointer) is what escalates into lockup,
  so avoid touching memory you have not checked.

## Verify
- [ ] Vector catch stops at the original fault; lockup no longer reproduced after the fix.
- [ ] The reset-cause register no longer reports lockup in soak tests.

## Checked
Confirmed from the Memfault HardFault post (priority -1 lockup, reset not required, nRF52840 debug
quote, 0xFFFFFFFE fetch loop) and the OpenOCD cortex_m vector_catch documentation (parameter names,
mapping to HardFault when NVIC setup does not enable the faults). Removed as unconfirmed (Arm
manuals were not readable): the DHCSR S_LOCKUP bit and address, the ARMv6-M SVC/BKPT cause, vendor
reset-cause registers, the bad-vector-table cause list and the naked-assembly handler advice. Fixed
the vector_catch argument list (`int_err` is not an OpenOCD name; `irq_err` is).

Method: docs-checked 2026-11-09 against the Memfault Interrupt Cortex-M HardFault post and the OpenOCD Architecture and Core Commands page, both read.
