---
id: computing-software.firmware-embedded-development.hardware-debugging.advanced-scope-triggering
name: advanced-scope-triggering
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [oscilloscope, scope-triggering, pulse-width-trigger, runt-trigger, serial-bus-trigger, segmented-memory, holdoff, single-shot, firmware-embedded-development]
level: advanced
status: draft
description: "Catch rare firmware-related events on a scope: pulse-width, runt, timeout and serial-decode triggers, holdoff, segmented memory and GPIO marker triggering."
sources:
  - https://www.tek.com/en/documents/primer/xyzs-oscilloscopes-primer
  - https://www.keysight.com/us/en/assets/7018-02556/application-notes/5990-6436.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Advanced oscilloscope triggering

**Goal:** capture the one-in-a-million glitch or timing violation instead of staring at
a continuously refreshing screen.

## Trigger types and firmware uses
| Trigger | Use |
|---|---|
| Edge, normal mode, single | one event after arming; the default for debugging |
| Pulse width (< or > T) | ISR or task that takes too long (marker GPIO high during the ISR, trigger on width > budget) |
| Timeout / dropout | a heartbeat or periodic signal that stops (watchdog-style capture) |
| Runt | a pulse that doesn't reach full logic level: marginal drive, contention |
| Setup/hold | data changes too close to clock: SPI/parallel bus timing violations |
| Serial bus (I2C/SPI/UART/CAN with decode option) | trigger on a specific address, NACK, byte value or error frame |
| Pattern/logic (multiple channels) | state combinations, e.g. CS low AND IRQ high |

## Firmware markers make triggers easy
Add debug GPIOs and toggle them in code: set at ISR entry, clear at exit; pulse on an error
path; set when a queue is full. The scope then triggers on the firmware event and shows the
analog context (supply, bus) around it. Keep a spare pin or two on every board for this.

## Holdoff and position
- **Holdoff** stops re-triggering for a time after a trigger: stabilises displays of burst
  traffic (trigger on the first byte of each packet only).
- Put the trigger point near the right edge (pre-trigger) to see what led up to the event.

## Segmented memory / history
Splits acquisition memory into segments, each captured on a trigger with timestamps. Capture
1000 occurrences of an intermittent event, then step through them or overlay them to find
the odd one out. Great for "the 1 in 10,000 SPI transaction that fails".

## Mask/limit testing
Define a pass/fail mask around a good waveform, run for hours, stop on first violation:
automated soak testing of signal quality.

## Gotchas
- Auto trigger mode free-runs and hides rare events; use **Normal** or **Single**.
- Trigger level on noisy signals: add hysteresis/noise reject or HF reject coupling.
- Serial decode triggers need correct thresholds and protocol settings (bit rate, CPOL/CPHA).

## Verify
- [ ] Pulse-width trigger set to the ISR budget catches overruns in a stress test.
- [ ] Segmented capture of 1000 events reviewed for outliers.
