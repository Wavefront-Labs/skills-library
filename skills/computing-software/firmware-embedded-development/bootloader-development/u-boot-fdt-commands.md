---
id: computing-software.firmware-embedded-development.bootloader-development.u-boot-fdt-commands
name: u-boot-fdt-commands
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [fdt-command, u-boot, device-tree-overlay, fdt-apply, boot-time-dt-fixup, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Inspect and modify the device tree in U-Boot before booting Linux: fdt addr/print/set, applying overlays with fdt apply, resizing, and board-code fixups."
sources:
  - https://docs.u-boot.org/en/latest/usage/cmd/fdt.html
  - https://docs.u-boot.org/en/latest/usage/fdt_overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Devicetree handling with fdt commands

## Load, inspect, modify
```
=> load mmc 0:1 ${fdt_addr_r} imx8mp-acme.dtb
=> fdt addr ${fdt_addr_r}
=> fdt resize 2000                       # extra room for edits/overlays; argument is hex
=> fdt print /soc@0/bus@30800000/i2c@30a20000
=> fdt list /chosen
=> fdt set /chosen bootargs "console=ttymxc1,115200 root=/dev/mmcblk2p2 rootwait"
=> fdt set /soc@0/.../uart@30880000 status okay
=> fdt rm /soc@0/.../gpu@38000000
=> fdt mknode / acme
=> fdt set /acme serial-number "SN12345"
=> booti ${kernel_addr_r} - ${fdt_addr_r}
```
Values: strings in quotes, cells as `<0x1 0x2>`, bytes as `[01 02]`.

## Overlays
Overlays (`.dtbo`) compiled with `dtc -@` so symbol information is present:
```
=> fdt addr ${fdt_addr_r}
=> fdt resize 8192
=> load mmc 0:1 ${fdtovaddr} overlays/acme-display.dtbo
=> fdt apply ${fdtovaddr}
```
Requirements: `CONFIG_OF_LIBFDT_OVERLAY`; the base DTB and every overlay compiled with `dtc -@`
(needs dtc 1.4.4 or newer). If `fdt apply` fails, both the base and the overlays are invalidated:
keep copies or reload them before retrying. Common pattern: list overlays in an environment
variable and loop over them in the boot script. FIT images can also carry overlays as separate
configurations, selected as `bootm <addr>#<config>#<config>`.

## Board code fixups (C)
For values known only at runtime (MAC addresses, memory size, board revision), implement
`ft_board_setup(void *blob, struct bd_info *bd)` and use
`fdt_status_disabled`, `do_fixup_by_path_u32` (declared in `fdt_support.h`).

## Debugging
- Linux boot messages and `/proc/device-tree/` show what the kernel actually received.
- `fdt print` right before `booti` confirms edits.

## Verify
- [ ] On target, `/proc/device-tree/chosen/bootargs` and overlay-enabled nodes match expectations.
- [ ] Boot script recovers (base DTB reloaded) when an overlay fails to apply.

## Checked

2026-10-28. Confirmed in the U-Boot fdt command page, fdt overlays page, cmd/fdt.c help text and lib/Kconfig: fdt addr/resize/apply/print/list/set/mknode/rm, resize argument is hex, `CONFIG_OF_LIBFDT_OVERLAY`, `dtc -@` requirement (dtc 1.4.4+), failed apply invalidates base and overlays, `bootm <addr>#<config>` selection, `ft_board_setup`, `fdt_status_disabled`, `do_fixup_by_path_u32`.
Removed: `DTC_FLAGS` kernel build variants, `CONFIG_OF_BOARD_SETUP`, the claim that U-Boot auto-fixes memory/MAC properties, `fdt_setprop`, and the `dmesg` and `dtc -I fs` tips (not in the fetched pages).

Method: documentation only; no commands were run.
