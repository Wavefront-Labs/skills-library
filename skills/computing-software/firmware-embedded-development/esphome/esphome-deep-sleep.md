---
id: computing-software.firmware-embedded-development.esphome.esphome-deep-sleep
name: esphome-deep-sleep
category: computing-software
field: firmware-embedded-development
product: esphome
tags: [esphome, deep-sleep, run-duration, sleep-duration, wakeup-pin, touch-wakeup, ext1-wakeup, battery, on-wake]
level: practitioner
status: docs-checked
description: "Configure ESPHome deep sleep for battery nodes: run and sleep durations, wake sources on ESP8266, ESP32 and BK72xx, pin and touch wakeup, and Home Assistant availability."
sources: ["https://esphome.io/components/deep_sleep/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Esphome deep sleep

`deep_sleep` puts ESP8266, ESP32, BK72xx and nRF52 nodes to sleep after a set time to conserve battery. While asleep the node does nothing and answers no network traffic, including OTA updates.

Pattern: set `run_duration` (how long the node stays active checking and reporting sensors), then choose how to wake.
- ESP8266: only timed wake with `sleep_duration`, and `GPIO16` must be wired to `RST`. Some boards with an onboard USB chip on the reset line (for example D1 mini) can interfere.
- ESP32: timer, or wake on an RTC pin (`GPIO0`, `2`, `4`, `12`, `13`, `14`, `15`, `25`, `26`, `27`, `32`, `39` per the page), or touch.
- BK72xx: timer (maximum 36 hours) and/or one or more non-strapping pins. Zephyr maximum sleep is 49 days.

Options:
- `run_duration`: on ESP32 can be a mapping with `default` (required), `gpio_wakeup_reason` and `touch_wakeup_reason`.
- `sleep_duration`.
- `touch_wakeup` (ESP32): requires a properly configured touch binary sensor.
- `wakeup_pin` (ESP32/BK72xx): a pin schema; use `inverted` to wake on LOW. BK72xx accepts a list of `pin` entries with `wakeup_pin_mode`.
- `wakeup_pin_mode` (default `IGNORE`): what to do when the pin is already in the wake state at sleep entry.
- `on_wake`: automation after waking.
- `esp32_ext1_wakeup`: wake on multiple pins; cannot be combined with `wakeup_pin`, and each pin may have its own `on_wake`.

If entities show Unavailable in Home Assistant while the device sleeps and deep_sleep was added after the device, remove and re-add the device in Home Assistant. Pair with `safe_mode.mark_successful` if the device sleeps before the good-boot time.

## Checked

2026-11-04. Prose, option names, defaults and ranges were compared with https://esphome.io/components/deep_sleep/ (fetched this batch). Nothing needed removing.

Method: documentation only; no commands were run.
