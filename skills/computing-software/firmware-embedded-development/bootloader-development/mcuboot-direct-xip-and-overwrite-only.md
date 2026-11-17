---
id: computing-software.firmware-embedded-development.bootloader-development.mcuboot-direct-xip-and-overwrite-only
name: mcuboot-direct-xip-and-overwrite-only
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [mcuboot-direct-xip, ab-update, overwrite-only, ram-load, upgrade-strategy, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Choose an MCUboot strategy other than swap: overwrite-only (no revert), direct-XIP (run from either slot), and RAM-load, with the revert and linking trade-offs."
sources:
  - https://docs.mcuboot.com/design.html
  - https://docs.mcuboot.com/imgtool.html
  - https://raw.githubusercontent.com/mcu-tools/mcuboot/main/boot/zephyr/Kconfig
  - https://raw.githubusercontent.com/zephyrproject-rtos/zephyr/main/share/sysbuild/images/bootloader/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overwrite-only and direct-XIP modes

MCUboot normally runs only the image in the primary slot and gets a new image there either by
swapping the slots or by overwriting the primary slot; the strategy is chosen at build time.
The alternatives below avoid swapping.

## Overwrite-only (`MCUBOOT_OVERWRITE_ONLY`)
The secondary slot's image overwrites the primary slot instead of being swapped with it.
- **No revert**: Zephyr's `CONFIG_BOOT_UPGRADE_ONLY` help says it prevents the fallback
  recovery but uses a much simpler code path, and the sysbuild text says the previous version
  is not stored in the secondary slot. Pair it with very careful testing and a recovery path
  (e.g. serial recovery).
- imgtool: `--overwrite-only` avoids adding the swap status area size when checking for slot overflow.
- Sysbuild: `SB_CONFIG_MCUBOOT_MODE_OVERWRITE_ONLY=y`; this mode supports the no-downgrade
  check (the overwrite does not happen unless the secondary slot's version is higher).

## Direct-XIP (`MCUBOOT_DIRECT_XIP`)
The bootloader runs an image directly from either the primary or the secondary slot, without
copying it. At boot it looks at both slots, takes the image with the highest version number,
checks its validity, and chain-loads it; if the selected image is invalid MCUboot erases that
slot and validates the other image.
- Images must be **built to run from their own slot**. The update client must know which slot
  is active and which is the staging area, and must load the proper image into the inactive slot.
- Zephyr sysbuild: `SB_CONFIG_MCUBOOT_MODE_DIRECT_XIP=y` (or `_DIRECT_XIP_WITH_REVERT`). With
  `SB_CONFIG_MCUBOOT_DIRECT_XIP_GENERATE_VARIANT` (experimental, default y in these modes) an
  extra image for `slot1_partition` named `<app>_slot_1_variant` is generated.
- Revert: `MCUBOOT_DIRECT_XIP_REVERT` (Zephyr `CONFIG_BOOT_DIRECT_XIP_REVERT`). The signed image
  needs the trailer (`imgtool sign --pad`), otherwise MCUboot will not recognise it as valid and
  tries to revert it. If the image is not confirmed at runtime before the next reboot, the
  bootloader considers it faulty, erases it and boots the previous image. Images can be made
  permanent in advance like in swap mode.
- Not compatible with on-the-fly image encryption; Zephyr's `MCUBOOT_DOWNGRADE_PREVENTION`
  option is not available with `BOOT_DIRECT_XIP`.

## RAM-load (`MCUBOOT_RAM_LOAD`)
MCUboot picks the newest image by version, copies it to RAM and runs it there. The design doc
frames it for SoCs with no internal flash but enough internal RAM, with images in external
storage; the image is always copied to internal RAM before authentication and execution. Images
must be built to execute from the RAM address and signed with `imgtool sign --load-addr`
(sets the `RAM_LOAD` header flag and address). The platform defines `IMAGE_EXECUTABLE_RAM_START`
and `IMAGE_EXECUTABLE_RAM_SIZE`. `MCUBOOT_RAM_LOAD_REVERT` adds a revert mechanism that works
like the direct-XIP one.

## Choosing
| Need | Mode |
|---|---|
| Revert on failure, single link address | swap-using-move / offset / scratch |
| Simple code path, accept no revert | overwrite-only |
| No copying, two link addresses OK | direct-XIP (+revert) |
| No internal flash, run from RAM | RAM-load |
The device-side update agent (MCUmgr, custom) must know the mode: in direct-XIP the new image
goes to the inactive slot, which alternates.

## Verify
- [ ] Update, reboot, and failure scenarios (unconfirmed image, bad signature, power cut) behave as the chosen mode promises.
- [ ] For direct-XIP: the server sends the image linked for the inactive slot (check its reset vector address).

## Checked
2026-10-31. Confirmed against the MCUboot design doc (upgrade strategies, direct-XIP selection and erase behaviour,
revert needs `--pad`, RAM-load description and parameters, encryption incompatibility), the imgtool page
(`--overwrite-only`, `--pad`, `--load-addr`), MCUboot `boot/zephyr/Kconfig` (`BOOT_UPGRADE_ONLY`, `BOOT_DIRECT_XIP`,
`_REVERT`, `BOOT_RAM_LOAD`) and Zephyr's sysbuild bootloader Kconfig (mode names, variant image). Removed:
`MCUBOOT_OVERWRITE_ONLY_FAST`, the speed/wear and compression claims, the `zephyr.signed.bin`/`_secondary_app`
output names, the OSPI/dual-bank remark and the encrypted-external-flash framing of RAM-load.
Method: documentation only; no commands were run.
