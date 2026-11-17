---
id: computing-software.firmware-embedded-development.arduino.watchdog-on-arm-arduino-boards
name: watchdog-on-arm-arduino-boards
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arm-arduino-watchdog, adafruit-sleepydog, samd-wdt, rp2040-watchdog, uno-r4-wdt, mbed-watchdog, arduino, firmware-embedded-development]
level: practitioner
status: draft
description: "Enable hardware watchdogs on ARM Arduino boards (SAMD, RP2040, UNO R4, Nano 33 BLE/mbed, ESP32): per-core APIs, max timeouts, reset-cause checks and debugger interaction."
sources:
  - https://github.com/adafruit/Adafruit_SleepyDog
  - https://arduino-pico.readthedocs.io/en/latest/rp2040.html
  - https://docs.arduino.cc/tutorials/uno-r4-minima/cheat-sheet/
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/wdts.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Watchdogs on ARM-based Arduino boards

`avr/wdt.h` does not exist on ARM cores. Each core has its own API.

## Per platform
- **SAMD21/SAMD51 (Zero, MKR, Nano 33 IoT, Feather M0/M4):** `Adafruit_SleepyDog`
  (`int ms = Watchdog.enable(4000); Watchdog.reset();`) or `WDTZero`. Max ~16 s. Reset cause:
  `PM->RCAUSE.bit.WDT` (SAMD21) / `RSTC->RCAUSE.bit.WDT` (SAMD51).
- **RP2040 / RP2350 (Earle Philhower core):** `rp2040.wdt_begin(8000); rp2040.wdt_reset();` max
  ~8.3 s. Pico SDK equivalents: `watchdog_enable(ms, pause_on_debug)`, `watchdog_update()`,
  `watchdog_caused_reboot()`. Mbed-based Arduino core for RP2040 uses `mbed::Watchdog`.
- **UNO R4 (Renesas RA4M1):** `#include <WDT.h>`, `WDT.begin(5000)`, `WDT.refresh()`; max ~5.5 s.
  (RA WDT can only be started once per reset.)
- **Nano 33 BLE / Portenta (mbed OS cores):** `mbed::Watchdog::get_instance().start(5000);
  ...kick();` Nano 33 BLE nRF52840 WDT cannot be stopped once started, and continues during sleep
  unless configured to pause.
- **ESP32 core:** task watchdog via ESP-IDF API (`esp_task_wdt_init()` / `esp_task_wdt_reconfigure()`
  in core 3.x, `esp_task_wdt_add(NULL)`, `esp_task_wdt_reset()`). `loop()` task is not subscribed by
  default in recent cores (`enableLoopWDT()` subscribes it).

## Usage rules (all platforms)
- Feed from one place in the main loop after confirming all work progressed (check-in flags),
  not from a timer ISR, which keeps feeding even when `loop()` is stuck.
- Choose a timeout above the longest legitimate blocking operation (Wi-Fi connect, SD write,
  flash erase). Feed inside long loops that are known to be healthy.
- Check the reset cause at boot and report watchdog resets (Serial log, counter in flash).
- Library `Watchdog.sleep(ms)` on SAMD uses the WDT as a wake timer, not a reset; do not confuse
  the two modes.

## Debugger interaction
Some WDTs keep counting while the core is halted at a breakpoint, resetting the board mid-debug.
RP2040 has `pause_on_debug` (`watchdog_enable(ms, true)`), nRF52 has `CONFIG.HALT = Pause`; check
the reference manual for others. Disable the watchdog in debug builds or enable the pause option.

## Verify
- [ ] A deliberate `while(1);` resets the board within the configured timeout.
- [ ] Boot code reports the watchdog as reset cause afterwards.
