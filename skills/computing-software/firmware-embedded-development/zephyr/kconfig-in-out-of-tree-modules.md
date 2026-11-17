---
id: computing-software.firmware-embedded-development.zephyr.kconfig-in-out-of-tree-modules
name: kconfig-in-out-of-tree-modules
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [module-kconfig, zephyr-module-kconfig, kconfig-zephyr-module-dir, app-kconfig, rsource, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Add Kconfig options to an out-of-tree Zephyr module or application: module.yml kconfig entry, rsource layout, ZEPHYR_<MODULE>_MODULE symbols, and app Kconfig files."
sources:
  - https://docs.zephyrproject.org/latest/develop/modules.html#build-system-integration
  - https://docs.zephyrproject.org/latest/develop/application/index.html#application-kconfig
  - https://docs.zephyrproject.org/latest/build/kconfig/setting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kconfig in out-of-tree modules

## Module
`zephyr/module.yml`:
```yaml
name: acme-sensors
build:
  cmake: .
  kconfig: Kconfig           # relative to module root
```
`Kconfig` (module root):
```kconfig
menuconfig ACME_SENSORS
    bool "ACME sensor drivers"
    depends on SENSOR

if ACME_SENSORS
rsource "drivers/Kconfig"    # relative source, works wherever the module is checked out

config ACME_SENSORS_POLL_MS
    int "Poll interval (ms)"
    default 100
    range 10 10000

module = ACME_SENSORS
module-str = acme_sensors
source "subsys/logging/Kconfig.template.log_config"   # adds ACME_SENSORS_LOG_LEVEL
endif
```
Rules:
- Use `rsource` (relative to the current Kconfig file) rather than `source` with absolute paths; module location
  varies per workspace.
- Zephyr generates the symbol `ZEPHYR_<MODULE_NAME>_MODULE` for each available module and the
  variable `ZEPHYR_<MODULE_NAME>_MODULE_DIR` (absolute path, usable in Kconfig as
  `$(ZEPHYR_<MODULE_NAME>_MODULE_DIR)`). In names, letters are upper-cased and non-alphanumerics
  become `_` (module `foo-bar` gives `ZEPHYR_FOO_BAR_MODULE_DIR`). Use them to make other Kconfig
  symbols depend on the module.
- `kconfig:` and `cmake:` are both optional; `kconfig` defaults to `zephyr/Kconfig`.
- Keep a top-level `menuconfig` so the options are easy to find.

## Build files in a MODULE_EXT_ROOT (`kconfig-ext`)
`build: {cmake-ext: True, kconfig-ext: True}` in `module.yml` says the module's `CMakeLists.txt`
and `Kconfig` live in a `MODULE_EXT_ROOT` instead of in the module, so the build inclusion is
described outside the module. Rare in product repos.

## Application Kconfig
Put a `Kconfig` file next to the app's `CMakeLists.txt`:
```kconfig
mainmenu "Widget app"

config APP_SAMPLE_RATE_HZ
    int "Sample rate"
    default 50

source "Kconfig.zephyr"      # sources Kconfig.zephyr from the Zephyr root
```
The file is picked up automatically next to the app's `CMakeLists.txt`, or elsewhere via an
absolute `KCONFIG_ROOT`. `source` paths are relative to the Zephyr root (`$srctree` is
`$ZEPHYR_BASE`); use `rsource` to source relative to the current Kconfig file. Prefix app options
(`APP_`) to avoid clashes with Zephyr symbols.

## Per-board defaults
To change the default of an invisible symbol for one board, extend its definition in the board's
`Kconfig.defconfig` (the type is given once at the base definition); to set values for existing
visible symbols use `boards/<board>.conf` in the app:
```kconfig
if BOARD_ACME_WIDGET
config ACME_SENSORS_POLL_MS
    default 20
endif
```

## Gotchas
- A module's `Kconfig` is only read if the module is found by the build (west manifest project
  with `zephyr/module.yml`, `ZEPHYR_MODULES` or `EXTRA_ZEPHYR_MODULES`) and `kconfig:` points at
  the right file.
- Forgetting `source "Kconfig.zephyr"` in an app Kconfig leaves out all Zephyr options.
- `select` ignores the target's dependencies; prefer `depends on` for prompted symbols.

## Verify
- [ ] `west build -t menuconfig` shows the module menu (search with `/`).
- [ ] `ZEPHYR_<NAME>_MODULE=y` in `.config`.
- [ ] Module options take effect in `build/zephyr/.config`.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed module.yml build: cmake/kconfig keys and defaults, ZEPHYR_<MODULE_NAME>_MODULE and _MODULE_DIR naming (modules page), cmake-ext/kconfig-ext meaning (MODULE_EXT_ROOT), application Kconfig layout with source Kconfig.zephyr and rsource (application-kconfig.include), the Kconfig.template.log_config module/module-str template, and Kconfig.defconfig defaults (Kconfig setting page). Wrong in the draft: kconfig-ext is not a way to inject symbols for modules with existing glue; removed the unconfirmed Modules-menu claim.
Method: documentation only; no commands were run.
