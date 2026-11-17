---
id: computing-software.firmware-embedded-development.bare-metal-programming.enabling-the-fpu-cpacr
name: enabling-the-fpu-cpacr
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [fpu, cpacr-fpu-enable, cp10-cp11, nocp-usagefault, systeminit, fpv4-sp, fpv5-d16, cortex-m4f, firmware-embedded-development]
level: practitioner
status: draft
description: "Turn on the Cortex-M FPU before any floating-point instruction runs: CPACR CP10/CP11, where in startup to do it, and diagnosing the NOCP UsageFault when you don't."
sources:
  - https://developer.arm.com/documentation/dui0553/latest/Cortex-M4-Peripherals/Floating-Point-Unit--FPU-/Enabling-the-FPU
  - https://arm-software.github.io/CMSIS_5/Core/html/group__system__init__gr.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enabling the FPU (CPACR)

**Goal:** a Cortex-M4F/M7/M33/M55 project built with hardware floating point that doesn't
fault on the first `VLDR`/`VMUL`.

## The register
`SCB->CPACR` (0xE000ED88): bits 20-23 grant access to coprocessors CP10 and CP11 (the FPU).
Out of reset they are 0 = access denied, so any FP instruction raises a **UsageFault with
NOCP** (escalated to HardFault if UsageFault isn't enabled).
```c
SCB->CPACR |= (3UL << (10 * 2)) | (3UL << (11 * 2));   /* full access CP10, CP11 */
__DSB();
__ISB();                                               /* required before the next FP instruction */
```

## Where
In `SystemInit()` (CMSIS device template does this when `__FPU_PRESENT == 1U && __FPU_USED == 1U`),
or in assembly at the top of `Reset_Handler`, **before** `__libc_init_array` / C++ static
constructors and before `main`. Gotchas:
- A compiler at `-O2` may emit FP instructions (e.g. `vpush`/`vstm` for saving registers, or
  memcpy using FP registers on some libc builds) in any C function, including the one that
  enables the FPU if it's not tiny. Keep the enabling code in assembly or a minimal function.
- Custom startup files written for Cortex-M3 omit the CPACR write.
- `__FPU_USED` is set by the CMSIS headers based on the compiler's `-mfloat-abi`/`-mfpu`; if
  you build soft-float, the template skips enabling it (fine).

## Diagnosing NOCP
HardFault with `CFSR` = 0x00080000 (UFSR.NOCP) and stacked PC pointing to a `v...`
instruction: FPU not enabled (or code running in a context where it was disabled again, e.g.
after a bootloader jump that reset CPACR, or on a core without an FPU).

## Bootloaders and multiple images
The bootloader may enable or not enable the FPU; the application must still enable it itself.
Conversely, if the bootloader used FP and leaves `CONTROL.FPCA` set when jumping, clear
CONTROL (`__set_CONTROL(0)`) before branching.

## Verify
- [ ] Disassemble `Reset_Handler`/`SystemInit`: CPACR write precedes any FP instruction
      (`arm-none-eabi-objdump -d firmware.elf | grep -n "vpush\|vldr"`).
- [ ] A float multiply in `main` runs without fault in a debug and release build.
