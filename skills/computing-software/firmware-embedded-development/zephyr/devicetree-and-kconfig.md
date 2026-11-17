---
id: computing-software.firmware-embedded-development.zephyr.devicetree-and-kconfig
name: devicetree-and-kconfig
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr, zephyr-rtos, west, west-build, west-init, west-update, west-flash, devicetree, dts, overlay, board-overlay, dt-nodelabel, dt-alias, gpio-dt-spec-get, device-is-ready, kconfig, prj-conf, menuconfig, guiconfig, pristine-build, nrf-connect-sdk, cmake, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Add or change hardware in a Zephyr app with devicetree overlays and select features with Kconfig, without editing the Zephyr tree; diagnose why a build ignored a change."
sources:
  - https://docs.zephyrproject.org/latest/develop/getting_started/index.html
  - https://docs.zephyrproject.org/latest/build/dts/index.html
  - https://docs.zephyrproject.org/latest/build/dts/howtos.html
  - https://docs.zephyrproject.org/latest/build/kconfig/index.html
  - https://docs.zephyrproject.org/latest/develop/application/index.html
  - https://docs.zephyrproject.org/latest/develop/west/build-flash-debug.html
  - https://docs.zephyrproject.org/latest/hardware/porting/board_porting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zephyr devicetree and Kconfig — hardware in DTS, features in Kconfig

**Goal:** add or change hardware (an LED, a sensor on I2C, a UART) and software features in a
Zephyr application without editing the Zephyr tree, and understand why a build did or did not
pick up your change.

## 1. Workspace and build
```bash
west init -m https://github.com/zephyrproject-rtos/zephyr --mr <release-tag> zephyrproject
cd zephyrproject && west update          # fetch modules at manifest revisions
west zephyr-export && west packages pip --install
west build -b <board> <app_dir>          # e.g. -b nrf52840dk/nrf52840
west flash
```
- Pin a release tag with `--mr` (or your own manifest repo). Building against `main` means a
  different Zephyr every `west update`.
- Board names use the qualifier syntax (`board/soc[/variant]`) of the hardware model introduced
  shortly after Zephyr 3.6.0; older docs show `nrf52840dk_nrf52840`. Use `west boards` to list valid names.
- Freestanding app layout: `CMakeLists.txt`, `prj.conf`, `src/main.c`, optional `boards/`.

## 2. Devicetree describes hardware
The board's `.dts` is final at build time; you change it with **overlays**, never by editing it.
With `DTC_OVERLAY_FILE` unset, the build looks in the application configuration directory for
`socs/<SOC>_<BOARD_QUALIFIERS>.overlay` and `boards/<BOARD>.overlay` (plus a revision file), and
only if none exist for `<BOARD>.overlay`, then `app.overlay`. Add files without losing that
default search with `west build -b <board> -- -DEXTRA_DTC_OVERLAY_FILE=extra.overlay` (semicolon
separated; applied after the others, so it wins). `-DDTC_OVERLAY_FILE=...` instead names exactly
the overlays to use, and is stored in the CMake cache.

```dts
/ {
    aliases { status-led = &led_status; };
    leds {
        compatible = "gpio-leds";
        led_status: led_status { gpios = <&gpio0 13 GPIO_ACTIVE_LOW>; };
    };
};
&i2c0 {
    status = "okay";
    clock-frequency = <I2C_BITRATE_FAST>;
    bme280@76 { compatible = "bosch,bme280"; reg = <0x76>; };
};
```
- `status = "okay"` is required: nodes left `"disabled"` produce no device and their macros fail.
- Node labels (`led_status:`) are what C code references; node names with `@unit-address` must
  match `reg`.
- The merged result is `build/zephyr/zephyr.dts` and the generated macros are in
  `build/zephyr/include/generated/zephyr/devicetree_generated.h`. Read these
  first when "my overlay was ignored".

