---
id: computing-software.firmware-embedded-development.zephyr.system-off-sys-poweroff
name: system-off-sys-poweroff
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [sys-poweroff, config-poweroff, system-off-wakeup, deep-sleep-reset, hwinfo-reset-cause, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Put a Zephyr device into its lowest-power system-off state with sys_poweroff: wake sources, preparing devices first, detecting the wake reset, and retaining data."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/sys/poweroff.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/hwinfo.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/boards/nordic/system_off/README.rst
  - https://docs.zephyrproject.org/latest/services/poweroff.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System off (sys_poweroff)

```
CONFIG_POWEROFF=y
```
```c
#include <zephyr/sys/poweroff.h>

void go_to_ship_mode(void)
{
    /* 1. configure wake source(s) */
    gpio_pin_configure_dt(&button, GPIO_INPUT);
    gpio_pin_interrupt_configure_dt(&button, GPIO_INT_LEVEL_ACTIVE);  /* nRF: sense for system-off wake */

    /* 2. quiesce peripherals that could draw current or hold the system awake */
    pm_device_action_run(sensor, PM_DEVICE_ACTION_SUSPEND);
    log_panic();                       /* flush logs */

    /* 3. off: never returns */
    sys_poweroff();
}
```
`sys_poweroff()` is `FUNC_NORETURN` and performs an immediate power off; the header makes the caller
responsible for putting the system in a safe state and for enabling any wake-up sources first. It needs
`CONFIG_POWEROFF`. The SoC port supplies `z_sys_poweroff()`. Whether RAM survives and how the device wakes
are SoC specific; expect wake to restart the application from reset, and check the SoC reference manual.

## Wake sources (SoC specific)
Which pins, timers or peripherals can wake the device from system off is defined by the SoC and its
Zephyr port; take the list from the SoC reference manual and the board or SoC documentation, and
configure them before calling `sys_poweroff()`. The Nordic "System Off" sample (nRF51 DK, nRF52 DK,
nRF54L15 DK) is the in-tree example of a button wake.

## Detecting the wake reset
```c
#include <zephyr/drivers/hwinfo.h>
uint32_t cause;
hwinfo_get_reset_cause(&cause);
if (cause & RESET_LOW_POWER_WAKE) { /* woke from system off */ }
hwinfo_clear_reset_cause();
```
`RESET_LOW_POWER_WAKE` is defined in `hwinfo.h` as "waking up from low power mode"; whether a given SoC
driver reports it for system-off wake is driver specific, so test it on the target.

## Keeping state
Assume RAM is lost unless the SoC documents otherwise. Options: the retention subsystem and retained-memory
drivers (the Nordic sample shows RAM retention in system off with `CONFIG_APP_USE_RETAINED_MEM=y`, keeping
the containing section powered), or flash/settings for non-volatile data. See the `retained-memory-and-boot-mode` skill.

## Verify
- [ ] Measured off current matches the SoC datasheet, measured as the datasheet specifies.
- [ ] Each configured wake source restarts the device; reset cause identifies it.

## Checked

Checked 2026-10-26 against Zephyr main on GitHub: `sys_poweroff()` signature, `FUNC_NORETURN`, `CONFIG_POWEROFF` and
the caller responsibilities from `include/zephyr/sys/poweroff.h`; `RESET_LOW_POWER_WAKE` in `hwinfo.h`; `pm_device_action_run()`,
`PM_DEVICE_ACTION_SUSPEND` and `log_panic()` exist; the Nordic system_off sample boards and `CONFIG_APP_USE_RETAINED_MEM`.
Removed the SoC wake-source table, the `wakeup-source` property claim, register-level retention details, the debugger caveat
and the current figure, which no Zephyr document confirms.

Method: documentation only; no commands were run.
