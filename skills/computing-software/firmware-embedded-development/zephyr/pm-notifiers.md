---
id: computing-software.firmware-embedded-development.zephyr.pm-notifiers
name: pm-notifiers
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [pm-notifier, pm-notifier-register, state-entry, state-exit, sleep-hooks, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Run code when Zephyr enters or leaves a system power state with pm_notifier callbacks: what context they run in, timing limits, and typical uses like debug pins."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/pm/pm.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/pm/pm.c
  - https://docs.zephyrproject.org/latest/services/pm/system.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PM notifiers

```c
#include <zephyr/pm/pm.h>

static void on_entry(enum pm_state state)
{
    if (state >= PM_STATE_SUSPEND_TO_IDLE) {
        gpio_pin_set_raw(dbg_port, DBG_PIN, 0);    /* scope marker: entering sleep */
    }
}

static void on_exit(enum pm_state state)
{
    gpio_pin_set_raw(dbg_port, DBG_PIN, 1);        /* awake */
}

static struct pm_notifier notifier = {
    .state_entry = on_entry,
    .state_exit  = on_exit,
};   /* report_substate defaults to false */

void app_pm_init(void) { pm_notifier_register(&notifier); }
```
`pm_notifier_unregister(&notifier)` removes it (returns 0 on success, negative errno on failure).
Several notifiers can be registered; they are appended to a list and called in registration order.
To receive the substate id too, set `.substate_entry`/`.substate_exit` and `.report_substate = true`
(the callbacks share a union with the plain pair).

## Context and limits
- The callbacks run from the PM core's suspend/resume path, under a spinlock that also guards
  the notifier list; the header says they can be called from the ISR of the event that ended idle.
  Keep them short and non-blocking, and never call `pm_notifier_register()` or
  `pm_notifier_unregister()` from inside a callback (the header forbids it).
- Entry runs just before `pm_state_set()`; exit runs after `pm_state_exit_post_ops()` and before
  the system-clock idle-exit accounting.
- The header describes the entry callback as firing on a transition from `PM_STATE_ACTIVE` to
  another state and the exit callback on the way back, and warns that this may change.
- Execution time adds directly to entry/exit latency; keep it to register writes.
- `sys_poweroff()` is a separate API; no notifier call is documented for it.

## Typical uses
- GPIO markers to measure sleep duration and wake latency with a scope or power analyser.
- Gating an external component that has no Zephyr driver (e.g. turn off a level shifter).
- Counting sleep entries per state when `CONFIG_PM_STATS` isn't available.
- Saving/restoring a peripheral that the SoC loses in a deep state and that has no device PM.

## Prefer instead
- Per-device sleep handling: device PM actions (`PM_DEVICE_ACTION_SUSPEND`) and
  `CONFIG_PM_DEVICE_SYSTEM_MANAGED`, which suspend devices before system sleep.
- Preventing sleep: `pm_policy_state_lock_get`, not a notifier.

## Verify
- [ ] Notifier code is non-blocking and short (scope shows microseconds).
- [ ] Debug-pin traces match PM stats counts.

## Checked

Checked 2026-10-26 against Zephyr main (headers and subsys/pm/pm.c on GitHub): `struct pm_notifier`
fields including `report_substate` and the substate callbacks, `pm_notifier_unregister()` return value, the
registration-order list, the ISR and no-(un)register-in-callback notes, and the order of notification
relative to `pm_state_set()` and `pm_state_exit_post_ops()`. `CONFIG_PM_DEVICE_SYSTEM_MANAGED` and
`pm_policy_state_lock_get()` exist. Removed the unconfirmed claims that callbacks run with interrupts locked
and that WFI idle never notifies, and the `exit-latency-us` advice.

Method: documentation only; no commands were run.
