---
id: computing-software.systems-network-administration.linux.kernel-headers-and-devel-packages
name: kernel-headers-and-devel-packages
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kernel-headers, kernel-devel, dkms, linux-headers, out-of-tree-module, build-symlink]
level: practitioner
status: docs-checked
description: "Install headers matching the running kernel for DKMS builds: kernel-devel vs kernel-headers on RHEL, linux-headers on Debian, the build symlink and mismatch fixes."
sources:
  - https://docs.kernel.org/kbuild/modules.html
  - https://src.fedoraproject.org/rpms/kernel/blob/rawhide/f/kernel.spec
  - https://packages.debian.org/stable/linux-headers-amd64
  - https://archlinux.org/packages/core/x86_64/linux-headers/
  - https://wiki.debian.org/KernelDKMS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matching kernel headers

**Symptom:** DKMS/vendor out-of-tree module builds fail because the build directory for the running kernel is missing, typically
`/lib/modules/<kver>/build: No such file or directory`. The kernel documentation builds external modules against the running kernel with `make -C /lib/modules/$(uname -r)/build M=$PWD`.

## The right package per distro
| Distro | For building modules | Note |
|---|---|---|
| RHEL/Fedora | `kernel-devel-$(uname -r)` | Fedora's kernel spec: `kernel-devel` provides "kernel headers and makefiles sufficient to build modules against the kernel package"; `kernel-headers` holds the C headers for the interface between the kernel and userspace libraries and programs (needed for rebuilding glibc), not for module builds |
| Debian | `linux-headers-<kernel release>` (for example the `linux-headers-amd64` meta-package, which tracks the current kernel) | Debian package names carry the architecture suffix, e.g. `linux-headers-6.12-amd64` |
| Debian derivatives | the headers package matching `uname -r` | check your distro's package search for the exact names, including for HWE or other kernel flavours |
| Arch | `linux-headers` (default kernel), `linux-lts-headers` (LTS kernel) | one headers package per kernel package |

```bash
dnf install "kernel-devel-uname-r == $(uname -r)"
apt install linux-headers-$(uname -r)
ls -l /lib/modules/$(uname -r)/build      # symlink to the installed kernel build tree (the target path is distro-specific)
```

## Mismatch: running kernel older than the newest installed
After `dnf update` the repo may no longer have devel for the running kernel. Options: reboot into the
newest kernel first (usually right), or look for the exact version with `dnf --showduplicates list kernel-devel`.
Install meta-packages so headers follow future kernel updates automatically, then DKMS builds on install.

## Gotchas
- Containers/CI building modules must target the HOST kernel's headers, not the container's distro.
- `/proc/version` shows the compiler that built the running kernel; compare it with the `gcc` used for module builds if out-of-tree builds fail unexpectedly.
- On Fedora-style systems `kernel-devel` carries `Provides: installonlypkg(kernel)` (kernel spec), so dnf treats it like the kernel itself and removes old ones according to `installonly_limit`.

## Verify
- [ ] `ls /lib/modules/$(uname -r)/build/Makefile` exists; `dkms status` shows modules `installed` for the running kernel.

## Checked
Checked 2026-10-27 against the kernel kbuild modules documentation, Fedora's kernel.spec (src.fedoraproject.org), the Debian and Arch package pages and the dnf documentation. The Red Hat knowledge-base link was replaced because that portal could not be read.
- docs.kernel.org: external modules are built against the running kernel with `make -C /lib/modules/$(uname -r)/build M=$PWD`.
- kernel.spec: `kernel-devel` description (headers and makefiles sufficient to build modules), `kernel-headers` description (C headers for the kernel/userspace interface, needed for rebuilding glibc), `Provides: kernel-devel-uname-r`, `Provides: installonlypkg(kernel)`.
- Debian package `linux-headers-amd64` and the `linux-headers-6.12-amd64` naming pattern exist; Arch has `linux-headers` and `linux-lts-headers` ("Headers and scripts for building modules for the LTS Linux kernel").
- Removed unconfirmed claims: literal DKMS error text, Ubuntu package names (packages.ubuntu.com returned HTTP 500), `/usr/src` target paths, the vault reference and the gcc-mismatch consequence statement.
Method: documentation only; no commands were run.
