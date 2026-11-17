---
id: computing-software.systems-network-administration.linux.kernel-retention-and-old-kernel-removal
name: kernel-retention-and-old-kernel-removal
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kernel-upgrade, installonly-limit, kernel-retention, old-kernels, kernel-removal, full-boot-partition, apt-autoremove, dnf-remove-oldkernels, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Control how many kernels stay installed (dnf installonly_limit, apt autoremove) and safely remove old kernels to free /boot without deleting the one you are running."
sources:
  - https://dnf.readthedocs.io/en/latest/conf_ref.html
  - https://dnf.readthedocs.io/en/latest/command_ref.html
  - https://github.com/rpm-software-management/dnf5/blob/main/doc/commands/remove.8.rst
  - https://manpages.debian.org/unstable/apt/apt.conf.5.en.html
  - https://manpages.debian.org/unstable/apt/apt-mark.8.en.html
  - https://manpages.debian.org/unstable/apt/apt-get.8.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel retention and old-kernel removal

**Goal:** keep enough kernels to roll back (normally 2–3), never fill `/boot`, and never
remove the running kernel.

## 1. RHEL/Fedora (dnf)
```bash
grep installonly_limit /etc/dnf/dnf.conf      # dnf default is 3 (set explicitly if absent)
rpm -q kernel-core --last                    # installed, newest first
uname -r                                     # running — never remove this one
dnf remove --oldinstallonly --setopt installonly_limit=2 kernel   # dnf4: remove old installonly packages, keep latest versions and the running kernel
dnf5 remove --oldinstallonly --limit=2                              # dnf5: remove installonly packages beyond the limit; the running kernel is never removed
dnf remove $(dnf repoquery --installonly --latest-limit=-2 -q)     # dnf4 explicit form: list installed installonly packages except the 2 latest
```
`installonly_limit=N` is the number of installonly packages (kernels) allowed at once; dnf removes the oldest beyond it. The default is 3 and the minimum is 2; `1` is not allowed because of the running-kernel protection; `0` means unlimited (/boot will fill eventually).

## 2. Debian/Ubuntu (apt)
```bash
dpkg -l 'linux-image-*' | awk '/^ii/{print $2}'
apt autoremove --purge          # removes automatically installed packages no longer needed, with their config files
```
apt protects kernels from autoremove (`APT::Protect-Kernels`, default true) and keeps `APT::NeverAutoRemove::KernelCount` kernels (default 2): always the running kernel and the latest one, plus the second latest when they are the same (apt.conf(5)). Kernels marked manual (for example installed with `apt install linux-image-X`) are not autoremoved: `apt-mark auto linux-image-X` hands them back to autoremove. `apt-mark showmanual` shows what is marked manual.
Manual removal: `apt purge linux-image-6.5.0-14-generic linux-modules-6.5.0-14-generic`.

## 3. /boot is already 100% full
apt/dnf can fail half-way because the new initramfs can't be written.
```bash
df -h /boot; ls -la /boot
dpkg --purge linux-image-<old-version>        # dpkg works even with apt in broken state
apt -f install                                # then finish the interrupted transaction
rpm -e kernel-core-<old> kernel-modules-<old> kernel-<old>    # RHEL fallback when dnf can't solve
```
Delete stray files only if no package owns them (`rpm -qf` / `dpkg -S` says "not owned"), e.g.
old `initramfs-*kdump.img` for removed kernels.

## Gotchas
- Never `rm /boot/vmlinuz-*`: the package database still believes it is installed and will
  later try to configure it.
- Removing the kernel meta-package (for example `linux-image-generic` on Ubuntu) stops new kernels arriving.
- DKMS modules for removed kernels linger in `/var/lib/dkms`; `dkms status` shows them.
- Small `/boot` with a big initramfs (out-of-tree drivers, firmware): lower installonly_limit to 2, enlarge `/boot`, or choose a stronger initramfs compressor (`compress=` in dracut.conf(5), which accepts `xz`, `zstd` and others).

## Verify
- [ ] `df -h /boot` leaves room for at least one more kernel + initramfs (compare the size of one existing set).
- [ ] The running kernel and at least one fallback remain in the boot menu.
- [ ] The next kernel update completes without manual cleanup.

## Checked
Checked 2026-10-27 against the dnf 4 configuration and command references, the dnf5 `remove` command page (github.com/rpm-software-management/dnf5), the Debian apt.conf(5), apt-mark(8) and apt-get(8) manuals and dracut.conf(5).
- dnf `installonly_limit`: default 3, minimum 2, `0` unlimited, `1` not allowed (running-kernel protection); `dnf remove --oldinstallonly` keeps latest versions and the running kernel; `dnf repoquery --installonly --latest-limit=-N` skips the N latest; dnf5 has `remove --oldinstallonly [--limit=N]` and never removes the running kernel.
- apt: `APT::Protect-Kernels` (default true) and `APT::NeverAutoRemove::KernelCount` (default 2: running kernel and latest, or the second latest if they coincide); `apt-mark auto|manual|showmanual|hold`; `autoremove --purge`.
- dracut `compress=` accepts xz, zstd and others.
- Removed unconfirmed claims: the generated `01autoremove-kernels` protected-list wording, Ubuntu-specific hook behaviour and the /boot size figures.
Method: documentation only; no commands were run.
