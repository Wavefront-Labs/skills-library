---
id: computing-software.firmware-embedded-development.bare-metal-programming.tightly-coupled-memory-placement
name: tightly-coupled-memory-placement
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [cortex-m7-cache, tcm, itcm, dtcm, zero-wait-state, deterministic-execution, isr-in-itcm, stack-in-dtcm, linker-sections, firmware-embedded-development]
level: advanced
status: draft
description: "Place time-critical code in ITCM and hot data/stacks in DTCM on Cortex-M7 for zero-wait, cache-independent timing: linker sections, startup copy, and DMA reachability."
sources:
  - https://www.st.com/resource/en/application_note/an4891-stm32h72x-stm32h73x-and-singlecore-stm32h74x75x-system-architecture-and-performance-stmicroelectronics.pdf
  - https://developer.arm.com/documentation/ddi0489/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tightly coupled memory (TCM) placement

**Goal:** deterministic, single-cycle access for interrupt handlers, control loops and their
data, unaffected by cache misses or flash wait states.

## What TCM is
- **ITCM** (instruction TCM, e.g. 64 KB at 0x00000000 on STM32H7/F7): zero-wait execution.
- **DTCM** (data TCM, e.g. 128 KB at 0x20000000): zero-wait data access, 64-bit wide.
- TCM is **not cached** (no need: already core speed), so timing is deterministic: same cycle
  count every run, unlike cached flash code whose first run misses.

## Linker setup
```ld
MEMORY {
  ITCM (xrw) : ORIGIN = 0x00000000, LENGTH = 64K
  DTCM (xrw) : ORIGIN = 0x20000000, LENGTH = 128K
  FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 1024K
}
.itcm_text : ALIGN(4) {
  _sitcm = .;
  *(.itcm_text*)
  *motor_control.o(.text .text*)     /* whole file into ITCM */
  . = ALIGN(4); _eitcm = .;
} > ITCM AT > FLASH
_siitcm = LOADADDR(.itcm_text);
```
Startup must copy `_siitcm` -> `_sitcm..._eitcm` before any ITCM function runs (same as `.data`
copy). Then mark functions:
```c
__attribute__((section(".itcm_text"), noinline)) void TIM1_UP_IRQHandler(void) { ... }
```
Calls from flash to ITCM (and back) may be out of `BL` range (+/-16 MB): GCC inserts long-call
veneers automatically with `--long-calls`-style stubs; check the map for `__..._veneer`.

## What to put where
- ITCM: high-rate ISRs, control loops, DSP kernels, flash-programming routines (flash is busy
  during erase).
- DTCM: main stack and ISR stack (MSP), RTOS kernel data, hot lookup tables, filter state.
  Setting `_estack` at the top of DTCM is a common default in Cube projects.

## Gotchas
- **DMA reachability**: on STM32H7, DMA1/DMA2 can't access DTCM; only MDMA can. Don't put DMA
  buffers there. On F7, DTCM is reachable by DMA via the AHBS port, check the bus matrix.
- ITCM at address 0 means NULL function pointers execute ITCM content instead of faulting; map
  an MPU no-access guard at 0 if ITCM's first bytes are unused.
- Debuggers can't set flash breakpoints in ITCM (it's RAM, software breakpoints work).
- Size budget is small: profile and place only the hot paths.

## Verify
- [ ] Map file shows chosen functions/data in TCM ranges.
- [ ] ISR cycle count (DWT) identical on first and subsequent runs.
