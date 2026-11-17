---
id: computing-software.systems-network-administration.linux.kexec-fast-reboot
name: kexec-fast-reboot
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kexec-reboot, kexec-load, kexec-tools, systemctl-kexec, fast-reboot, kernel-upgrade]
level: advanced
status: docs-checked
description: "Reboot into a new kernel without firmware POST using kexec: kexec -l with the right initrd and cmdline, systemctl kexec, when hardware breaks, and verifying the switch."
sources:
  - https://man7.org/linux/man-pages/man8/kexec.8.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
  - https://wiki.archlinux.org/title/Kexec
  - https://github.com/horms/kexec-tools/blob/master/kexec/kexec.8
  - https://github.com/systemd/systemd/blob/main/man/systemctl.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kexec fast reboot

**Goal:** apply a kernel update on a big server whose firmware POST takes 5–10 minutes, by loading
the new kernel from the running one and jumping into it.

## Steps
```bash
dnf install kexec-tools        # or your distribution's kexec-tools package
KVER=<new-kernel-version>
kexec -l /boot/vmlinuz-$KVER --initrd=/boot/initramfs-$KVER.img --reuse-cmdline
#   or --command-line="$(cat /proc/cmdline)" ; edit it if the new kernel needs other args
cat /sys/kernel/kexec/loaded    # 1 (older kernels: /sys/kernel/kexec_loaded, deprecated)
systemctl kexec                 # clean shutdown of services, then jump
```
`kexec -e` runs the loaded kernel **without** calling shutdown(8), so services are not stopped — only for emergencies.
Unload a staged kernel: `kexec -u`.
`-s` selects the newer kexec_file_load syscall and `-c` the old kexec_load; which one your kernel allows depends on its Secure Boot and lockdown policy.
With a kernel loaded, a plain `systemctl reboot` also performs a kexec unless `SYSTEMCTL_SKIP_AUTO_KEXEC=1` is set.

## When not to
- A kexec skips firmware initialisation, so changes that need a firmware reset do not apply.
- Hardware that does not reinitialise cleanly can hang or lose devices; test per hardware model.
- With a kernel loaded, `systemctl reboot` turns into a kexec — surprising for operators expecting a full reset.

## Relationship to kdump
kdump uses `kexec -p` (`--load-panic`) to preload a crash kernel into reserved memory; a normal kexec reboot is separate.

## Verify
- [ ] `uname -r` shows the new version and `journalctl --list-boots` shows a new boot.
- [ ] Devices and storage all present (`lsblk`, `ip link`) — compare with pre-reboot inventory.

## Checked

Checked against the kexec-tools `kexec(8)` man source, the systemd `systemctl` man source and the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (ABI testing and obsolete kexec sysfs) on 2026-10-26. Confirmed: `-l`, `-p`, `-u`, `-e`, `-s` (KEXEC_FILE_LOAD), `-c` (KEXEC_LOAD), `--initrd=`, `--reuse-cmdline`, `--command-line`, `-e` runs without shutdown(8), `systemctl kexec`, auto-kexec on reboot with `SYSTEMCTL_SKIP_AUTO_KEXEC=1` opt-out, `/sys/kernel/kexec/loaded` (old `/sys/kernel/kexec_loaded` is obsolete). Removed: example kernel version, Debian `LOAD_KEXEC`, firmware-update and BMC claims.

Method: documentation only; no commands were run.
