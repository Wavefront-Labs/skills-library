---
id: computing-software.firmware-embedded-development.zephyr.shields
name: shields
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-shield, shield-overlay, connector-nexus, arduino-header, west-build-shield, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Describe add-on boards as Zephyr shields: shield.yml, overlays against connector nexus nodes (arduino_header, mikrobus), Kconfig.shield, and building with --shield."
sources:
  - https://docs.zephyrproject.org/latest/hardware/porting/shields.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/west_commands/build.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shields

A shield is a daughter board described once and usable on any board that exposes the right
connector. The board's devicetree maps connector pins to real GPIOs and labels the buses; the
shield's overlay refers to those labels, and at build time the two are combined.

## Layout (upstream: `boards/shields/<shield>`)
```
boards/shields/acme_sensor/
  shield.yml
  acme_sensor.overlay
  Kconfig.shield
  Kconfig.defconfig
  pre_dt_shield.cmake         # optional: extra arguments for dtc
```
`shield.yml` (metadata; `name`, `full_name` and `vendor` are required):
```yaml
shields:
  - name: acme_sensor
    full_name: ACME Sensor Shield
    vendor: acme
    supported_features:        # optional; values from dts/bindings/binding-types.txt
      - sensor
```
`Kconfig.shield`:
```kconfig
config SHIELD_ACME_SENSOR
    def_bool $(shields_list_contains,acme_sensor)
```
`Kconfig.defconfig`: the default shield configuration, kept consistent with the default board
configuration (activating features is the application's responsibility), guarded for the shield:
```kconfig
if SHIELD_ACME_SENSOR
config SENSOR
    default y
endif
```
Shield source code is possible (a `CMakeLists.txt` plus sources) but only for shield-specific
requirements such as initialisation or timing; generic code does not belong there.

## Overlay against connectors, not SoC pins
```dts
&arduino_i2c {
    status = "okay";
    bme280@76 {
        compatible = "bosch,bme280";
        reg = <0x76>;
    };
};

/ {
    acme_pins {
        compatible = "gpio-keys";
        shield_int: int { gpios = <&arduino_header 8 GPIO_ACTIVE_LOW>; };  /* D2 */
    };
};
```
- `arduino_header`, `mikrobus_header`, `feather_header`, `pico_header`, `xiao_d` and similar
  are **GPIO nexus** nodes in the board devicetree that map connector pin numbers to real GPIO
  controllers with `gpio-map`.
- Bus labels such as `arduino_i2c`, `arduino_spi` and `arduino_serial` (and `mikrobus_i2c`,
  `feather_i2c`, ...) are alternate node labels the board defines, for example
  `arduino_i2c: &i2c1 {};`.
- A board without the connector labels cannot host the shield without a board-specific overlay.
- To avoid name clashes with board-level devices, label shield devices as `<device>_<shield>`
  (for example `sdhc_myshield`).

## Board-specific fixes and variants
Override a shield for one board or board revision inside the shield directory:
`boards/<board>.overlay`, `<board>_<revision>.overlay`, `<board>.defconfig`, `<board>.conf` and
`<board>_<revision>.conf`. Shields with several variants provide `<shield_v1>.overlay`,
`<shield_v1>.defconfig`, `<shield_v2>.overlay`, ... and are selected by variant name; per-board
overrides for a variant go in `boards/<shield_v2>/<board>.overlay` and `.defconfig`.

## Build
```bash
west build -b nucleo_f401re app --shield acme_sensor
west build -b nucleo_f401re app --shield acme_sensor --shield x_nucleo_iks01a3   # several
west build -b nucleo_f401re app -- -DSHIELD="acme_sensor;x_nucleo_iks01a3"       # CMake list
west shields                                                                     # list supported shields
```
`--shield` may be repeated (west joins the values with `;` into `-DSHIELD`). A project can also
set `SHIELD` in its `CMakeLists.txt` (`set(SHIELD x_nucleo_iks01a1)`).

## Verify
- [ ] Shield overlay uses only connector labels; builds on two different boards.
- [ ] `zephyr.dts` shows shield nodes under the board's connector bus.
- [ ] `SHIELD_<NAME>` is y in `.config` when built with the shield.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed the shield file layout, required shield.yml fields, Kconfig.shield/Kconfig.defconfig roles, pre_dt_shield.cmake, board-specific and variant override layouts, GPIO nexus node mapping (arduino_header index 8 is D2), connector label names and the --shield / SHIELD / set(SHIELD) usage (hardware/porting/shields page, west build.py joining shields with a semicolon), and the shields listing command. Fixed: space-separated -DSHIELD list (west joins with semicolons), bus labels are node labels not aliases, and the unconfirmed Zephyr 4.1 shield.yml gate, doc/index.rst entry and BOARD_ROOT sentence were removed.
Method: documentation only; no commands were run.
