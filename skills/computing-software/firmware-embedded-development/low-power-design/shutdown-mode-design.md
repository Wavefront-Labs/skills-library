---
id: computing-software.firmware-embedded-development.low-power-design.shutdown-mode-design
name: shutdown-mode-design
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [shutdown-mode, system-off, standby, nanoamp-sleep, wake-from-reset, backup-registers, low-power, firmware-embedded-development]
level: practitioner
status: draft
description: "Use the deepest MCU state (STM32 Shutdown/Standby, nRF System OFF): what survives, wake sources, boot-path detection, state in backup registers, and the latency cost."
sources:
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
  - https://docs.nordicsemi.com/bundle/ps_nrf52840/page/power.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/sleep_modes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shutdown mode

The deepest state: core and almost all RAM off, wake is a reset. Use it when the device sleeps for
minutes to months and wake latency of a full boot (ms) is fine.

## Typical figures and what survives
| Part / mode | Current | Survives | Wake sources |
|---|---|---|---|
| STM32L4 Shutdown | ~30 nA (no RTC), ~300 nA with RTC on LSE | backup registers (VBAT domain), RTC | WKUP pins, RTC, tamper, NRST |
| STM32L4 Standby | ~120-300 nA | + optional SRAM2 retention, pull config via PWR | + IWDG, LSE CSS |
| nRF52840 System OFF | ~0.4 uA (no RAM), ~1.5 uA with some RAM retained | selected RAM blocks, GPREGRET | GPIO DETECT/SENSE, LPCOMP, NFC field, reset |
| ESP32 deep sleep (closest) | ~10 uA | RTC memory, RTC GPIO hold | timer, ext0/ext1, touch, ULP |
Shutdown on STM32 disables the brownout reset: supply dips are not detected while in it.

## Entering (STM32 L4 HAL)
```c
HAL_PWREx_EnableGPIOPullDown(PWR_GPIO_A, PWR_GPIO_BIT_5);   /* hold pins via PWR pulls */
HAL_PWREx_EnablePullUpPullDownConfig();
__HAL_PWR_CLEAR_FLAG(PWR_FLAG_WU);                          /* clear stale wake flags first */
HAL_PWR_EnableWakeUpPin(PWR_WAKEUP_PIN1_HIGH);
HAL_PWREx_EnterSHUTDOWNMode();
```
nRF: `NRF_POWER->SYSTEMOFF = 1;` (or `sys_poweroff()` in Zephyr) after configuring GPIO SENSE.

## On wake
- It is a reset: detect it in early boot. STM32: `PWR_SR1` WUFx/SBF flags (SBF for Standby);
  nRF: `RESETREAS.OFF` / `.LPCOMP` / `.NFC`. Branch to a fast path (skip splash, re-init only
  what you need).
- Restore state from backup registers (`RTC->BKPxR`, 32 x 32-bit on L4), retained RAM, or flash.
- Clear the wake flags, otherwise the next entry wakes immediately.

## Trade-offs
- Boot time (clock setup, RTOS start, peripheral init) is paid every wake: 1-50 ms of active current.
  Above roughly one wake per second, Stop/System ON idle is often cheaper; measure both.
- GPIO state is lost unless held by PWR pull configuration or pad hold; outputs float otherwise
  and external loads may turn on.
- Debugger attached prevents true shutdown (see debugger measurement pitfalls).

## Verify
- [ ] Measured current in shutdown matches datasheet with probe disconnected.
- [ ] Each wake source detected correctly in the boot path; no immediate re-wake loops.
