---
id: computing-software.firmware-embedded-development.zephyr.deferred-device-initialisation
name: deferred-device-initialisation
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [device-deferred-init, zephyr-deferred-init, device-init, init-priority, power-sequenced-devices, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Delay a Zephyr device's init until the application calls device_init(), using the zephyr,deferred-init devicetree property, for devices that need power or detection first."
sources:
  - https://docs.zephyrproject.org/latest/kernel/drivers/index.html#deferred-initialization
  - https://docs.zephyrproject.org/latest/kernel/drivers/index.html#initialization-levels
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/device.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/base/base.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deferred device initialisation

By default every enabled device's init function runs at boot (in `PRE_KERNEL_1`,
`PRE_KERNEL_2`, `POST_KERNEL` order by priority). Some devices can't be initialised then:
- powered by a rail the application turns on later,
- on an optional plug-in board detected at runtime,
- needing a slow external component to boot (modem, sensor with long start-up).

If their init fails at boot, the device stays "not ready" until something initialises it again.

## Mark the node
```dts
&i2c1 {
    pressure: lps22hh@5c {
        compatible = "st,lps22hh";
        reg = <0x5c>;
        zephyr,deferred-init;
    };
};
```

## Initialise later
```c
static const struct device *const prs = DEVICE_DT_GET(DT_NODELABEL(pressure));

void sensors_power_on(void)
{
    regulator_enable(vdd_sens);
    k_msleep(5);                      /* datasheet power-up time */
    int rc = device_init(prs);        /* runs the driver's init function now */
    if (rc) LOG_ERR("pressure init: %d", rc);
}
```
- `device_init()` returns 0 on success, `-EALREADY` if the device is already initialised, or the
  `-errno` returned by the init function. After success, `device_is_ready()` is true.
- It can also be called again for a device whose initialisation failed, or that was
  de-initialised.
- Before init, the device must not be used; check `device_is_ready()` in code paths that may run
  first.

## Alternatives
| Situation | Better tool |
|---|---|
| Power off/on cycles at runtime | device PM (`pm_device_action_run`, runtime PM) with a power domain |
| Order issue between two boot-time devices | init level and priority (`PRE_KERNEL_1`, `PRE_KERNEL_2`, `POST_KERNEL` plus a numeric priority; per-driver Kconfig such as `CONFIG_SENSOR_INIT_PRIORITY`) |

`device_deinit()` exists but returns `-ENOTSUP` unless `CONFIG_DEVICE_DEINIT_SUPPORT` is enabled and
the driver supports de-initialisation. For repeated power cycling, use PM actions
(`TURN_ON`/`RESUME`).

## Gotchas
- `zephyr,deferred-init` appeared in Zephyr 3.7; older releases lack the property.

## Verify
- [ ] Node has `zephyr,deferred-init;` and `device_is_ready()` is false until `device_init()`.
- [ ] Init after power-up succeeds reliably across cold boots.

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/kernel/drivers/index.rst, include/zephyr/device.h, dts/bindings/base/base.yaml and the 3.7 release notes.
Confirmed: the `zephyr,deferred-init` property and its meaning; `device_init()` return values (0, `-EALREADY`, `-errno`) and re-initialisation of failed or de-initialised devices; `device_deinit()` and `CONFIG_DEVICE_DEINIT_SUPPORT`; init levels `PRE_KERNEL_1`, `PRE_KERNEL_2`, `POST_KERNEL`; `CONFIG_SENSOR_INIT_PRIORITY` exists; the property was introduced in 3.7 (release notes).

Method: documentation only; no commands were run.
