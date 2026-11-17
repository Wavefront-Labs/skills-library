---
id: computing-software.firmware-embedded-development.stm32.msi-pll-mode-lse-calibration
name: msi-pll-mode-lse-calibration
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-clocks, msi-pll-mode, msipllen, msi-auto-calibration, lse-trimming, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Use STM32L4/L5/U5/WB MSI PLL mode to auto-trim the MSI from the LSE crystal, getting accurate USB, UART and system clocks without an HSE."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MSI PLL mode (LSE auto-calibration)

MSI is the multi-speed internal RC on low-power STM32s (100 kHz to 48 MHz). Untrimmed it is
about +/-1%; with `MSIPLLEN` set, hardware continuously locks it to the 32.768 kHz LSE,
reaching roughly +/-0.25% or better: good enough for crystal-less USB FS on L4 at 48 MHz.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Enable
```c
/* 1. LSE on first (backup domain access) */
HAL_PWR_EnableBkUpAccess();
__HAL_RCC_LSEDRIVE_CONFIG(RCC_LSEDRIVE_LOW);
RCC_OscInitTypeDef o = {0};
o.OscillatorType = RCC_OSCILLATORTYPE_LSE | RCC_OSCILLATORTYPE_MSI;
o.LSEState = RCC_LSE_ON;
o.MSIState = RCC_MSI_ON;
o.MSICalibrationValue = RCC_MSICALIBRATION_DEFAULT;
o.MSIClockRange = RCC_MSIRANGE_11;            /* 48 MHz */
o.PLL.PLLState = RCC_PLL_NONE;
HAL_RCC_OscConfig(&o);
/* 2. enable PLL mode */
HAL_RCCEx_EnableMSIPLLMode();                  /* sets RCC_CR_MSIPLLEN */
```
In CubeMX: RCC > "MSI Auto Calibration" enabled with LSE configured.

## Rules
- LSE must be running and stable before setting MSIPLLEN; if the LSE fails, MSI keeps running
  untrimmed. Enable LSE CSS (`HAL_RCCEx_EnableLSECSS`) to detect it.
- Don't change MSI range while PLL mode is on unless the RM sequence allows it (L4: allowed;
  check your series).
- Wake-up from Stop with MSI as wake clock: calibration resumes after wake.

## USB without HSE
Select MSI as the 48 MHz clock source (`RCC_USBCLKSOURCE_MSI`) with range 11 and PLL mode on.
On parts with HSI48 + CRS (L4+, L5, G4, U5), HSI48 trimmed by CRS from USB SOF is the
alternative.

## Verify
- [ ] Measure MCO output (`HAL_RCC_MCOConfig(RCC_MCO1, RCC_MCO1SOURCE_MSI, ...)`) with a counter: within spec.
- [ ] USB enumerates across temperature range without HSE.
- [ ] Behaviour defined if LSE is missing at boot (timeout, fallback).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
