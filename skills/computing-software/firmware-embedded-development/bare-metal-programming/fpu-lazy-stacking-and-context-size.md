---
id: computing-software.firmware-embedded-development.bare-metal-programming.fpu-lazy-stacking-and-context-size
name: fpu-lazy-stacking-and-context-size
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [fpu, lazy-stacking, fpccr, aspen, lspen, extended-stack-frame, exc-return-fpu, interrupt-latency-fpu, firmware-embedded-development]
level: advanced
status: draft
description: "Understand Cortex-M FPU lazy stacking (FPCCR ASPEN/LSPEN): exception frame sizes, latency effects, stack sizing for FP context, and when to disable it."
sources:
  - https://developer.arm.com/documentation/dai0298/latest/
  - https://developer.arm.com/documentation/dui0553/latest/Cortex-M4-Peripherals/Floating-Point-Unit--FPU-
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FPU lazy stacking and context size

**Goal:** correct stack sizes and predictable interrupt latency on cores with an FPU, without
paying FP save/restore cost on every interrupt.

## Frames
- Basic exception frame: 8 words (R0-R3, R12, LR, PC, xPSR) = 32 bytes.
- Extended frame when the interrupted context used the FPU (`CONTROL.FPCA = 1`): adds S0-S15 +
  FPSCR + reserved = **26 words = 104 bytes** total.
- `EXC_RETURN` bit 4 = 0 indicates an extended frame (0xFFFFFFE1/E9/ED vs F1/F9/FD).

## Lazy stacking (FPCCR, default on)
- `ASPEN = 1`: automatically set FPCA when FP instructions execute, and use extended frames.
- `LSPEN = 1`: **reserve** space for S0-S15/FPSCR on exception entry but don't write them; the
  core saves them only if the handler itself executes an FP instruction. Entry latency stays
  at ~12 cycles unless the ISR uses FP.
- Space is always reserved, so **stack sizing must assume 104-byte frames** per nesting level
  for any context that touched the FPU.

## Configurations
| ASPEN | LSPEN | Behaviour |
|---|---|---|
| 1 | 1 | default: lazy, best average latency |
| 1 | 0 | always save FP regs if context used FPU: deterministic but slower entry |
| 0 | 0 | no automatic FP context saving: only safe if FP is used in a single context (no ISR/task preemption with FP), or saved manually |
RTOS ports (FreeRTOS ARM_CM4F, Zephyr) rely on ASPEN/LSPEN and additionally save S16-S31 for
tasks that used the FPU (`EXC_RETURN` bit 4 tells them), making a task context 50 words.

## Gotchas
- An ISR that calls `printf("%f")` or any float math pays the deferred save: entry latency jumps
  by ~17+ cycles at the first FP instruction, measurable as jitter.
- Interrupt stack overflow appears only when an FP-using context is interrupted by nested
  ISRs: size MSP for (nesting depth x 104 B) + handler locals.
- Debuggers showing "imprecise" faults inside an ISR's first FP instruction: the lazy save
  hit a stack overflow or MPU violation (`LSPERR`/`MLSPERR` bits in CFSR).

## Verify
- [ ] MSP high-water mark measured with FP-heavy code running when interrupts nest.
- [ ] Latency of critical ISRs measured with and without FP use in the interrupted code.
