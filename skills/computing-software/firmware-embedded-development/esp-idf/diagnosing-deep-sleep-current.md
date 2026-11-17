---
id: computing-software.firmware-embedded-development.esp-idf.diagnosing-deep-sleep-current
name: diagnosing-deep-sleep-current
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-sleep, deep-sleep-current, sleep-current-measurement, leakage-current, power-profiler, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Find why an ESP32 board draws milliamps instead of microamps in deep sleep: measurement setup, board leakage sources, pin states, flash and RTC domain options."
sources:
  - https://github.com/espressif/esp-idf/blob/master/components/esp_hw_support/include/esp_sleep.h
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/sleep_modes.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/current-consumption-measurement-modules.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing high deep-sleep current

## Measure correctly
- Use an ammeter with low internal resistance that switches current ranges dynamically (the ESP-IDF measurement guide recommends the Joulescope and the Nordic Power Profiler Kit II). Ordinary ammeters drop enough voltage to destabilise the module.
- Measure the bare module rail, not a dev board's USB input: on most chips the guide says some dev-board circuits still draw power in deep sleep, so use a bare module as it describes.
- Disconnect USB and debuggers; the USB Serial/JTAG controller and USB PHY are powered off in deep sleep, but a connected host and debugger make the setup unrepresentative.

## Binary search the board
1. Module alone on a jig with only supply: compare with the deep-sleep current in your chip's datasheet.
2. Add board sections back (regulator, sensors, pull resistors) one at a time.
Common board offenders (size each from the part datasheet or Ohm's law, V/R for resistors):
| Source | Fix |
|---|---|
| LDO quiescent current | low-quiescent-current regulator |
| Power LED | remove or switch |
| USB-UART bridge powered from 3V3 | power from VBUS only |
| Resistor divider for battery sense | high values plus a switch, or gate it |
| Sensor left powered | power through a GPIO or load switch held off |
| Pull-up to a pin driven low | match pin state to pull |

## Firmware causes
- Floating or driven pins: set outputs to the level that turns loads off before sleeping;
  `rtc_gpio_isolate()` unused pins with external pulls.
- RTC peripherals left on: `esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH, ESP_PD_OPTION_OFF)` when
  ext0/touch/ULP are not needed (the sleep-modes page uses `ESP_PD_OPTION_ON` for the ext0 case where the RTC IO module must stay enabled).
- ULP program running with a short period.
- Wake source misconfigured: device actually reboots in a loop. Log `esp_sleep_get_wakeup_cause()`
  and reset reason; the current trace shows periodic spikes.
- Wi-Fi/BT not stopped: the sleep-modes page requires `esp_wifi_stop()` (and the Bluetooth stop calls) before entering sleep.

## Debug aid
`esp_sleep_config_gpio_isolate()` isolates all GPIO pins in the sleep state, and `esp_sleep_enable_gpio_switch(bool)` enables or disables switching pin state between sleep and wake. `CONFIG_ESP_SLEEP_GPIO_RESET_WORKAROUND` is unrelated to leakage: it addresses resets from electrostatic pulses on input-only GPIOs during light sleep. Read your chip's errata for leakage issues.

## Verify
- [ ] Current trace (screenshot) shows the sleep floor within budget over a full cycle.
- [ ] Measured on at least 3 boards (component variance).
- [ ] Battery-life calculation updated with measured floor and wake energy.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the sleep-modes page, esp_sleep.h, esp_hw_support Kconfig and the module current measurement guide: recommended ammeters and burden-voltage warning, dev boards unsuitable for module measurement on most chips, rtc_gpio_isolate, esp_sleep_pd_config with ESP_PD_DOMAIN_RTC_PERIPH, wireless stop requirement, esp_sleep_config_gpio_isolate and esp_sleep_enable_gpio_switch. Wrong: CONFIG_ESP_SLEEP_GPIO_RESET_WORKAROUND was described as a leakage fix; it addresses light-sleep resets from electrostatic pulses. Removed unconfirmed datasheet currents, offender current ranges, Otii and PSRAM/flash claims.
Method: documentation only; no commands were run.
