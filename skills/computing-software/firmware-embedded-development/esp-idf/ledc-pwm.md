---
id: computing-software.firmware-embedded-development.esp-idf.ledc-pwm
name: ledc-pwm
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-peripherals, ledc, pwm, duty-resolution, ledc-fade, servo-pwm, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Generate PWM on ESP32 with the LEDC peripheral: timer/channel setup, the frequency vs resolution trade-off, hardware fades, servo timing, and thread-safe duty updates."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/ledc.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_ledc/include/driver/ledc.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LEDC PWM

LEDC has timers (frequency + resolution) and channels (pin + duty) that pick a timer. Despite
the name it's the general PWM peripheral for LEDs, fans, buzzers and servos. (MCPWM is for
motor control with dead time and sync.)

## Setup
```c
#include "driver/ledc.h"
ledc_timer_config_t t = {
    .speed_mode      = LEDC_LOW_SPEED_MODE,     /* only original ESP32 has HIGH_SPEED */
    .duty_resolution = LEDC_TIMER_13_BIT,
    .timer_num       = LEDC_TIMER_0,
    .freq_hz         = 5000,
    .clk_cfg         = LEDC_AUTO_CLK,
};
ESP_ERROR_CHECK(ledc_timer_config(&t));

ledc_channel_config_t c = {
    .gpio_num = GPIO_NUM_5, .speed_mode = LEDC_LOW_SPEED_MODE,
    .channel = LEDC_CHANNEL_0, .timer_sel = LEDC_TIMER_0,
    .duty = 0, .hpoint = 0,
};
ESP_ERROR_CHECK(ledc_channel_config(&c));

ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, 4096);    /* of 8191 at 13-bit */
ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);       /* takes effect next period */
```

## Frequency vs resolution
The frequency and duty resolution are interdependent and the source clock limits the maximum frequency.
Values below assume an 80 MHz source clock (`freq_hz x 2^resolution <= source clock`):
| Frequency | Max resolution |
|---|---|
| 1 kHz | 16 bits (65.5 MHz) |
| 5 kHz | 13 bits (41 MHz) |
| 20 kHz (silent fans, motors) | 11 bits (41 MHz) |
| 40 MHz | 1 bit (fixed 50% duty, per the guide) |
`ledc_timer_config` logs "requested frequency and duty resolution cannot be achieved, try reducing freq_hz or
duty_resolution" and fails when you ask for too much. `ledc_find_suitable_duty_resolution()` computes the maximum.

## Hardware fades
```c
ledc_fade_func_install(0);
ledc_set_fade_with_time(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, 8191, 1000);   /* to full in 1 s */
ledc_fade_start(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, LEDC_FADE_NO_WAIT);
```
Use `ledc_cb_register` (after installing the fade service) for a fade-end callback. On ESP32 the hardware does not
support a duty change while a fade is running on that channel.

## Thread safety
`ledc_set_duty` + `ledc_update_duty` is two calls, and the header says `ledc_set_duty`, `ledc_set_duty_with_hpoint`
and `ledc_update_duty` are not thread-safe for one channel across tasks. `ledc_set_duty_and_update()` is the thread-safe version.

## Servos
50 Hz; take the pulse-width range from the servo datasheet. With 14-bit resolution
one step is 20 ms / 16384 = 1.22 us, enough for smooth positioning:
```c
uint32_t duty = (pulse_us * 16384) / 20000;
```

## Gotchas
- Channels sharing a timer share frequency; use separate timers for different frequencies.
- The LEDC driver does not take a power-management lock. Sleep behaviour is set per channel with
  `ledc_channel_config_t::sleep_mode`: the default `LEDC_SLEEP_MODE_NO_ALIVE_NO_PD` gives no output in light sleep;
  `LEDC_SLEEP_MODE_KEEP_ALIVE` keeps PWM running if the timer clock source is light-sleep compatible (for
  example `LEDC_USE_RC_FAST_CLK`), at higher sleep power.
- Inverting output: `.flags.output_invert = 1` in the channel config.
- Duty values range from 0 to `2^res`, but when the timer uses its maximum duty resolution the duty cannot be set
  to `2^res` (the hardware counter overflows); use `2^res - 1` there.

## Verify
- [ ] Scope confirms frequency and duty at 0%, 50% and 100%.
- [ ] No audible whine (frequency above 20 kHz for motors/fans if needed).
- [ ] Concurrent duty updates from two tasks use the thread-safe call.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in peripherals/ledc.rst and ledc.h: speed modes (high speed only on ESP32), 5 kHz at 13 bits and 40 MHz at 1 bit examples, the error text, ledc_find_suitable_duty_resolution, fade API and fade callback, thread-safety note and ledc_set_duty_and_update, output_invert flag, sleep_mode options and the absence of a PM lock, duty 2^res restriction. Fixed: the PM-lock advice was wrong, the 'only with fade installed' qualifier on the thread-safe call was unconfirmed and removed, the servo pulse range claim removed.

Method: documentation only; no commands were run.
