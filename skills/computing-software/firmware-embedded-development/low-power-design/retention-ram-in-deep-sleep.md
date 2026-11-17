---
id: computing-software.firmware-embedded-development.low-power-design.retention-ram-in-deep-sleep
name: retention-ram-in-deep-sleep
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [retention-ram, sram-retention, standby-mode, system-off, rtc-data-attr, backup-sram, deep-sleep, wake-state, sram2, firmware-embedded-development]
level: practitioner
status: draft
description: "Keep state through deep sleep with retention RAM: STM32 SRAM2/backup SRAM, nRF RAM section retention, ESP32 RTC memory, linker placement, current cost, and startup handling on wake."
sources:
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
  - https://docs.nordicsemi.com/bundle/ps_nrf52840/page/power.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/deep-sleep-stub.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Retention RAM

**Goal:** use the deepest sleep mode (which normally loses SRAM) while keeping a small amount of
state (counters, sensor history, radio session keys) without writing flash on every cycle.

## What each family offers
| MCU | Deepest mode | Retention option | Notes |
|---|---|---|---|
| STM32L4/L4+/U5 | Standby/Shutdown | SRAM2 retained in Standby with `PWR_CR3.RRS` (`HAL_PWREx_EnableSRAM2ContentRetention()`) | lost in Shutdown; Stop2 keeps all SRAM at higher current |
| STM32F4/F7/H7 | Standby | 4 KB backup SRAM (`PWR_CSR.BRE`, backup regulator), also on VBAT | plus RTC backup registers (20-32 words) |
| nRF52 | System OFF | per-RAM-section retention bits `NRF_POWER->RAM[n].POWERSET` (S0RETENTION...) | ~30 nA per 4 KB section retained (check PS) |
| nRF53/nRF91 | System OFF | `VMC` RAM retention registers | Zephyr: `retained_mem` / `retention` subsystem |
| ESP32 family | Deep-sleep | RTC slow memory (8 KB): `RTC_DATA_ATTR`, `RTC_NOINIT_ATTR` | RTC fast memory for wake stubs |
| ATmega/AVR | Power-down | all SRAM retained | (no deeper mode) |

## Placement
Put retained variables in a dedicated linker section that maps to the retained RAM block and is
**not** zeroed or initialised by startup on wake:
```c
__attribute__((section(".sram2_noinit"))) static app_state_t s_state;   /* STM32L4 SRAM2 at 0x10000000 alias */
RTC_DATA_ATTR static uint32_t s_boot_count;                              /* ESP-IDF */
```
ESP-IDF `RTC_DATA_ATTR` is initialised on power-on and kept across deep sleep; `RTC_NOINIT_ATTR`
is never initialised. For STM32/nRF add the section to the linker script with `NOLOAD`
(see `noinit-ram-sections`).

## Wake handling
Waking from Standby/System OFF is a **reset**: code runs from the reset vector.
1. Check wake cause early (`PWR_FLAG_SB` / `__HAL_PWR_GET_FLAG(PWR_FLAG_SB)`,
   `NRF_POWER->RESETREAS` OFF bit, `esp_sleep_get_wakeup_cause()`), clear it.
2. If woken from sleep and the retained block's magic/CRC is valid, resume from it; otherwise cold
   init.
3. Re-enable retention before the next sleep if the setting is not persistent.

## Cost and trade-offs
- Retention current scales with retained size: retain only the sections you use (nRF per
  section, STM32 SRAM2 as a whole). Measure: e.g. STM32L4 Standby ~0.1-0.3 µA more with SRAM2.
- Retained RAM is not power-fail safe: brown-out or battery change loses it. Mirror essential
  data to flash occasionally.
- Parity/ECC SRAM may need initialisation after power-on before reads (STM32 SRAM2 parity,
  H7 ECC) - init only on cold boot.

## Verify
- [ ] Counter in retained RAM increments across 100 sleep/wake cycles.
- [ ] Sleep current with retention matches datasheet figure for mode + retained RAM.
- [ ] Power-on reset detected as cold boot (magic invalid) and state reinitialised.
