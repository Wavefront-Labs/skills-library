---
id: computing-software.firmware-embedded-development.zephyr.sysbuild-multi-image-builds
name: sysbuild-multi-image-builds
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-build-system, sysbuild, multi-image, sysbuild-conf, sb-config, mcuboot-image, netcore, image-specific-config, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Build several Zephyr images together with sysbuild (app + MCUboot, multi-core): sysbuild.conf, per-image Kconfig/overlays, and the -D<image>_ argument syntax."
sources:
  - https://docs.zephyrproject.org/latest/build/sysbuild/index.html
  - https://docs.zephyrproject.org/latest/develop/west/build-flash-debug.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/share/sysbuild/cmake/modules/sysbuild_extensions.cmake
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sysbuild multi-image builds

**Goal:** one `west build` that produces the bootloader, the application and any
co-processor images with consistent configuration, and flashes them all.

## Turning it on
```
west build -b nrf52840dk/nrf52840 --sysbuild app/      # or set in config:
west config build.sysbuild True
```
Each image gets its own build system and directory (for example `build/mcuboot/` next to the
main application's), plus a sysbuild-level build; `west flash` flashes the images in the order
sysbuild records in `domains.yaml` (the order they were added, unless dependencies change it).
Targets are prefixed with the image name, for example `ninja sysbuild_menuconfig` or
`mcuboot_menuconfig`.

## Choosing images: sysbuild.conf
`app/sysbuild.conf` (Kconfig for the sysbuild layer, looked up in the application top-level
directory; `-DSB_CONF_FILE=<file>` selects another file):
```
SB_CONFIG_BOOTLOADER_MCUBOOT=y
SB_CONFIG_BOOT_SIGNATURE_TYPE_ECDSA_P256=y
SB_CONFIG_BOOT_SIGNATURE_KEY_FILE="<absolute path to key>.pem"
```
`SB_CONFIG_*` symbols are defined in `share/sysbuild/` (for example
`share/sysbuild/images/bootloader/Kconfig`) and in module sysbuild Kconfig files; set one on the
command line with `-DSB_CONFIG_<name>=<value>`. With `SB_CONFIG_BOOTLOADER_MCUBOOT=y`, sysbuild
builds MCUboot and the main application as an MCUboot-bootable image.

## Per-image configuration
- Command line: namespace variables with the image (application) name, `-D<image>_<VAR>`, and
  Kconfig options with `-D<image>_CONFIG_<OPTION>`:
  `west build --sysbuild -- -Dmcuboot_EXTRA_CONF_FILE=mcuboot-extra.conf -Dmcuboot_CONFIG_DEBUG_OPTIMIZATIONS=y`
  An unprefixed `-DCONFIG_<OPTION>` goes to the main application, so the same command works with
  or without `--sysbuild`. `<image>_FILE_SUFFIX` applies a file suffix to one image.
- Files: in the main application folder, `sysbuild/<image>.conf` (Kconfig fragment) and
  `sysbuild/<image>.overlay` (devicetree overlay) are used together with the image's default
  configuration. A folder `sysbuild/<image>/` is used as that image's application configuration
  directory instead (its `prj.conf`, `boards/<board>.conf`, `boards/<board>.overlay`), and the
  image's default configuration files are then ignored.
- Shared partition layout: put the `fixed-partitions` / `zephyr,code-partition` choices in an
  overlay used by **both** images, or the app is linked at an address MCUboot doesn't boot.

## Adding your own image
`app/sysbuild.cmake`:
```cmake
ExternalZephyrProject_Add(
  APPLICATION remote_core
  SOURCE_DIR  ${APP_DIR}/remote
  BOARD       nrf5340dk/nrf5340/cpunet)
sysbuild_add_dependencies(CONFIGURE <main-image-name> remote_core)   # configure remote_core first
```
`sysbuild_add_dependencies(<CONFIGURE | FLASH> <image> [<dependency> ...])` orders the listed
dependencies before `<image>` when configuring, or in `domains.yaml` flash order (by default
images follow the order they were added). Other `ExternalZephyrProject_Add` keywords include
`APP_TYPE <MAIN|BOOTLOADER|FIRMWARE_LOADER>` and `BUILD_ONLY <bool>`; omit `BOARD` to target the
same board as the main image. `APP_DIR` is the path to the main application.

## Gotchas
- Unprefixed `-D` variables and `-DCONFIG_*` options go to the main application, not MCUboot;
  use `-Dmcuboot_...` rather than editing MCUboot's source tree.
- MCUboot accepts only the signed image (`zephyr.signed.bin` in the application's build
  directory), not `zephyr.bin`.
- Hex merging: `SB_CONFIG_MERGED_HEX_FILES=y` writes `merged_<NORMALIZED_BOARD_TARGET>.hex` per
  board target (all images must output hex files).

## Verify
- [ ] `west build -t sysbuild_menuconfig` (or `ninja sysbuild_menuconfig`) shows the expected `SB_CONFIG_*` values.
- [ ] `west flash` programs MCUboot and the signed app; MCUboot log shows the image validated.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed --sysbuild and build.sysbuild, sysbuild.conf and SB_CONF_FILE, SB_CONFIG_ namespace and -D<image>_ syntax, sysbuild/<image>.conf, .overlay and sysbuild/<image>/ config directory semantics, ExternalZephyrProject_Add keywords and sysbuild_add_dependencies signature (share/sysbuild/cmake/modules/sysbuild_extensions.cmake), image-prefixed menuconfig targets, merged hex files (sysbuild page), and that the SB_CONFIG_BOOT_SIGNATURE_* symbols exist. Wrong in the draft: add_dependencies(${DEFAULT_IMAGE} ...) is not the sysbuild mechanism, unprefixed -D goes to the main application (named by its project, not app), and the sysbuild/mcuboot/ directory replaces rather than adds to default config. Removed the unconfirmed NCS child-image and pristine-build claims. The sysbuild page example writes sysbuild_add_dependencies(IMAGE CONFIGURE ...) but the function signature takes CONFIGURE or FLASH first.
Method: documentation only; no commands were run.
