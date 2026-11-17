---
id: computing-software.firmware-embedded-development.bare-metal-programming.running-code-from-ram-ramfunc
name: running-code-from-ram-ramfunc
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [ramfunc, code-in-ram, ramfunc-section, linker-script, flash-programming, cortex-m, gnu-ld, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Place selected functions in RAM with a .ramfunc section: linker script LMA/VMA with AT>, the startup copy loop, and when it is required (flash erase, zero-wait loops)."
sources:
  - https://sourceware.org/binutils/docs/ld/Output-Section-LMA.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running code from RAM (ramfunc)

**Goal:** a handful of functions execute from SRAM (or ITCM) instead of flash, correctly
copied at boot and callable from flash code.

## When it is actually needed
- **Flash erase/program routines** on single-bank parts: the bus stalls or faults if code
  fetches from the bank being written (check the part's reference manual).
- Tight loops that must not see flash wait states or prefetch misses (bit-banged
  protocols, cycle-exact ISRs).
Do not move whole applications to RAM "for speed" without measuring: SRAM is scarce.

## Linker script: VMA and LMA
Every section has a virtual address (VMA, where it runs) and a load address (LMA, where it is stored in the
image). The GNU ld manual says the LMA is set with `AT` (an exact address expression) or `AT>` (a memory
region name; the LMA is the next free address in that region, aligned to the section). The location counter
holds the VMA, not the LMA.
```ld
.ramfunc : ALIGN(4)
{
    _sramfunc = .;
    *(.ramfunc .ramfunc.*)
    . = ALIGN(4);
    _eramfunc = .;
} > RAM AT > FLASH
```
The manual's own example does the same for initialised data: an output section whose VMA is in RAM and whose
LMA follows `.text` in ROM, plus start-up code that copies from the ROM address to the run-time address
using symbols defined by the linker script. Do the same for `.ramfunc`, or place `*(.ramfunc*)` inside the
existing `.data` output section so the normal `.data` copy loop handles it (the common vendor approach).
Obtain the load address with a linker-script symbol or `LOADADDR(.ramfunc)` (ld built-in; not covered by the
page read in this review, check the ld manual).

## Marking functions
Tag the function with a GCC `section` attribute naming `.ramfunc`, and prevent inlining so the body is not
pulled back into a flash caller. Branch range between flash and SRAM, and attributes such as `long_call`,
are toolchain-specific: check the GCC ARM function attributes documentation and your linker map.
- Everything the RAM function calls (compiler helpers, HAL functions) still runs from flash unless it is
  also placed in RAM. For flash-write code, keep it leaf-only and inspect the disassembly.

## Startup copy
If not merged into `.data`, copy the LMA image to the VMA in `Reset_Handler` before any call.

## Gotchas
- If RAM is marked execute-never, carve out the ramfunc region in your protection setup.
- Interrupts during flash erase can still fetch vectors and handlers from flash: disable them or
  relocate the vector table and handlers to RAM too.

## Verify
- [ ] The linker map or symbol table shows the function at a RAM address.
- [ ] Section headers show `.ramfunc` with VMA in RAM and LMA in flash.
- [ ] Stepping in the debugger, the PC is in SRAM inside the function.

## Checked
Checked 2026-11-09 against the GNU ld manual "Output Section LMA" page (read in full). The GCC ARM function
attributes page returned an empty stub and the Arm architecture reference manual is unreadable, so removed:
`long_call` and `noinline` rationale, the 16 MB `BL` range claim, veneer behaviour, literal pool placement,
Cortex-M7 cache maintenance, IAR and Keil syntax, the flash accelerator remark, low-power-mode use, and the
`nm` and `objdump` command lines.
Method: docs-checked 2026-11-09 against the GNU ld Output Section LMA page.
