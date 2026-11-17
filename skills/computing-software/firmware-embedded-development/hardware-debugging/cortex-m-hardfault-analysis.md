---
id: computing-software.firmware-embedded-development.hardware-debugging.cortex-m-hardfault-analysis
name: cortex-m-hardfault-analysis
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [hardfault, hard-fault, cortex-m, arm, fault-analysis, exception-stack-frame, cfsr, hfsr, mmfar, bfar, ufsr, bfsr, mmfsr, exc-return, msp, psp, addr2line, gdb, openocd, pyocd, j-link, segger, imprecise-bus-fault, usage-fault, stack-overflow, swd, logic-analyzer, firmware-embedded-development]
level: advanced
status: gated
description: "Find the faulting line of a Cortex-M HardFault: capture the stacked frame via EXC_RETURN, decode CFSR/HFSR/MMFAR/BFAR, map PC with addr2line, handle imprecise bus faults."
sources:
  - https://developer.arm.com/documentation/
  - https://openocd.org/pages/documentation.html
  - https://pyocd.io/
  - https://github.com/ARM-software/CMSIS_6/blob/main/CMSIS/Core/Include/core_cm4.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cortex-M HardFault analysis — from "stuck in HardFault_Handler" to the faulting line

**Goal:** given a device sitting in `HardFault_Handler`, recover the program counter and fault
cause, name the line of code, and know which class of bug it is. Applies to ARMv7-M/ARMv8-M
(M3/M4/M7/M33). Cortex-M0/M0+ (ARMv6-M) have no CFSR — only the stacked frame is available. (gated: unconfirmed, source is paywalled or blocked)

## 1. Capture the stacked frame
On exception entry the core pushes R0, R1, R2, R3, R12, LR, PC, xPSR onto whichever stack was in
use. The value in LR on entry (**EXC_RETURN**) says which: bit 2 = 0 → MSP, 1 → PSP (tasks under an
RTOS run on PSP). Bit 4 = 0 means an extended FPU frame was pushed (frame is larger, but the first
eight words are the same). (gated: unconfirmed, source is paywalled or blocked)

```c
__attribute__((naked)) void HardFault_Handler(void) {
    __asm volatile(
        "tst lr, #4      \n"
        "ite eq          \n"
        "mrseq r0, msp   \n"
        "mrsne r0, psp   \n"
        "mov r1, lr      \n"
        "b hardfault_c   \n");
}
void hardfault_c(uint32_t *f, uint32_t exc_return) {
    volatile uint32_t pc = f[6], lr = f[5], psr = f[7];
    volatile uint32_t cfsr = SCB->CFSR, hfsr = SCB->HFSR;
    volatile uint32_t mmfar = SCB->MMFAR, bfar = SCB->BFAR;
    __BKPT(0);                 // halt here with a debugger; in the field, save to noinit RAM and reset
    for (;;) {}
}
```
(`ite`/`mrseq` is Thumb-2; on M0 use a branch instead.) Save the values into a `.noinit` RAM
section and log them on the next boot for field devices.

## 2. Decode the fault registers
| Register | Address | Meaning |
|---|---|---|
| CFSR | `0xE000ED28` | MMFSR (byte 0), BFSR (byte 1), UFSR (upper half) |
| HFSR | `0xE000ED2C` | `FORCED` (bit 30): a configurable fault escalated; `VECTTBL` (bit 1): vector fetch failed |
| MMFAR | `0xE000ED34` | faulting address if MMARVALID (CFSR bit 7) |
| BFAR | `0xE000ED38` | faulting address if BFARVALID (CFSR bit 15) |

(SCB base 0xE000ED00 plus offsets 0x28, 0x2C, 0x34, 0x38, from the CMSIS `SCB_Type`.)

Common CFSR bits and what they usually mean:
- **UFSR** `UNDEFINSTR` (bit 16): jumped into data or a corrupted function pointer.
  `INVSTATE` (bit 17): branch to an even address (Thumb bit clear) — often a NULL or bad function
  pointer. `NOCP` (bit 19): FPU used but not enabled. `UNALIGNED` (bit 24) / `DIVBYZERO` (bit 25):
  only if trapping is enabled in `SCB->CCR`.
