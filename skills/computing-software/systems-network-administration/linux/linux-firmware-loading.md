---
id: computing-software.systems-network-administration.linux.linux-firmware-loading
name: linux-firmware-loading
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, linux-firmware, firmware-loading, direct-firmware-load-failed, iwlwifi, amdgpu, microcode, initramfs, lib-firmware]
level: practitioner
status: docs-checked
description: "Fix 'Direct firmware load failed' errors: how the kernel loads /lib/firmware blobs, linux-firmware packages, firmware in initramfs, CPU microcode and verifying versions."
sources:
  - https://docs.kernel.org/driver-api/firmware/fw_search_path.html
  - https://docs.kernel.org/arch/x86/microcode.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firmware loading

**Symptom:** `iwlwifi 0000:00:14.3: Direct firmware load for iwlwifi-so-a0-gf-a0-89.ucode failed with error -2`
and the device doesn't work (Wi-Fi, GPU, NIC, Bluetooth).

## How it works
Driver asks for a file name; kernel looks in `firmware_class.path=` first if set (also settable at run time via
`/sys/module/firmware_class/parameters/path`, up to 256 characters), then `/lib/firmware/updates/<kver>`,
`/lib/firmware/updates`, `/lib/firmware/<kver>`, `/lib/firmware`. Error `-2` = not found.
Drivers often try several versions — a failed newer name followed by a successful older one is normal.

## Install the blobs
Install the distribution's firmware package (commonly named `linux-firmware`, sometimes split per vendor or in a
non-free component); package names vary, so check your distribution's documentation.
Then reload: `modprobe -r iwlwifi && modprobe iwlwifi`, or reboot.

## Early-boot drivers need firmware in the initramfs
GPU (amdgpu/i915 KMS) and storage drivers load in the initramfs: rebuild it after installing firmware
with your distribution's initramfs tool (for example `dracut -f`) and list the image to confirm the blob is inside.

## CPU microcode
The kernel can apply microcode very early in boot from the initrd: an uncompressed cpio archive holding
`kernel/x86/microcode/GenuineIntel.bin` or `AuthenticAMD.bin` placed before the main initrd. Your distribution's
microcode package normally arranges this. Late loading is triggered with `echo 1 > /sys/devices/system/cpu/microcode/reload`;
check the kernel log (`journalctl -k | grep -i microcode`) for the result.

## Gotchas
- Compressed firmware (`.xz`/`.zst`) needs kernel support (`CONFIG_FW_LOADER_COMPRESS`, with XZ or ZSTD sub-options); check your kernel config.
- Copying a single blob by hand from linux-firmware.git works but is overwritten/unmanaged — prefer packages.
- Old firmware + new kernel can mismatch; update both together.

## Verify
- [ ] `journalctl -k -b | grep -i 'firmware'` shows no remaining load failure for the device, and the device works.

## Checked

Checked 2026-10-27 against Linux kernel documentation (firmware search paths, x86 microcode), firmware_loader Kconfig and dracut man page, current master, 2026-10-27. Confirmed: firmware search order and firmware_class.path (256-character limit, sysfs file), compression Kconfig options, early microcode initrd layout and reload file. Removed or softened: distribution package-name table, mkinitcpio and update-initramfs commands, lsinitrd usage, microcode package names, example log lines.

Method: documentation only; no commands were run.
