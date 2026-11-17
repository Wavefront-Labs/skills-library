---
id: computing-software.firmware-embedded-development.arduino.watchdog-and-brownout-recovery
name: watchdog-and-brownout-recovery
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino, watchdog, wdt, avr-wdt, brownout, bod, bootloader-watchdog-bug, wdt-disable, reset-reason, mcusr, power-glitch, esp32-task-watchdog, esp-task-wdt, hang-recovery, firmware-embedded-development]
level: practitioner
status: draft
description: "Use the hardware watchdog to recover from hangs on Arduino without bricking the board on the bootloader-WDT bug, and read the reset-cause register to tell a watchdog reset from a brownout."
sources:
  - https://www.nongnu.org/avr-libc/user-manual/group__avr__watchdog.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Watchdog timer and brownout recovery on Arduino

**Goal:** have the board reset itself out of a hang in the field, and know *why*
it reset afterward — instead of either never recovering, or bricking itself on
the classic bootloader watchdog bug.

## The AVR bootloader-watchdog infinite-reset bug
On classic Arduino boards (Uno/Nano with the optiboot or stock bootloader), if
your sketch enables the watchdog (`wdt_enable()`) and then the watchdog fires, the
chip resets with WDT still enabled and a short timeout. The Arduino bootloader
does not disable the watchdog before jumping to the sketch, so if your sketch's
first instructions take longer than the watchdog timeout to re-reach
`wdt_disable()`, the board resets again before fully booting — an infinite
reset loop that looks like a bricked board. **Fix:** disable the watchdog as the
very first thing in `setup()` (or even earlier via a `.init3` section constructor
that runs before `main()`), before any other initialization:
```c
#include <avr/wdt.h>
void setup() {
  MCUSR = 0;
  wdt_disable();
  // ... rest of setup
}
```
Newer cores (e.g. optiboot ≥ 5) handle this for you; don't assume it without
checking the bootloader version.

## Using the watchdog correctly
- `wdt_enable(WDTO_4S)` arms a 4 s timeout; call `wdt_reset()` periodically from
  the main loop while things are healthy. If `wdt_reset()` isn't called in time,
  the chip resets.
- Pick the timeout longer than your longest legitimate blocking operation (a
  sensor read with retries, an EEPROM write), or the watchdog fires during normal
  operation.
- Don't call `wdt_reset()` inside an ISR that could itself be the thing hanging —
  that defeats the point. Reset it only from code that proves forward progress
  (e.g. after a full loop iteration, after a successful transaction).

## Telling a watchdog reset from a brownout or power-on
On AVR, `MCUSR` (read it before clearing/before `wdt_disable()` touches it) has
`WDRF`, `BORF`, `EXTRF`, `PORF` bits identifying watchdog, brownout, external
reset-pin, and power-on resets respectively. Log this at boot (to Serial, or a
retained RAM/EEPROM counter) — a field unit that resets every few minutes from
brownout needs a better power supply, not a watchdog bug hunt.

## ESP32/ESP-IDF-based Arduino cores
The Arduino-ESP32 core runs under FreeRTOS with its own **task watchdog**
(`esp_task_wdt`), separate from AVR-style WDT semantics. A task watchdog timeout
reports *which task* failed to yield, which is far more diagnosable — check the
serial panic dump for the task name before assuming it's your own code.

## Verify
- [ ] `wdt_disable()` runs before anything else in `setup()` on AVR, or bootloader is confirmed to already do it.
- [ ] Watchdog timeout is longer than the longest legitimate blocking path, measured not guessed.
- [ ] Reset-cause register is read and logged on every boot.
- [ ] Deliberately hung the main loop on the bench; board recovers via reset within the configured timeout, exactly once (no reset loop).
