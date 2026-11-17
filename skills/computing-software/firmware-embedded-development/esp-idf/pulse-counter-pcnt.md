---
id: computing-software.firmware-embedded-development.esp-idf.pulse-counter-pcnt
name: pulse-counter-pcnt
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-peripherals, pcnt, pulse-counter, quadrature-encoder, glitch-filter, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Count pulses and decode quadrature encoders with the ESP-IDF PCNT driver: units and channels, edge/level actions, glitch filter, watch points and overflow accumulation."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/pcnt.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_pcnt/include/driver/pulse_cnt.h
  - https://github.com/espressif/esp-idf/blob/master/examples/peripherals/pcnt/rotary_encoder/main/rotary_encoder_example_main.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pulse counter (PCNT)

Hardware counting with no CPU per pulse: flow meters, anemometers, encoders. Not every chip has a PCNT
peripheral; check the chip's PCNT support before choosing it.

## Quadrature encoder (x4)
```c
#include "driver/pulse_cnt.h"
pcnt_unit_config_t uc = { .low_limit = -1000, .high_limit = 1000,
                          .flags.accum_count = true };       /* keep counting across overflow */
pcnt_unit_handle_t u; ESP_ERROR_CHECK(pcnt_new_unit(&uc, &u));
pcnt_glitch_filter_config_t gf = { .max_glitch_ns = 1000 };
ESP_ERROR_CHECK(pcnt_unit_set_glitch_filter(u, &gf));

pcnt_chan_config_t a = { .edge_gpio_num = 4, .level_gpio_num = 5 };
pcnt_chan_config_t b = { .edge_gpio_num = 5, .level_gpio_num = 4 };
pcnt_channel_handle_t ca, cb;
pcnt_new_channel(u, &a, &ca); pcnt_new_channel(u, &b, &cb);
pcnt_channel_set_edge_action(ca, PCNT_CHANNEL_EDGE_ACTION_DECREASE, PCNT_CHANNEL_EDGE_ACTION_INCREASE);
pcnt_channel_set_level_action(ca, PCNT_CHANNEL_LEVEL_ACTION_KEEP, PCNT_CHANNEL_LEVEL_ACTION_INVERSE);
pcnt_channel_set_edge_action(cb, PCNT_CHANNEL_EDGE_ACTION_INCREASE, PCNT_CHANNEL_EDGE_ACTION_DECREASE);
pcnt_channel_set_level_action(cb, PCNT_CHANNEL_LEVEL_ACTION_KEEP, PCNT_CHANNEL_LEVEL_ACTION_INVERSE);
pcnt_unit_add_watch_point(u, 1000); pcnt_unit_add_watch_point(u, -1000);   /* needed for accum */
pcnt_unit_enable(u); pcnt_unit_clear_count(u); pcnt_unit_start(u);

int pos; pcnt_unit_get_count(u, &pos);
```
`accum_count` extends the counter's width (16 bits by default in hardware); the documented recipe is to enable it and
add the high and low limits as watch points, after which `pcnt_unit_get_count` includes the overflow loss.

## Frequency measurement
Count edges on one channel; read and clear every gate period from a GPTimer or esp_timer:
f = count / gate time. For low frequencies, measure period instead (MCPWM capture or RMT RX).

## Glitch filter
Pulses narrower than `max_glitch_ns` are ignored. The filter runs on the APB clock, so the maximum glitch width
should be longer than one APB cycle (12.5 ns at 80 MHz); with power management enabled the APB frequency can
change before light sleep and the filter may misread valid signals. Mechanical contacts need RC filtering or
software debouncing.

## Watch point events
Register a watch-point callback (`pcnt_unit_register_event_callbacks`, `on_reach`) to trigger at a count (for example
every 100 litres) without polling. After adding a watch point on chips without runtime threshold update, call
`pcnt_unit_clear_count` for it to take effect.

## Verify
- [ ] Encoder turned one full revolution reads counts-per-rev x 4.
- [ ] Count correct beyond +/-32767 (accumulation works).
- [ ] Function generator test at max expected frequency: no lost counts.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in peripherals/pcnt.rst, pulse_cnt.h and the IDF rotary_encoder example: encoder channel and action setup (channel A edge/level swapped for B, identical action pairs), accum_count and the watch-point recipe, 16-bit default width, glitch filter behaviour and APB note, watch points and callbacks. Removed: the chip availability list, the 1023-cycle glitch limit and the 12.8 us figure (not in the guide), and the claim that the count is signed 16-bit hardware.

Method: documentation only; no commands were run.
