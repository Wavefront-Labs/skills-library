---
id: computing-software.firmware-embedded-development.low-power-design.wakeup-pins-and-polarity
name: wakeup-pins-and-polarity
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [wakeup-pin, wkup-polarity, pwr-cr3-ewup, wakeup-flag, standby-wakeup, gpio-sense, low-power, firmware-embedded-development]
level: practitioner
status: draft
description: "Configure dedicated wake-up pins for Standby/Shutdown/System OFF: WKUP polarity bits, clearing WUF flags before entry, PWR pulls, nRF SENSE levels, and immediate-wake loops."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://docs.nordicsemi.com/bundle/ps_nrf52840/page/gpio.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/sleep_modes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wake-up pins and polarity

In the deepest modes, normal EXTI is off; only dedicated wake-up logic in the always-on domain
can wake the chip. Getting polarity and flags right is most of the work.

## STM32 (L4/L5/U5/G4 PWR)
- WKUP1..5 on fixed pins (L4: PA0, PC13, PE6, PA2, PC5). Enable with `PWR_CR3.EWUPx`.
- Polarity `PWR_CR4.WPx`: 0 = rising/high, 1 = falling/low. HAL: `PWR_WAKEUP_PIN1_HIGH` /
  `PWR_WAKEUP_PIN1_LOW`.
- Wake flags `PWR_SR1.WUFx` are set whenever the pin is at the active level and must be cleared
  (`PWR_SCR.CWUFx`) **after** the pin goes inactive and **before** entering Standby/Shutdown, or the
  chip wakes immediately.
- Pin pulls in Standby/Shutdown come from `PWR_PUCRx`/`PDCRx` with `PWR_CR3.APC = 1`, not from GPIO
  registers.
```c
HAL_PWR_DisableWakeUpPin(PWR_WAKEUP_PIN1);          /* change polarity with pin disabled */
__HAL_PWR_CLEAR_FLAG(PWR_FLAG_WUF1);
HAL_PWR_EnableWakeUpPin(PWR_WAKEUP_PIN1_LOW);       /* button to GND */
HAL_PWREx_EnableGPIOPullUp(PWR_GPIO_A, PWR_GPIO_BIT_0);
HAL_PWREx_EnablePullUpPullDownConfig();
HAL_PWR_EnterSTANDBYMode();
```
STM32F4 has a single WKUP pin (PA0), rising edge only; a button must pull high.

## nRF52 System OFF
Any GPIO can wake: configure input with `SENSE = High` or `Low`. The DETECT signal is a level, so if
the pin is already at the sense level when entering System OFF, the chip wakes at once. Set SENSE
to the opposite of the current level (toggle-style) for buttons that may be held.
`nrf_gpio_cfg_sense_input(pin, NRF_GPIO_PIN_PULLUP, NRF_GPIO_PIN_SENSE_LOW)`.

## ESP32
`esp_sleep_enable_ext0_wakeup(GPIO_NUM_33, 0)` (single RTC GPIO, level) or
`esp_sleep_enable_ext1_wakeup(mask, ESP_EXT1_WAKEUP_ANY_HIGH)` (ANY_LOW on S3/C6, ALL_LOW on
ESP32). Pulls via `rtc_gpio_pullup_en()` and keep RTC peripherals powered for ext0.

## Polarity choice
- Pull-up + button to GND (active low) is standard; with active-low wake the pull-up current only
  flows while pressed.
- Sensor INT outputs: match active level; push-pull INT avoids pull current entirely.

## Verify
- [ ] Wake works for each pin and each polarity on hardware; held button does not cause loops.
- [ ] Boot code reports which WKUP pin woke the device (WUFx) and clears it.
