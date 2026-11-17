---
id: computing-software.firmware-embedded-development.hardware-debugging.code-section-cycle-counting
name: code-section-cycle-counting
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [timing-analysis, cycle-counting, profiling-macros, min-max-statistics, gpio-timing-marker, debugger-cycle-counter, benchmark-harness, firmware-embedded-development]
level: practitioner
status: draft
description: "Measure how long firmware sections take: cycle-counter instrumentation with min/max/avg statistics, GPIO markers on a scope, and debugger cycle counters, with their pitfalls."
sources:
  - https://developer.arm.com/documentation/ddi0403/latest
  - https://www.segger.com/products/development-tools/ozone-j-link-debugger/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cycle counting code sections

**Goal:** reliable numbers for "how long does this function / ISR / loop take", including the
worst observed case, on the real target.

## Instrumentation with statistics
```c
typedef struct { uint32_t min, max, last; uint64_t sum; uint32_t n; } prof_t;
#define PROF_START()   uint32_t _t0 = DWT->CYCCNT
#define PROF_END(p)    do { uint32_t d = DWT->CYCCNT - _t0; (p).last = d; \
    if (d < (p).min || !(p).n) (p).min = d; if (d > (p).max) (p).max = d; \
    (p).sum += d; (p).n++; } while (0)

prof_t p_filter;
void control_isr(void) { PROF_START(); run_filter(); PROF_END(p_filter); }
```
Read the struct via debugger live view, a shell command, or telemetry. **max** is the number
that matters for real-time budgets; averages hide the problem. On cores without DWT (M0/M0+),
use a free-running hardware timer instead.

## GPIO markers (no code-size or debugger dependence)
Set a pin at entry, clear at exit; measure pulse widths on a scope or logic analyser, with
infinite persistence or width histogram to see the distribution. Costs ~2-4 cycles per edge
with direct register writes (`GPIOx->BSRR`), much more with `HAL_GPIO_WritePin`/`digitalWrite`.
Also shows *when* it runs relative to other signals.

## Debugger features
- Ozone, IAR, Keil and STM32CubeIDE show a cycle counter in the register view; run to breakpoint
  A, reset counter, run to B. Interrupts during stepping distort results.
- Instruction-trace tools (ETM, Ozone timeline) give exact per-function timing with no
  instrumentation.

## Pitfalls
- **Cold vs warm cache / flash accelerator**: first execution is slower; report both.
- **Compiler moves code across the measurement**: the measured region may not contain what you
  think at `-O2`. Use `__DSB()` or a compiler barrier (`__asm volatile("" ::: "memory")`) around
  the region and check the disassembly.
- **Interrupts inside the section** inflate max. Decide whether you want pure execution time
  (mask interrupts) or response time (leave enabled).
- **Debug builds** time differently from release: measure the shipping configuration.
- Data-dependent paths: drive inputs to their worst case (largest buffers, error paths).

## Verify
- [ ] Measurements taken on the release build, with min/max/avg reported.
- [ ] Instrumentation overhead calibrated (empty region measurement).
