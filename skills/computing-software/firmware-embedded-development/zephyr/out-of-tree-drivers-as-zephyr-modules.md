---
id: computing-software.firmware-embedded-development.zephyr.out-of-tree-drivers-as-zephyr-modules
name: out-of-tree-drivers-as-zephyr-modules
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-module, module-yml, out-of-tree-driver, zephyr-extra-modules, dts-root, zephyr-library, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Package custom Zephyr drivers, bindings and Kconfig as an out-of-tree module (zephyr/module.yml) and pull it into products via west or ZEPHYR_EXTRA_MODULES."
sources:
  - https://docs.zephyrproject.org/latest/develop/modules.html
  - https://github.com/zephyrproject-rtos/example-application
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/cmake/modules/zephyr_module.cmake
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Out-of-tree drivers as Zephyr modules

Keep company drivers out of the Zephyr tree (no fork to rebase) and out of each app (shared
across products) by making them a **Zephyr module**.

## Layout
```
acme-drivers/
├── zephyr/module.yml
├── CMakeLists.txt
├── Kconfig
├── dts/bindings/sensor/acme,tmp42.yaml
└── drivers/sensor/tmp42/{CMakeLists.txt,Kconfig,tmp42.c}
```
`zephyr/module.yml`:
```yaml
name: acme-drivers
build:
  cmake: .
  kconfig: Kconfig
  settings:
    dts_root: .          # makes dts/bindings visible
    # board_root: .      # if the module also carries boards
```
Top-level `CMakeLists.txt`:
```cmake
add_subdirectory_ifdef(CONFIG_ACME_TMP42 drivers/sensor/tmp42)
```
Driver `CMakeLists.txt`:
```cmake
zephyr_library()
zephyr_library_sources(tmp42.c)
```
`Kconfig` (module root):
```kconfig
rsource "drivers/sensor/tmp42/Kconfig"
```
Driver `Kconfig`:
```kconfig
config ACME_TMP42
    bool "ACME TMP42 temperature sensor"
    default y
    depends on DT_HAS_ACME_TMP42_ENABLED
    select I2C
```

## Pulling it in
- **west (products):** add as a project in `west.yml`; west-managed projects with
  `zephyr/module.yml` are discovered automatically.
  ```yaml
  - name: acme-drivers
    revision: v1.3.0
    path: modules/acme/drivers
  ```
- **Without west:** set `ZEPHYR_MODULES` (a list of module directories, each with `zephyr/module.yml`)
  on the CMake command line (`-DZEPHYR_MODULES=<path1>;<path2>`) or before `find_package(Zephyr)` in
  the app `CMakeLists.txt`. The build also reads `ZEPHYR_EXTRA_MODULES`/`EXTRA_ZEPHYR_MODULES` to add
  modules.
- Check discovery: the build directory's `zephyr_modules.txt` lists the discovered modules, and
  CMake defines `ZEPHYR_<MODULE_NAME>_MODULE_DIR` for each.

## Driver API choice
Implement an existing subsystem API (sensor, regulator, led, gpio) so apps and shells work
unchanged. A custom API class needs its own header with `__subsystem struct acme_api` and,
for userspace, syscall definitions (`zephyr_syscall_header()` in CMake).

## Gotchas
- The module name is turned into `ZEPHYR_<NAME>_MODULE_DIR`; the build rejects restricted names
  with a fatal error.
- Binding not found: `dts_root` missing in `module.yml`.
- Kconfig symbol defined but always n: wrong path in `rsource`, or the DT node isn't `okay`.
- Module CMake runs for every app, so guard sources with Kconfig.
- Version the module and pin it by tag/SHA in each product's manifest.

## Verify
- [ ] `zephyr_modules.txt` in the build directory lists `acme-drivers`.
- [ ] App builds with the driver enabled by a devicetree node only (no explicit `CONFIG_`).
- [ ] Module's own CI builds a sample app and twister tests (e.g. on native_sim with an emulator).

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed in the modules doc and CMake sources: modules are repositories with `zephyr/module.yml`; `build: cmake/kconfig` entries and `settings: dts_root/board_root/soc_root`; `ZEPHYR_MODULES` set on the command line or before `find_package(Zephyr)`; `zephyr_modules.txt` written to the build directory; `ZEPHYR_<NAME>_MODULE_DIR` variables and the restricted-name error; `add_subdirectory_ifdef`, `zephyr_library`, `zephyr_syscall_header` exist in extensions.cmake; `__subsystem` and `__syscall` in the driver documentation; `DT_HAS_<COMPAT>_ENABLED` Kconfig symbols.
Wrong claims fixed: the "Including module" log line is not printed by current CMake (only found in 1.14 release notes), and the unconfirmed claim that duplicate module names break the build was replaced by the documented restricted-name error. `ZEPHYR_EXTRA_MODULES` is read in zephyr_module.cmake but is not in the modules doc, so it is mentioned only as an additional variable.

Method: documentation only; no commands were run.
