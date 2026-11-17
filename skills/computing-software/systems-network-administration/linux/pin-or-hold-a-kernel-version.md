---
id: computing-software.systems-network-administration.linux.pin-or-hold-a-kernel-version
name: pin-or-hold-a-kernel-version
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kernel-pin, kernel-hold, apt-mark-hold, dnf-versionlock, exclude-kernel, kernel-update, grubby]
level: practitioner
status: docs-checked
description: "Freeze the kernel on a known-good version: apt-mark hold on meta packages, dnf versionlock or exclude=kernel*, default boot entry pinning, and how to unpin safely later."
sources:
  - https://manpages.debian.org/stable/apt/apt-mark.8.en.html
  - https://dnf-plugins-core.readthedocs.io/en/latest/versionlock.html
  - https://dnf.readthedocs.io/en/latest/conf_ref.html
  - https://github.com/rhboot/grubby
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pinning a kernel version

**Goal:** stop kernel updates (driver certification, a regression, a vendor module) while still patching
the rest of the system — and remember to undo it.

## Debian/Ubuntu
```bash
apt-mark hold <kernel-meta-package>      # hold the package that tracks the latest kernel image
apt-mark hold linux-image-$(uname -r)    # hold the running kernel image package
apt-mark showhold
```
`apt-mark hold` marks a package as held back so it is not automatically installed, upgraded or removed (apt-mark(8)). Hold the meta package that pulls in new kernel versions as well as the versioned image.

## RHEL/Fedora
```bash
dnf install python3-dnf-plugin-versionlock           # dnf4 plugin; dnf5 has `dnf5 versionlock`
dnf versionlock add kernel-<version> kernel-core-<version> kernel-modules-<version>
dnf versionlock list
# blunt alternative (blocks all kernel updates): /etc/dnf/dnf.conf  ->  excludepkgs=kernel*   (alias: exclude=)
```
To boot a specific kernel by default: `grubby --set-default=<kernel-path>` (`grubby --default-kernel` prints the current default).
`installonly_limit` (default 3, minimum 2) controls how many kernels dnf keeps.

## Unpin
`apt-mark unhold ...`, `dnf versionlock delete ...` / remove the exclude, `grubby --set-default=<newest kernel>`.
Put a ticket/date on every pin — forgotten pins become years-old unpatched kernels.

## Gotchas
- `excludepkgs=` in a repo file only applies to that repo; the main-section option applies to all repos.
- Security exposure: document compensating controls for the pinned period.

## Verify
- [ ] `apt -s full-upgrade` / `dnf check-update kernel` proposes no kernel; `grubby --default-kernel` is the pinned one.

## Checked

Checked against apt-mark(8) (Debian/apt doc/, last commit 2025-11-10), dnf-plugins-core versionlock.rst, dnf4 conf_ref.rst (`excludepkgs`, `installonly_limit`) and grubby(8) (rhboot/grubby).
Confirmed: `apt-mark hold/unhold/showhold`, `dnf versionlock add/list/delete`, `excludepkgs` with its `exclude` alias, `installonly_limit` default 3 and minimum 2, `grubby --set-default` and `--default-kernel`.
Removed as unconfirmed: Ubuntu meta package names, example kernel version strings, the claim that unattended-upgrades and dnf-automatic respect holds, and the Livepatch/kpatch remark.

Method: documentation only; no commands were run.
