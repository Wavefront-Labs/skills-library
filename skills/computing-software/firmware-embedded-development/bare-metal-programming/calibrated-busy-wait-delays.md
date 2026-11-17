---
id: computing-software.firmware-embedded-development.bare-metal-programming.calibrated-busy-wait-delays
name: calibrated-busy-wait-delays
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [systick-timebase, busy-wait-delay, delay-us, nop-loop, timer-delay, one-shot-timer, cortex-m, firmware-embedded-development]
level: practitioner
status: draft
description: "Build microsecond delays that stay correct across optimisation levels and clock changes: timer-based, CYCCNT-based and why naive NOP loops drift."
sources:
  - https://developer.arm.com/documentation/dui0553/latest
  - https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calibrated busy-wait delays

**Goal:** short blocking delays (1 us to a few ms) for sensor power-up, bit-banged
protocols and datasheet timing, that are never shorter than specified.

## Pick the mechanism
| Need | Use |
|---|---|
| >= 1 ms, OS-less | SysTick millisecond counter with unsigned compare |
| 1 us to 1 ms on M3/M4/M7/M33 | DWT CYCCNT compare |
| M0/M0+ or exact hardware timing | a free-running hardware timer at 1 MHz (prescaler = f_timer/1 MHz - 1) |
| Sub-microsecond (tens of ns) | inline-asm cycle loop, or better a peripheral (timer one-pulse, SPI) |

## Why `for (i = 0; i < N; i++)` fails
At `-O2` the compiler deletes an empty loop entirely. Making `i` volatile keeps it but the
cycle count per iteration now depends on optimisation level, flash wait states, ART/I-cache
and compiler version. A delay tuned at `-O0` becomes 3-4x shorter at `-Os`.

## Timer-based (portable, works on M0)
```c
// TIMx: prescaler set so CNT ticks at 1 MHz, auto-reload 0xFFFF, running.
void delay_us(uint16_t us) {
    uint16_t start = TIMx->CNT;
    while ((uint16_t)(TIMx->CNT - start) < us) { }
}
```
The cast keeps the subtraction modulo 16 bits, so a counter wrap is harmless for delays up
to 65535 us.

## Deterministic asm loop (when no timer is free)
```c
static inline void delay_cycles(uint32_t n) {   // ~3 cycles/iter on M3/M4 from zero-wait RAM
    __asm volatile("1: subs %0, %0, #1 \n bne 1b" : "+r"(n) :: "cc");
}
```
Calibrate once on target (CYCCNT or scope) and document the clock and memory it was measured
from; branch cost changes when the code runs from flash with wait states.

## Rules
- Always round **up**: `n = (us * f_mhz) + 1`. A datasheet minimum is a minimum.
- Recompute from `SystemCoreClock` at run time if the clock changes (low-power clock
  switching), never hard-code cycles.
- Interrupts may lengthen a delay but never shorten it; fine for "at least" timing, wrong for
  bit-banged protocols with maximum timing (WS2812, 1-Wire). Mask interrupts for those, or use
  a peripheral (SPI/RMT/PWM+DMA) instead.
- Don't busy-wait for long periods in battery devices: sleep with a wake timer instead.

## Verify
- [ ] Scope a GPIO pulse around `delay_us(10)` at `-O0` and `-Os`: both >= 10 us.
- [ ] Repeat after changing the system clock: still correct.
