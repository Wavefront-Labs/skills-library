---
id: computing-software.firmware-embedded-development.esp-idf.esp-timer-high-resolution
name: esp-timer-high-resolution
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-system, esp-timer, esp-timer-create, periodic-timer, microsecond-timing, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Schedule one-shot and periodic callbacks with ESP-IDF esp_timer at microsecond resolution, choose task vs ISR dispatch, and measure time with esp_timer_get_time."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/esp_timer.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_timer/include/esp_timer.h
  - https://github.com/espressif/esp-idf/blob/master/components/esp_timer/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# esp_timer high-resolution timers

`esp_timer` gives 64-bit microsecond time and software timers backed by one hardware timer.
Much finer resolution than FreeRTOS software timers (per the ESP Timer page).

## Timestamp
```c
int64_t t0 = esp_timer_get_time();     /* microseconds since boot (52 or 64 bit counter, chip-dependent) */
work();
ESP_LOGI(TAG, "took %lld us", esp_timer_get_time() - t0);
```

## Create timers
```c
static void blink_cb(void *arg) { gpio_set_level(LED, toggle ^= 1); }
esp_timer_handle_t t;
const esp_timer_create_args_t a = { .callback = blink_cb, .name = "blink",
                                    .dispatch_method = ESP_TIMER_TASK };
ESP_ERROR_CHECK(esp_timer_create(&a, &t));
ESP_ERROR_CHECK(esp_timer_start_periodic(t, 500 * 1000));   /* us */
/* esp_timer_start_once(t, 2000); esp_timer_stop(t); esp_timer_delete(t); */
```
`esp_timer_restart(t, timeout_us)` restarts a running timer with a new timeout (it returns
`ESP_ERR_INVALID_STATE` if the timer is not running); stop the timer or restart it before calling a
start function again.

## Dispatch
- `ESP_TIMER_TASK` (default): callbacks run in the high-priority `esp_timer` task, one after
  another. A slow callback delays every other timer. Keep callbacks short; hand off work.
- `ESP_TIMER_ISR` (`CONFIG_ESP_TIMER_SUPPORTS_ISR_DISPATCH_METHOD`): runs in the ISR for lower
  jitter; ISR rules apply (IRAM, no blocking, `*FromISR` APIs).
Task stack size: `CONFIG_ESP_TIMER_TASK_STACK_SIZE` (raise it on stack overflow in a callback).

## Light sleep
Automatic light sleep wakes the chip at the right time for a pending esp_timer callback. While
in light sleep the counter is suspended and advanced from the RTC timer on wake-up.
`.skip_unhandled_events = true` skips unhandled events in light sleep for periodic timers.

## Debug
```c
esp_timer_dump(stdout);      /* needs CONFIG_ESP_TIMER_PROFILING for statistics */
```

## Limits
- Resolution is one microsecond; for waveforms or bit banging use GPTimer, RMT or another
  dedicated peripheral, as the ESP Timer page recommends.
- Task-mode callbacks are serialized and can be delayed by higher-priority tasks.

## Verify
- [ ] Scope on a toggled GPIO shows expected period and jitter.
- [ ] `esp_timer_dump` shows no callback with excessive run time.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed: 1 us resolution and 52/64-bit range, ESP_TIMER_TASK vs ESP_TIMER_ISR dispatch and CONFIG_ESP_TIMER_SUPPORTS_ISR_DISPATCH_METHOD, serialized callbacks in the high-priority esp_timer task, skip_unhandled_events field meaning, esp_timer_restart / esp_timer_restart_at, esp_timer_dump, CONFIG_ESP_TIMER_PROFILING, CONFIG_ESP_TIMER_TASK_STACK_SIZE, light-sleep behaviour, GPTimer/RMT recommendation. Removed unconfirmed 50 us minimum period, jitter figures, FreeRTOS tick figures and the "IDF 5.x" gate for restart.
Method: documentation only; no commands were run.
