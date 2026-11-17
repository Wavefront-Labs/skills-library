---
id: computing-software.firmware-embedded-development.zephyr.delayable-work-items
name: delayable-work-items
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [k-work-delayable, k-work-schedule, k-work-reschedule, k-work-cancel-delayable-sync, debounce, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Schedule deferred work in Zephyr with k_work_delayable: schedule vs reschedule semantics for timeouts and debouncing, cancellation races, and the _sync variants."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/threads/workqueue.html#delayable-work
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/kernel.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delayable work items

```c
static void blink_off(struct k_work *work)
{
    struct k_work_delayable *dw = k_work_delayable_from_work(work);
    struct led_ctx *ctx = CONTAINER_OF(dw, struct led_ctx, off_work);
    gpio_pin_set_dt(&ctx->led, 0);
}

struct led_ctx { struct gpio_dt_spec led; struct k_work_delayable off_work; };
static struct led_ctx ctx = { .led = GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios) };

void init(void) { k_work_init_delayable(&ctx.off_work, blink_off); }
/* or statically: K_WORK_DELAYABLE_DEFINE(off_work, blink_off); */
```

## schedule vs reschedule
| Call | If already scheduled (pending timeout) |
|---|---|
| `k_work_schedule(&dw, delay)` | **no-op** (returns 0), even if `delay` is `K_NO_WAIT` |
| `k_work_reschedule(&dw, delay)` | can change the deadline: restarts with the new delay |

- Timeout/inactivity timer ("turn backlight off 5 s after the last key"): `k_work_reschedule` on
  every key press.
- Debounce a button: in the GPIO ISR call `k_work_reschedule(&debounce, K_MSEC(20))`; the handler
  reads the pin once the bouncing stops.
- Rate limit ("at most once per 100 ms"): `k_work_schedule` so repeated triggers don't push it out.
- With `K_NO_WAIT` and the work not pending, `k_work_schedule` is equivalent to submitting the
  work directly (`k_work_submit_to_queue`).

`k_work_schedule`, `k_work_reschedule` and `k_work_cancel_delayable` are documented as ISR-safe.
Use `k_work_schedule_for_queue` / `k_work_reschedule_for_queue` to target a dedicated work queue
instead of the system one.

## Cancel
```c
k_work_cancel_delayable(&dw);                 /* async: handler may still be running */

struct k_work_sync sync;
k_work_cancel_delayable_sync(&dw, &sync);     /* waits for a running handler to finish */
```
Use the `_sync` form (from a thread, never an ISR) before freeing the containing object or
powering down the peripheral the handler uses; the `struct k_work_sync` must persist until the
call returns. `k_work_flush_delayable(&dw, &sync)` waits for the item to complete instead of
cancelling it. Cancelling does not prevent rescheduling.

## State queries
`k_work_delayable_is_pending(&dw)`, `k_work_delayable_remaining_get(&dw)` (returns `k_ticks_t`),
`k_work_delayable_busy_get(&dw)` for the state flags.

## Gotchas
- A handler that reschedules itself is a periodic job.
- Handlers run on the work queue thread: blocking there delays every other item on that queue.
- A pending work item must not be altered, and must not be re-initialised while busy; init once.

## Verify
- [ ] Each delayable item's trigger uses the intended schedule/reschedule semantics.
- [ ] Objects containing work items are only freed after `_cancel_delayable_sync`.

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/kernel/services/threads/workqueue.rst and include/zephyr/kernel.h.
Confirmed: `k_work_init_delayable`, `K_WORK_DELAYABLE_DEFINE`, `k_work_delayable_from_work` with `CONTAINER_OF`; `k_work_schedule` is a no-op if already scheduled or submitted, `k_work_reschedule` can change the deadline; `_for_queue` variants; `k_work_cancel_delayable`, `k_work_cancel_delayable_sync` and `k_work_flush_delayable` signatures and semantics; `k_work_delayable_is_pending`, `_remaining_get`, `_busy_get`; ISR-safety marks (`@isr_ok`) on schedule, reschedule and cancel; the rule against altering or re-initialising a busy item.

Method: documentation only; no commands were run.
