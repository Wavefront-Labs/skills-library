---
id: computing-software.firmware-embedded-development.zephyr.kernel-timers-k-timer
name: kernel-timers-k-timer
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [k-timer, k-timer-define, k-timer-start, k-timer-status-sync, isr-context-callback, periodic-timer, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use Zephyr k_timer for one-shot and periodic timing: ISR-context expiry functions, handing work to a workqueue, status sync for periodic threads, and tick rounding."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/timing/timers.html
  - https://docs.zephyrproject.org/latest/kernel/services/timing/clocks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel timers (k_timer)

## Define and start
```c
static void blink_expiry(struct k_timer *t);
static void blink_stop(struct k_timer *t);           /* optional, may be NULL */
K_TIMER_DEFINE(blink_timer, blink_expiry, blink_stop);

k_timer_start(&blink_timer, K_MSEC(100), K_MSEC(500));  /* first after 100 ms, then every 500 ms */
k_timer_start(&timeout,     K_SECONDS(5), K_NO_WAIT);   /* one-shot: period K_NO_WAIT */
k_timer_stop(&blink_timer);                              /* calls stop fn if running */
```
Runtime init: `k_timer_init(&t, expiry, stop)`. Restarting a running timer with `k_timer_start`
restarts it with the new duration and period (the "kick the timeout" idiom). The stop
function runs in the context of the thread that calls `k_timer_stop`.

## Expiry runs in ISR context
The expiry function runs from the system clock interrupt. No blocking, no mutexes, no
`k_sleep`, no logging at high rates. Do real work in a thread:
```c
static void sample_work_fn(struct k_work *w) { read_sensor_over_i2c(); }
K_WORK_DEFINE(sample_work, sample_work_fn);
static void sample_expiry(struct k_timer *t) { k_work_submit(&sample_work); }
```
Context per timer: `k_timer_user_data_set(&t, ptr)` and `k_timer_user_data_get(t)` in the callback.

## Status for synchronous use (no callback)
```c
K_TIMER_DEFINE(period_timer, NULL, NULL);
k_timer_start(&period_timer, K_MSEC(10), K_MSEC(10));
for (;;) {
    uint32_t n = k_timer_status_sync(&period_timer);  /* blocks until next expiry */
    if (n > 1) overruns += n - 1;                     /* expiries missed while busy */
    control_step();
}
```
`k_timer_status_get()` reads and resets the count without blocking. ISRs must not synchronise with
timers because they may not block.

## Timing precision
- Resolution is the system tick: `CONFIG_SYS_CLOCK_TICKS_PER_SEC` defaults to 10000 with
  `CONFIG_TICKLESS_KERNEL` and 100 otherwise (100 on QEMU and POSIX targets). Check your board's
  value before relying on 1 ms.
- Periodic timers do not drift against the system timer, but the interval between two expiries can
  be shorter or longer than the period. To guarantee a minimum delay, restart the timer from the
  expiry function or after it expired.
- `k_timer_remaining_get()` / `k_timer_remaining_ticks()` for "time left".
- For microsecond pulses use a counter or PWM driver, not k_timer.

## Verify
- [ ] No blocking calls in any expiry function (review, or enable `CONFIG_ASSERT`, which catches some).
- [ ] Period measured on a GPIO matches expectation at the board's tick rate.
- [ ] Overrun counts from `k_timer_status_sync` stay 0 under load.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Expiry function runs from the system clock interrupt, stop function semantics, restart behaviour, no-drift note and
  `k_timer_status_sync` example (doc: kernel/services/timing/timers; `kernel.h` comment on `stop_fn`).
- `CONFIG_SYS_CLOCK_TICKS_PER_SEC` defaults (`kernel/Kconfig`: 10000 if tickless, else 100, QEMU/POSIX 100).
- Removed: the `xTaskDelayUntil` comparison and the tickless power remark (no source).

Method: documentation only; no commands were run.
