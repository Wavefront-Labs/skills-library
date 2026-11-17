---
id: computing-software.firmware-embedded-development.stm32.tamper-detection-and-backup-registers
name: tamper-detection-and-backup-registers
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-security, tamper-detection, tamp-peripheral, backup-register-erase, active-tamper, stm32, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Configure STM32 tamper detection (TAMP/RTC tamper): passive and active tamper pins, internal tamper sources, automatic backup register erase and timestamping events."
sources:
  - https://www.st.com/resource/en/application_note/an4759-using-the-hardware-realtime-clock-rtc-and-the-tamper-management-unit-tamp-with-stm32-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0456-stm32u5-series-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tamper detection and backup registers

Tamper inputs detect enclosure opening, probing or environmental attacks and immediately erase
secrets kept in backup registers (and on newer parts, backup SRAM and crypto keys). Runs from the
backup domain, so it works on VBAT with the main supply off.

## Passive tamper
A switch to ground (or VDD) on a TAMP_INx pin:
```c
RTC_TamperTypeDef t = {0};
t.Tamper = RTC_TAMPER_1;
t.Trigger = RTC_TAMPERTRIGGER_FALLINGEDGE;            /* or level with filter */
t.NoErase = RTC_TAMPER_ERASE_BACKUP_ENABLE;           /* erase backup regs on event */
t.MaskFlag = RTC_TAMPERMASK_FLAG_DISABLE;
t.Filter = RTC_TAMPERFILTER_4SAMPLE;                   /* level mode: debounce */
t.SamplingFrequency = RTC_TAMPERSAMPLINGFREQ_RTCCLK_DIV256;
t.PrechargeDuration = RTC_TAMPERPRECHARGEDURATION_1RTCCLK;
t.TamperPullUp = RTC_TAMPER_PULLUP_ENABLE;
t.TimeStampOnTamperDetection = RTC_TIMESTAMPONTAMPERDETECTION_ENABLE;
HAL_RTCEx_SetTamper_IT(&hrtc, &t);
```
Level mode with sampling and precharge reduces current (the pull-up is pulsed) and rejects glitches.

## Active tamper (L5, U5, H5, G0B/C, WBA)
TAMP outputs a pseudo-random pattern on an output pin that must return on an input pin through a
mesh/trace across the enclosure. Cut or shorted traces mismatch the pattern and trigger. Configure
with `HAL_RTCEx_SetActiveTampers` and seed the LFSR (`HAL_RTCEx_SetActiveSeed`) from the RNG.

## Internal tamper sources
Newer TAMP blocks monitor internally: backup domain voltage/temperature out of range, LSE failure,
RTC calendar overflow, RNG/crypto faults, debug access (on some), monotonic counter overflow.
Enable with `HAL_RTCEx_SetInternalTamper`.

## What gets erased
Backup registers (erased on a tamper event: `RTC_TAMPER_ERASE_BACKUP_*` in the HAL), and on
newer parts backup SRAM and key registers, depending on the part. See your series' TAMP
chapter for the full erase list and any exclusion options.

## Firmware response
Tamper flag survives; on boot read `TAMP_SR` (`__HAL_RTC_TAMPER_GET_FLAG`), log the timestamp
(`HAL_RTCEx_GetTimeStamp`), mark the device as tampered and require re-provisioning.

## Verify
- [ ] Trigger each tamper with main power off (VBAT only): backup registers erased.
- [ ] No false triggers over temperature and vibration tests (filter settings).

## Checked

2026-10-31: Confirmed the L4 passive-tamper API (`RTC_TamperTypeDef`, `RTC_TAMPER_1/2/3`, `RTC_TAMPERTRIGGER_*`, `RTC_TAMPERFILTER_*`, `RTC_TAMPERSAMPLINGFREQ_*`, `RTC_TAMPERPRECHARGEDURATION_*`, `RTC_TAMPER_PULLUP_ENABLE`, `RTC_TIMESTAMPONTAMPERDETECTION_ENABLE`, the `RTC_TAMPER_ERASE_BACKUP_*` erase options and `HAL_RTCEx_SetTamper_IT`) from stm32l4xx_hal_rtc_ex.h, and the newer-series active/internal tamper APIs (`HAL_RTCEx_SetActiveTampers`, `HAL_RTCEx_SetActiveSeed`, `HAL_RTCEx_SetInternalTamper` with the internal-tamper pin definitions) from stm32u5xx_hal_rtc_ex.h. Rewrote the erased-assets list to point at each series' TAMP chapter (RM0456 exceeds the fetch size limit).

Method: documentation only; no commands were run.
