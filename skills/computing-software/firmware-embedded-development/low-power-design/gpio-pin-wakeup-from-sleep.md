---
id: computing-software.firmware-embedded-development.low-power-design.gpio-pin-wakeup-from-sleep
name: gpio-pin-wakeup-from-sleep
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [wake-source, gpio-wakeup, exti-wakeup, wkup-pin, edge-trigger, level-wake, debounce-in-sleep, standby-wakeup-pin, firmware-embedded-development]
level: practitioner
status: draft
description: "Wake an MCU from stop/standby/deep sleep on a GPIO (button, sensor interrupt line): EXTI vs dedicated WKUP pins, edge vs level, pulls, and missed-edge races."
sources:
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/sleep_modes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPIO / EXTI wake-up from sleep

**Goal:** a button press or a sensor's INT line reliably wakes the device from its deepest
usable sleep mode, without spurious wakes or missed events.

## Which pins can wake which mode
| Mode (STM32 naming) | GPIO wake |
|---|---|
| Sleep | any interrupt |
| Stop 0/1/2 | any EXTI line (all GPIOs via EXTI mux), edge-triggered |
| Standby / Shutdown | only dedicated **WKUPx** pins (a handful), chip resets on wake |
ESP32 deep sleep: `ext0` (one RTC GPIO, level), `ext1` (several RTC GPIOs, ANY_HIGH/ALL_LOW),
`gpio` wake on C3/S3 (`esp_deep_sleep_enable_gpio_wakeup`). nRF52 System OFF: any GPIO with
SENSE configured. Check this table for your part before choosing pins in the schematic.

## Edge vs level
- **Edge (EXTI rising/falling):** misses an event that happened just before entering sleep.
  Race: INT asserts, you check "nothing pending", then sleep: the edge is gone and the sensor
  holds INT low forever.
- **Level wake (ESP32 ext0/ext1, nRF SENSE, some WKUP polarities):** can't miss, but wakes
  immediately if the line is still active: clear the source first.
- Robust pattern with edge-only EXTI: disable interrupts, check the pin **level**, sleep only
  if inactive, then `WFI` (pending interrupt still wakes WFI even with PRIMASK set).
```c
__disable_irq();
if (HAL_GPIO_ReadPin(INT_GPIO_Port, INT_Pin) == GPIO_PIN_SET) {  /* idle high */
    HAL_PWREx_EnterSTOP2Mode(PWR_STOPENTRY_WFI);
}
__enable_irq();
```

## Pulls and leakage
- Configure the pull in the domain that is still powered during sleep: Standby uses
  `HAL_PWREx_EnableGPIOPullUp()`/`PWR->PUCRx` because normal GPIO config is lost; ESP32 deep
  sleep uses `rtc_gpio_pullup_en()`.
- An open-drain sensor INT needs a pull-up; a 10 k pull held low by an asserted INT draws
  330 uA at 3.3 V. Use 100 k+ or ensure the line is idle-high in sleep.

## Debounce
Mechanical buttons bounce for 1-20 ms: on wake, disable the EXTI line, start a timer, sample
the level after ~20 ms, then re-enable. Don't sleep while the button is still bouncing.

## Verify
- [ ] 1000 button presses: 1000 wakes, no spurious wakes in a 12 h idle soak.
- [ ] Asserting INT just before sleep entry (scripted) never deadlocks the device.
- [ ] Sleep current unchanged with the button released.
