---
id: computing-software.firmware-embedded-development.zephyr.driver-model-and-device-api
name: driver-model-and-device-api
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr, device-driver-model, device-api, device-get-binding, device-is-ready, dt-inst, sensor-driver, syscall, device-pm, init-level, device-defer-init, zephyr-sensor-api, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write a Zephyr driver that fits the device model: DEVICE_DT_INST_DEFINE, device_is_ready, init levels and priority, device PM hooks and subsystem API tables."
sources:
  - https://docs.zephyrproject.org/latest/kernel/drivers/index.html
  - https://docs.zephyrproject.org/latest/services/pm/device.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zephyr driver model and device API

**Goal:** write a driver that fits Zephyr's device model correctly, so it
composes with devicetree configuration and other drivers instead of fighting
the framework — builds directly on
`computing-software.firmware-embedded-development.zephyr.devicetree-and-kconfig`'s
devicetree/Kconfig basics, applied to writing the driver itself rather than
just configuring an existing one.

## Defining a device instance
```c
#define DT_DRV_COMPAT vnd_mysensor
static int mysensor_init(const struct device *dev) { ... }
static const struct mysensor_config mysensor_cfg_0 = {
  .i2c = I2C_DT_SPEC_GET(DT_DRV_INST(0)),
};
static struct mysensor_data mysensor_data_0;
DEVICE_DT_INST_DEFINE(0, mysensor_init, NULL,
                       &mysensor_data_0, &mysensor_cfg_0,
                       POST_KERNEL, CONFIG_SENSOR_INIT_PRIORITY,
                       &mysensor_api);
```
`DEVICE_DT_INST_DEFINE` wires a devicetree node instance to a concrete device
object; `I2C_DT_SPEC_GET` pulls the bus handle and address straight from the
devicetree node (no hardcoded address in C) — this is why
`computing-software.firmware-embedded-development.zephyr.devicetree-and-kconfig`'s
overlay work has to happen first: the driver literally cannot be instantiated
without a matching devicetree node declaring it.

## `device_is_ready()` — don't skip it
A `const struct device *dev = DEVICE_DT_GET(...)` pointer is non-NULL even if
the device's `init` function failed or hasn't run yet depending on init
ordering — `device_is_ready(dev)` is the actual check that initialization
succeeded. Code that uses a device pointer without checking this can call
into an uninitialized driver and either hit undefined behavior or a confusing
downstream failure far from the real cause. Call it once at application
startup for every device the app depends on, not scattered defensively before
every single call.

## Init levels and priority — ordering that matters
`PRE_KERNEL_1`, `PRE_KERNEL_2` and `POST_KERNEL` are the three levels the driver documentation lists
for drivers (`include/zephyr/init.h` also defines `EARLY`, `APPLICATION` and `SMP` for
other init hooks); they define coarse
phases devices initialize in; within a level, `CONFIG_..._INIT_PRIORITY`
(a small integer) orders devices relative to each other. A driver depending
on another device (e.g. a sensor driver depending on the I2C bus controller
being initialized first) must be at an equal-or-later level/priority than its
dependency — getting this backward means the dependent driver's `init`
function runs against a bus controller that hasn't initialized yet, which
often "mostly works" (bus controller happens to have sane reset-state
defaults) until a specific board/timing combination exposes the ordering bug.

## Device PM and deferred init
With `CONFIG_PM_DEVICE`, a driver's power-management action callback
(`pm_device_action_cb_t`, handling suspend/resume actions) is exposed to the PM subsystem,
enabling runtime power management of the device — relevant
when a driver's peripheral needs explicit power-down beyond what the generic
clock-gating advice in
`computing-software.firmware-embedded-development.low-power-design.clock-gating-and-peripheral-sleep-modes`
covers for bare-metal; Zephyr's device PM framework is the structured way to
hook into that on an RTOS-managed system instead of hand-rolling sleep-entry
pin/clock sequences per driver.

## Fitting an existing subsystem API (e.g. `sensor_driver_api`)
Where Zephyr already defines a subsystem API (sensor, GPIO, PWM, etc.),
implement that interface's function table rather than inventing a bespoke
one — this is what lets application code written against
`sensor_sample_fetch()`/`sensor_channel_get()` work unmodified against any
compliant sensor driver, yours included. Check the subsystem's header for the
exact function-pointer struct shape before designing a driver's internal
API, not after.

## Verify
- [ ] Driver instantiates correctly from a devicetree overlay with no hardcoded bus/address values in the C source.
- [ ] `device_is_ready()` is checked at application startup for every device the app depends on.
- [ ] Init level/priority was checked against actual dependencies (bus controllers, GPIO drivers the device uses) and ordering was tested by varying `INIT_PRIORITY`, not assumed correct.
- [ ] If a standard subsystem API applies (sensor, GPIO, etc.), the driver implements that exact function-table shape, confirmed against generic subsystem sample code working unmodified.

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed: DEVICE_DT_INST_DEFINE argument order and the I2C_DT_SPEC_GET macro exist in the sources; the kernel driver documentation lists the three init levels PRE_KERNEL_1, PRE_KERNEL_2 and POST_KERNEL; `device_is_ready()` is documented as reporting a device that has been successfully initialized, for pointers taken from DEVICE_DT_GET(); with CONFIG_PM_DEVICE the drivers' pm_device_action_cb_t hooks are exposed to the PM subsystem (device PM doc).
Fixed: APPLICATION is not one of the three driver levels listed in the driver docs; the claim that the power subsystem calls device hooks "automatically" was reworded to what the PM doc states.

Method: documentation only; no commands were run.
