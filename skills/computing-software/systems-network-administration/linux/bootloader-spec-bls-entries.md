---
id: computing-software.systems-network-administration.linux.bootloader-spec-bls-entries
name: bootloader-spec-bls-entries
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, grub, bootloader-spec, blscfg, loader-entries, grubby, rhel, fedora, kernel-install]
level: practitioner
status: docs-checked
description: "Work with BootLoaderSpec entries in /boot/loader/entries on RHEL/Fedora: what blscfg does and editing options per kernel with grubby."
sources:
  - https://github.com/uapi-group/specifications/blob/main/specs/boot_loader_specification.md
  - https://cgit.git.savannah.gnu.org/cgit/grub.git/tree/docs/grub.texi
  - https://github.com/rhboot/grubby/blob/main/grubby.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BootLoaderSpec (BLS) entries

**Goal:** understand and safely change per-kernel boot entries on systems that use BLS entries with GRUB's `blscfg`
(RHEL 8+/Fedora), where entries are not listed in `grub.cfg`.

## How it works
- GRUB's `blscfg` command loads BLS entries from `/loader/entries` in the boot partition into the menu
  in memory; they do not update `grub.cfg` (GRUB manual). Entry files are named
  `<entry-token-or-machine-id>-<version>.conf` (BLS specification).
- `kernel-install` can write and remove those files through its `90-loaderentry.install` plugin.
```
title Red Hat Enterprise Linux (5.14.0-427.el9.x86_64) 9.4
version 5.14.0-427.el9.x86_64
linux /vmlinuz-5.14.0-427.el9.x86_64
initrd /initramfs-5.14.0-427.el9.x86_64.img
options root=/dev/mapper/rhel-root ro
```
Keys follow the BLS specification: `title`, `version`, `linux`, `initrd`, `options`, `machine-id`, `sort-key`.
Paths are relative to the boot partition.

## Change options: use grubby
```bash
grubby --info=ALL | grep -E '^(index|kernel|args)'
grubby --update-kernel=ALL --args="audit=1" --remove-args="rhgb quiet"
grubby --update-kernel=/boot/vmlinuz-$(uname -r) --args="systemd.log_level=debug"
grubby --set-default=/boot/vmlinuz-5.14.0-427.el9.x86_64 ; grubby --default-kernel
```
`--update-kernel` accepts a kernel path, an index, `ALL` or `DEFAULT` (grubby(8)).

## Gotchas
- Entry file names start with the entry token, which is the machine ID (`/etc/machine-id`) by default,
  so cloned images that keep one machine-id share the same token (BLS specification).
- Prefer `grubby` to hand-editing entry files.

## Verify
- [ ] `grubby --info=DEFAULT` shows the intended args; `cat /proc/cmdline` after reboot matches.
- [ ] Every `linux` path in `/boot/loader/entries/*.conf` exists.

## Checked
Checked 2026-10-26 against the UAPI Boot Loader Specification (uapi-group/specifications main), the GNU GRUB manual source (docs/grub.texi, blscfg section) and grubby(8) (rhboot/grubby).
Confirmed: BLS Type #1 entries as `.conf` files in `loader/entries` named `<entry-token-or-machine-id>-<version>.conf` with keys title, version, machine-id, sort-key, linux, initrd, options; GRUB `blscfg` loading entries into memory without touching `grub.cfg`; grubby `--info`, `--update-kernel` (path, index, ALL, DEFAULT), `--args`, `--remove-args`, `--set-default`, `--default-kernel`.
Removed as unconfirmed: the Red Hat grub_users/grub_arg/grub_class keys and tuned variables, grubenv notes, RHEL 9.3 behaviour, GRUB_ENABLE_BLSCFG, and orphan-entry behaviour.
Method: documentation only; no commands were run.
