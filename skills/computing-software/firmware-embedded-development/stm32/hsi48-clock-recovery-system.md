---
id: computing-software.firmware-embedded-development.stm32.hsi48-clock-recovery-system
name: hsi48-clock-recovery-system
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-clocks, crs, hsi48, crystal-less-usb, usb-sof-sync, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Run STM32 USB without a crystal by trimming HSI48 with the Clock Recovery System (CRS) synchronised to USB SOF or LSE, including error flags and verification."
sources:
  - https://www.st.com/resource/en/application_note/an4879-introduction-to-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0444-stm32g0x1-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HSI48 and the clock recovery system

Many STM32s (F0, F04x/F07x, L0, L4+, L5, G0, G4, U5, H5, H7) have a 48 MHz RC (HSI48) and a CRS
block that trims it continuously against a reference: USB Start-Of-Frame packets (1 kHz), LSE,
or a GPIO. USB FS needs +/-0.25% accuracy; CRS synced to SOF gives that.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Configure
```c
RCC_OscInitTypeDef o = { .OscillatorType = RCC_OSCILLATORTYPE_HSI48, .HSI48State = RCC_HSI48_ON };
HAL_RCC_OscConfig(&o);
RCC_PeriphCLKInitTypeDef p = { .PeriphClockSelection = RCC_PERIPHCLK_USB,
                               .UsbClockSelection = RCC_USBCLKSOURCE_HSI48 };
HAL_RCCEx_PeriphCLKConfig(&p);

__HAL_RCC_CRS_CLK_ENABLE();
RCC_CRSInitTypeDef c = {0};
c.Prescaler = RCC_CRS_SYNC_DIV1;
c.Source = RCC_CRS_SYNC_SOURCE_USB;
c.Polarity = RCC_CRS_SYNC_POLARITY_RISING;
c.ReloadValue = __HAL_RCC_CRS_RELOADVALUE_CALCULATE(48000000, 1000);   /* 47999 */
c.ErrorLimitValue = RCC_CRS_ERRORLIMIT_DEFAULT;                          /* 34 */
c.HSI48CalibrationValue = RCC_CRS_HSI48CALIBRATION_DEFAULT;              /* 32 (0x20 on some) */
HAL_RCCEx_CRSConfig(&c);
```
CubeMX: RCC > CRS SYNC "USB" and clock tree USB mux on HSI48.

## Before enumeration
SOFs only arrive after the host configures the device, so the initial untrimmed HSI48
(~+/-3% worst case over temperature, typically much better at room temp) must be good enough to
enumerate. It usually is, but in cold or hot extremes, sync to LSE instead
(`RCC_CRS_SYNC_SOURCE_LSE` with reload computed for 32768 Hz) for a trimmed clock from boot.

## Monitoring
`HAL_RCCEx_CRSWaitSynchronization(timeout)` or interrupts: `CRS_FLAG_SYNCOK`, `SYNCWARN`,
`SYNCERR` (error too large), `SYNCMISS` (no SOF, e.g. suspended bus), `TRIMOVF`. Log SYNCERR
counts in the field.

## Verify
- [ ] MCO output of HSI48 measured with USB connected: within 0.25%.
- [ ] Enumeration and bulk transfer pass at temperature extremes.
- [ ] CRS flags show SYNCOK during traffic, SYNCMISS only during suspend.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
