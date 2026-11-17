---
id: computing-software.firmware-embedded-development.device-driver-development.linux-regulator-consumers
name: linux-regulator-consumers
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [regulator-api, platform-driver, vdd-supply, devm-regulator-get-enable, power-sequencing, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Power external chips from Linux drivers with the regulator consumer API: *-supply DT properties, bulk get/enable, startup delays, dummy regulators, and suspend handling."
sources:
  - https://docs.kernel.org/power/regulator/consumer.html
  - https://docs.kernel.org/power/regulator/overview.html
  - https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/regulator/regulator.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regulator consumers

## Device tree
```dts
&i2c1 {
    imu@68 {
        compatible = "acme,imu";
        reg = <0x68>;
        vdd-supply  = <&ldo3>;      /* 1.8 V core */
        vddio-supply = <&vreg_3v3>;
    };
};
```
Supply names come from the binding (`vdd`, `vddio`); the property is `<name>-supply`.

## Probe
```c
static const char * const supplies[] = { "vdd", "vddio" };

ret = devm_regulator_bulk_get_enable(dev, ARRAY_SIZE(supplies), supplies);
if (ret) return dev_err_probe(dev, ret, "supplies\n");
usleep_range(2000, 3000);            /* datasheet power-up time before first I2C access */
```
For drivers that switch supplies at runtime (suspend):
```c
struct regulator_bulk_data sup[2] = { { .supply = "vdd" }, { .supply = "vddio" } };
devm_regulator_bulk_get(dev, 2, sup);
regulator_bulk_enable(2, sup);       /* in resume */
regulator_bulk_disable(2, sup);      /* in suspend, after putting the chip in reset */
```
Order: `regulator_bulk_enable()` starts the enables asynchronously (core.c), so do not rely on
array order; if the datasheet requires VDDIO before VDD, get and enable them individually with
delays.

## Behaviour to know
- **Dummy regulator**: if the DT lacks the supply, `regulator_get` returns a dummy and logs
  "supply vdd not found, using dummy regulator". Fine for always-on rails; use
  `regulator_get_optional` when absence must change behaviour (returns `-ENODEV`).
- Enable is reference counted; the rail turns off only when all consumers disable it (and
  `regulator-always-on` isn't set).
- `regulator_set_voltage(reg, min_uV, max_uV)` is limited by the provider constraints
  (`regulator-min-microvolt` etc.); the core returns `-EPERM` when changing voltage is not permitted.
- Unused regulators are disabled by a delayed work after boot (`regulator_init_complete_work`);
  a device powered only by bootloader setup dies then unless its driver claims the supply.

## Debugging
```sh
cat /sys/kernel/debug/regulator/regulator_summary    # consumers, use counts, voltages
ls /sys/class/regulator/*/
```

## Verify
- [ ] `regulator_summary` lists the device as consumer of each supply with the right use count.
- [ ] Suspend/resume cycles power the chip down and back up, and it works after resume.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in include/linux/regulator/consumer.h: devm_regulator_bulk_get_enable, devm_regulator_bulk_get, regulator_bulk_enable and _disable, regulator_get_optional (returns -ENODEV when absent in the stub). Confirmed in drivers/regulator/core.c: the warning "supply %s not found, using dummy regulator", regulator_bulk_enable runs the enables through async calls (so order is not guaranteed; the skill previously claimed array order), -EPERM returns for disallowed changes, the regulator_summary debugfs file, and the delayed regulator_init_complete_work that disables unused regulators. Confirmed in regulator.yaml: regulator-min-microvolt, regulator-always-on, regulator-boot-on, and the .*-supply property pattern. Removed the unconfirmed "6.1+" gate. The boot-on claim was dropped from the reference-count bullet (not confirmed as affecting disable).

Method: documentation only; no commands were run.
