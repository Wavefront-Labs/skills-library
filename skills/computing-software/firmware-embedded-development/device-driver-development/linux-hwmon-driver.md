---
id: computing-software.firmware-embedded-development.device-driver-development.linux-hwmon-driver
name: linux-hwmon-driver
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [hwmon, linux-driver-subsystem, hwmon-chip-info, sysfs-sensors, lm-sensors, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Expose temperature, voltage, current, power and fan sensors through Linux hwmon using devm_hwmon_device_register_with_info, standard attribute names and units, and lm-sensors."
sources:
  - https://docs.kernel.org/hwmon/hwmon-kernel-api.html
  - https://docs.kernel.org/hwmon/sysfs-interface.html
  - https://github.com/lm-sensors/lm-sensors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hwmon drivers

hwmon is for **monitoring** sensors (board temperature, supply voltages, fan speed). Precise
measurement or high-rate sampling belongs in IIO; both can coexist (the in-tree `iio_hwmon`
driver exposes IIO channels through hwmon).

## Registration with the info API
```c
static umode_t acme_is_visible(const void *data, enum hwmon_sensor_types type, u32 attr, int ch) {
    return 0444;
}
static int acme_read(struct device *dev, enum hwmon_sensor_types type, u32 attr, int ch, long *val) {
    struct acme *a = dev_get_drvdata(dev);
    switch (type) {
    case hwmon_temp: if (attr == hwmon_temp_input) return acme_temp_mdegc(a, val); break;
    case hwmon_in:   if (attr == hwmon_in_input)   return acme_mv(a, ch, val);    break;
    default: break;
    }
    return -EOPNOTSUPP;
}
static const struct hwmon_ops acme_ops = { .is_visible = acme_is_visible, .read = acme_read };
static const struct hwmon_channel_info * const acme_info[] = {
    HWMON_CHANNEL_INFO(temp, HWMON_T_INPUT | HWMON_T_MAX | HWMON_T_CRIT),
    HWMON_CHANNEL_INFO(in, HWMON_I_INPUT | HWMON_I_LABEL, HWMON_I_INPUT),
    NULL
};
static const struct hwmon_chip_info acme_chip = { .ops = &acme_ops, .info = acme_info };

hw = devm_hwmon_device_register_with_info(dev, "acme", a, &acme_chip, NULL);
```
Registration rejects names containing whitespace, `*` or `-` (use `hwmon_sanitize_name()` or
`devm_hwmon_sanitize_name()` for dynamic names, e.g. from `dev_name()`); a NULL name derives the
name from the parent device.

## Units (sysfs-interface ABI)
| Attribute | Unit |
|---|---|
| `tempN_input` | millidegree Celsius |
| `inN_input` | millivolt |
| `currN_input` | milliampere |
| `powerN_input` | microwatt |
| `fanN_input` | RPM |
| `humidityN_input` | milli-percent |
Units come from the hwmon ABI file `Documentation/ABI/testing/sysfs-class-hwmon`. Channel
numbering usually starts from 1, except voltages (`in`), which start from 0.

## Alarms and limits
`tempN_max`, `tempN_crit`, `*_alarm` attributes; notify userspace on alarm changes with
`hwmon_notify_event(hw, hwmon_temp, hwmon_temp_max_alarm, ch)`. Register as a thermal zone
sensor too with `HWMON_CHANNEL_INFO(chip, HWMON_C_REGISTER_TZ)` to let the thermal framework use it.

## Userspace
```sh
ls /sys/class/hwmon/hwmon*/          # name, temp1_input ...
sensors                              # lm-sensors
```

## Verify
- [ ] `sensors` shows plausible values with correct units; limits writable only if implemented.
- [ ] Readings match a reference thermometer/multimeter within datasheet accuracy.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/hwmon/hwmon-kernel-api.rst: devm_hwmon_device_register_with_info, hwmon_sanitize_name and devm_hwmon_sanitize_name, names with whitespace, '*' or '-' are rejected, hwmon_notify_event, HWMON_C_REGISTER_TZ for thermal registration. Confirmed in Documentation/hwmon/sysfs-interface.rst: numbering starts from 1 except voltages from 0. Confirmed in Documentation/ABI/testing/sysfs-class-hwmon: units millivolt, milliampere, RPM, milli-percent (humidity), and millidegree Celsius for temperature (power uses microWatt in sysfs-interface.rst). Confirmed in include/linux/hwmon.h: HWMON_CHANNEL_INFO, HWMON_T_CRIT, HWMON_I_LABEL. drivers/hwmon/iio_hwmon.c exists. Removed the unconfirmed sensors.d path detail.

Method: documentation only; no commands were run.
