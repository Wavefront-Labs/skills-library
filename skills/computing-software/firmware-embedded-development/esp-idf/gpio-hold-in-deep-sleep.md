---
id: computing-software.firmware-embedded-development.esp-idf.gpio-hold-in-deep-sleep
name: gpio-hold-in-deep-sleep
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-sleep, gpio-hold, rtc-gpio-hold, gpio-deep-sleep-hold, pin-state-retention, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Keep ESP32 output pins at a defined level through deep sleep and reset with gpio_hold_en, rtc_gpio_hold_en and gpio_deep_sleep_hold_en, and release them on wake."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/gpio.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/sleep_modes.html
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_driver_gpio/include/driver/gpio.h
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_driver_gpio/include/driver/rtc_io.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPIO hold in deep sleep

During deep sleep the digital GPIO domain powers down: outputs float unless held. A floating
enable pin can switch on a regulator or a load and destroy your sleep current.

## Hold an output
```c
gpio_set_direction(GPIO_NUM_4, GPIO_MODE_OUTPUT);
gpio_set_level(GPIO_NUM_4, 0);          /* sensor power off */
gpio_hold_en(GPIO_NUM_4);               /* latch the pad's current output level and configuration */
gpio_deep_sleep_hold_en();              /* ESP32/S2/C3/S3/C2 (see below): keep digital pad holds in deep sleep */
esp_deep_sleep_start();
```
On wake:
```c
gpio_hold_dis(GPIO_NUM_4);              /* otherwise the pin ignores gpio_set_level */
```
Per the `gpio_hold_en` header notes, on ESP32/S2/C3/S3/C2 `gpio_hold_en` alone does not keep a digital
GPIO through deep sleep: the pin resets to its default state on wake unless `gpio_deep_sleep_hold_en()`
was also called (that function is only declared on chips without single-pad hold in deep sleep, so a
newer chip may not have it; check the header for your target). After `gpio_hold_dis`, a pin that
was input by default goes to that default, so set the output mode and level before calling it if the
level must not glitch. For an RTC IO pad you can use `rtc_gpio_hold_en()` instead (returns
`ESP_ERR_INVALID_ARG` if the pin is not an RTC IO).

## Inputs and pulls
To keep a pull-up active in sleep:
```c
rtc_gpio_pullup_en(GPIO_NUM_33); rtc_gpio_pulldown_dis(GPIO_NUM_33);
```
Or configure the sleep-time pull with `gpio_sleep_set_pull_mode()` (and `gpio_sleep_set_direction()`).

## Isolation
For pins not used during sleep that connect to external pulls, `rtc_gpio_isolate(pin)` disconnects
the pad to stop leakage; the sleep-modes guide's example is GPIO12 on an ESP32-WROVER module, which is
pulled up externally and has an internal pulldown. Call it before `esp_deep_sleep_start()`.

## Holds survive more than sleep
While a hold is enabled a held output level cannot be changed, and it stays enabled until
`gpio_hold_dis` or power-down. Startup code that configures a pin and sees no effect usually forgot to
release a hold.

## Strapping pins
Do not hold a strapping pin at a level that selects the wrong boot mode on the next reset; the
strapping pins for each chip are listed in the GPIO documentation for that target.

## Verify
- [ ] Scope or meter on held pins during sleep shows the intended level.
- [ ] Sleep current with held pins matches budget (no regulator half-enabled).
- [ ] After wake, the pin responds to `gpio_set_level` (hold released).

## Checked

Checked against ESP-IDF v6.1 headers (components/esp_driver_gpio/include/driver/gpio.h and rtc_io.h) and docs/en/api-reference/system/sleep_modes.rst.
Confirmed: `gpio_hold_en`/`gpio_hold_dis` semantics, the note that on ESP32/S2/C3/S3/C2 `gpio_deep_sleep_hold_en` is needed to hold a digital GPIO through deep sleep and that it is only declared where single-pad hold in deep sleep is unsupported, the gpio_hold_dis default-input glitch warning, `rtc_gpio_hold_en`, `rtc_gpio_pullup_en`, `rtc_gpio_pulldown_dis`, `rtc_gpio_isolate` and the GPIO12 WROVER example, `gpio_sleep_set_pull_mode`. Removed unconfirmed claims: the list of ESP32 RTC GPIOs, the statement that C3/C6/S3 hold digital pins through `gpio_hold_en` alone (the header says the opposite for C3/S3), `CONFIG_GPIO_ESP32_SUPPORT_SWITCH_SLP_PULL` (no such symbol found), hold persistence through software and watchdog reset, and the named ESP32 strapping pins.

Method: documentation only; no commands were run.
