---
id: computing-software.firmware-embedded-development.stm32.shutdown-mode-and-backup-domain
name: shutdown-mode-and-backup-domain
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-low-power, stm32-shutdown-mode, backup-domain, rtc-backup-registers, wakeup-pins, stm32, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Put STM32L4/L5/U5/G4 into Shutdown mode for the lowest current, keep data in backup registers and RTC, configure wake-up pins and handle the reset-like wake."
sources:
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shutdown mode and the backup domain

Shutdown turns off the main regulator, all SRAM (no retention option), the brown-out reset and
most clocks. Only the backup domain (RTC, LSE, backup registers, tamper) and wake-up logic
remain. Current: 30-110 nA without RTC, about 420 nA at 3 V with RTC on LSE (L476 datasheet,
part dependent).

## Differences from Standby
| | Standby | Shutdown |
|---|---|---|
| BOR active | yes | no (brown-outs not detected) |
| SRAM2 retention option | yes | no |
| LSI/IWDG | can run | off |
| Pull-up/down retention | yes (`APC`) | yes |
| Wake | WKUP pins, RTC, IWDG, NRST | WKUP pins, RTC, NRST |

## Enter
```c
HAL_PWR_DisableWakeUpPin(PWR_WAKEUP_PIN1);
__HAL_PWR_CLEAR_FLAG(PWR_FLAG_WU);                 /* clear stale wake flags first */
HAL_PWR_EnableWakeUpPin(PWR_WAKEUP_PIN1_HIGH);    /* PA0 rising */
HAL_RTCEx_SetWakeUpTimer_IT(&hrtc, 3600, RTC_WAKEUPCLOCK_CK_SPRE_16BITS, 0);   /* 1 h */
HAL_PWREx_EnablePullUpPullDownConfig();           /* keep defined pin levels */
HAL_PWREx_EnableGPIOPullDown(PWR_GPIO_B, PWR_GPIO_BIT_5);
HAL_PWREx_EnterSHUTDOWNMode();
```

## Wake behaves like reset
Execution restarts from the reset vector. Distinguish wake from power-on:
```c
if (__HAL_PWR_GET_FLAG(PWR_FLAG_SB) ) { /* woke from Standby */ }
uint32_t wu = PWR->SR1 & (PWR_SR1_WUF1 | PWR_SR1_WUF2 | PWR_SR1_WUFI);   /* which source */
uint32_t magic = HAL_RTCEx_BKUPRead(&hrtc, RTC_BKP_DR0);                   /* our own marker */
```
Set a backup-register marker before entering Shutdown; on boot, a valid marker + wake flag means
"woke from Shutdown".

## Backup domain
- 32 x 32-bit backup registers (`RTC_BKPxR` / `TAMP_BKPxR` on newer series) survive Shutdown,
  Standby and resets, lost on VBAT/VDD loss and on tamper events.
- Access needs `HAL_PWR_EnableBkUpAccess()` (DBP bit) after every reset.
- VBAT pin keeps the backup domain alive when VDD is off.
- Backup domain reset (`__HAL_RCC_BACKUPRESET_FORCE`) wipes RTC and registers: never call it
  unconditionally in init code (CubeMX-generated RTC init can reset the RTC time each boot if the
  user section check is missing).

## Verify
- [ ] Current measured in shutdown (with and without RTC) matches datasheet class.
- [ ] Each wake source works; boot code correctly identifies wake vs power-on.

## Checked

2026-10-31: Confirmed Shutdown-mode behaviour (internal regulators and voltage monitoring off, BOR not available, IWDG off, wake via the 5 WKUP pins / NRST / RTC, I/O pull configuration retained but lost on exit) against AN4621 and the STM32L476RG datasheet; the shutdown currents (about 30-110 nA without RTC, about 420 nA at 3 V with RTC on LSE, Table 49); `PWR_CR1_LPMS_SHUTDOWN` (stm32l476xx.h), `HAL_PWREx_EnterSHUTDOWNMode` and the wake-up/pull APIs (stm32l4xx_hal_pwr_ex.h); the backup-register family (RTC_BKP0R.., RTC_BKP_NUMBER = 32 on L4; TAMP_BKPxR on TAMP-equipped parts per the L4 HAL's TAMP_BKP_NUMBER guard). Removed the unverified 'tamper' Shutdown wake source and the SBF-after-shutdown note.

Method: documentation only; no commands were run.
