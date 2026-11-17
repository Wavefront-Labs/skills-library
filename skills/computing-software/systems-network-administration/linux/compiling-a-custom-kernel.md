---
id: computing-software.systems-network-administration.linux.compiling-a-custom-kernel
name: compiling-a-custom-kernel
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kernel, kernel-compile, menuconfig, localmodconfig, olddefconfig, make-modules-install, bindeb-pkg, binrpm-pkg, lpic-2]
level: advanced
status: docs-checked
description: "Configure and build a Linux kernel from source: olddefconfig from the running config, localmodconfig, menuconfig, building deb/rpm packages, install and boot safely."
sources:
  - https://docs.kernel.org/admin-guide/README.html
  - https://docs.kernel.org/kbuild/kconfig.html
  - https://docs.kernel.org/kbuild/kbuild.html
  - https://github.com/torvalds/linux/blob/master/scripts/Makefile.package
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compiling a custom kernel

**Goal:** a patched/newer/trimmed kernel installed as a package next to the distro one, with the
distro kernel kept as a fallback (LPIC-2 201.2).

## 1. Prepare
```bash
# build dependencies: see Documentation/process/changes.rst in the source tree for the required tool versions; package names are distro-specific
tar xf linux-6.10.tar.xz && cd linux-6.10        # verify the .tar.sign with gpg first
cp <config file of the running kernel> .config    # start from the running config (the location is distro-specific)
make olddefconfig                                  # set new symbols to their defaults without prompting
```
## 2. Adjust config
- `make localmodconfig` — creates a config from the current config and the loaded modules (`lsmod`), disabling module options not needed for them (plug in all devices first; pass `LSMOD=<file>` to build for another machine). Big build-time saving; dangerous for machines that later need other drivers.
- `make menuconfig` (ncurses), `make nconfig`, or `scripts/config --disable DEBUG_INFO_BTF --set-str LOCALVERSION "-custom"` (`scripts/config` offers `--enable`, `--disable`, `--module`, `--set-str`, `--set-val`).
- Distro configs may set `SYSTEM_TRUSTED_KEYS` and `SYSTEM_REVOCATION_KEYS` (filenames of PEM files) to certificates that are not in your tree; set them to empty strings if the build stops on them: `scripts/config --set-str SYSTEM_TRUSTED_KEYS "" --set-str SYSTEM_REVOCATION_KEYS ""`.

## 3. Build
```bash
make -j"$(nproc)" bindeb-pkg                            # binary Debian packages (image, headers)
make -j"$(nproc)" binrpm-pkg                            # binary RPMs, built under rpmbuild/
# traditional: make -j"$(nproc)" && sudo make modules_install && sudo make install
```
`make install` calls the `installkernel` script (kbuild's `INSTALLKERNEL`, default name `installkernel`) with the kernel version, image, map file and install path. What it does (copy to /boot, initramfs, bootloader entry) depends on your distribution's script; the kernel README says most distributions have a recognised one.

## 4. Boot safely
- Keep the distro kernel as default until the new one boots: `grub-reboot`/`grubby --set-default` only after testing.
- Out-of-tree modules (nvidia, zfs) need DKMS rebuild against the new headers.
- Secure Boot: if enabled, the new kernel image and modules must be signed with a key your firmware or shim trusts; follow your distro's Secure Boot documentation.

## Gotchas
- `make clean` removes most generated files but keeps the config; `make mrproper` also removes the config and backup files; `make distclean` adds editor backup and patch files.
- Debug info makes the build tree and packages much larger; disable it if you don't need it.
- Give the kernel a unique `LOCALVERSION` suffix (set it in the "General Setup" menu, as the README advises) so its release string, and its module directory, differ from the distro kernel's.

## Verify
- [ ] `uname -r` shows `-custom` after reboot; `dmesg -l err` has nothing new; the old kernel still in the menu.

## Checked
Checked 2026-10-27 against the Linux kernel source tree (github.com/torvalds/linux master): Documentation/admin-guide/README.rst, Documentation/kbuild/kconfig.rst, kbuild.rst, the top-level Makefile help text, scripts/config, scripts/Makefile.package, certs/Kconfig and lib/Kconfig.debug.
- `make olddefconfig`, `make localmodconfig` (with `LSMOD`), `menuconfig`, `nconfig`, `make modules_install install`, `make mrproper`; `clean` keeps the config while `mrproper` and `distclean` remove more.
- `bindeb-pkg` and `binrpm-pkg` targets exist; `SYSTEM_TRUSTED_KEYS` and `SYSTEM_REVOCATION_KEYS` are filename options; `DEBUG_INFO_BTF` exists; `scripts/config --set-str/--disable`.
- `INSTALLKERNEL` defaults to `installkernel`; the README says to use `LOCALVERSION` for a unique suffix.
- Removed unconfirmed claims: per-distro dependency package names, the `LOCALVERSION=` make argument, package output directories, the 10 GB build-size figure, and exact `make install` side effects.
Method: documentation only; no commands were run.
