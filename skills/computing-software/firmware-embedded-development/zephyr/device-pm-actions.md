---
id: computing-software.firmware-embedded-development.zephyr.device-pm-actions
name: device-pm-actions
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [pm-device-action, pm-device-dt-define, pm-device-action-run, pm-device-runtime-get, power-domains, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Implement and use Zephyr device power management: the pm action callback (suspend, resume, turn on/off), PM_DEVICE_DT_DEFINE, manual actions, runtime PM, and power domains."
sources:
  - https://docs.zephyrproject.org/latest/services/pm/device.html
  - https://docs.zephyrproject.org/latest/services/pm/device_runtime.html
  - https://docs.zephyrproject.org/latest/services/pm/power_domain.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/pm/device.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Device PM actions

```
CONFIG_PM_DEVICE=y
CONFIG_PM_DEVICE_RUNTIME=y      # optional, reference-counted
```

## Driver side
```c
#include <zephyr/pm/device.h>

static int widget_pm_action(const struct device *dev, enum pm_device_action action)
{
    const struct widget_cfg *cfg = dev->config;
    switch (action) {
    case PM_DEVICE_ACTION_SUSPEND:
        widget_write(cfg, REG_CTRL, CTRL_SLEEP);
        return pinctrl_apply_state(cfg->pcfg, PINCTRL_STATE_SLEEP);
    case PM_DEVICE_ACTION_RESUME:
        pinctrl_apply_state(cfg->pcfg, PINCTRL_STATE_DEFAULT);
        return widget_write(cfg, REG_CTRL, CTRL_RUN);
    case PM_DEVICE_ACTION_TURN_OFF:      /* power removed by a domain */
        return 0;
    case PM_DEVICE_ACTION_TURN_ON:       /* power restored: registers lost, re-init */
        return widget_reinit(dev);
    default:
        return -ENOTSUP;
    }
}

#define WIDGET_INIT(n)                                                        \
    PM_DEVICE_DT_INST_DEFINE(n, widget_pm_action);                            \
    DEVICE_DT_INST_DEFINE(n, widget_init, PM_DEVICE_DT_INST_GET(n),           \
                          &widget_data_##n, &widget_cfg_##n,                  \
                          POST_KERNEL, CONFIG_SENSOR_INIT_PRIORITY, &widget_api);
DT_INST_FOREACH_STATUS_OKAY(WIDGET_INIT)
```
In init, `pm_device_driver_init(dev, widget_pm_action)` moves the device to its initial state: with
`CONFIG_PM_DEVICE` off it issues `TURN_ON` then `RESUME`. To use runtime PM, the driver calls
`pm_device_runtime_enable(dev)` at init time, which suspends the device if it is active; if the
device is physically suspended, call `pm_device_init_suspended(dev)` first.

## Application side
Manual:
```c
pm_device_action_run(dev, PM_DEVICE_ACTION_SUSPEND);
pm_device_action_run(dev, PM_DEVICE_ACTION_RESUME);
enum pm_device_state st; pm_device_state_get(dev, &st);
```
Runtime (reference counted, preferred when several users share a device):
```c
pm_device_runtime_get(dev);     /* resumes the device */
use(dev);
pm_device_runtime_put(dev);     /* suspends it when no longer used; _put_async schedules the suspend */
```
Runtime PM is enabled globally with `CONFIG_PM_DEVICE_RUNTIME_DEFAULT_ENABLE`, or per device with
`zephyr,pm-device-runtime-auto;` on the node (then `pm_device_runtime_enable()` is called right
after a successful init) or by calling `pm_device_runtime_enable()`. Suspend operations run on
the system work queue by default and must not block;
`CONFIG_PM_DEVICE_RUNTIME_USE_DEDICATED_WQ` selects a dedicated one.

## Power domains
```dts
sensor_pd: power-domain {
    compatible = "power-domain-gpio";
    enable-gpios = <&gpio0 3 GPIO_ACTIVE_HIGH>;
    startup-delay-us = <1000>;
    #power-domain-cells = <0>;
};
&widget0 { power-domains = <&sensor_pd>; };
```
When the domain turns off, its devices get `TURN_OFF`; on power-up, `TURN_ON`.

## Busy and system PM
`pm_device_busy_set(dev)` during a transfer prevents system PM from suspending it (with
`CONFIG_PM_DEVICE_SYSTEM_MANAGED`). Devices that must stay on across system sleep:
`wakeup-source` in DT plus `pm_device_wakeup_enable(dev, true)`.

## Gotchas
- The action callback type documents `-ENOTSUP` for an unsupported action (and
  `pm_device_driver_init` tolerates `-ENOTSUP` for `TURN_ON`); don't return 0 for actions you
  didn't handle.
- Resume must restore everything suspend changed (pins, clocks, registers).
- PM actions can only be called from ISRs for a device defined with the `PM_DEVICE_ISR_SAFE` flag
  (an optional last argument of the `PM_DEVICE_*_DEFINE` macros).

## Verify
- [ ] `pm_device_state_get` shows SUSPENDED when idle and ACTIVE in use.
- [ ] Current drops by the expected amount when suspended (power analyser).

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/services/pm/device.rst, device_runtime.rst, power_domain.rst, include/zephyr/pm/device.h and dts/bindings/power-domain/power-domain-gpio.yaml.
Confirmed: `PM_DEVICE_ACTION_SUSPEND/RESUME/TURN_OFF/TURN_ON` semantics; `PM_DEVICE_DT_INST_DEFINE` and `PM_DEVICE_DT_INST_GET`; `pm_device_driver_init`; `pm_device_runtime_enable`, `pm_device_init_suspended`, `pm_device_runtime_get/put/put_async`; `zephyr,pm-device-runtime-auto`; `CONFIG_PM_DEVICE_SYSTEM_MANAGED` with `pm_device_busy_set`; `wakeup-source` and `pm_device_wakeup_enable`; the `power-domain-gpio` compatible with `enable-gpios`, `startup-delay-us` and `#power-domain-cells`; `power-domains` property; `TURN_OFF`/`TURN_ON` delivered on domain power changes; `PM_DEVICE_ISR_SAFE`.

Method: documentation only; no commands were run.
