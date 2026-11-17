---
id: computing-software.firmware-embedded-development.esp-idf.touch-sensor
name: touch-sensor
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-peripherals, esp-touch-sensor, capacitive-touch, touch-pad, touch-threshold, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Implement capacitive touch buttons on ESP32, S2 and S3 with the ESP-IDF touch sensor driver: controller and channels, filtering, thresholds, waterproofing and wake from sleep."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/cap_touch_sens.rst
  - https://github.com/espressif/esp-idf/blob/master/components/driver/touch_sensor/esp32s3/include/driver/touch_sensor.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Touch sensor

The capacitive touch peripheral exists on ESP32 (version 1), ESP32-S2 and S3 (version 2) and ESP32-P4 (version 3);
the guide's version table does not list C3 or C6. The legacy `driver/touch_pad.h` API is deprecated (its header warns
and points to a Kconfig option to suppress the warning); the current driver is `driver/touch_sens.h`.

## Setup (current API)
```c
touch_sensor_handle_t sens;
touch_sensor_sample_config_t sample[1] = { /* TOUCH_SENSOR_Vn_DEFAULT_SAMPLE_CONFIG(...) for your chip */ };
touch_sensor_config_t cfg = TOUCH_SENSOR_DEFAULT_BASIC_CONFIG(1, sample);
ESP_ERROR_CHECK(touch_sensor_new_controller(&cfg, &sens));

touch_channel_handle_t chan;
touch_channel_config_t cc = { /* per-channel thresholds, see touch_channel_config_t */ };
ESP_ERROR_CHECK(touch_sensor_new_channel(sens, 1 /* channel id */, &cc, &chan));

touch_event_callbacks_t cbs = { .on_active = on_active_cb, .on_inactive = on_inactive_cb };
ESP_ERROR_CHECK(touch_sensor_register_callbacks(sens, &cbs, NULL));
ESP_ERROR_CHECK(touch_sensor_enable(sens));
ESP_ERROR_CHECK(touch_sensor_start_continuous_scanning(sens));   /* or touch_sensor_trigger_oneshot_scanning */
```
Configure filters with `touch_sensor_config_filter` before enabling; read benchmark, smooth or raw data with
`touch_channel_read_data(chan, TOUCH_CHAN_DATA_TYPE_SMOOTH, ...)`. Delete channels before the controller
(`touch_sensor_del_channel`, then `touch_sensor_del_controller`).

## Direction
On ESP32 (version 1) the channel value decreases when touched; on S2 and S3 (version 2) it increases.
On version 2 a channel is active when its data exceeds the benchmark plus `active_threshold`, and the driver then
calls `on_active`.

## Tuning
- Log raw and smoothed values for every pad under real conditions (enclosure, overlay, powered versus battery).
  Choose thresholds from the measured touch delta, not a magic number.
- The benchmark normally tracks slow drift itself; `touch_channel_config_benchmark` can force a reset to the current
  smooth value.

## Waterproofing (chips with waterproof support, such as S2 and S3)
`touch_sensor_config_waterproof` takes a `guard_chan` (a ring around the pads, detects immersion) and a `shield_chan`
(a grid over the panel, detects moisture). Pass NULL to deregister.

## Wake from sleep
Chips with sleep wake-up support register it with `touch_sensor_config_sleep_wakeup`; set `slp_wakeup_lvl` to
`TOUCH_LIGHT_SLEEP_WAKEUP` for light sleep (any registered channel can wake) or `TOUCH_DEEP_SLEEP_WAKEUP` for deep
sleep where documented for the chip. Check the chip's section of the guide for the supported combinations.

## Hardware rules
Follow the Espressif touch sensor application note (linked from the guide) for pad shape, traces and shielding.

## Verify
- [ ] Measure the touch and no-touch values across temperature and supply variation and set the threshold between them with margin.
- [ ] No false triggers with water spray (if waterproofing is required).

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in peripherals/cap_touch_sens.rst and the legacy touch headers: sensor versions per chip and the direction of the value change, the controller and channel API names, filter / benchmark / waterproof / sleep wake-up APIs, the on_active rule (data above benchmark plus active_threshold on V2), deprecation of the legacy touch_pad API. Fixed: the legacy driver/touch_pad.h example is deprecated (its header warns) so the skill now uses the current controller API; removed the unconfirmed 2% threshold, overlay thickness, resistor value and 3x margin figures and the IDF version claim.

Method: documentation only; no commands were run.
