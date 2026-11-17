---
id: computing-software.firmware-embedded-development.low-power-design.gpio-leakage-and-floating-pin-elimination
name: gpio-leakage-and-floating-pin-elimination
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [low-power, gpio-leakage, floating-input, analog-switch-leakage, pull-up-pull-down, before-sleep-pin-config, external-pull-resistor, level-shifter-leakage, unused-pin-configuration, sleep-current-debug, pull-resistor-current, unused-pins, firmware-embedded-development]
level: advanced
status: draft
description: "Find GPIO-level sleep-current leaks a microamp budget misses: floating inputs, unconfigured analog switches, external pull paths, and pins left in the wrong state before sleep."
sources:
  - https://www.st.com/resource/en/application_note/an4899-how-to-use-the-ultralow-power-stm32l4-series-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPIO leakage and floating-pin elimination

**Goal:** find the microamp-to-milliamp leakage paths that live at the pin
level, which a datasheet's headline "deep sleep current" number never
includes because they're board-and-firmware-specific — the next layer down
from `computing-software.firmware-embedded-development.low-power-design.current-profiling-and-duty-cycle-budget`'s
measurement method, once the measured number is higher than the datasheet says
it should be.

## Floating inputs draw real current
A GPIO configured as input with no pull resistor (internal or external) and no
driven source floats near the input buffer's switching threshold, where CMOS
input stages draw unusually high current (sometimes orders of magnitude above
their nominal leakage) because the input transistor pair is partially
conducting rather than cleanly on or off. This is one of the most common
causes of "measured sleep current is 10-100× the datasheet figure" — audit
every GPIO pin's configuration specifically for sleep mode, not just active
mode: a pin correctly driven by application logic while awake can default
back to a floating input the instant a sleep-mode GPIO reconfiguration routine
forgets about it.

## Pins that matter even when "unused"
- Any pin left unconnected on the PCB but still configured as a floating
  digital input internally leaks the same way as a connected floating pin —
  configure genuinely unused pins to analog mode (disables the digital input
  buffer entirely on most Cortex-M families) or to output, not left at
  input-no-pull reset defaults, if sleep current matters.
- ADC/comparator analog switches connected to a pin can leak through the
  switch even when the ADC itself is clock-gated, unless the switch is
  explicitly disabled — check whether the specific peripheral's "disable"
  bit covers the analog switch or just the conversion logic.
- Pins driving an external pull-up/pull-down network (a level shifter, an
  I2C bus pull-up) continue sourcing/sinking current through that external
  resistor for as long as the pin or the bus is held in the state that draws
  current — an I2C bus idling at a stable high level with weak pull-ups
  draws negligible current, but a pin accidentally left driving low into an
  external pull-up burns milliwatts the whole sleep period, invisible from
  the MCU's own current trace alone (it shows up as *board* current, not
  core current, if measured at different points).

## Pre-sleep pin reconfiguration sequencing
Reconfigure every pin to its lowest-leakage sleep-mode state as one of the
last steps before entering sleep, and restore application configuration as
one of the first steps after waking — not interleaved with other sleep-entry
work where a pin can sit in an intermediate (higher-leakage) state for longer
than necessary. Order matters doubly for pins shared between a peripheral
function and GPIO: disable the peripheral (clock-gate it, per
`computing-software.firmware-embedded-development.low-power-design.clock-gating-and-peripheral-sleep-modes`)
before reconfiguring its pins, or the peripheral may still be driving/sensing
through the pin during the transition.

## Finding leakage on the bench
Toggle pins to their intended sleep state one subsystem at a time while
watching total current on a profiler (PPK2/Joulescope, per the
current-profiling skill above) — a leakage source usually shows as a step
change in the trace the moment a specific pin group is (mis)configured, which
localizes the culprit far faster than auditing the whole pinout by inspection
first.

## Verify
- [ ] Every GPIO pin's sleep-mode configuration (not just active-mode) was explicitly set, including pins the application never touches directly.
- [ ] Analog switches/comparators on pins used for ADC or analog comparison are confirmed disabled, not just clock-gated, before sleep.
- [ ] External pull paths (level shifters, bus pull-ups) were checked for current draw while the MCU sleeps, measured at the board's actual sleep-state pin levels.
- [ ] Bench-measured sleep current matches the datasheet's typical figure within a reasonable margin; any larger gap was traced to a specific pin via step-change profiling, not left unexplained.
