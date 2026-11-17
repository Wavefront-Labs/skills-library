---
id: computing-software.systems-network-administration.linux.boot-previous-kernel-after-bad-update
name: boot-previous-kernel-after-bad-update
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kernel-rollback, boot-previous-kernel, grub-default-kernel, grubby, grub-reboot, kernel-regression, remote-console, rhcsa, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Recover from a kernel update that breaks boot, drivers or performance: pick the old kernel at GRUB or remotely, pin it as default, and hold the bad version until fixed."
sources:
  - https://github.com/rhboot/grub2/blob/master/docs/grub.texi
  - https://src.fedoraproject.org/rpms/grubby/blob/rawhide/f/grubby.8
  - https://dnf.readthedocs.io/en/latest/conf_ref.html
  - https://manpages.debian.org/unstable/apt/apt-mark.8.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Boot the previous kernel after a bad update

**Goal:** get back to the last good kernel quickly, make that stick across reboots, and keep
the package manager from bringing the bad one back until a fix ships.

## 1. At the console
- GRUB menu hidden? Press **Esc** or **F4**, or hold **Shift**, during the timeout and GRUB shows the menu (GRUB manual, `GRUB_TIMEOUT_STYLE`).
- Debian/Ubuntu: usually *Advanced options for …* → the older `linux-image` entry.
- RHEL/Fedora: entries are typically listed newest first; pick an older one.
- Cloud VMs without a console: use the provider's serial console or boot diagnostics, or detach the root disk to a rescue VM.

## 2. Remotely, before a risky reboot
```bash
# Debian/Ubuntu (needs GRUB_DEFAULT=saved in /etc/default/grub, then regenerate grub.cfg once)
grep -E "menuentry '|submenu '" /boot/grub/grub.cfg | cut -d"'" -f2
grub-reboot 'Advanced options for Ubuntu>Ubuntu, with Linux 6.8.0-40-generic'   # next boot only
# RHEL/Fedora
grubby --info=ALL | grep -E '^(index|kernel)'
grub2-reboot 1                                  # boot entry index 1 once (also needs GRUB_DEFAULT=saved; check /etc/default/grub)
```
`grub-reboot` sets GRUB's `next_entry` for the next boot only; GRUB clears it after use, so a hang in the new kernel falls back to the saved default on the next power cycle.

## 3. Make the old kernel the default
```bash
grubby --set-default=/boot/vmlinuz-5.14.0-362.el9.x86_64          # RHEL/Fedora
grub-set-default 'Advanced options for Ubuntu>Ubuntu, with Linux 6.8.0-40-generic'   # stored in the saved_entry variable (needs GRUB_DEFAULT=saved)
```
Then stop updates from reinstalling or removing it:
```bash
dnf versionlock add kernel-core-5.14.0-362.el9 || echo 'excludepkgs=kernel*' >> /etc/dnf/dnf.conf
apt-mark hold linux-image-generic linux-headers-generic       # stop the meta-package moving on
apt-mark manual linux-image-6.8.0-40-generic                    # keep autoremove from deleting it
```
`installonly_limit` (dnf, default 3) and apt autoremove (which keeps the running and the latest kernel) may otherwise delete the good kernel once enough
newer ones arrive and you are not running it.

## 4. Diagnose the bad one
```bash
journalctl --list-boots; journalctl -b -1 -p err      # previous boot's errors
journalctl -k -b -1 | grep -iE 'fail|error|taint'
```
Common causes: out-of-tree module (NVIDIA, ZFS, VirtualBox) not rebuilt by DKMS for the new
version (`dkms status`), initramfs missing a driver, Secure Boot rejecting an unsigned module.

## Gotchas
- Deleting `/boot/vmlinuz-*` by hand leaves orphaned package records; remove via the package
  manager.
- `GRUB_DEFAULT=0` boots the first menu entry, which is normally the newest kernel after the next update.
- Unpin and test each new kernel release; holding forever means missed security fixes.

## Verify
- [ ] `uname -r` shows the good version after a full reboot.
- [ ] `grubby --default-kernel` / `grub-editenv list` points at it.
- [ ] Next `dnf upgrade`/`apt upgrade` neither removes it nor changes the default.

## Checked
Checked 2026-10-27 against the GRUB manual source (texinfo in github.com/rhboot/grub2), the Fedora grubby(8) man page, the dnf configuration reference and the Debian apt-mark(8) and apt.conf(5) manuals. The gnu.org GRUB manual and Red Hat portal pages could not be read, so the replaced source links point to the mirrored source files.
- GRUB: `GRUB_DEFAULT` accepts a number, an entry id or `saved`; Esc/F4 or holding Shift shows a hidden menu; `grub-set-default` writes `saved_entry`; `grub-reboot` sets `next_entry`, cleared after use; `grub-editenv` manages the environment block.
- grubby: `--info=` accepts `ALL`, `--set-default=<kernel-path>`, `--default-kernel`.
- dnf: `installonly_limit` default 3; `excludepkgs` is the option name for excluding packages; `dnf versionlock` is a plugin command.
- apt: `apt-mark hold` and `manual`; autoremove keeps the running and latest kernel (`APT::NeverAutoRemove::KernelCount`).
- Removed unconfirmed claims: vendor CLI commands for console access, the "RHEL default is GRUB_DEFAULT=saved" statement, and the `update-grub` step after `grub-set-default`.
Method: documentation only; no commands were run.
