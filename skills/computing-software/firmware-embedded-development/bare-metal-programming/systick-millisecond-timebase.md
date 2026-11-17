---
id: computing-software.firmware-embedded-development.bare-metal-programming.systick-millisecond-timebase
name: systick-millisecond-timebase
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [systick-timebase, systick-config, systick, cortex-m, millisecond-tick, reload-value, clksource, cmsis, systick-handler, firmware-embedded-development]
level: practitioner
status: gated
description: "Configure the Cortex-M SysTick as a 1 ms timebase: reload maths, clock source, priority, atomic tick reads and the off-by-one and 24-bit limits that bite."
sources:
  - https://developer.arm.com/documentation/dui0553/latest/Cortex-M4-Peripherals/System-timer--SysTick
  - https://arm-software.github.io/CMSIS_5/Core/html/group__SysTick__gr.html
  - https://github.com/ARM-software/CMSIS_6/blob/main/CMSIS/Core/Include/core_cm7.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SysTick as a millisecond timebase

**Goal:** a monotonic `uint32_t` millisecond counter driven by SysTick, correct to the
clock, safe to read from any context, with no RTOS.

## Registers (ARMv7-M B3.3)
| Reg | Addr | Meaning |
|---|---|---|
| `SYST_CSR` (CTRL) | 0xE000E010 | bit0 ENABLE, bit1 TICKINT, bit2 CLKSOURCE (1 = core clock, gated: unconfirmed, source is paywalled or blocked), bit16 COUNTFLAG |
| `SYST_RVR` (LOAD) | 0xE000E014 | 24-bit reload value |
| `SYST_CVR` (VAL) | 0xE000E018 | current value, 24 bits |
| `SYST_CALIB` | 0xE000E01C | TENMS (vendor calibration value; compute from the clock instead) |

The counter counts **down** from LOAD to 0, then reloads, so the period is `LOAD + 1` clocks.
For 1 ms at 64 MHz: `LOAD = 64000000/1000 - 1 = 63999`.

## Minimal setup
```c
volatile uint32_t g_ms;
void SysTick_Handler(void) { g_ms++; }

void timebase_init(uint32_t core_hz) {
    SysTick_Config(core_hz / 1000u);   // CMSIS: writes LOAD = ticks-1, VAL = 0,
                                       // sets lowest priority, CLKSOURCE=1, TICKINT, ENABLE
}
```
`SysTick_Config()` returns 1 if `ticks - 1 > 0xFFFFFF` (24 bits). At 480 MHz a 1 ms tick
needs 480000, which fits, but a 100 ms tick (48 M) doesn't: use a slower tick or the
`CLKSOURCE=0` external reference (vendor-defined).

## Gotchas
- **Call it after the clock tree is final.** Setting up SysTick and then switching PLL
  makes every `delay` wrong by the PLL ratio. Use `SystemCoreClockUpdate()` then pass
  `SystemCoreClock`.
- **Priority.** CMSIS sets SysTick to the lowest priority. If the tick drives timeouts
  that an ISR busy-waits on, the wait never ends: never spin on `g_ms` inside a
  higher-priority ISR.
- **Coexisting with a vendor HAL or an RTOS.** A HAL tick and an RTOS kernel tick both want SysTick; give
  one of them a different timer.
- **Reading a 32-bit counter is a single aligned load** on Cortex-M3 and later, so `g_ms` needs only
  `volatile` (gated: unconfirmed, source is paywalled or blocked). A 64-bit counter is not atomic: read high, low, high again and retry if the
  high word changed, or briefly mask interrupts.
- **Sub-millisecond time:** combine `g_ms` with `SysTick->VAL` (counts down), re-reading
  if COUNTFLAG/`g_ms` changed between the two reads. For cycle timing prefer DWT CYCCNT
  (see `computing-software.firmware-embedded-development.bare-metal-programming.dwt-cycle-counter-profiling`).

## Verify
- [ ] Toggle a GPIO every 1000 ticks and measure 1.000 s on a scope/logic analyser (error
      should match the oscillator tolerance in its datasheet).
- [ ] `SysTick_Config` return value checked.
- [ ] SysTick priority is below any ISR that might wait on time.

## Checked
2026-11-01. Confirmed in `core_cm7.h` and the CMSIS-Core SysTick page: `SysTick_Config` writes LOAD = ticks - 1,
sets the lowest priority (`(1 << __NVIC_PRIO_BITS) - 1`), clears VAL, sets CLKSOURCE, TICKINT and ENABLE, and
returns 1 when `ticks - 1` exceeds 0xFFFFFF; register offsets from 0xE000E010 and bit positions; the 1 ms
example structure. Removed: STM32 HAL/CubeMX specifics, crystal and RC tolerance figures. Gated: CLKSOURCE
meaning and the single-load atomicity claim, because the Arm documents are JavaScript-only.
Method: documentation only; no commands were run.
