---
id: computing-software.firmware-embedded-development.device-driver-development.sysfs-device-attributes
name: sysfs-device-attributes
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [linux-driver-subsystem, sysfs-attribute, device-attr-rw, attribute-groups, sysfs-emit, dev-groups, abi-documentation, sysfs-notify, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Expose driver settings and status through sysfs device attributes: DEVICE_ATTR_RW, attribute groups via dev_groups, sysfs_emit, input validation, sysfs_notify and ABI docs."
sources:
  - https://docs.kernel.org/filesystems/sysfs.html
  - https://docs.kernel.org/admin-guide/abi.html
  - https://github.com/torvalds/linux/blob/master/Documentation/ABI/README
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sysfs device attributes

**Goal:** simple, scriptable configuration and status files for a driver (one value per file),
created race-free with the device.

## Defining attributes
```c
static ssize_t threshold_show(struct device *dev, struct device_attribute *attr, char *buf) {
    struct acme *a = dev_get_drvdata(dev);
    return sysfs_emit(buf, "%u\n", READ_ONCE(a->threshold));
}
static ssize_t threshold_store(struct device *dev, struct device_attribute *attr,
                               const char *buf, size_t count) {
    struct acme *a = dev_get_drvdata(dev);
    unsigned int v;
    int ret = kstrtouint(buf, 0, &v);
    if (ret) return ret;
    if (v > 4095) return -EINVAL;
    mutex_lock(&a->lock);
    ret = acme_set_threshold(a, v);
    mutex_unlock(&a->lock);
    return ret ? ret : count;
}
static DEVICE_ATTR_RW(threshold);              /* mode 0644, uses threshold_show/_store */
static DEVICE_ATTR_RO(fault_count);            /* fault_count_show only */

static struct attribute *acme_attrs[] = {
    &dev_attr_threshold.attr, &dev_attr_fault_count.attr, NULL };
ATTRIBUTE_GROUPS(acme);                        /* defines acme_groups */

static struct platform_driver acme_driver = {
    .driver = { .name = "acme", .dev_groups = acme_groups, ... },
};
```
`dev_groups` (a member of `struct device_driver`) attaches the attributes to the device instance
once it is bound to the driver, so the driver core creates and removes them; prefer it over
calling `sysfs_create_group` by hand in probe.

## Rules (from the sysfs docs)
- ASCII text, preferably one value per file; arrays of the same type are tolerated (sysfs.rst).
- Use `sysfs_emit()` (bounds-checked, PAGE_SIZE) in show functions, not `sprintf`.
- Validate input in store; return negative errno on error, `count` on success.
- Document each attribute in `Documentation/ABI/testing/sysfs-bus-platform-drivers-acme` (What,
  Date, KernelVersion, Contact, Description): sysfs files are user-space ABI.

## Notifying user space
For status changes, call `sysfs_notify(&dev->kobj, NULL, "fault_count")` so user space waiting on
the attribute is woken instead of busy-polling.

## When not sysfs
High-rate data -> char device/IIO buffer; structured commands -> ioctl/netlink; debugging-only
knobs -> debugfs (not ABI).

## Verify
- [ ] `echo 5000 > threshold` returns "Invalid argument"; valid writes take effect.
- [ ] The attributes exist for every bound device and are removed on unbind.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/filesystems/sysfs.rst: attributes are ASCII text files preferably with one value, arrays of the same type tolerated, DEVICE_ATTR and __ATTR_RW definitions, new show() methods should use sysfs_emit() or sysfs_emit_at(). Confirmed in include/linux/device/driver.h: dev_groups are attributes attached to the device once bound to the driver. Confirmed in include/linux/sysfs.h: ATTRIBUTE_GROUPS, sysfs_notify, sysfs_emit; include/linux/device.h: DEVICE_ATTR_RW/RO helpers. Confirmed in Documentation/ABI/README: ABI entries use What, Date, KernelVersion (optional), Contact and Description fields. Removed as unconfirmed: the claim that dev_groups files exist before the uevent (and the udev verification step based on it) and the poll() POLLPRI/POLLERR semantics.

Method: documentation only; no commands were run.
