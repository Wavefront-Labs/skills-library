---
id: computing-software.firmware-embedded-development.zephyr.devicetree-functions-in-kconfig
name: devicetree-functions-in-kconfig
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [dt-kconfig-functions, dt-has-compat-enabled, dt-compat-enabled, dt-chosen-reg-size, kconfig-preprocessor, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Drive Kconfig from devicetree with the Kconfig preprocessor functions (dt_compat_enabled, dt_chosen_reg_size_hex, dt_node_has_prop) and DT_HAS_<compat>_ENABLED symbols."
sources:
  - https://docs.zephyrproject.org/latest/build/kconfig/preprocessor-functions.html
  - https://docs.zephyrproject.org/latest/build/dts/dt-vs-kconfig.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/kconfig/kconfigfunctions.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Devicetree functions in Kconfig

Hardware facts live in devicetree; Kconfig sometimes needs them (enable a driver only if the
hardware exists, size a flash option from a partition). Kconfig is parsed after devicetree, so it
can query the EDT through preprocessor functions.

## Auto-generated symbols (preferred for drivers)
For every compatible in the tree with an `okay` node, Zephyr generates
`DT_HAS_<COMPAT>_ENABLED` (compatible upper-cased, non-alphanumerics to `_`):
```kconfig
config SENSOR_BME280
    bool "BME280 sensor"
    default y
    depends on DT_HAS_BOSCH_BME280_ENABLED
    select I2C if $(dt_compat_on_bus,$(DT_COMPAT_BOSCH_BME280),i2c)
    select SPI if $(dt_compat_on_bus,$(DT_COMPAT_BOSCH_BME280),spi)
```
`DT_COMPAT_BOSCH_BME280` is defined in `Kconfig.dts` as the string `bosch,bme280`.

## Preprocessor functions
Called with `$(fn,args)`. Common ones:
| Function | Returns |
|---|---|
| `dt_compat_enabled,<compat>` | `y`/`n`: any okay node with that compatible |
| `dt_compat_on_bus,<compat>,<bus>` | `y` if such a node sits on that bus type |
| `dt_nodelabel_enabled,<label>` | `y` if labelled node is okay |
| `dt_node_has_prop,<path>,<prop>` / `dt_nodelabel_has_prop` | `y`/`n` |
| `dt_node_int_prop_int,<path>,<prop>` / `_hex` | integer property value |
| `dt_chosen_reg_addr_hex,<chosen>` / `dt_chosen_reg_size_hex` | address/size of the chosen node's reg |
| `dt_node_reg_addr_hex,<path>[,idx,unit]` | reg address; optional index and unit scale (K, M, G) |
| `dt_chosen_enabled,<chosen>` | `y` if a chosen node exists and is okay |
| `dt_node_str_prop_equals,<path>,<prop>,<val>` | `y`/`n` |

Example: flash size from the chosen flash node.
```kconfig
DT_CHOSEN_Z_FLASH := zephyr,flash
config FLASH_SIZE
    default $(dt_chosen_reg_size_int,$(DT_CHOSEN_Z_FLASH),0,K)
```

## Rules
- Use `default` or `depends on` with DT data; don't make users set Kconfig values that duplicate
  DT facts.
- Devicetree is processed before Kconfig, so overlays already apply when the functions run.
- Each `*_int` function returns a decimal value and each `*_hex` function a `0x` value.
- Debug a value: check `build/zephyr/.config` and the generated `Kconfig.dts` in the build
  directory (`<build>/<image>/zephyr` under sysbuild).

## Verify
- [ ] Driver Kconfig depends on `DT_HAS_..._ENABLED` and defaults y.
- [ ] Disabling the DT node turns the driver option off in `.config`.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed the function list and argument forms (kconfig preprocessor-functions page and scripts/kconfig/kconfigfunctions.py), the _int/_hex rule, unit scales, and DT_HAS_<COMPAT>_ENABLED / DT_COMPAT_<COMPAT> generation in Kconfig.dts (dt-vs-kconfig page). Removed the unconfirmed edt.pickle and evaluate-once claims.
Method: documentation only; no commands were run.
