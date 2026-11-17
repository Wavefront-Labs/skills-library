---
id: computing-software.firmware-embedded-development.device-driver-development.yocto-machine-configuration
name: yocto-machine-configuration
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [machine-configuration, yocto, machine-conf, preferred-provider, kernel-devicetree, serial-consoles, machine-features, wic, defaulttune, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write a Yocto machine .conf for a custom board: SoC include, tune, kernel and bootloader providers, device trees, serial console, MACHINE_FEATURES and WIC layout."
sources:
  - https://docs.yoctoproject.org/dev-manual/new-machine.html
  - https://docs.yoctoproject.org/ref-manual/variables.html
  - https://docs.yoctoproject.org/dev-manual/wic.html
  - https://docs.yoctoproject.org/ref-manual/kickstart.html
  - https://docs.yoctoproject.org/migration-guides/migration-5.3.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Machine configuration

**Goal:** `MACHINE = "myboard"` selects the right CPU tune, kernel, bootloader, device tree,
console and image format for your hardware.

## conf/machine/myboard.conf
```bitbake
#@TYPE: Machine
#@NAME: My Board (i.MX8M Mini)
#@DESCRIPTION: Custom carrier board based on i.MX8MM

require conf/machine/include/imx8mm-evk.inc      # reuse the closest reference board/SoC include

KERNEL_DEVICETREE = "imx8mm-myboard.dtb"
UBOOT_CONFIG ??= "sd"
UBOOT_CONFIG[sd] = "imx8mm_myboard_defconfig"
PREFERRED_PROVIDER_virtual/kernel = "linux-vendor"
PREFERRED_PROVIDER_virtual/bootloader = "u-boot-vendor"

SERIAL_CONSOLES = "115200;ttymxc1"
MACHINE_FEATURES:append = " wifi bluetooth"
MACHINE_FEATURES:remove = "alsa"
MACHINE_EXTRA_RRECOMMENDS += "linux-firmware-wifi kernel-module-foo-sensor"

IMAGE_FSTYPES = "wic.zst wic.bmap"
WKS_FILE = "myboard.wks"
```
- Start from the SoC include or the evaluation board conf the vendor supports; derive rather
  than copy so BSP updates flow in.
- Generic (non-vendor) boards pick the CPU via a tune include:
  `require conf/machine/include/arm/armv8a/tune-cortexa53.inc` (paths vary by release;
  older: `conf/machine/include/tune-cortexa53.inc`), `DEFAULTTUNE` to select a variant.
- The root name of the file is the machine name (`myboard.conf` is `MACHINE = "myboard"`), and the
  machine is part of `MACHINEOVERRIDES`, so `:myboard` overrides apply.
- `MACHINEOVERRIDES =. "mx8mm:"` adds an override for the SoC family; `SOC_FAMILY` (a colon-separated
  list, needs `conf/machine/include/soc-family.inc`) does the same for families. Vendor includes
  usually set these.

## Key variables
| Variable | Purpose |
|---|---|
| `KERNEL_IMAGETYPE` | `Image`, `zImage`, `fitImage` |
| `KERNEL_DEVICETREE` | dtb file name(s) to build and deploy (a full path is legacy; the bare `.dtb` name is preferred) |
| `UBOOT_MACHINE` / `UBOOT_CONFIG` | U-Boot defconfig, or several via `UBOOT_CONFIG[name]` flags (each must set `UBOOT_MACHINE`; extras `UBOOT_CONFIG_BINARY`, `UBOOT_CONFIG_IMAGE_FSTYPES`) |
| `SERIAL_CONSOLES` | getty on the debug UART (`baud;tty`) |
| `MACHINE_FEATURES` | hardware capabilities gating packages (wifi, bluetooth, usbhost, pci) |
| `MACHINE_ESSENTIAL_EXTRA_RDEPENDS` | packages needed to boot (firmware loaders) |
| `IMAGE_BOOT_FILES` | files copied to the boot partition by wic's `bootimg_partition` plugin (names looked up in `DEPLOY_DIR_IMAGE`; `src;dest` renames) |

## WIC kickstart (wic/myboard.wks)
```
part u-boot --source rawcopy --sourceparams="file=imx-boot" --ondisk mmcblk --no-table --align 33
part /boot --source bootimg_partition --ondisk mmcblk --fstype=vfat --label boot --align 4096 --size 64
part / --source rootfs --ondisk mmcblk --fstype=ext4 --label root --align 4096
bootloader --ptable msdos
```

## Verify
- [ ] `bitbake -e core-image-minimal | grep -E '^(MACHINE|TUNE_FEATURES|PREFERRED_PROVIDER_virtual/kernel)='` shows intended values.
- [ ] Image boots to a login on the configured serial console.

## Checked

Yocto Project documentation (docs.yoctoproject.org, development tip 6.1 after the 6.0 release) and OE-Core sources, read 2026-10-27.
Confirmed: machine name is the root name of the machine .conf (dev-manual/new-machine); the important variables TARGET_ARCH, PREFERRED_PROVIDER_virtual/kernel, MACHINE_FEATURES, SERIAL_CONSOLES format `baud;tty` with space-separated entries, KERNEL_IMAGETYPE, IMAGE_FSTYPES; UBOOT_CONFIG flag form and its companion variables; MACHINE_ESSENTIAL_EXTRA_RDEPENDS; IMAGE_BOOT_FILES; MACHINEOVERRIDES `=.` prefix form with a trailing colon; SOC_FAMILY and soc-family.inc; `tune-cortexa53.inc` under conf/machine/include/arm/armv8a; wic.bmap conversion type; kickstart `--align` in KBytes, `--no-table`, `--ptable msdos`, rawcopy with `--sourceparams`.
Stale claim fixed: the WIC source plugin `bootimg-partition` was renamed `bootimg_partition` in 5.3 (the migration guide; dashes are auto-converted for upstream plugins). Removed the unsupported rule about underscores in machine names, the legacy comma form of UBOOT_CONFIG, and the dead bsp-guide link. Recipe names such as linux-vendor, u-boot-vendor and linux-firmware-wifi are placeholders for your vendor BSP recipes; `conf/machine/include/imx8mm-evk.inc` exists in meta-freescale.

Method: documentation only; no commands were run.
