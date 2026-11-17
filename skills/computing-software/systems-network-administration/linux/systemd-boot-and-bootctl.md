---
id: computing-software.systems-network-administration.linux.systemd-boot-and-bootctl
name: systemd-boot-and-bootctl
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, bootctl, systemd-boot, uefi, esp, loader-conf, boot-loader-entries, uki]
level: practitioner
status: docs-checked
description: "Install and run systemd-boot on UEFI: bootctl install/update/status, loader.conf, entry files, default/oneshot entries and recovering when the ESP is full or the entry vanishes."
sources:
  - https://github.com/systemd/systemd/blob/main/man/bootctl.xml
  - https://github.com/systemd/systemd/blob/main/man/loader.conf.xml
  - https://github.com/systemd/systemd/blob/main/man/systemd-boot.xml
  - https://github.com/systemd/systemd/blob/main/man/systemctl.xml
  - https://github.com/uapi-group/specifications/blob/main/specs/boot_loader_specification.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# systemd-boot with bootctl

**Goal:** a simple UEFI-only boot manager that reads BLS entry files from the ESP (or XBOOTLDR).

## Install and inspect
```bash
bootctl install                   # installs systemd-boot to the ESP (also as the fallback ESP/EFI/BOOT/BOOT*.EFI), adds it to the top of the firmware boot list
bootctl status                    # firmware, Secure Boot state, current entry, ESP path
bootctl list                      # entries found (Type #1 .conf and Type #2 UKIs in EFI/Linux/)
bootctl update                    # updates installed copies if the available version is newer
```
The BLS specification prefers the ESP mounted at `/efi` (`/boot/efi` is traditional but discouraged); `--esp-path=` overrides detection.

## Configuration
`<ESP>/loader/loader.conf`:
```
default  arch.conf          # or glob: default @saved / default *lts*
timeout  3
console-mode max
editor   no                 # disable kernel cmdline editing at the menu (security)
```
`<ESP>/loader/entries/arch.conf`:
```
title   Arch Linux
linux   /vmlinuz-linux
initrd  /intel-ucode.img
initrd  /initramfs-linux.img
options root=UUID=<root-uuid> rw quiet
```
Type #1 entries and the files they reference live on the ESP or the XBOOTLDR partition (BLS specification).

## Day-to-day
```bash
bootctl set-default arch-lts.conf
bootctl set-oneshot arch-fallback.conf   # next boot only (great for testing)
systemctl reboot --boot-loader-entry=arch-lts.conf
systemctl reboot --firmware-setup
```
At the menu: `e` edits the kernel command line (the editor is enabled by default), `t`/`T` change the timeout, `D` makes the selected entry the default and `d` the preferred entry (systemd 260+).

## Gotchas
- The BLS specification suggests an ESP of at least 1G when it is used as `$BOOT`.
- Kernels and initrds have to be copied into `$BOOT`; `kernel-install` does this with `90-loaderentry.install`.
- `bootctl install` also stores a copy as the fallback loader `ESP/EFI/BOOT/BOOT*.EFI`, which firmware can still find if its boot list is reset.

## Verify
- [ ] `bootctl status` shows `Current Boot Loader: systemd-boot` and the expected default entry.
- [ ] `bootctl list` shows the entries you expect.

## Checked
Checked 2026-10-26 against systemd man pages (bootctl, loader.conf, systemd-boot, systemctl; main) and the UAPI Boot Loader Specification.
Confirmed: `bootctl status`, `list`, `install` and `update` behaviour, `set-default`, `set-oneshot`, `--esp-path=`; loader.conf `default` (glob and `@saved`), `timeout`, `console-mode max`, `editor`; Type #1 entries and Type #2 UKIs in `EFI/Linux`; menu keys e, t, T, D, d (d and D from v260); `systemctl reboot --boot-loader-entry=` and `--firmware-setup`; fallback `EFI/BOOT/BOOT*.EFI`; spec guidance for `/efi` mounting and 1G ESP.
Wrong in the draft: `d` is not "set default" (D sets the default, d the preferred entry, since v260).
Removed as unconfirmed: the FAT-only statement, sbctl/shim advice, systemd-boot-update.service, 100 MB ESP figure and the missing-files check.
Method: documentation only; no commands were run.
