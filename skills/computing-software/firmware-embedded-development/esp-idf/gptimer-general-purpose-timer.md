---
id: computing-software.firmware-embedded-development.esp-idf.gptimer-general-purpose-timer
name: gptimer-general-purpose-timer
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-peripherals, gptimer, hardware-timer, timer-alarm-callback, gptimer-capture, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use ESP-IDF GPTimer for precise alarms and periodic interrupts: resolution, alarm config with auto-reload, ISR callbacks in IRAM, and replacing the legacy timer_group API."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/gptimer.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_gptimer/include/driver/gptimer.h
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_gptimer/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPTimer

The `esp_driver_gptimer` driver for the general-purpose hardware timers. Use it when esp_timer's
task-dispatched callbacks are too slow or jittery for the job.

## Periodic alarm
```c
#include "driver/gptimer.h"
static bool IRAM_ATTR on_alarm(gptimer_handle_t t, const gptimer_alarm_event_data_t *e, void *ctx)
{
    BaseType_t woken = pdFALSE;
    vTaskNotifyGiveFromISR((TaskHandle_t)ctx, &woken);
    return woken == pdTRUE;           /* request a context switch if a higher task woke */
}

gptimer_handle_t t;
gptimer_config_t cfg = { .clk_src = GPTIMER_CLK_SRC_DEFAULT, .direction = GPTIMER_COUNT_UP,
                         .resolution_hz = 1000000 };          /* 1 tick = 1 us */
ESP_ERROR_CHECK(gptimer_new_timer(&cfg, &t));
gptimer_alarm_config_t al = { .alarm_count = 1000, .reload_count = 0,
                              .flags.auto_reload_on_alarm = true };   /* 1 kHz */
ESP_ERROR_CHECK(gptimer_set_alarm_action(t, &al));
gptimer_event_callbacks_t cb = { .on_alarm = on_alarm };
ESP_ERROR_CHECK(gptimer_register_event_callbacks(t, &cb, xTaskGetCurrentTaskHandle()));
ESP_ERROR_CHECK(gptimer_enable(t));
ESP_ERROR_CHECK(gptimer_start(t));
```
State machine: new -> enable -> start/stop -> disable -> delete. Calling in the wrong state
returns `ESP_ERR_INVALID_STATE`.

## One-shot and dynamic alarms
Without auto-reload, update the alarm inside the callback:
```c
gptimer_alarm_config_t next = { .alarm_count = e->alarm_value + period };
gptimer_set_alarm_action(t, &next);
```

## Measuring
`gptimer_get_raw_count(t, &v)` reads the counter; `gptimer_get_captured_count` reads a captured value
(documented as callable from ISR context).

## ISR safety
- With `CONFIG_GPTIMER_ISR_CACHE_SAFE=y` the interrupt keeps running while the cache is disabled (for example
  during flash writes); then all callbacks and their context data must be in internal memory.
- Keep it short; hand work to a task.
- `CONFIG_GPTIMER_ISR_HANDLER_IN_IRAM` places the driver's handler in IRAM, but the user callback and its
  context may still be in flash unless you place them in internal RAM (for example with `IRAM_ATTR`);
  `CONFIG_GPTIMER_CTRL_FUNC_IN_IRAM` does the same for control functions called from ISR.

## Power management
With `CONFIG_PM_ENABLE` the system may adjust or stop the clock source in sleep; the driver creates a power
management lock internally and holds it from `gptimer_enable` until `gptimer_disable`. Disable the timer when idle
to allow sleep (this stops the timer). `allow_pd` in the config lets the peripheral power down in sleep.

## Verify
- [ ] Scope on a GPIO toggled from the task shows period and jitter in spec.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in peripherals/gptimer.rst, gptimer.h and the driver Kconfig: gptimer_new_timer / set_alarm_action / register_event_callbacks / enable / start flow, alarm_count, reload_count and auto_reload_on_alarm semantics, next-alarm pattern using alarm_value, gptimer_get_captured_count, Kconfig names GPTIMER_ISR_CACHE_SAFE, GPTIMER_ISR_HANDLER_IN_IRAM, GPTIMER_CTRL_FUNC_IN_IRAM, internal PM lock between enable and disable. Fixed: CONFIG_GPTIMER_ISR_IRAM_SAFE is not a current option (now ISR_CACHE_SAFE). Removed the unconfirmed jitter figure and the legacy-driver check.

Method: documentation only; no commands were run.
