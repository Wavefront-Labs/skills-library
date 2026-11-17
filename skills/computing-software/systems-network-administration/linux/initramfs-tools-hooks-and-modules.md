---
id: computing-software.systems-network-administration.linux.initramfs-tools-hooks-and-modules
name: initramfs-tools-hooks-and-modules
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, debian, ubuntu, initramfs-tools, initramfs-tools-hooks, update-initramfs, initramfs-modules, break-parameter, lsinitramfs]
level: practitioner
status: docs-checked
description: "Customise Debian/Ubuntu initramfs-tools: /etc/initramfs-tools/modules, hook and boot scripts with copy_exec, MODULES=most vs dep, break= debugging and lsinitramfs checks."
sources:
  - https://manpages.debian.org/bookworm/initramfs-tools-core/initramfs-tools.7.en.html
  - https://manpages.debian.org/bookworm/initramfs-tools-core/initramfs.conf.5.en.html
  - https://manpages.debian.org/bookworm/initramfs-tools/update-initramfs.8.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# initramfs-tools hooks and modules (Debian/Ubuntu)

## Force modules
`/etc/initramfs-tools/modules` — one module per line (with options): `nvme`, `dm_crypt`, `i915 modeset=1`.
`/etc/initramfs-tools/initramfs.conf`: `MODULES=most` (default, broad) vs `MODULES=dep` (guesses the modules
this machine needs and adds only those: smaller, but can break after hardware changes); `list` adds nothing beyond the
modules files, `netboot` skips block devices. `COMPRESS` picks the compression method (gzip is the fallback when the
chosen one is unsupported).

## Hook script (build time) — /etc/initramfs-tools/hooks/mytool
```sh
#!/bin/sh
PREREQ=""
prereqs() { echo "$PREREQ"; }
case "$1" in prereqs) prereqs; exit 0;; esac
. /usr/share/initramfs-tools/hook-functions
copy_exec /usr/sbin/mytool /sbin          # binary + libs
manual_add_modules usb_storage
cp /etc/mytool.conf "${DESTDIR}/etc/"
```
Keep the hook script executable.

## Boot script (runtime) — /etc/initramfs-tools/scripts/local-top/myscript
Same prereqs boilerplate, then `. /scripts/functions` and your code. Directories run in phases:
`init-top`, `init-premount`, `local-top` (before root device is looked for — unlock/assemble here),
`local-block` (retried while waiting for root), `local-premount`, `local-bottom`, `init-bottom`.

## Build and inspect
```bash
update-initramfs -u -k all        # rebuild all installed kernels
update-initramfs -c -k <kernel-version>   # create for one kernel
lsinitramfs /boot/initrd.img-$(uname -r) | grep mytool
unmkinitramfs /boot/initrd.img-$(uname -r) initramfs/   # full unpack (handles a prepended early initramfs)
```

## Debugging
Kernel args: `break=top|modules|premount|mount|mountroot|bottom|init` spawns a shell in the initramfs at that phase,
before its scripts run (default phase `premount`; several phases may be comma-separated); `debug` writes
`/run/initramfs/initramfs.debug` (`debug=vc` sends output to the console). `panic=<sec>` disables the debug shell, and
with both `panic` and `break` present the initramfs reboots instead of spawning a shell.

## Gotchas
- `rd.*` (dracut) parameters do nothing here.
- Check free space on `/boot` before rebuilding.

## Verify
- [ ] `lsinitramfs` shows your binary/module; reboot runs your script (add a `log_success_msg` line).

## Checked

Documentation check. Checked 2026-10-27 against Debian bookworm initramfs-tools(7), initramfs.conf(5), update-initramfs(8), lsinitramfs(8) and unmkinitramfs(8) (manpages.debian.org): `MODULES` values (`most` default, `dep`, `list`, `netboot`), `/etc/initramfs-tools/modules`, `copy_exec`, `manual_add_modules` and `DESTDIR` in hooks, the boot script phases including `local-block` retried until the device appears, `update-initramfs -u`, `-c -k`, `-k all`, the `break`, `debug` and `panic` parameters, and `unmkinitramfs` handling a prepended early initramfs. Removed the inverted claim that `panic=0` keeps the shell, the `zstd` value, the executable-bit rule, the Ubuntu dracut remark, the crypttab remark and the `rd.*` remark.
Method: documentation only; no commands were run.
