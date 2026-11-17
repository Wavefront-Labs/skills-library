---
id: computing-software.firmware-embedded-development.bare-metal-programming.extending-32-bit-counter-to-64-bit
name: extending-32-bit-counter-to-64-bit
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [timestamp-extension, systick-timebase, 64-bit-timestamp, overflow-interrupt, torn-read-avoidance, firmware-embedded-development]
level: advanced
status: draft
description: "Extend a 16/32-bit hardware counter to a monotonic 64-bit timestamp with an overflow ISR and a lock-free read loop that never goes backwards."
sources:
  - https://developer.arm.com/documentation/ddi0403/latest/
  - https://www.st.com/resource/en/application_note/an4776-generalpurpose-timer-cookbook-for-stm32-microcontrollers-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 64-bit timestamp extension of a 32-bit counter

A 32-bit microsecond counter wraps every 71.6 minutes; DWT CYCCNT at 480 MHz wraps every 9 s; a
16-bit timer at 1 MHz every 65 ms. Logs, protocols and scheduling want a monotonic 64-bit value.

## Overflow-counting scheme
```c
static volatile uint32_t s_hi;                 /* incremented on counter overflow */
void TIM2_IRQHandler(void) {
    if (TIM2->SR & TIM_SR_UIF) { TIM2->SR = ~TIM_SR_UIF; s_hi++; }
}

uint64_t now_us(void) {
    uint32_t hi, lo;
    do {
        hi = s_hi;
        lo = TIM2->CNT;
    } while (hi != s_hi);                       /* overflow ISR ran between the two reads: retry */
    return ((uint64_t)hi << 32) | lo;
}
```
This handles the ISR running between the reads, but not the case where the counter has
wrapped and the **ISR has not run yet** (interrupts masked, or called from a higher-priority
ISR). Then `lo` is small, `hi` is old, and time jumps back by one period.

## Robust read (works with interrupts masked)
```c
uint64_t now_us(void) {
    uint32_t primask = __get_PRIMASK(); __disable_irq();
    uint32_t hi = s_hi;
    uint32_t lo = TIM2->CNT;
    if ((TIM2->SR & TIM_SR_UIF) && lo < 0x80000000u)   /* wrapped, ISR pending */
        hi++;
    __set_PRIMASK(primask);
    return ((uint64_t)hi << 32) | lo;
}
```
The pending-flag check plus "lo is in the lower half" distinguishes "wrapped just now" from
"flag set right after we read a value near the top".

## Alternative without an ISR (periodically called)
Keep `last_lo` and `hi` in software; on each call, if `lo < last_lo` then `hi++`. Correct as
long as the function runs at least once per wrap period (call it from a slower periodic task).

## Hardware options
- Chain two 16-bit timers (master/slave ITR trigger) or use a 32-bit timer (TIM2/TIM5 on STM32).
- Nordic RTC is 24-bit at 32.768 kHz: the overflow event + same scheme.
- Cortex-M55/M85 and some vendors have 64-bit system timers (e.g. ARM System Timer, RP2040
  TIMER with latched `TIMELR`/`TIMEHR` read order).

## Verify
- [ ] Preload the counter near overflow (`TIM2->CNT = 0xFFFFFF00`) and call `now_us()` in a tight loop with interrupts masked: values never decrease.
- [ ] Long-run test: successive readings are monotonic over several wraps.
