---
id: computing-software.firmware-embedded-development.bootloader-development.u-boot-standard-boot-bootstd
name: u-boot-standard-boot-bootstd
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [u-boot-bootstd, u-boot, extlinux-conf, bootflow, distro-boot, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use U-Boot standard boot (bootstd): bootdevs, bootmeths and bootflows, extlinux.conf and boot scripts, boot_targets ordering, and migrating from distro_bootcmd."
sources:
  - https://docs.u-boot.org/en/latest/develop/bootstd/overview.html
  - https://docs.u-boot.org/en/latest/usage/cmd/bootflow.html
  - https://uapi-group.org/specifications/specs/boot_loader_specification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Standard boot (bootstd and extlinux)

Standard boot replaces the old `distro_bootcmd` shell-script machinery. It scans devices natively
for bootable OS images instead of using scripts built from environment variables.

## Concepts
- **bootdev**: a device that can hold an OS (mmc0, usb, nvme, ethernet, spi flash).
- **bootmeth**: a method to find and boot an OS on a bootdev: `extlinux` (looks for
  `extlinux/extlinux.conf` on a filesystem), `script` (`boot.scr`), `efi`, `pxe`, `android`, `cros`,
  `vbe`. Some bootmeths (VBE, EFI boot manager) are "global": they pick the bootdev themselves.
- **bootflow**: a discovered (bootdev, partition, bootmeth) combination that can be booted.

## Commands
```
=> bootdev list -p             # probe and list devices
=> bootmeth list
=> bootflow scan -l            # scan and list bootflows found
=> bootflow list
=> bootflow select 0; bootflow info
=> bootflow boot
=> bootflow scan -lb           # scan and boot the first that works (what bootcmd normally does)
```
Ordering: the `bootmeths` environment variable (e.g. `env set bootmeths "extlinux efi"`; needs
`CONFIG_BOOTSTD_FULL`) and bootdev priority. The `boot_targets` variable is deprecated and, if
present, overrides the default order; remove it unless you need it. The one command needed to boot
is `bootflow scan -lb`.

## extlinux.conf example
```
# /boot/extlinux/extlinux.conf on the boot partition
default acme
timeout 1
label acme
    kernel /Image
    fdt /imx8mp-acme.dtb
    append console=ttymxc1,115200 root=/dev/mmcblk0p2 rootwait ro
```
Build systems and distros can generate this file; check yours rather than hand-writing it.

## Board configuration
`CONFIG_BOOTSTD` enables standard boot; `CONFIG_BOOTSTD_FULL` adds the full command set, more
error messages and `bootmeths` ordering; `CONFIG_BOOTSTD_DEFAULTS` and one option per bootmeth
(e.g. `CONFIG_BOOTMETH_EXTLINUX`, `CONFIG_BOOTMETH_EFILOADER`). Bootdevs come from the driver model
(each MMC/USB device gets a bootdev child). Boot-script compatible variables
(`kernel_addr_r`, `fdt_addr_r`, `ramdisk_addr_r`, `scriptaddr`, `pxefile_addr_r`) must be defined
in the board environment.

## A/B and custom logic
For A/B rootfs, keep using a `boot.scr` (script bootmeth) or implement the logic in board code
(VBE: Verified Boot for Embedded is the bootstd-native approach); extlinux alone has no fallback
counters.

## Verify
- [ ] `bootflow scan -l` lists the expected flows in the intended priority order.
- [ ] Removing the first boot device falls through to the next one automatically.

## Checked
2026-10-31. Confirmed against the U-Boot standard boot overview, the bootflow command page and boot/Kconfig on GitHub: bootdev/bootmeth/bootflow terms, `bootflow scan -lb`, `bootmeths`, deprecated `boot_targets`, CONFIG_BOOTSTD, BOOTSTD_FULL, BOOTSTD_DEFAULTS, BOOTMETH_EXTLINUX, BOOTMETH_EFILOADER, VBE. Removed the unverified removal dates, Yocto/Debian generator names, the example file paths and the EFI default filename.
Method: documentation only; no commands were run.
