---
id: computing-software.firmware-embedded-development.low-power-design.determining-wakeup-cause
name: determining-wakeup-cause
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [wakeup-cause, reset-reason, esp-sleep-get-wakeup-cause, hwinfo-reset-cause, wake-source-dispatch, low-power, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Find out why the MCU woke and dispatch on it: ESP32 esp_sleep_get_wakeup_cause and esp_reset_reason, Zephyr hwinfo reset cause, vendor reset flags, and logging spurious wakes."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/sleep_modes.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/misc_system_api.html
  - https://raw.githubusercontent.com/zephyrproject-rtos/zephyr/main/include/zephyr/drivers/hwinfo.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Determining the wake-up cause

Every wake should be explained. Unexplained wakes are the main way battery life silently collapses.

## Where the information lives
**Cores that resume after the sleep instruction (light sleep, Stop-type modes):** the pending
interrupt tells you; check the interrupt controller's pending bits and the peripheral flags in
their ISRs.

**Cores that reset on wake (deep sleep, Standby, System OFF-type modes):** the wake source is
recorded in a vendor reset/wake status register. Find the register and its clear procedure in
the part's reference manual (for example the power controller's wake flags and the reset
controller's reset-reason flags); read it at the start of boot, then clear it.

**Zephyr:** `hwinfo_get_reset_cause(uint32_t *cause)` returns a bit mask of `RESET_*` flags such
as `RESET_PIN`, `RESET_POR`, `RESET_WATCHDOG`, `RESET_BROWNOUT` and `RESET_LOW_POWER_WAKE`.

**ESP32**
```c
switch (esp_sleep_get_wakeup_cause()) {
  case ESP_SLEEP_WAKEUP_TIMER:    break;
  case ESP_SLEEP_WAKEUP_EXT0:     break;
  case ESP_SLEEP_WAKEUP_EXT1:     { uint64_t m = esp_sleep_get_ext1_wakeup_status(); break; }
  case ESP_SLEEP_WAKEUP_TOUCHPAD: { int p = esp_sleep_get_touchpad_wakeup_status(); break; }
  case ESP_SLEEP_WAKEUP_ULP:      break;
  case ESP_SLEEP_WAKEUP_UNDEFINED: /* not a sleep wake (power-on or reset) */ break;
  default: break;
}
```
`esp_sleep_get_ext1_wakeup_status()` identifies which GPIO woke the chip and
`esp_sleep_get_touchpad_wakeup_status()` which touch pad. Combine with `esp_reset_reason()`
(`ESP_RST_DEEPSLEEP` for a deep-sleep wake).

## Dispatch pattern
Read and latch the cause into a variable at the very start of boot (before drivers clear flags),
then clear hardware flags, then branch:
- timer -> periodic job fast path,
- button -> UI path (full init),
- sensor -> read sensor, decide,
- unknown/POR -> full boot.

## Spurious wake hunting
Count wakes per cause in retained RAM or backup registers; expose via telemetry. A rising
"unknown" count usually means: a floating wake pin, a flag not cleared before sleep, a peripheral
interrupt left enabled (SysTick in Stop, UART noise), or a debugger attached.

## Verify
- [ ] Each wake source, triggered individually, is reported correctly.
- [ ] Wake counters over a 24 h soak show only expected causes.

## Checked
2026-10-31. Confirmed on the ESP-IDF sleep-modes and system API pages and the Zephyr hwinfo
header: `esp_sleep_get_wakeup_cause`, `esp_sleep_get_ext1_wakeup_status`,
`esp_sleep_get_touchpad_wakeup_status`, the `ESP_SLEEP_WAKEUP_*` enumerators, `esp_reset_reason`,
`ESP_RST_DEEPSLEEP`, `hwinfo_get_reset_cause` and the `RESET_*` flags. Removed: the STM32
(PWR_SR1, RCC_CSR, EXTI, RTC flag names) and nRF52 (RESETREAS, LATCH, DETECTMODE) register
details, because the ST reference manual PDF and Nordic documentation could not be read here.
Method: documentation only; no commands were run.
