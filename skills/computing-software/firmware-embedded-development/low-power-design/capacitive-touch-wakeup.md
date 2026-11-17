---
id: computing-software.firmware-embedded-development.low-power-design.capacitive-touch-wakeup
name: capacitive-touch-wakeup
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [touch-wakeup, capacitive-touch, esp32-touch-sleep, lesense, tsc, touch-threshold, low-power, firmware-embedded-development]
level: practitioner
status: draft
description: "Wake from deep sleep on a capacitive touch: ESP32 touch-pad wake, STM32 TSC and SiLabs LESENSE scanning, threshold calibration, measuring interval vs current, and drift."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/v5.2/esp32/api-reference/peripherals/touch_pad.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/sleep_modes.html
  - https://www.silabs.com/documents/public/application-notes/an0028-low-energy-sensor-interface-capacitive-sense.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capacitive touch wake-up

## How it works
A touch controller measures pad capacitance periodically without the CPU (ESP32 RTC touch FSM,
SiLabs LESENSE in EM2, Microchip PTC with event system, STM32 TSC needs the CPU running so it is
mostly for Sleep/LP-run). When a reading crosses a threshold, it wakes the core.

## ESP32 (IDF v5 legacy touch driver; new `touch_sens` driver on S3/P4 is similar)
```c
touch_pad_init();
touch_pad_set_fsm_mode(TOUCH_FSM_MODE_TIMER);
touch_pad_config(TOUCH_PAD_NUM8, 0);
touch_pad_filter_start(10);
uint16_t base; touch_pad_read_filtered(TOUCH_PAD_NUM8, &base);
touch_pad_set_thresh(TOUCH_PAD_NUM8, base * 2 / 3);    /* ESP32: value DROPS on touch */
esp_sleep_enable_touchpad_wakeup();
esp_deep_sleep_start();
```
On ESP32 the raw count decreases with touch; on S2/S3 it increases (threshold above baseline).
Measurement interval (`touch_pad_set_measurement_interval` / sleep cycle) trades response time for
current: deep sleep with touch wake is roughly 10-40 uA on ESP32 depending on interval.

## SiLabs LESENSE
Scans up to 16 channels in EM2 (~1-2 uA), compares against thresholds per channel, and wakes only
on a qualifying event; the CPU never runs for no-touch scans.

## Threshold calibration
- Measure baseline per pad at boot and after each wake; store in RTC memory for deep sleep.
- Threshold = baseline +/- (30-50% of the measured touch delta). Measure delta with the real
  overlay (glass/plastic thickness, enclosure) and a finger, not a bare pad.
- Track drift: humidity and temperature move the baseline. Recalibrate when idle (filtered
  baseline update, but not while touched).

## Gotchas
- Water films and condensation cause false touches; use guard/shield electrodes and require
  multi-sample confirmation after wake before acting.
- Long traces to pads add parasitic capacitance and reduce sensitivity; keep them short and away
  from noisy signals.
- Mains-powered phases (USB charger connected) inject noise; test with the device charging.
- On ESP32, touch pads share pins with strapping/ADC functions; GPIO0 (T1) is a strap pin.

## Verify
- [ ] Wake on touch through the final enclosure, no false wakes in a 12 h humid soak.
- [ ] Sleep current with touch wake enabled measured at the chosen interval.
