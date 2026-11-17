---
id: computing-software.firmware-embedded-development.bare-metal-programming.dwt-cycle-counter-profiling
name: dwt-cycle-counter-profiling
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [systick-timebase, dwt-cyccnt, dwt, cycle-counter, demcr, trcena, cortex-m, profiling, lar-unlock, firmware-embedded-development]
level: practitioner
status: draft
description: "Enable and use the Cortex-M DWT CYCCNT cycle counter for precise timing: DEMCR.TRCENA, Cortex-M7 lock access, overflow, and what it can't do on M0/M0+."
sources:
  - https://developer.arm.com/documentation/ddi0403/latest
  - https://developer.arm.com/documentation/dui0553/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DWT cycle counter (CYCCNT)

**Goal:** count core clock cycles to time a code section, measure ISR cost or build an
accurate short delay, without a timer peripheral.

## Availability
DWT CYCCNT exists on ARMv7-M/ARMv8-M Mainline (Cortex-M3/M4/M7/M33/M55). It is **absent on
Cortex-M0/M0+/M23** (ARMv6-M/v8-M Baseline): use SysTick VAL or a hardware timer there.
`DWT->CTRL` bit 25 `NOCYCCNT` = 1 also means not implemented.

## Enable
```c
static inline void cyccnt_init(void) {
    CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;   // power the DWT/ITM blocks
#if defined(__CORTEX_M) && (__CORTEX_M == 7)
    DWT->LAR = 0xC5ACCE55;                            // M7: unlock software access
#endif
    DWT->CYCCNT = 0;
    DWT->CTRL  |= DWT_CTRL_CYCCNTENA_Msk;
}
```
On ARMv8-M the register is `DCB->DEMCR` in newer CMSIS headers (`CoreDebug` is kept as an
alias in most packs).

## Measuring
```c
uint32_t t0 = DWT->CYCCNT;
work();
uint32_t cycles = DWT->CYCCNT - t0;   // unsigned subtraction survives one wrap
```
32 bits wrap at 2^32 cycles: 26.8 s at 160 MHz, 8.9 s at 480 MHz. Unsigned difference is
right for intervals shorter than one wrap.

## Gotchas
- **Debugger owns DEMCR.** Some probes clear TRCENA on disconnect/reset; re-run init after
  every reset, not just once in a debug session. Works without a debugger attached once
  TRCENA is set by firmware.
- **Cache and flash wait states.** The first run of a loop includes cache misses; time the
  second iteration or run it several times and report min and max.
- **Interrupts inflate measurements.** Mask them (`__disable_irq`) around the section if you
  want pure code cost, or leave them enabled if you want real-world latency.
- **Measurement overhead** is a few cycles (two LDRs and a SUB); calibrate by timing an empty
  section and subtracting.
- **Low-power modes stop the core clock**, so CYCCNT doesn't advance during WFI; don't use it
  as wall-clock time.

## Microsecond delay from CYCCNT
```c
void delay_us(uint32_t us) {
    uint32_t start = DWT->CYCCNT, n = us * (SystemCoreClock / 1000000u);
    while ((DWT->CYCCNT - start) < n) { }
}
```

## Verify
- [ ] `DWT->CYCCNT` increments between two reads in a free-running loop.
- [ ] Timing a known `delay_us(1000)` against a scope GPIO toggle matches within a few cycles.
- [ ] Init is called on every boot path, including after watchdog reset.
