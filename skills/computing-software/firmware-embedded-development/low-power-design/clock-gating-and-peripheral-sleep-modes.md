---
id: computing-software.firmware-embedded-development.low-power-design.clock-gating-and-peripheral-sleep-modes
name: clock-gating-and-peripheral-sleep-modes
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [low-power, clock-gating, peripheral-clock-enable, rcc, sleep-mode, stop-mode, standby-mode, wake-up-time, clock-tree-shutdown, unused-peripheral, flash-wait-states, power-mode-transition, wfi, wfe, firmware-embedded-development]
level: advanced
status: draft
description: "Cut active-mode current by gating clocks to unused peripherals and choosing the right sleep/stop/standby depth, trading wake-up latency against the current savings each depth actually buys."
sources:
  - https://www.st.com/resource/en/application_note/an4365-lowpower-modes-management-for-stm32-microcontrollers-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clock gating and peripheral sleep modes

**Goal:** stop paying active-mode current for peripherals and clock domains
the firmware isn't using right now — the lever that applies *while the core is
running*, complementing the deep-sleep-depth decisions in
`computing-software.firmware-embedded-development.low-power-design.current-profiling-and-duty-cycle-budget`
and `computing-software.firmware-embedded-development.esp-idf.deep-sleep-power-budgeting`.

## Clock gating: the easiest, most forgotten win
Most MCUs power every enabled peripheral's clock whether or not the firmware
currently uses it — a timer, UART, or ADC clocked but idle still draws
current just from its clock tree toggling internal logic. CubeMX/HAL projects
in particular tend to enable every peripheral clock the `.ioc` configured at
boot and never disable any that are only used intermittently. Gate clocks
explicitly:
```c
__HAL_RCC_ADC1_CLK_DISABLE();   // after an ADC conversion burst, before sleep
// ... later, before next use ...
__HAL_RCC_ADC1_CLK_ENABLE();
```
This is nearly free current savings that requires no sleep-mode change at
all — do this before reaching for a deeper sleep mode (rung-4-before-rung-7:
don't redesign the power architecture to save what turning off an unused
timer clock already saves).

## Sleep depth vs wake-up latency trade-off
Deeper sleep modes save more current but take longer to resume useful work
and preserve less state:
- **Sleep/Idle**: core clock stopped, peripherals keep running, wakes in a
  few cycles — use when a peripheral (DMA, a timer) must keep operating
  while the core waits for it.
- **Stop**: most clocks stopped, SRAM and register contents retained, wake-up
  in microseconds to low-single-digit milliseconds depending on part/voltage
  regulator mode — the usual choice for "wake on a GPIO/RTC and resume exactly
  where you left off."
- **Standby/Shutdown**: nearly everything off including most SRAM (only a
  tiny backup-domain survives), wake-up re-boots from reset (not a resume) and
  costs the most time, but current draw is lowest by a wide margin. Choosing
  this when the application actually needed Stop's state retention forces a
  slow, unnecessary full reinit on every wake — check which the application
  genuinely needs before picking the deepest mode "to be safe."

## Wake-up time eats into the duty-cycle budget
A wake-up that takes 2ms before useful work starts, happening every 100ms,
is 2% of the duty cycle spent on transition overhead alone — this must be
accounted in the average-current math from
`computing-software.firmware-embedded-development.low-power-design.current-profiling-and-duty-cycle-budget`,
not treated as free. Measure actual wake-to-ready time on the bench (scope a
GPIO toggled at wake and again when the real work starts) rather than trusting
the datasheet's typical figure, which often excludes regulator/PLL settling
specific to the board's actual clock configuration.

## Flash wait states and voltage-scaling interaction
Lower core voltage/power modes often force lower maximum clock speed (and
different flash wait-state settings) — resuming from a low-power mode at the
same clock configuration used before sleep without re-checking voltage
scaling/wait-state requirements can either leave performance on the table
(ran slower than it needed to) or, worse on some parts, cause flash read
errors if wait states don't match the actual voltage/clock combination.
Always set wait states before raising the clock, and lower the clock before
dropping voltage scaling — reference manual tables, not trial and error.

## Verify
- [ ] Every peripheral clock is gated off when the peripheral is genuinely idle for a meaningful fraction of the duty cycle, confirmed by current measurement before/after.
- [ ] Sleep depth matches what the application actually needs to retain (state vs just time), not the deepest mode by default.
- [ ] Wake-to-ready latency is measured on the bench and included in the average-current/duty-cycle calculation.
- [ ] Wait-state/voltage-scaling changes around sleep entry/exit follow the reference manual's required ordering, verified with a scope trace across at least one full sleep/wake cycle.