- **BFSR** `PRECISERR` (bit 9): BFAR holds the exact address — an unclocked peripheral, a
  bad pointer, reading unmapped memory. `IMPRECISERR` (bit 10): see section 4.
  `STKERR` (bit 12): fault while stacking — stack overflow.
- **MMFSR** `DACCVIOL` / `IACCVIOL`: MPU violation (stack guard regions catch overflows this way).

Enable the separate handlers (`SCB->SHCSR |= SCB_SHCSR_USGFAULTENA_Msk | SCB_SHCSR_BUSFAULTENA_Msk
| SCB_SHCSR_MEMFAULTENA_Msk`) so faults arrive with less escalation.

## 3. Map the PC to source
```bash
arm-none-eabi-addr2line -e app.elf -f -C -i 0x08001a3c   # stacked PC
arm-none-eabi-addr2line -e app.elf -f -C 0x08001977      # stacked LR = caller
```
Build with `-g` (it does not change the code) and archive every release ELF. LR shows the caller
when PC is garbage.

## 4. Imprecise bus faults
Writes are buffered, so the fault is reported some instructions later and PC points past the
culprit; BFAR is invalid. To make it precise during debugging, set
`SCnSCB->ACTLR |= SCnSCB_ACTLR_DISDEFWBUF_Msk` (defined in the CMSIS headers for Cortex-M3 and M4 only, bit 1;
it slows execution; `core_cm7.h` does not define it, so check the core's TRM for other cores). Then the fault becomes `PRECISERR` with a
valid BFAR. Usual causes: writing to a peripheral whose clock is off, a DMA buffer pointer into
the wrong RAM, or a corrupted pointer.

## 5. Debugger workflow
```bash
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg     # or: pyocd gdbserver / JLinkGDBServer
arm-none-eabi-gdb app.elf -ex "target extended-remote :3333"
(gdb) x/8xw $sp            # raw stacked frame (if handler hasn't moved SP)
(gdb) p/x *(uint32_t*)0xE000ED28
(gdb) info symbol 0x08001a3c
```
GDB's `bt` often stops at the
exception frame; newer GDB plus correct unwind info can show through it, but reading the frame
yourself is reliable. Under FreeRTOS, `STKERR` or garbage PCs strongly suggest a task stack overflow —
see computing-software.firmware-embedded-development.freertos.task-and-queue-design.

## 6. When registers make no sense
If faults vary between runs, suspect hardware: scope the supply and reset line (brown-out) and
put a logic analyser on the buses. Faults that vanish under the debugger suggest timing,
low-power modes or uninitialised memory. Faults before `main()` point to startup code: see
computing-software.firmware-embedded-development.bare-metal-programming.startup-code-and-linker-script.

## Verify
- [ ] The handler picks MSP vs PSP from EXC_RETURN bit 2 and records PC, LR, CFSR, HFSR, MMFAR, BFAR.
- [ ] A deliberate fault (call a NULL function pointer, or write to an address your reference manual lists as reserved) is decoded to the right line with addr2line.
- [ ] The release ELF for every shipped build is archived for later symbolisation.
- [ ] Field units persist fault data in noinit RAM and report it after reboot.
- [ ] Imprecise faults are reproduced with write buffering disabled to get a valid BFAR.

## Checked
2026-11-01. Confirmed in the CMSIS headers `core_cm3.h`, `core_cm4.h` and `core_cm7.h`: SCB register offsets
(CFSR, HFSR, MMFAR, BFAR addresses), CFSR byte layout (MMFSR, BFSR, UFSR), bit positions of MMARVALID,
BFARVALID, UNDEFINSTR, INVSTATE, NOCP, UNALIGNED, DIVBYZERO, PRECISERR, IMPRECISERR, STKERR, HFSR FORCED and
VECTTBL, SHCSR fault enables, CCR UNALIGN_TRP and DIV_0_TRP, and DISDEFWBUF on M3 and M4 only. Removed: debug
server default port numbers and the J-Link product source. Gated: EXC_RETURN bit meaning and the ARMv6-M
statement, because the Arm documentation pages are JavaScript-only. The OpenOCD, GDB and addr2line commands
were not checked against their manuals.
Method: documentation only; no commands were run.
