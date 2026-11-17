---
id: computing-software.firmware-embedded-development.device-driver-development.probe-deferral-handling
name: probe-deferral-handling
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [platform-driver, probe-defer, eprobe-defer, dev-err-probe, devices-deferred, fw-devlink, supplier-consumer, boot-order, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Handle Linux probe deferral correctly: propagate -EPROBE_DEFER, log with dev_err_probe, find why a device is stuck in devices_deferred, and use fw_devlink ordering."
sources:
  - https://docs.kernel.org/driver-api/driver-model/driver.html
  - https://docs.kernel.org/admin-guide/kernel-parameters.html
  - https://github.com/torvalds/linux/blob/master/drivers/base/dd.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Probe deferral handling

**Goal:** drivers that cope with suppliers (clocks, regulators, GPIO controllers, PHYs) not yet
probed, and boot logs that explain why a device never appeared.

## The mechanism
When a resource getter returns `-EPROBE_DEFER`, the supplier hasn't probed yet. The driver must
**return that error from probe unchanged**, releasing anything acquired (devm does this). The
driver core retries deferred devices after a successful probe of another device.

## Correct pattern
```c
a->vdd = devm_regulator_get(dev, "vdd");
if (IS_ERR(a->vdd))
    return dev_err_probe(dev, PTR_ERR(a->vdd), "failed to get vdd\n");
```
`dev_err_probe` prints for real errors, stays quiet for `-EPROBE_DEFER` and records the reason
in `/sys/kernel/debug/devices_deferred`.

## Mistakes that break deferral
- Converting the error: `if (IS_ERR(x)) return -ENODEV;` turns a transient condition into a
  permanent failure. The device never probes on boots where ordering differs.
- Using non-`_optional` getters for optional resources: an absent optional supply then defers
  forever (or fails); use `devm_gpiod_get_optional`, `devm_clk_get_optional`,
  `devm_regulator_get_optional` (the last returns -ENODEV when absent).
- Side effects before deferral: enabling hardware, registering a child device or starting a
  thread and then deferring causes repeated side effects on each retry. Acquire all resources
  first, then touch hardware.

## Debugging stuck devices
```
cat /sys/kernel/debug/devices_deferred          # device + recorded reason
ls /sys/class/devlink/                          # supplier->consumer links (fw_devlink)
cat /sys/kernel/debug/clk/clk_summary           # is the clock provider registered?
```
Common causes: supplier driver not built (`=n`) or module not loaded, DT phandle to a node with
`status = "disabled"`, circular dependencies. Boot parameter `fw_devlink=permissive` (or `off`)
helps test whether fw_devlink's strict ordering is the blocker;
`deferred_probe_timeout=<seconds>` sets how long deferred probe waits on dependencies before giving up.

## fw_devlink
The kernel parses firmware (DT) phandles to create supplier/consumer device links and, with
`fw_devlink=on` or `rpm`, uses them to enforce probe ordering (suppliers first), reducing deferral
churn. `permissive` only uses the links for sync_state() ordering and `off` creates none. Drivers for suppliers must not be modules loaded too late in a way that
blocks consumers needed for rootfs (e.g. a regulator for the eMMC): build them in.

## Verify
- [ ] `devices_deferred` empty after boot.
- [ ] Unbind/rebind of a supplier makes consumers re-probe correctly.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/driver-api/driver-model/driver.rst: probe may return -EPROBE_DEFER, it must not be returned after creating child devices or other side effects, the device goes onto the deferred probe list and is retried. Confirmed in drivers/base/dd.c: a successful probe triggers retry of the pending list, and the devices_deferred debugfs file. Confirmed in drivers/base/core.c: dev_err_probe handling of -EPROBE_DEFER. Confirmed in admin-guide/kernel-parameters.txt: fw_devlink= values off, permissive, on, rpm (on enforces probe ordering) and deferred_probe_timeout=. Confirmed in Documentation/ABI/testing/sysfs-class-devlink: /sys/class/devlink/. Removed the "since ~5.x" gate and the fixed "=30" value. Confirmed in drivers/clk/clk.c: the clk_summary debugfs file.

Method: documentation only; no commands were run.
