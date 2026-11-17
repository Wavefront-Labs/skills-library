---
id: computing-software.firmware-embedded-development.hardware-debugging.gpio-toggle-timing-instrumentation
name: gpio-toggle-timing-instrumentation
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [gpio-toggle-timing, debug-pins, isr-latency, execution-time-measurement, logic-analyzer, bsrr, timing-instrumentation, oscilloscope, firmware-embedded-development]
level: practitioner
status: draft
description: "Instrument firmware timing with debug GPIO toggles: single-store set/clear, macros that compile out, encoding states on several pins, measuring ISR latency, durations and jitter on a scope or LA."
sources:
  - https://www.st.com/resource/en/application_note/an4899-stm32-microcontroller-gpio-hardware-settings-and-lowpower-consumption-stmicroelectronics.pdf
  - https://developer.arm.com/documentation/ddi0403/latest
  - https://sigrok.org/wiki/PulseView
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPIO toggle timing instrumentation

**Goal:** see exactly when code runs, how long it takes, and how it interleaves with interrupts
and bus traffic - with nanosecond resolution and almost no overhead.

## Make the toggle cheap and atomic
```c
#if DEBUG_PINS
#define DBG_HI(n) (GPIOB->BSRR = (1u << (n)))           /* single store, no RMW */
#define DBG_LO(n) (GPIOB->BSRR = (1u << ((n) + 16)))
#else
#define DBG_HI(n) ((void)0)
#define DBG_LO(n) ((void)0)
#endif
```
- Atomic set/clear registers (STM32 BSRR, nRF OUTSET/OUTCLR, RP2040 SIO set/clr, SAM OUTSET)
  avoid read-modify-write races with ISRs and cost ~2-3 cycles plus bus latency.
- `HAL_GPIO_WritePin` / Arduino `digitalWrite` add 10s-100s of cycles and distort short
  measurements.
- Configure the pin push-pull, high speed (OSPEEDR) so edges are crisp; route to a test point.

## What to measure
| Pattern | Measures |
|---|---|
| HI at ISR entry, LO at exit | ISR duration and frequency |
| external signal edge vs ISR HI | interrupt latency (input edge on ch1, debug pin on ch2) |
| HI before, LO after a function | execution time; scope "width" statistics give min/max/jitter |
| toggle each loop iteration | loop period and jitter |
| one pin per task/context | scheduling timeline, preemption visible as overlapping highs |
Use the scope's measurement statistics or a logic analyser over thousands of events; worst
case matters more than average.

## Encoding more states
- Several pins as a binary state code (3 pins = 8 states) written with one BSRR store
  (`BSRR = (code << base) | ((~code & 7) << (base + 16))`).
- A pulse train count to signal an event id on one pin (costs time, use sparingly).
- A DAC output as an analog "state" trace on a scope.

## Accuracy notes
- On Cortex-M7 and parts with write buffers, the pin changes a few cycles after the store;
  constant offset, cancels in durations. Add `__DSB()` only if you need edge ordering against
  other bus accesses.
- Compiler may move code across the toggle; MMIO is volatile so the toggle stays in program
  order with other volatile accesses, but pure computations can be reordered around it -
  check disassembly for tight measurements.
- Compare with the DWT cycle counter (see `dwt-cycle-counter-profiling`) when no pins are free.

## Verify
- [ ] Toggle with nothing between HI/LO measures only tens of ns (instrumentation overhead).
- [ ] Release build has the macros compiled out (`nm`/disassembly shows no BSRR writes).
