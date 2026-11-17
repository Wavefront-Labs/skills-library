---
id: computing-software.systems-network-administration.linux.kernel-install-and-boot-entries
name: kernel-install-and-boot-entries
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kernel-upgrade, kernel-install, installkernel, bls, boot-loader-spec, systemd-boot, uki, initramfs, postinst-kernel, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "How kernels reach the boot partition: kernel-install plugins, layouts and BLS entries, and fixing a kernel missing from the menu."
sources:
  - https://github.com/systemd/systemd/blob/main/man/kernel-install.xml
  - https://github.com/uapi-group/specifications/blob/main/specs/boot_loader_specification.md
  - https://github.com/dracut-ng/dracut-ng/tree/main/install.d
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kernel-install and boot entries

**Goal:** understand and repair the chain that turns "package installed a kernel" into
"bootloader shows it with a working initramfs".

## 1. The chain
- **systemd `kernel-install`:** `kernel-install add <version> <kernel-image> [initrd...]` runs every plugin in
  `/usr/lib/kernel/install.d/*.install` and `/etc/kernel/install.d/*.install` in lexicographic order (a file in
  `/etc` overrides one of the same name in `/usr/lib`; a symlink to `/dev/null` disables it).
  `50-depmod.install` runs depmod; `90-loaderentry.install` copies the kernel to
  `$BOOT/<entry-token>/<version>/linux` and writes `$BOOT/loader/entries/<entry-token>-<version>.conf`
  for the BLS layout. Initramfs generators such as dracut's `50-dracut.install` are separate plugins.
- Other distributions use their own hooks; read your distribution's documentation for them.

## 2. Inspect
```bash
kernel-install inspect                 # paths and parameters configured or auto-detected (systemd 251+)
ls /boot/loader/entries/; cat /boot/loader/entries/*$(uname -r).conf
cat /etc/kernel/cmdline 2>/dev/null    # kernel command line kernel-install uses for new entries
cat /etc/kernel/install.conf 2>/dev/null   # layout=bls|uki|other, initrd_generator=
```

## 3. Repair a kernel that isn't in the menu
```bash
kernel-install add 5.14.0-427.el9.x86_64 /lib/modules/5.14.0-427.el9.x86_64/vmlinuz
grubby --info=/boot/vmlinuz-5.14.0-427.el9.x86_64
```
Remove an entry the same way: `kernel-install remove <version>` (plugins run with `remove`, then
the entry directory `$BOOT/<entry-token>/<version>/` is deleted).

## 4. Custom hooks
Drop an executable named `NN-name.install` into `/etc/kernel/install.d/` — e.g. sign the kernel for Secure Boot or copy it to a
second ESP. Arguments: `add <version> <entry-dir> <kernel-image> [initrd...]` or `remove <version> <entry-dir>`.
Return 0 on success; 77 ends the whole operation (later plugins are skipped); any other non-zero status is reported as failure.

## Gotchas
- Entry names use the entry token (the machine ID by default, or the contents of `/etc/kernel/entry-token`), so a changed
  token means new entries are named differently from old ones.
- With the `uki` layout the UKI is copied under `ESP/EFI/Linux/`; `90-loaderentry.install` does nothing unless the layout is `bls`.

## Verify
- [ ] Every installed kernel has a matching entry and initramfs under the boot partition.
- [ ] The new initramfs can be listed (for dracut, `lsinitrd`).
- [ ] Reboot into the new kernel: `uname -r` matches.

## Checked
Checked 2026-10-26 against systemd man/kernel-install.xml (main), the UAPI Boot Loader Specification and the dracut-ng install.d directory.
Confirmed: plugin directories and ordering, `/etc` override and `/dev/null` masking, `add`/`remove`/`inspect` (inspect marked v251), plugin arguments, `50-depmod.install` and `90-loaderentry.install` behaviour, entry token default (machine ID) and `/etc/kernel/entry-token`, `KERNEL_INSTALL_LAYOUT` values and `layout=`/`initrd_generator=` in `install.conf`, `/etc/kernel/cmdline`, exit status 0 and 77, dracut's `50-dracut.install`.
Removed as unconfirmed: all Debian/Ubuntu chain claims (postinst.d, installkernel, update-initramfs), the make install note, full-/boot behaviour and machine-id regeneration advice.
Method: documentation only; no commands were run.
