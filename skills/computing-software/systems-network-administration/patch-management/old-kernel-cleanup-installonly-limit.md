---
id: computing-software.systems-network-administration.patch-management.old-kernel-cleanup-installonly-limit
name: old-kernel-cleanup-installonly-limit
category: computing-software
field: systems-network-administration
product: patch-management
tags: [installonly-limit, old-kernels, linux-patching, boot-partition, apt-autoremove, dnf]
level: practitioner
status: docs-checked
description: "Keep /boot from filling with old kernels: dnf installonly_limit, package-cleanup and dnf remove --oldinstallonly, apt autoremove behaviour, and keeping a known-good fallback."
sources:
  - https://dnf.readthedocs.io/en/latest/conf_ref.html
  - https://dnf.readthedocs.io/en/latest/command_ref.html
  - https://manpages.debian.org/stable/apt/apt-get.8.en.html
  - https://github.com/mvo5/unattended-upgrades/blob/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Old kernel cleanup

A full `/boot` makes the next kernel update fail half-way (initramfs not generated) and the
host may not boot the new kernel. Typical on small (500 MB-1 GB) `/boot` partitions.

## RHEL family
Kernels are "install-only" packages: each update adds one.
```ini
# /etc/dnf/dnf.conf
installonly_limit=3        # default 3; minimum 2; 0 = unlimited; 1 is not allowed
```
Remove extras now (`--oldinstallonly` keeps only the latest versions and the running kernel;
the retained count follows `installonly_limit`):
```sh
dnf remove --oldinstallonly --setopt installonly_limit=2
rpm -q kernel-core; df -h /boot
```

## Debian/Ubuntu
```sh
apt autoremove --purge          # removes automatically installed packages no longer needed, including old kernels
dpkg -l 'linux-image-*' | awk '/^ii/{print $2}'
```
unattended-upgrades can remove unused kernel packages before upgrading, to avoid filling
`/boot`: `Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";` (the README lists the
default as true).
If `/boot` is already 100% full and apt is broken: remove one old kernel with
`dpkg --purge linux-image-<old-version>-generic` (never the running one, check `uname -r`),
then `apt -f install`.

## Keep a fallback
Always keep at least one previous known-good kernel until the new one has run through a
reboot and a business day. Don't set installonly_limit=1.

## Monitoring
Alert when `/boot` usage crosses a threshold you choose (for example 80%).

## Gotchas
- Livepatch/kpatch module packages and kernel-devel/headers also accumulate; remove with
  matching versions.
- Removing the running kernel's modules package breaks module loading until reboot.

## Verify
`/boot` usage below threshold, at least two bootable kernels present (`ls /boot/vmlinuz-*`), next kernel update completes and initramfs exists for it.

## Checked

Checked 2026-10-27 against the DNF configuration and command references, the Debian apt-get manual page and the unattended-upgrades README.
- `installonly_limit` default 3, minimum 2, 0 means unlimited, 1 is explicitly not allowed: confirmed.
- `dnf remove --oldinstallonly` keeps the latest versions and the running kernel: confirmed.
- `apt-get autoremove` removes automatically installed packages no longer needed; unattended-upgrades `Remove-Unused-Kernel-Packages` (default True): confirmed.
- Removed unconfirmed: EL7 `package-cleanup`, the `01autoremove-kernels` rule description and "+1 previous" count, Proxmox ESP check, `grubby` check.
Method: documentation only; no commands were run.
