---
id: computing-software.firmware-embedded-development.bare-metal-programming.floating-point-in-interrupt-handlers
name: floating-point-in-interrupt-handlers
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [fpu, fpu-in-isr, isr-float-math, fixed-point, q15-q31, deterministic-latency, rtos-fpu-tasks, firmware-embedded-development]
level: advanced
status: draft
description: "Decide whether to use floating point inside ISRs: latency and stack cost on FPU cores, the soft-float trap on M0/M3, fixed-point alternatives, and RTOS rules for FP tasks."
sources:
  - https://developer.arm.com/documentation/dai0298/latest/
  - https://arm-software.github.io/CMSIS-DSP/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Floating point in interrupt handlers

**Goal:** fast, deterministic ISRs that still do the math the control loop needs.

## On cores with an FPU (M4F/M7/M33)
Using FP in an ISR is allowed and common (motor control loops run in ADC/timer ISRs), but:
- Lazy stacking saves S0-S15/FPSCR the first time the ISR executes an FP instruction if the
  interrupted context used the FPU: ~17-30 extra cycles at that point.
- The 104-byte extended frame is reserved on entry for any FP-using interrupted context.
- If your ISR runs at a zero-latency priority above an RTOS's syscall threshold, nothing else
  changes; FP use is safe because hardware saves the caller-saved FP registers.
For tight loops this cost is small compared to the speedup over fixed-point; measure.

## On cores without an FPU (M0/M0+/M3)
Every float operation is a library call (`__aeabi_fmul` ~30-100 cycles, divide and trig far
more). In an ISR this destroys latency budgets. Use **fixed-point** instead:
```c
/* Q15: value = raw / 32768 */
static inline int16_t q15_mul(int16_t a, int16_t b) {
    return (int16_t)(((int32_t)a * b) >> 15);
}
```
CMSIS-DSP has Q7/Q15/Q31 filters, PID (`arm_pid_q15`), FFTs and saturation helpers; Q31 math
on M3 uses `SMULL` and is fast.

## Never in ISRs, any core
- `printf("%f")`, `strtod`, `sinf` from newlib on non-reentrant builds: may use shared state
  and heap.
- Double-precision on a single-precision FPU (software emulated).

## RTOS considerations
- FreeRTOS on M4F/M7: tasks using FP get extended frames automatically (ARM_CM4F port). On
  ports without automatic FP context saving (some RISC-V, Cortex-A), tasks must call
  `portTASK_USES_FLOATING_POINT()`.
- Zephyr: `CONFIG_FPU=y` with `CONFIG_FPU_SHARING=y` when more than one thread (or thread +
  ISR) uses FP; without sharing, FP registers are corrupted between threads.

## Verify
- [ ] ISR execution time measured with FP math, compared with the latency budget.
- [ ] On FPU-less builds, `nm` shows no `__aeabi_f*` calls reachable from ISRs (call graph or
      map review).
- [ ] Zephyr/FreeRTOS FP context sharing settings match the number of FP-using contexts.
