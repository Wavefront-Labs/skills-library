---
id: computing-software.firmware-embedded-development.low-power-design.rtc-periodic-wakeup
name: rtc-periodic-wakeup
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [wake-source, rtc-wakeup, stm32-rtc-wakeup, wakeup-timer, wutr, rtc-alarm, lse, stop-mode, standby-mode, exti-line, firmware-embedded-development]
level: practitioner
status: draft
description: "Wake an MCU periodically from stop or standby with the RTC wake-up timer or alarm: clock choice, EXTI routing, flag clearing and drift."
sources:
  - https://www.st.com/resource/en/application_note/an4759-using-the-hardware-realtime-clock-rtc-and-the-tamper-management-unit-tamp-with-stm32-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RTC periodic wake-up

**Goal:** sleep in the deepest mode that keeps the RTC running and wake every N seconds
(sensor sampling, radio check-in) with low drift and no missed wakes.

## Wake-up timer vs alarm
| | Wake-up timer (WUT) | Alarm A/B |
|---|---|---|
| Purpose | periodic interval | absolute calendar time |
| Range | ~122 us to ~36 h (16-bit counter + clock select) | any time/date with masks |
| Re-arm | automatic | must set next alarm |
Use WUT for "every 10 s"; use alarms for "at 02:00" schedules.

## Clock source
- **LSE 32.768 kHz crystal**: ~20 ppm (~1.7 s/day), runs in all low-power modes. Default
  choice.
- **LSI** RC: +/-5..10 % or worse, temperature dependent. Fine for watchdogs, poor for
  timekeeping; calibrate against HSE if used.
- WUT clock: `RTCCLK/16` for fine intervals (488 us resolution with LSE), or `ck_spre`
  (1 Hz) for 1 s..18 h intervals.

## STM32 HAL sequence
```c
HAL_RTCEx_DeactivateWakeUpTimer(&hrtc);
__HAL_RTC_WAKEUPTIMER_CLEAR_FLAG(&hrtc, RTC_FLAG_WUTF);
__HAL_RTC_WAKEUPTIMER_EXTI_CLEAR_FLAG();   /* EXTI line 20 on F4, 20/22 on others */
HAL_RTCEx_SetWakeUpTimer_IT(&hrtc, 10 - 1, RTC_WAKEUPCLOCK_CK_SPRE_16BITS, 0); /* 10 s */
HAL_SuspendTick();
HAL_PWREx_EnterSTOP2Mode(PWR_STOPENTRY_WFI);
SystemClock_Config();      /* stop mode returns on HSI/MSI: restore PLL */
HAL_ResumeTick();
```

## Gotchas
- **Clear both RTC WUTF and the EXTI pending flag** before sleeping, or the core wakes
  immediately and you measure milliamps instead of microamps.
- Counter value is N-1 for N periods.
- **Standby**: the RTC wakes the chip, but it resets; check `PWR_FLAG_SB`/`WUF` in early boot
  to know it was a timed wake, then clear them.
- Backup domain write protection (`HAL_PWR_EnableBkUpAccess()`) is needed to configure the
  RTC; easy to miss in hand-written code.
- Drift: for long deployments use RTC smooth calibration (`RTC_CALR`) against a reference, or
  resync from network time.
- ESP32 equivalent: `esp_sleep_enable_timer_wakeup(us)`; nRF: RTC or `k_sleep` with
  Zephyr's tickless kernel.

## Verify
- [ ] Wake interval measured with a GPIO pulse over 100 periods: error within LSE tolerance.
- [ ] Sleep current equals datasheet figure for mode + RTC (e.g. ~1-2 uA STOP2 with RTC on
      STM32L4).
- [ ] No immediate wake after entering sleep (flags cleared).