## 3. Using devicetree from C
```c
#include <zephyr/drivers/gpio.h>
static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(DT_NODELABEL(led_status), gpios);
static const struct device *bme = DEVICE_DT_GET_ONE(bosch_bme280);

int main(void) {
    if (!gpio_is_ready_dt(&led) || !device_is_ready(bme)) return -ENODEV;
    gpio_pin_configure_dt(&led, GPIO_OUTPUT_INACTIVE);
    gpio_pin_toggle_dt(&led);
}
```
- `DT_NODELABEL(x)`, `DT_ALIAS(x)`, `DT_CHOSEN(x)` all expand at compile time. A typo is a cryptic
  compile error mentioning `__device_dts_ord_...` undefined — usually a missing node, disabled
  status, or a driver not enabled in Kconfig.
- Compatibles use commas in DTS and underscores in macros (`bosch,bme280` → `bosch_bme280`).
- `GPIO_ACTIVE_LOW` in DTS means "logical 1 = pin low"; the `_dt` APIs handle it, so code says
  on/off, not high/low.

## 4. Kconfig selects software
`prj.conf` sets symbols for the app:
```
CONFIG_GPIO=y
CONFIG_I2C=y
CONFIG_SENSOR=y
CONFIG_LOG=y
CONFIG_LOG_DEFAULT_LEVEL=3
CONFIG_MAIN_STACK_SIZE=2048
```
- Many drivers now default on when a matching enabled DT node exists, but subsystem symbols
  (`CONFIG_SENSOR`, `CONFIG_I2C`) still need enabling.
- Board-specific additions go in `boards/<board>.conf`; extra fragments via
  `-DEXTRA_CONF_FILE=debug.conf` (spaces or semicolons between files).
- Explore interactively: `west build -t menuconfig` (terminal) or `west build -t guiconfig`.
  Changes there land only in `build/zephyr/.config` and are lost on pristine builds — copy the
  symbols you want back into `prj.conf`.
- A symbol whose dependencies are unmet is silently dropped with a warning; always check the
  final value in `build/zephyr/.config`.

## 5. When to build pristine
CMake caches the board, overlays and conf files. After changing board, adding a new overlay or
`.conf` file, or switching branches, run `west build -p always -b <board> <app>`. `-p auto` makes the build folder pristine only when
the build would otherwise fail (for example a different board or application than last time);
the default of the `build.pristine` setting is `never`. Stale caches are the most common
cause of "my change did nothing".

For writing the sensor driver itself, see
computing-software.firmware-embedded-development.device-driver-development.i2c-sensor-driver-from-datasheet.

## Verify
- [ ] `west build -p always` succeeds from a fresh workspace pinned to a release tag.
- [ ] `build/zephyr/zephyr.dts` contains your overlay's nodes with `status = "okay"`.
- [ ] `build/zephyr/.config` shows each symbol from `prj.conf` with the intended value.
- [ ] The app checks `device_is_ready()` / `gpio_is_ready_dt()` and logs a clear error when false.
- [ ] Settings explored in menuconfig are copied into `prj.conf` and survive a pristine build.

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed: `west init --mr`, `west update`, `west zephyr-export` and `west packages pip --install` (getting started); overlay search order, DTC_OVERLAY_FILE versus EXTRA_DTC_OVERLAY_FILE, semicolon lists and the generated `zephyr.dts` and `include/generated/zephyr/devicetree_generated.h` paths (dts howtos); EXTRA_CONF_FILE and `boards/<BOARD>.conf` merging with prj.conf (application and Kconfig setting docs); menuconfig and guiconfig targets and that unmet-dependency assignments in `.config` are ignored; `build.pristine` values and default `never`; the `__device_dts_ord_<N>` undefined-reference troubleshooting entry; the hardware model v2 transition text; `DEVICE_DT_GET_ONE`, `gpio_is_ready_dt` and `device_is_ready` exist in the headers.
Wrong claims fixed: `-p auto` is not the default; the `-DDTC_OVERLAY_FILE replaces` note was inaccurate for current releases (it names the exact overlays); the generated header lives under `generated/zephyr/`; the pip requirements command is now `west packages pip --install`. Removed the unconfirmed `hardenconfig` target and the `OVERLAY_CONFIG` aside.

Method: documentation only; no commands were run.
