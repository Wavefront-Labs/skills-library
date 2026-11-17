---
id: computing-software.firmware-embedded-development.zephyr.devicetree-node-status-and-compatible
name: devicetree-node-status-and-compatible
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [dt-status, status-okay, compatible-matching, dt-has-compat-status-okay, dt-foreach-status-okay, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Control which Zephyr devicetree nodes become devices with status and compatible: enabling and disabling in overlays, compatible fallback order, and status-okay iteration macros."
sources:
  - https://docs.zephyrproject.org/latest/build/dts/intro-syntax-structure.html
  - https://docs.zephyrproject.org/latest/build/dts/api/api.html
  - https://docs.zephyrproject.org/latest/build/dts/bindings-intro.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/devicetree.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node status and compatible matching

## status
```dts
&i2c1 { status = "okay"; };          /* enable */
&uart1 { status = "disabled"; };     /* disable */
```
- No `status` property means "okay". Zephyr treats any value other than `"okay"` as disabled.
- A `struct device` is allocated only for enabled nodes, and `DT_HAS_<COMPAT>_ENABLED` is y only
  when a node with that compatible is `okay`. Disabled nodes still produce DT macros, so
  `DT_NODELABEL(uart1)` compiles but `DEVICE_DT_GET` on it fails to link
  (`undefined reference to __device_dts_ord_<N>`).
- `reserved` documents a node that exists but is enabled elsewhere (for example by another core
  or domain); `edtlib` handles it like `disabled`. `fail` and `fail-sss` are not used by Zephyr.
- A child node is not implicitly disabled when its parent is disabled; disable children
  explicitly if you want that.

## compatible
```dts
sensor@76 {
    compatible = "bosch,bme280";
    reg = <0x76>;
};
```
- Recommended format `"vendor,device"`; `dts/bindings/vendor-prefixes.txt` lists commonly
  accepted vendor names. Generic values such as `gpio-keys` or `fixed-clock` are also used.
- Multiple values go most specific first: `compatible = "acme,widget-v2", "acme,widget";`
  The build system looks for bindings in the listed order and uses the **first** compatible that
  has a binding.
- In C the compatible becomes a lowercase-underscore token without quotes: `bosch,bme280` ->
  `bosch_bme280`, used for `DT_DRV_COMPAT` and for macros such as `DT_HAS_COMPAT_STATUS_OKAY`.

## Status-aware macros
```c
#if DT_HAS_COMPAT_STATUS_OKAY(bosch_bme280)
/* at least one enabled BME280 */
#endif

#define SENSOR_DEV(node) DEVICE_DT_GET(node),
static const struct device *const sensors[] = {
    DT_FOREACH_STATUS_OKAY(bosch_bme280, SENSOR_DEV)
};

DT_NODE_HAS_STATUS(DT_NODELABEL(spi2), okay)   /* single node check */
DT_NODE_HAS_STATUS_OKAY(DT_NODELABEL(spi2))    /* shorthand for the above with okay */
```
Drivers use `DT_INST_FOREACH_STATUS_OKAY(MY_DEFINE)` with `DT_DRV_COMPAT` so one instance is
created per enabled node.

## Gotchas
- When enabling a node, check that its pin configuration (`pinctrl-0` and friends) is defined
  for your board.
- If you disable a node that `/chosen` points at (for example `zephyr,console`), update `chosen`
  too.
- Using `DT_NODELABEL` on a disabled node in shared code: guard with
  `DT_NODE_HAS_STATUS_OKAY`/`COND_CODE_1` so the build works on boards where it's off.

## Verify
- [ ] `zephyr.dts` shows the intended status for every node the app uses.
- [ ] Shared code guards optional nodes with status checks.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed status values and semantics, reserved handling, parent/child rule, compatible format, vendor-prefixes file and first-binding-wins matching (build/dts intro-syntax-structure and bindings-intro pages), DT_DRV_COMPAT naming and DT_INST_FOREACH_STATUS_OKAY (dts api and howtos pages), and that DT_NODE_HAS_STATUS, DT_NODE_HAS_STATUS_OKAY, DT_HAS_COMPAT_STATUS_OKAY and DT_FOREACH_STATUS_OKAY exist (include/zephyr/devicetree.h). Removed the unconfirmed claim that SoC dtsi files disable all peripherals and the silent-console-failure remark.
Method: documentation only; no commands were run.
