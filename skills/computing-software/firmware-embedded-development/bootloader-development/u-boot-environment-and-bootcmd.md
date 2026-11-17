---
id: computing-software.firmware-embedded-development.bootloader-development.u-boot-environment-and-bootcmd
name: u-boot-environment-and-bootcmd
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [u-boot, bootcmd, u-boot-environment, fw-setenv, redundant-environment, bootcount, distro-boot, bootstd, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Control U-Boot boot flow with its environment: bootcmd scripting, redundant env storage, fw_setenv from Linux, bootcount/altbootcmd fallback and locking env in production."
sources:
  - https://docs.u-boot.org/en/latest/usage/environment.html
  - https://docs.u-boot.org/en/latest/api/bootcount.html
  - https://raw.githubusercontent.com/u-boot/u-boot/master/env/Kconfig
  - https://raw.githubusercontent.com/u-boot/u-boot/master/tools/env/fw_env.config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# U-Boot environment and bootcmd

**Goal:** a deterministic boot sequence for an embedded Linux board, with A/B fallback and an
environment that survives power loss and can't be tampered with in production.

## The environment
Key=value variables stored in flash/eMMC/SPI NOR (`CONFIG_ENV_IS_IN_MMC`, `CONFIG_ENV_IS_IN_SPI_FLASH`,
offset `CONFIG_ENV_OFFSET`, size `CONFIG_ENV_SIZE`). Defaults are compiled in from a board `.env`
file (named by `CONFIG_ENV_SOURCE_FILE`) or `CFG_EXTRA_ENV_SETTINGS` in the board header. At the prompt:
```
printenv bootcmd
setenv bootargs console=ttymxc0,115200 root=/dev/mmcblk2p2 rootwait ro
saveenv
```
`bootcmd` runs after `bootdelay` seconds unless a key is pressed (`bootdelay` 0 still allows
interrupting by key, -1 disables autoboot, -2 boots with no delay and no abort check).

## A typical A/B bootcmd
```
bootcmd=run boot_${slot}
boot_a=setenv bootargs ${common_args} root=/dev/mmcblk2p2; load mmc 2:2 ${loadaddr} /boot/fitImage; bootm ${loadaddr}
boot_b=setenv bootargs ${common_args} root=/dev/mmcblk2p3; load mmc 2:3 ${loadaddr} /boot/fitImage; bootm ${loadaddr}
altbootcmd=if test ${slot} = a; then setenv slot b; else setenv slot a; fi; saveenv; run bootcmd
```
With `CONFIG_BOOTCOUNT_LIMIT`, `bootcount` starts at 1 after a power-on reset and, while
`upgrade_available` is non-zero, increments on each reboot; when it exceeds `bootlimit` U-Boot
runs `altbootcmd` instead of `bootcmd`. If `bootlimit` is not defined the feature is off; if
`altbootcmd` is missing U-Boot stays in interactive mode. A userspace application must reset
`bootcount` (and `upgrade_available`) to 0 after a successful boot. That's the U-Boot side of rollback.

## Redundant environment
`CONFIG_ENV_REDUNDANT=y` with `CONFIG_ENV_OFFSET_REDUND` keeps a backup copy so there is a valid
copy if power fails during `saveenv`. Use it if anything writes the environment in the field.

## Linux access
`fw_printenv` / `fw_setenv` (U-Boot's `tools/env`, or the `libubootenv` library). Configure
`/etc/fw_env.config` with the **same** device, offset and size as U-Boot; with two entries the
second is the redundant copy. Block-device example from the U-Boot sample file (device, offset,
environment size):
```
/dev/mmcblk0   0xc0000    0x20000
```
A mismatch with U-Boot's layout reads or writes the wrong place.

## Standard boot / distro boot
Modern U-Boot uses **bootstd** (`bootflow scan`, `bootmeth`) to find `extlinux.conf` or boot
scripts on any device. For products, a fixed `bootcmd` is more predictable; bootstd is good for
general-purpose boards.

## Production hardening
- `CONFIG_ENV_WRITEABLE_LIST`: only variables with the `w` flag can be written at runtime; or
  `CONFIG_ENV_IS_NOWHERE` with compiled-in env plus a small separate state store.
- `bootdelay=-2` (no abort check); otherwise anyone on the serial console can change
  `bootargs`. The environment page lists the other autoboot-stop options.

## Verify
- [ ] Power-cut during `fw_setenv` 100 times: env always valid.
- [ ] Corrupt slot A kernel: after `bootlimit` attempts the board boots slot B.
- [ ] `fw_printenv` matches U-Boot's `printenv`.

## Checked
2026-10-31. Confirmed against the U-Boot environment and bootcount pages, env/Kconfig and tools/env/fw_env.config on GitHub: bootdelay values, bootcount/bootlimit/altbootcmd/upgrade_available behaviour, ENV_IS_IN_MMC/SPI_FLASH, ENV_OFFSET, ENV_SIZE, ENV_REDUNDANT, ENV_OFFSET_REDUND, ENV_WRITEABLE_LIST, ENV_IS_NOWHERE, two-entry fw_env.config. Corrected the redundant-environment symbol (was a misspelled legacy name), the extra-env symbol (now CFG_), and removed the RAUC/SWUpdate/Mender claim, the "Bad CRC" message, `CONFIG_ENV_FLAGS_LIST_STATIC` and `CONFIG_AUTOBOOT_KEYED`, which the fetched pages do not support.
Method: documentation only; no commands were run.
