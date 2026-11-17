---
id: computing-software.firmware-embedded-development.esp-idf.brownout-detector
name: brownout-detector
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-system, esp-brownout, brownout-reset, power-supply-droop, bod-threshold, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Diagnose ESP32 brownout resets: detector thresholds, Wi-Fi TX current peaks, supply and decoupling fixes, and handling brownout in firmware."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/fatal-errors.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_hw_support/power_supply/port/esp32/Kconfig.power
  - https://github.com/espressif/esp-idf/blob/master/components/esp_wifi/include/esp_wifi.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Brownout detector

## Symptom
```
Brownout detector was triggered
```
Followed by a reset, often right when Wi-Fi starts (TX bursts draw current peaks) or a
motor/LED strip switches on. `esp_reset_reason()` returns `ESP_RST_BROWNOUT`.

## Config
```
CONFIG_ESP_BROWNOUT_DET=y
CONFIG_ESP_BROWNOUT_DET_LVL_SEL_0    # default; on ESP32 level 0 is the lowest threshold (2.43 V +/- 0.05) and level 7 the highest (2.80 V +/- 0.05)
```
Disabling the detector to "fix" resets is wrong: running below spec voltage corrupts flash
writes and causes random crashes. The threshold levels are estimates and vary between chips; fix the supply first.

## Root causes and fixes
| Cause | Fix |
|---|---|
| USB cable/port can't supply peaks | short thick cable, powered hub, or local supply |
| LDO dropout | low-dropout regulator with enough current rating for TX peaks |
| Insufficient bulk capacitance | add bulk plus ceramic decoupling close to the module supply pins (see the hardware design guidelines) |
| Battery with high internal resistance (coin cell, cold Li-ion) | larger cell, supercap buffer, lower TX power |
| Shared rail with motors/LEDs | separate rails or bigger reservoir caps |

Firmware mitigations:
- `esp_wifi_set_max_tx_power(52)` (units 0.25 dBm, so 52 is 13 dBm; valid range 8 to 84; call after Wi-Fi is started) to cut peak current.
- Stagger loads: start Wi-Fi after LEDs/motors settle.

## Measure
Scope the 3V3 rail at the module with a short ground spring and trigger on a falling edge below the brownout threshold for your chip.

## Handling in firmware
The brownout detector (`CONFIG_ESP_BROWNOUT_DET`) resets the chip after printing the message, so there is no time to save data reliably. On
next boot, check the reset reason, log a counter in NVS, and back off (lower TX power, delay
radio start) after repeated brownouts.

## Verify
- [ ] Rail stays above the threshold during worst-case TX plus peripheral load on the scope.
- [ ] 24 h soak at minimum supply voltage with no `ESP_RST_BROWNOUT`.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed: CONFIG_ESP_BROWNOUT_DET and ESP_BROWNOUT_DET_LVL_SEL_0..7 with voltages (ESP32 Kconfig), message text and reset in fatal-errors guide, esp_wifi_set_max_tx_power units and range. Wrong: level 0 was called the highest threshold; on ESP32 it is the lowest (2.43 V) and higher levels raise the threshold. Removed unconfirmed current peaks, AMS1117 dropout, capacitor values and scope trigger figures. ESP_RST_BROWNOUT confirmed in esp_system.h.
Method: documentation only; no commands were run.
