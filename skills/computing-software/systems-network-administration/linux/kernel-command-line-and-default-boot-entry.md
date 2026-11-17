---
id: computing-software.systems-network-administration.linux.kernel-command-line-and-default-boot-entry
name: kernel-command-line-and-default-boot-entry
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, grub, grub2, kernel-cmdline, kernel-command-line, grubby, grub-default, saved-entry, grub-set-default, grub-reboot, bls, boot-entries, rhcsa, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Change kernel boot parameters once or permanently and choose the default boot entry with grubby (RHEL/Fedora BLS) or GRUB_DEFAULT/grub-set-default (Debian/Ubuntu)."
sources:
  - https://cgit.git.savannah.gnu.org/cgit/grub.git/tree/docs/grub.texi
  - https://github.com/rhboot/grubby/blob/main/grubby.8
  - https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/kernel-parameters.txt
  - https://github.com/torvalds/linux/blob/master/init/main.c
  - https://github.com/systemd/systemd/blob/main/man/kernel-install.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel command line and the default boot entry

**Goal:** add/remove a kernel parameter (once, for a test, or for every boot) and make the
right kernel boot by default — without hand-editing a generated `grub.cfg`.

## 1. What is running now
```bash
cat /proc/cmdline                      # the parameters this boot actually used
grubby --info=ALL | grep -E '^(index|kernel|args)'      # RHEL/Fedora: every BLS entry
grubby --default-kernel; grubby --default-index
ls /boot/loader/entries/               # BLS snippets (one file per kernel) on RHEL 8+/Fedora
grep -E '^GRUB_(DEFAULT|CMDLINE_LINUX)' /etc/default/grub
```

## 2. One-off test (nothing persists)
At the GRUB menu press `e`, find the line starting `linux`, append e.g.
`systemd.unit=rescue.target` or `nomodeset`, boot with **Ctrl-x**. Use this first for anything
that might stop the box booting.

## 3. Persistent parameters
**RHEL/Fedora/CentOS (grubby, BLS):**
```bash
grubby --update-kernel=ALL --args="audit=1 crashkernel=256M"
grubby --update-kernel=ALL --remove-args="rhgb quiet"
grubby --update-kernel=/boot/vmlinuz-$(uname -r) --args="intel_iommu=on"   # one kernel only
```
`ALL` updates the existing entries. How new kernels get their arguments depends on the setup (with systemd's
`kernel-install` it is `/etc/kernel/cmdline`); confirm the args survive the next kernel install (see Verify).

**Debian/Ubuntu:** edit `/etc/default/grub`:
```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"   # normal entries only
GRUB_CMDLINE_LINUX="audit=1"                # every entry including recovery
```
then regenerate the config with `grub-mkconfig -o /boot/grub/grub.cfg` (Debian-family systems wrap this as `update-grub`).

## 4. Choosing the default entry
**grubby:** `grubby --set-default=/boot/vmlinuz-<version>` or `--set-default-index=1`.
**GRUB_DEFAULT on Debian-style systems:**
```
GRUB_DEFAULT=saved          # remember what grub-set-default / grub-reboot chose
GRUB_SAVEDEFAULT=true       # optional: whatever the user picked last becomes default
```
```bash
grub-mkconfig -o /boot/grub/grub.cfg
grub-set-default 'Advanced options for Ubuntu>Ubuntu, with Linux 6.8.0-45-generic'   # persistent
grub-reboot 1 && reboot     # next boot only, then back to saved default (needs GRUB_DEFAULT=saved)
grub-editenv list           # shows saved_entry / next_entry
```
A submenu entry is identified by the number, title or id of each submenu from the top level, separated by `>`;
copy them from `grep -E "menuentry |submenu " /boot/grub/grub.cfg`. A numeric `GRUB_DEFAULT` counts entries
from zero and shifts when entries are added; the GRUB manual recommends an entry `--id` over a title, or `saved`.

## Gotchas
- Unknown parameters are not fatal: the kernel logs "Unknown kernel command line parameters ..., will be passed to
  user space" and carries on. Check `dmesg | grep -i 'unknown kernel command line'`.
- Removing `quiet` is the first step when a boot hangs without messages.
- `GRUB_TIMEOUT=0` boots immediately without showing the menu; with `GRUB_TIMEOUT_STYLE=hidden` or `countdown`, press Esc or F4, or hold Shift, during the timeout to see it (GRUB manual).

## Verify
- [ ] After reboot `cat /proc/cmdline` contains the new parameter and lacks the removed one.
- [ ] `grubby --default-kernel` / `grub-editenv list` names the intended kernel.
- [ ] Install or reinstall a kernel package and confirm the new entry also carries the args.

## Checked
Checked 2026-10-26 against the GNU GRUB manual source (docs/grub.texi, git master), grubby(8) (rhboot/grubby), the kernel's kernel-parameters.txt and init/main.c, and systemd kernel-install(8).
Confirmed: `e` and Ctrl-x editing; GRUB_DEFAULT (number, title, id or `saved`; id recommended over title), GRUB_SAVEDEFAULT, GRUB_CMDLINE_LINUX and GRUB_CMDLINE_LINUX_DEFAULT semantics, GRUB_TIMEOUT and GRUB_TIMEOUT_STYLE with Esc/F4/Shift, grub-set-default and grub-reboot with saved_entry/next_entry and submenu paths; grubby `--update-kernel`, `--args`, `--remove-args`, `--set-default`, `--set-default-index`, `--default-kernel`, `--default-index`; kernel parameters audit=, crashkernel=, intel_iommu=, nomodeset, quiet; the "Unknown kernel command line parameters ... passed to user space" message; `/etc/kernel/cmdline` for kernel-install.
Removed as unconfirmed: grub2-mkconfig --update-bls-cmdline, RHEL grub.cfg locations and stub, linuxefi, rhgb, and the update-grub wrapper claim (kept as a hedged note).
Method: documentation only; no commands were run.
