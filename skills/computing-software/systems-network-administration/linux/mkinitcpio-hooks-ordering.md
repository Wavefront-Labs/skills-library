---
id: computing-software.systems-network-administration.linux.mkinitcpio-hooks-ordering
name: mkinitcpio-hooks-ordering
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, arch-linux, mkinitcpio, mkinitcpio-hooks, sd-encrypt, initramfs, mkinitcpio-conf, uki]
level: practitioner
status: docs-checked
description: "Configure Arch mkinitcpio HOOKS: busybox udev vs systemd-based hooks, encrypt vs sd-encrypt, lvm2/mdadm placement, presets and rebuilding with mkinitcpio -P."
sources:
  - https://wiki.archlinux.org/title/Mkinitcpio
  - https://man.archlinux.org/man/mkinitcpio.8
  - https://wiki.archlinux.org/title/Dm-crypt/System_configuration
  - https://wiki.archlinux.org/title/Unified_kernel_image
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mkinitcpio HOOKS

**Goal:** an Arch initramfs that finds encrypted/LVM/RAID root on every boot.

## /etc/mkinitcpio.conf
Two styles — do not mix their hooks:
```
# systemd-based (the default style)
HOOKS=(base systemd autodetect microcode modconf kms keyboard sd-vconsole block sd-encrypt lvm2 filesystems fsck)
# busybox/udev-based
HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block encrypt lvm2 filesystems fsck)
```
Order matters: `keyboard` (and the console keymap hook) before the encryption hook so the passphrase can be typed;
`block` before `encrypt`/`sd-encrypt`; `autodetect` before the other subsystem hooks so they are trimmed (hooks placed
before it are installed in full).

| busybox | systemd equivalent | kernel parameter |
|---|---|---|
| `encrypt` | `sd-encrypt` | `cryptdevice=UUID=..:cryptroot` → `rd.luks.name=<uuid>=cryptroot` |
| `keymap`+`consolefont` | `sd-vconsole` | reads `/etc/vconsole.conf` |

`MODULES=(...)` forces modules (e.g. `nvidia` for early KMS); `FILES=(/crypto_keyfile.bin)` embeds files.

## Build
```bash
mkinitcpio -P                       # all presets in /etc/mkinitcpio.d/*.preset
mkinitcpio -p linux-lts
lsinitcpio -a /boot/initramfs-linux.img   # analyse contents
```
`autodetect` trims modules to the current hardware; the optional `fallback` preset image skips it. The fallback image
is disabled by default; enable it in the preset file if you want one for hardware changes.

## Gotchas
- Switching to `sd-encrypt` without changing `cryptdevice=` to `rd.luks.*` → no passphrase prompt.
- When the target system differs from the one running mkinitcpio, add the keyboard and filesystem modules needed to unlock and mount root to `MODULES`.
- UKIs: set `default_uki=` in the preset (for example `default_uki="esp/EFI/Linux/arch-linux.efi"`) to emit a unified kernel image.

## Verify
- [ ] `lsinitcpio /boot/initramfs-linux.img | grep -E 'cryptsetup|lvm'` shows the tools; reboot prompts for the passphrase and mounts root.

## Checked

Documentation check. Checked 2026-10-27 against the Arch wiki pages Mkinitcpio, Dm-crypt/System_configuration and Unified_kernel_image, and the mkinitcpio(8), mkinitcpio.conf(5) and lsinitcpio(1) man pages (man.archlinux.org), read 2026-10-27: that the systemd-based initramfs is the default style; both example HOOKS lines (identical to the dm-crypt page); `sd-vconsole`, `keymap`, `consolefont` and `encrypt` versus `sd-encrypt`; `cryptdevice=device:dmname` and `rd.luks.name`; `autodetect` placement; `-P`, `-p`, `lsinitcpio -a`, `FILES` and `MODULES`; fallback disabled by default; and `default_uki=` in a preset. Removed the 2023 date, the resume-in-systemd claim, the lvm2-after-encryption rule and the chroot and pacman-hook remarks.
Method: documentation only; no commands were run.
