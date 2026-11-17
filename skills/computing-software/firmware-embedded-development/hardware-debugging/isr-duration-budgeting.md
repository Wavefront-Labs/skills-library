---
id: computing-software.firmware-embedded-development.hardware-debugging.isr-duration-budgeting
name: isr-duration-budgeting
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [isr-duration, interrupt-latency, cpu-load, dwt-cyccnt, nvic-priority, deferred-processing, hardware-debugging, firmware-embedded-development]
level: advanced
status: draft
description: "Budget and measure ISR execution time: per-ISR CPU load, DWT cycle counts and GPIO markers, worst-case latency for lower-priority IRQs, and moving work out of interrupts."
sources:
  - https://developer.arm.com/documentation/dai0179/b/
  - https://interrupt.memfault.com/blog/arm-cortex-m-exceptions-and-nvic
  - https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ISR duration budgeting

## The budget
For each interrupt: `load_i = rate_i x duration_i`. Sum over all ISRs is CPU time stolen from
tasks; keep it well under 30-50% so tasks meet deadlines.
Latency for an IRQ at priority P = its entry latency (12 cycles on M3/M4, 15-16 on M0+) + the
longest-running ISR that can block it (same or higher priority, or any critical section with
interrupts masked) + all higher-priority ISRs that can fire meanwhile.

Example: UART RX at 921600 baud with 1-byte FIFO = 92 kHz. A 4 us ISR uses 37% of CPU; with an
8 MHz SPI DMA ISR at the same priority taking 20 us, a byte arrives every 10.8 us and is lost.
Fix: DMA + idle-line detection, or priority above the SPI ISR.

## Measuring
- **GPIO marker:** set a pin at ISR entry, clear at exit; scope measures duration, period and
  jitter, with infinite persistence for worst case. Cheapest and most trustworthy.
- **DWT cycle counter:**
  ```c
  CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk; DWT->CYCCNT = 0; DWT->CTRL |= 1;
  void TIM2_IRQHandler(void){ uint32_t t0 = DWT->CYCCNT; /* ... */
      uint32_t d = DWT->CYCCNT - t0; if (d > isr_max[TIM2_IRQn]) isr_max[TIM2_IRQn] = d; }
  ```
  On M7 unlock with `DWT->LAR = 0xC5ACCE55` first. Not on M0/M0+ (no CYCCNT): use a free-running
  timer.
- **Trace tools:** SystemView/Tracealyzer record every ISR enter/exit with timestamps and give
  min/avg/max per ISR and CPU load.

## Shortening ISRs
- Do only time-critical work (read data register, clear flag, timestamp); defer the rest to a task
  via notification/queue or a lower-priority software interrupt (PendSV-like `NVIC_SetPendingIRQ`
  on a spare vector).
- Use DMA for bulk transfers, hardware FIFOs, and peripheral-to-peripheral triggers.
- No blocking calls, printf, or floating point without lazy stacking awareness (M4F stacks 18
  extra words when FP is used).
- Place hot ISRs in RAM/ITCM on parts with flash wait states (M7 at 480 MHz: 7 WS flash).

## Priority design
Rank by deadline, not importance: the shortest deadline gets the highest priority (rate-monotonic
style). RTOS kernels require API-calling ISRs at or below `configMAX_SYSCALL_INTERRUPT_PRIORITY`.

## Verify
- [ ] Per-ISR max duration and rate recorded under worst-case load; total < budget.
- [ ] Worst-case latency of each IRQ below its deadline (e.g. FIFO overrun time).
