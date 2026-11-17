---
id: computing-software.firmware-embedded-development.device-driver-development.linux-runtime-pm-in-drivers
name: linux-runtime-pm-in-drivers
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [linux-runtime-pm, platform-driver, pm-runtime-get-sync, autosuspend, dev-pm-ops, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Add runtime PM to a Linux driver: runtime_suspend/resume callbacks, get/put around hardware access, autosuspend delay, and enable/disable ordering in probe and remove."
sources:
  - https://docs.kernel.org/power/runtime_pm.html
  - https://docs.kernel.org/driver-api/pm/devices.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime PM in drivers

Runtime PM powers a device down (clocks off, regulators off, power domain off) while the system
runs, whenever no one is using it.

## Callbacks
```c
static int mydrv_runtime_suspend(struct device *dev) {
    struct mydrv *d = dev_get_drvdata(dev);
    clk_disable_unprepare(d->clk);
    return 0;
}
static int mydrv_runtime_resume(struct device *dev) {
    struct mydrv *d = dev_get_drvdata(dev);
    int ret = clk_prepare_enable(d->clk);
    if (ret) return ret;
    mydrv_restore_regs(d);          /* registers may have lost state */
    return 0;
}
static DEFINE_RUNTIME_DEV_PM_OPS(mydrv_pm, mydrv_runtime_suspend, mydrv_runtime_resume, NULL);
/* .driver.pm = pm_ptr(&mydrv_pm) */
```
`DEFINE_RUNTIME_DEV_PM_OPS` also uses `pm_runtime_force_suspend()` and `pm_runtime_force_resume()`
for its system sleep callbacks (the deprecated `UNIVERSAL_DEV_PM_OPS` used the same callbacks for both).

## Probe and remove
```c
/* probe: hardware is powered (clock enabled by probe code) */
pm_runtime_set_active(dev);                  /* tell the core it's on */
pm_runtime_set_autosuspend_delay(dev, 500);  /* ms */
pm_runtime_use_autosuspend(dev);
ret = devm_pm_runtime_enable(dev);           /* disables automatically on remove */
```
Then every hardware access path:
```c
ret = pm_runtime_resume_and_get(dev);        /* returns <0 on failure and drops the ref for you */
if (ret < 0) return ret;
/* ... access registers ... */
pm_runtime_put_autosuspend(dev);             /* also calls pm_runtime_mark_last_busy() */
```
`pm_runtime_get_sync` increments the usage count even if it returns an error; the header
recommends `pm_runtime_resume_and_get` instead, which drops the reference on failure.

## Gotchas
- Interrupt handlers must not touch registers of a suspended device: check
  `pm_runtime_suspended()` or keep a reference while interrupts are expected.
- Callbacks run in process context by default; `pm_runtime_irq_safe(dev)` declares that they may run
  in atomic context (they must then not sleep), which allows the synchronous helpers in atomic code.
- Active children keep the parent from suspending (unless `power.ignore_children` is set).

## Debugging
```sh
cat /sys/devices/.../power/runtime_status        # active / suspended
cat /sys/devices/.../power/runtime_usage         # usage count (stuck > 0 = leaked get)
echo on > /sys/devices/.../power/control         # force on for debugging; "auto" allows runtime PM
```

## Verify
- [ ] Device reports `suspended` after the autosuspend delay when idle; usage count returns to 0.
- [ ] Access after suspend works (registers restored).

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in include/linux/pm_runtime.h: pm_runtime_resume_and_get, the note that pm_runtime_get_sync bumps the usage counter even on error and resume_and_get is preferred, pm_runtime_irq_safe, pm_runtime_suspended, pm_runtime_mark_last_busy, devm_pm_runtime_enable, and DEFINE_RUNTIME_DEV_PM_OPS using pm_runtime_force_suspend/resume (versus deprecated UNIVERSAL_DEV_PM_OPS). Confirmed in Documentation/power/runtime_pm.rst: autosuspend variants also call pm_runtime_mark_last_busy() (so the explicit call before put_autosuspend was dropped), pm_runtime_irq_safe semantics, pm_runtime_set_active before enable, pm_runtime_use_autosuspend, active children keep the parent active, the control attribute with "on" and "auto". Confirmed in include/linux/pm.h: pm_ptr(). Confirmed in Documentation/ABI/testing/sysfs-devices-power: runtime_status, runtime_usage and control files. Removed as unconfirmed: the "without CONFIG_PM callbacks are never called" bullet and the I2C adapter remark.

Method: documentation only; no commands were run.
