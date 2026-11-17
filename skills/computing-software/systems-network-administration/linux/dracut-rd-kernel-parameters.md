---
id: computing-software.systems-network-administration.linux.dracut-rd-kernel-parameters
name: dracut-rd-kernel-parameters
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dracut, rd-cmdline, dracut-cmdline, rd-lvm-lv, rd-luks-uuid, rd-break, rd-shell, root-parameter, early-boot]
level: advanced
status: docs-checked
description: "Steer early boot with dracut kernel parameters: root=, rd.lvm.lv, rd.luks.uuid, rd.md, ip=, rd.neednet, rd.break points and rd.shell, with fixes for root not found."
sources:
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.cmdline.7.adoc
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.8.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dracut kernel command-line parameters

**Goal:** tell the initramfs exactly which devices to assemble and when to stop, so "dracut-initqueue
timeout / could not boot / /dev/mapper/rhel-root does not exist" becomes fixable.

## Root and storage
| Parameter | Meaning |
|---|---|
| `root=UUID=...` / `root=/dev/mapper/vg-root` | root device |
| `rootflags=<options>` / `rootfstype=<type>` | extra root mount options / filesystem type |
| `rd.lvm.lv=vg/root` (repeat) | only activate the logical volumes with the given name; can be given several times |
| `rd.lvm.vg=vg` | activate whole VG |
| `rd.luks.uuid=<luks-uuid>` | only activate LUKS devices with this UUID (a `luks-` prefix is stripped; the start of the UUID is enough) |
| `rd.luks.allow-discards=<luks-uuid>` | allow discards (TRIM) on that LUKS device |
| `rd.md.uuid=<md-uuid>` / `rd.md=0` | only activate raid sets with this UUID / disable MD RAID detection |
| `rd.multipath=default` / `rd.multipath=0` | use default multipath settings / disable multipath detection |
| `resume=UUID=<swap>` | resume from a swap partition |

## Network root / iSCSI / NFS
`ip=dhcp`, `ip=192.0.2.10::192.0.2.1:255.255.255.0:host:ens3:none`, `rd.neednet=1`,
`netroot=iscsi:<server>::::<target-iqn>` (as in the man page examples), `root=nfs:<server-ip>:<root-dir>[:<nfs-options>]`. The explicit `ip=` form is `<client-IP>:[<peer>]:<gateway-IP>:<netmask>:<hostname>:<interface>:{none|off|dhcp|on|any|dhcp6|auto6|ibft}`.

## Debug and stop points
- `rd.shell` allows dropping to a shell if root mounting fails; `rd.shell=0` disables it (`rd.emergency=reboot|poweroff|halt` then picks the action, and needs `rd.shell=0`).
- `rd.break` drops to a shell at the end; `rd.break=<point>` drops to a shell before that point starts (`cmdline`, `pre-udev`, `pre-trigger`, `initqueue`, `pre-mount`, `mount`, `pre-pivot`, `cleanup`); it can be given several times.
- `rd.debug` runs the dracut shell with `set -x`; `rd.udev.log_level=err|info|debug` raises udev logging.
- `rd.retry=<seconds>` is how long the initqueue is retried; `rd.timeout=<seconds>` is how long to wait for devices (default 0 = forever, and it should exceed `rd.retry`).
- `rd.driver.blacklist=<module>[,...]` skips a kernel module, `rd.driver.pre=<module>[,...]` forces loading one.

## Typical fix: renamed VG
After renaming the VG, `rd.lvm.lv=oldvg/root` still points at the old name → emergency shell.
At the boot loader menu edit the entry (for GRUB, press `e`), fix `root=` and `rd.lvm.lv=`, boot, then make it permanent with your distribution's kernel-argument tooling, fix `/etc/fstab`, and rebuild the images:
```bash
dracut -f --regenerate-all
```

## Gotchas
- Host-only images can embed host-specific arguments in `etc/cmdline.d` inside the initramfs (`hostonly_cmdline`); inspect with `lsinitrd -f`.
- `rootfstype=` defaults to "auto"; `rootflags=` overrides mount options otherwise parsed from the real root's `/etc/fstab`.

## Verify
- [ ] `cat /proc/cmdline` after boot matches; `lsblk` shows every expected LV/LUKS device opened.

## Checked
Checked 2026-10-25 against the dracut-ng man page sources (dracut-ng/dracut-ng man/*.adoc and doc_site, main as of 2026-10-24; latest release 112). Confirmed: every `rd.*`, `root*`, `resume=`, `ip=` and `netroot` parameter in the table, `rd.break=` point names and meaning, `rd.shell`/`rd.emergency`, `rd.timeout` default, `rd.driver.*`, `rd.udev.log_level`, and `etc/cmdline.d` host-only storage. Removed unconfirmed claims: RHEL default for `rd.shell`, `rd.luks.options` (not a documented parameter), the swap side effect of `rd.lvm.lv`, the `grubby` command and the Debian/Ubuntu note.

Method: documentation only; no commands were run.
