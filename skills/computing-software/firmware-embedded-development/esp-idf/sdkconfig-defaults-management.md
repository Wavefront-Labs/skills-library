---
id: computing-software.firmware-embedded-development.esp-idf.sdkconfig-defaults-management
name: sdkconfig-defaults-management
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [idf-py, sdkconfig-defaults, sdkconfig, menuconfig, save-defconfig, sdkconfig-defaults-target, kconfig, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Manage ESP-IDF configuration as reviewable sdkconfig.defaults files (layered per target and per build profile) instead of committing a generated sdkconfig."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/build-system.html#custom-sdkconfig-defaults
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/kconfig/project-configuration-guide.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/tools/idf-py.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing sdkconfig.defaults

**Goal:** configuration that is minimal, reviewable in a diff, and reproducible on a clean
checkout and across IDF upgrades.

## How the files combine
On a build with no `sdkconfig`, IDF generates it from Kconfig defaults overridden by `sdkconfig.defaults`
(the values in it are treated as user-set). Per the build system guide:
1. `sdkconfig.defaults` is the default file name; setting `SDKCONFIG_DEFAULTS` (environment variable or top-level
   `CMakeLists.txt`) replaces it, so list it explicitly if you still want it. Several files are separated by
   semicolons, files listed first apply first and later files override earlier ones.
2. `sdkconfig.defaults.<target>` (for example `sdkconfig.defaults.esp32s3`) is loaded after the file it belongs to, but
   only if the generic `sdkconfig.defaults` file exists (create an empty one if you only have target files). With
   `SDKCONFIG_DEFAULTS`, a target variant is looked up for every listed file.
The defaults files are used when creating a new config from scratch or when a config value has not yet been set
in `sdkconfig`; a value already stored in `sdkconfig` (for example one you changed in menuconfig) is not overwritten by
editing the defaults file. That is the source of "I changed sdkconfig.defaults and nothing happened": delete
`sdkconfig` (or run `idf.py set-target <chip>`, which also clears the build directory) after editing defaults.

## Workflow
```
idf.py menuconfig                 # change things interactively
idf.py save-defconfig             # generates a sdkconfig.defaults with the options that differ from the defaults
git diff sdkconfig.defaults       # review it: confirm nothing intended was dropped
```
Commit `sdkconfig.defaults*`, add `sdkconfig` and `sdkconfig.old` to `.gitignore` (or commit
`sdkconfig` too if you want byte-exact reproducibility, but then review both).

## Build profiles
```
idf.py -B build-prod -DSDKCONFIG=build-prod/sdkconfig \
       -DSDKCONFIG_DEFAULTS="sdkconfig.defaults;sdkconfig.prod" build
```
Keep `sdkconfig.prod` tiny (for example `CONFIG_LOG_DEFAULT_LEVEL_WARN=y`,
`CONFIG_ESP_SYSTEM_PANIC_PRINT_REBOOT=y`, `CONFIG_COMPILER_OPTIMIZATION_SIZE=y`). Separate `-B` dirs stop profiles clobbering each
other's `sdkconfig`.

## Gotchas
- **Renamed options across IDF versions**: options are renamed between releases (for example the memory protection
  options changed in v6.0), so after upgrading IDF regenerate with `save-defconfig` and review the Kconfig messages
  in the build log rather than assuming old names still apply.
- Partition table and flash size live in sdkconfig (`CONFIG_PARTITION_TABLE_CUSTOM=y` with
  `CONFIG_PARTITION_TABLE_CUSTOM_FILENAME`, and `CONFIG_ESPTOOLPY_FLASHSIZE_4MB`); if they are missing you get the
  defaults (flash size 2 MB, single factory app partition table), which causes "app partition too small" errors for larger apps.
- Components can ship their own `Kconfig` with defaults; `sdkconfig.defaults` overrides them.
- `idf.py set-target` clears the build directory and regenerates `sdkconfig` from scratch (the old one is saved as `sdkconfig.old`);
  `CONFIG_IDF_TARGET="esp32s2"` in `sdkconfig.defaults` sets the project's default target.

## Verify
- [ ] Fresh clone, `idf.py set-target <chip> build` produces the same `sdkconfig` as CI.
- [ ] `sdkconfig.defaults` contains only intentional non-default lines.

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-guides/build-system.rst custom sdkconfig defaults, kconfig/project-configuration-guide.rst, tools/idf-py.rst, tools/idf_py_actions/core_ext.py, components/partition_table and esptool_py Kconfig.projbuild).
Confirmed: SDKCONFIG_DEFAULTS replaces the default file name, semicolon list with later files winning, target-specific files loaded only when the generic file exists, defaults used for new configs or unset values, `idf.py save-defconfig` ("Generate a sdkconfig.defaults with options different from the default ones"), `idf.py set-target` behaviour and `sdkconfig.old`, `-B` build directory option, `CONFIG_PARTITION_TABLE_CUSTOM_FILENAME`, `ESPTOOLPY_FLASHSIZE_4MB` with default flash size 2 MB and default single-app partition table, `CONFIG_LOG_DEFAULT_LEVEL_WARN`, `CONFIG_ESP_SYSTEM_PANIC_PRINT_REBOOT`, `CONFIG_COMPILER_OPTIMIZATION_SIZE`. Corrected: SDKCONFIG_DEFAULTS replaces rather than adds to `sdkconfig.defaults`, and defaults are applied for values not yet set in an existing sdkconfig. Removed unconfirmed claims: `sdkconfig.rename` handling, the guidance on setting other choice items to n, `CONFIG_BOOTLOADER_LOG_LEVEL_NONE` and the 1 MB partition default.

Method: documentation only; no commands were run.
