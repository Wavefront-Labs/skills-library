---
id: computing-software.firmware-embedded-development.zephyr.writing-devicetree-bindings
name: writing-devicetree-bindings
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [devicetree, devicetree-bindings, binding-yaml, compatible, dt-drv-compat, child-binding, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write Zephyr devicetree binding YAML for a new device: compatible, bus, property types, defaults, enums, child bindings, and using them from a driver."
sources:
  - https://docs.zephyrproject.org/latest/build/dts/bindings-syntax.html
  - https://docs.zephyrproject.org/latest/build/dts/bindings-intro.html
  - https://docs.zephyrproject.org/latest/build/dts/dt-vs-kconfig.html
  - https://docs.zephyrproject.org/latest/develop/application/index.html
  - https://docs.zephyrproject.org/latest/develop/modules.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing devicetree bindings

Zephyr's DTS tooling only generates macros for properties that a **binding** declares. No
binding means the node is ignored (no `DT_PROP` macros, no driver instance).

## File location and name
`<DTS_ROOT>/dts/bindings/<class>/<vendor>,<device>.yaml`. The application directory, the board
directory, `ZEPHYR_BASE`, a module `dts_root` (set in `zephyr/module.yml`) and extra roots given
with `-DDTS_ROOT=` are searched. Bindings submitted upstream need a vendor prefix listed in
`dts/bindings/vendor-prefixes.txt`.

## Example: an I2C sensor
```yaml
# dts/bindings/sensor/acme,tmp42.yaml
description: ACME TMP42 temperature sensor
compatible: "acme,tmp42"
include: [sensor-device.yaml, i2c-device.yaml]   # i2c-device.yaml sets on-bus: i2c and requires reg

properties:
  int-gpios:
    type: phandle-array
    description: Data-ready interrupt line
  conversion-rate-hz:
    type: int
    default: 4
    enum: [1, 2, 4, 8]
    description: Output data rate
  extended-range:
    type: boolean
```
Node:
```dts
&i2c1 {
    tmp42@48 {
        compatible = "acme,tmp42";
        reg = <0x48>;
        int-gpios = <&gpioa 5 GPIO_ACTIVE_LOW>;
        conversion-rate-hz = <8>;
    };
};
```

## Property types
`int`, `array`, `uint8-array`, `string`, `string-array`, `boolean`, `phandle`, `phandles`,
`phandle-array`, `path`, `compound`. Keys: `required`, `default`, `enum`, `const`,
`deprecated`, `specifier-space`. Property names use dashes; macros use underscores
(`conversion_rate_hz`).

## Bus and child bindings
- Controller: `bus: i2c`. Device: `on-bus: i2c` (included via `i2c-device.yaml`). The same
  compatible can then have different bindings per bus (SPI vs I2C variants).
- `child-binding:` describes child nodes (LED channels, regulator outputs, ADC channels)
  without a compatible on each child.
- Specifier cells for providers: `gpio-cells: [pin, flags]` in a GPIO controller binding.

## Driver side
```c
#define DT_DRV_COMPAT acme_tmp42       /* comma and dash become underscore */
#define TMP42_DEFINE(n)                                                    \
    static const struct tmp42_cfg cfg_##n = {                              \
        .i2c  = I2C_DT_SPEC_INST_GET(n),                                   \
        .irq  = GPIO_DT_SPEC_INST_GET_OR(n, int_gpios, {0}),               \
        .rate = DT_INST_PROP(n, conversion_rate_hz),                       \
        .ext  = DT_INST_PROP(n, extended_range),                           \
    };                                                                     \
    DEVICE_DT_INST_DEFINE(n, tmp42_init, NULL, NULL, &cfg_##n,             \
                          POST_KERNEL, CONFIG_SENSOR_INIT_PRIORITY, &tmp42_api);
DT_INST_FOREACH_STATUS_OKAY(TMP42_DEFINE)
```

## Debugging
- `build/zephyr/zephyr.dts` = final merged tree. `build/zephyr/include/generated/zephyr/devicetree_generated.h` = macros (search for your node path).
- "Unknown property" errors mean a typo or a missing include. Value outside `enum` fails at build time; that's the point of bindings.
- `DT_HAS_COMPAT_STATUS_OKAY(acme_tmp42)` gates Kconfig: `default y` + `depends on DT_HAS_ACME_TMP42_ENABLED`.

## Verify
- [ ] Build fails when a `required` property is removed from the node (binding is actually applied).
- [ ] Generated header contains `DT_N_..._P_conversion_rate_hz`.
- [ ] Driver Kconfig depends on `DT_HAS_<COMPAT>_ENABLED`.

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed: the binding property schema (types, required, default, enum, const, deprecated, specifier-space), `on-bus`, `child-binding` and `<name>-cells` keys (bindings-syntax); bindings search roots including ZEPHYR_BASE, the board directory and DTS_ROOT, and `dts_root` in module.yml; vendor-prefixes.txt is for upstream submissions; `DT_HAS_<COMPAT>_ENABLED` Kconfig symbols (dt-vs-kconfig); `i2c-device.yaml` includes base.yaml, sets `on-bus: i2c` and requires `reg`; `sensor-device.yaml` exists; the macros I2C_DT_SPEC_INST_GET, GPIO_DT_SPEC_INST_GET_OR and DEVICE_DT_INST_DEFINE and Kconfig SENSOR_INIT_PRIORITY exist in the sources; names are lowercased with dashes and at signs becoming underscores.
Fixed: the old comment claiming `i2c-device.yaml` brings a `label`; the vendor-prefix rule is limited to upstream submissions; bus search roots made complete.

Method: documentation only; no commands were run.
