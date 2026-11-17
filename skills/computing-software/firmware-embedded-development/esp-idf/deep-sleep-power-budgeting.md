---
id: computing-software.firmware-embedded-development.esp-idf.deep-sleep-power-budgeting
name: deep-sleep-power-budgeting
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-idf, esp32, esp32-s3, esp32-c3, deep-sleep, light-sleep, modem-sleep, esp-sleep-enable-timer-wakeup, ext0, ext1, rtc-data-attr, rtc-memory, esp-deep-sleep-start, esp-sleep-get-wakeup-cause, esp-pm-configure, config-pm-enable, tickless-idle, wifi-power, battery-life, power-budget, rtc-gpio-isolate, ulp, firmware-embedded-development, sleep-timer-wakeup]
level: practitioner
status: docs-checked
description: "Make an ESP32 battery node sleep properly with ESP-IDF: timer/ext0/ext1 wake-ups, RTC_DATA_ATTR state, light vs deep sleep trade-offs, Wi-Fi connect cost and measured power budgets."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/sleep_modes.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_hw_support/include/esp_sleep.h
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/power_management.rst
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ESP-IDF deep sleep — wake, work, sleep, and know what it costs

**Goal:** a sensor node that wakes on a timer or pin, does its work in as little awake
time as possible, keeps state across sleeps, and has a measured (not guessed) battery
life estimate.

## 1. Pick the sleep mode
| Mode | What keeps running | Resume |
|---|---|---|
| Modem sleep (Wi-Fi idle, CPU on) | CPU, RAM | continues |
| Light sleep | RAM retained, clocks gated | continues after `esp_light_sleep_start()` |
| Deep sleep | RTC domain + RTC memory | **reboots** into `app_main()` |
Current and wake-latency figures vary by SoC and revision: read your SoC's datasheet. A **dev board** with a USB-UART bridge, power LED and generic LDO can draw far more than the chip alone in "deep sleep". Budget against the bare module on your own board, and measure.

## 2. Configure wake sources, then sleep
```c
#include "esp_sleep.h"
#define SLEEP_US (10ULL * 60 * 1000000)       // 10 min; note 64-bit literal
RTC_DATA_ATTR static uint32_t boot_count;    // survives deep sleep, not power loss

void app_main(void) {
    boot_count++;
    esp_sleep_wakeup_cause_t why = esp_sleep_get_wakeup_cause();
    // ESP_SLEEP_WAKEUP_TIMER, _EXT0, _EXT1, _UNDEFINED (power-on/reset) ...
    do_measurement_and_send(why);
    esp_sleep_enable_timer_wakeup(SLEEP_US);
    esp_sleep_enable_ext0_wakeup(GPIO_NUM_33, 0);              // one RTC GPIO, level
    esp_sleep_enable_ext1_wakeup((1ULL << 34) | (1ULL << 35),
                                 ESP_EXT1_WAKEUP_ANY_HIGH);    // several RTC GPIOs (deprecated since v6.0)
    esp_deep_sleep_start();                                     // does not return
}
```
Gotchas:
- ext0/ext1 only work on **RTC-capable GPIOs**, and ext0 and ext1 availability is per SoC (the sleep-modes page gates them by chip). `esp_sleep_enable_ext1_wakeup` is deprecated from v6.0 in favour of `esp_sleep_enable_ext1_wakeup_io` and `esp_sleep_disable_ext1_wakeup_io`; chips without ext1 or ext0 use `esp_sleep_enable_gpio_wakeup_on_hp_periph_powerdown`.
- ext1 `ESP_EXT1_WAKEUP_ALL_LOW` (original ESP32 only) means *all* selected pins low, easy to misread as "any"; on later chips use `ESP_EXT1_WAKEUP_ANY_LOW`.
- `RTC_DATA_ATTR` variables live in RTC slow memory (RTC fast memory on chips without slow memory) and stay powered in deep sleep by default (`esp_sleep_pd_config` can override). They are cleared on power loss; validate them with a magic number or CRC on boot.
- Pins left floating or driving loads leak. Call `rtc_gpio_isolate(GPIO_NUM_12)` (and similar) for pins with external pulls before sleeping.

## 3. Wi-Fi is the budget
On a periodic sender, the radio dominates, so measure the connect-and-send phase on your own AP and board. Ways to cut it:
- Static IP instead of DHCP; cache the AP channel and BSSID in `RTC_DATA_ATTR` and pass them in
  `wifi_config_t` to skip the scan.
- Call `esp_wifi_stop()` before sleeping (required: Wi-Fi is powered down and connections are not kept). Batch readings and transmit every N wakes.
- Consider ESP-NOW or BLE advertising if a gateway exists, since they need far less airtime than TCP/TLS.
- Reuse TLS sessions or use a lighter protocol where policy allows.

## 4. Automatic light sleep (always-on devices)
Enable `CONFIG_PM_ENABLE` and `CONFIG_FREERTOS_USE_TICKLESS_IDLE` in `idf.py menuconfig`, then:
```c
esp_pm_config_t pm = { .max_freq_mhz = 160, .min_freq_mhz = 40, .light_sleep_enable = true };
ESP_ERROR_CHECK(esp_pm_configure(&pm));
```
The system light-sleeps automatically when no power management lock is held (`CONFIG_FREERTOS_USE_TICKLESS_IDLE` is required for this). Held `esp_pm_lock`s (for example from active peripherals and some drivers) keep it awake.

## 5. Budget and measure
Average current = sum(phase current x phase time) / period. Illustrative arithmetic (substitute your measurements): 2.5 s awake at 110 mA
plus 597.5 s at 15 µA over 600 s gives about 0.473 mA average; a cell derated to 1600 mAh
lasts about 3400 h. Awake time dominates, so shave seconds before micro-amps. Full method in
computing-software.firmware-embedded-development.low-power-design.current-profiling-and-duty-cycle-budget.
Measure with a current profiler that captures fast bursts over a complete wake cycle; a multimeter averages them away.

## Verify
- [ ] `esp_sleep_get_wakeup_cause()` is logged and shows TIMER/EXT0/EXT1 as expected on each wake.
- [ ] RTC variables survive deep sleep and are rejected after a power cycle (magic/CRC check).
- [ ] Measured sleep current on your own board (not a dev kit) matches the datasheet order of magnitude.
- [ ] Awake time per cycle is measured from the current trace and recorded in the budget.
- [ ] Battery-life estimate uses measured average current and a derated capacity.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed: esp_sleep_enable_timer_wakeup, ext0 and ext1 wakeup (ANY_HIGH, ALL_LOW semantics and per-chip availability), deprecation of esp_sleep_enable_ext1_wakeup in favour of the _io functions, RTC_DATA_ATTR placement and default power state, rtc_gpio_isolate, esp_wifi_stop requirement, CONFIG_PM_ENABLE, esp_pm_configure fields (max_freq_mhz, min_freq_mhz, light_sleep_enable) and tickless idle requirement, ESP_SLEEP_WAKEUP_* enums. Wrong or stale: ext1 helper advice (deprecated from v6.0), ALL_LOW on later chips, C3 gpio wakeup function name, 8 KB RTC memory size. Removed unconfirmed current, latency and Wi-Fi association figures, tool names and gpio_hold advice; battery arithmetic marked illustrative.
Method: documentation only; no commands were run.
