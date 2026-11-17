---
id: computing-software.firmware-embedded-development.bootloader-development.mcuboot-with-zephyr-sysbuild
name: mcuboot-with-zephyr-sysbuild
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [sysbuild-mcuboot, sysbuild, mcuboot, zephyr, west-build, signing-key, flash-partitions, sb-config, multi-image-build, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Build MCUboot and a Zephyr app together with sysbuild: SB_CONFIG options, signing keys, upgrade modes, per-image config fragments, partitions in devicetree, and flashing both."
sources:
  - https://docs.zephyrproject.org/latest/build/sysbuild/index.html
  - https://docs.mcuboot.com/readme-zephyr.html
  - https://raw.githubusercontent.com/zephyrproject-rtos/zephyr/main/share/sysbuild/images/bootloader/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building MCUboot with Zephyr sysbuild

**Goal:** one `west build` produces a matching MCUboot bootloader and a signed application,
and `west flash` programs both.

## Quick start
```sh
west build -b <board> --sysbuild samples/subsys/mgmt/mcumgr/smp_svr \
  -- -DSB_CONFIG_BOOTLOADER_MCUBOOT=y
west flash
```
Persist it in the app's `sysbuild.conf` (sysbuild reads this file in the application top-level
directory by default; `-DSB_CONF_FILE=<file>` picks another):
```
SB_CONFIG_BOOTLOADER_MCUBOOT=y
SB_CONFIG_BOOT_SIGNATURE_TYPE_ECDSA_P256=y
SB_CONFIG_BOOT_SIGNATURE_KEY_FILE="<path>/sign-ec256.pem"
SB_CONFIG_MCUBOOT_MODE_SWAP_USING_MOVE=y     # or _SWAP_USING_OFFSET (default), _OVERWRITE_ONLY, _DIRECT_XIP, _SWAP_SCRATCH
```
Signature types are `NONE` (hash only), `RSA` (default), `ECDSA_P256` and `ED25519`. When no key
file is set, the Kconfig default is a sample key shipped with the MCUboot module
(`root-ec-p256.pem`, `root-ed25519.pem` or `root-rsa-2048.pem`): **every production build must set
`SB_CONFIG_BOOT_SIGNATURE_KEY_FILE`** to your own key. `BOOT_SIGNATURE_KEY_FILE` also accepts a
comma-separated list: the first entry signs the application, later entries are public-only
verification keys embedded in the bootloader.

## Customising each image
- Sysbuild Kconfig fragments for an image go in the app's `sysbuild/<image>.conf`, devicetree
  overlays in `sysbuild/<image>.overlay` (so `sysbuild/mcuboot.conf`, `sysbuild/mcuboot.overlay`).
  They are used together with the image's default configuration. A folder `sysbuild/mcuboot/`
  instead becomes that image's application configuration directory and the default configuration
  files are ignored.
- Set an MCUboot Kconfig value on the command line with `-Dmcuboot_CONFIG_<option>=<value>`.
- `FILE_SUFFIX` is supported (`sysbuild/mcuboot_<suffix>.conf`; per image `-Dmcuboot_FILE_SUFFIX=...`).
- `west build -t menuconfig` targets the app; the bootloader's menuconfig target is prefixed with
  its image name (`mcuboot_menuconfig`), and sysbuild's own is `sysbuild_menuconfig`.
- `west debug --domain mcuboot` debugs MCUboot; `west flash` flashes each image in sequence.

## Partitions
MCUboot's Zephyr port expects these flash partitions in devicetree: `boot_partition` (MCUboot
itself), `slot0_partition` (primary slot of image 0) and `slot1_partition` (secondary slot); the
two slots must be contiguous. `scratch_partition` is only needed for swap-using-scratch, which
MCUboot's docs do not recommend (use swap-using-offset or swap-using-move; scratch is required
when the slots have different or non-uniform sector sizes). With more updateable images, further
slot pairs (`slot2_partition`, `slot3_partition` for image 1) are needed. If MCUboot is the first
stage, `boot_partition` must be where the SoC starts running out of reset.
The most memory-efficient swap-using-move layout makes the primary slot larger than the secondary
by exactly one sector plus the swap status area (MCUboot design doc).

## Gotchas
- Enlarge `boot_partition` when enabling serial recovery or heavier crypto; the application's slot
  addresses move with it, so rebuild both images.
- A sample key in the bootloader means anyone can sign images for it.
- Vendor forks (nRF Connect SDK) add their own SB_CONFIG options; follow their docs where they
  differ.

## Verify
- [ ] Both images are built and flashed by `west build --sysbuild` and `west flash`.
- [ ] `imgtool dumpinfo` on the signed application image shows the expected header and TLVs, and the device boots it.

## Checked
2026-10-31. Confirmed against the Zephyr sysbuild page (`sysbuild.conf`, `-DSB_CONF_FILE`, `sysbuild/<image>.conf`
and `.overlay`, configuration directory, FILE_SUFFIX, `mcuboot_menuconfig`, `sysbuild_menuconfig`, `--domain`),
Zephyr `share/sysbuild/images/bootloader/Kconfig` (mode and signature names, key defaults, key list), the MCUboot
Zephyr readme (partition names, contiguity, scratch advice) and the MCUboot design doc (move layout). Removed:
the build output file list and `merged.hex`, the devicetree example with addresses and `zephyr,code-partition`,
`-Dmcuboot_EXTRA_CONF_FILE`, `-Dmcuboot_DTC_OVERLAY_FILE`, `CONFIG_MCUBOOT_LOG_LEVEL`, the boot log strings and the
claim that fragments replace MCUboot's defaults (they are merged with them).
Method: documentation only; no commands were run.
