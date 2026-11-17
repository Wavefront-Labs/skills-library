---
id: computing-software.firmware-embedded-development.device-driver-development.dkms-module-packaging
name: dkms-module-packaging
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [dkms, linux-kernel-module, dkms-conf, kernel-upgrade, deb-packaging, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Package an out-of-tree kernel module with DKMS so it rebuilds on every kernel upgrade: dkms.conf, add/build/install, signing hooks, and shipping it in a .deb or .rpm."
sources:
  - https://github.com/dell/dkms
  - https://github.com/dell/dkms/blob/master/dkms.8.in
  - https://github.com/dell/dkms/blob/master/dkms_framework.conf.in
  - https://manpages.debian.org/bookworm/dh-dkms/dh_dkms.1.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DKMS packaging

DKMS (Dynamic Kernel Module Support) keeps module sources in `/usr/src/<name>-<version>` and
rebuilds them automatically when new kernel headers are installed. Use it for drivers shipped to
general-purpose Linux machines (PCs, x86/ARM gateways running distro kernels). Embedded images
built with Yocto/Buildroot should build modules in the image recipe instead.

## Layout and dkms.conf
```
/usr/src/mydrv-1.2.0/
  dkms.conf
  Makefile        # standard Kbuild wrapper: obj-m := mydrv.o
  mydrv.c
```
```sh
PACKAGE_NAME="mydrv"
PACKAGE_VERSION="1.2.0"
BUILT_MODULE_NAME[0]="mydrv"
DEST_MODULE_LOCATION[0]="/updates/dkms"
MAKE[0]="make -C ${kernel_source_dir} M=${dkms_tree}/${PACKAGE_NAME}/${PACKAGE_VERSION}/build modules"
CLEAN="make -C ${kernel_source_dir} M=${dkms_tree}/${PACKAGE_NAME}/${PACKAGE_VERSION}/build clean"
AUTOINSTALL="yes"
# BUILD_EXCLUSIVE_KERNEL="^6\.(1|6|8)\."   # restrict to kernels you support
```

## Workflow
```sh
sudo dkms add -m mydrv -v 1.2.0          # registers /usr/src/mydrv-1.2.0
sudo dkms build -m mydrv -v 1.2.0        # for the running kernel (-k <ver> for others)
sudo dkms install -m mydrv -v 1.2.0
dkms status                              # mydrv/1.2.0, 6.8.0-45-generic, x86_64: installed
sudo dkms remove -m mydrv -v 1.2.0 --all
```
The build directory is `/var/lib/dkms/mydrv/1.2.0/build/`; look there for build output. After every kernel
upgrade check `dkms status`: a module that failed to build is missing for the new kernel.

## Packaging
- Debian/Ubuntu: `dh_dkms` (from the `dh-dkms` package) sets up the postinst and postrm scripts and the
  dependencies, and installs `debian/<package>.dkms` as `dkms.conf`.
- Other distributions: follow their packaging policy for DKMS packages.
- Depend on `dkms` and the kernel headers package for each installed kernel.
- Current `dkms(8)` lists these commands: add, remove, build, unbuild, install, uninstall, match, mktarball,
  ldtarball, status, autoinstall, generate_mok. It has no `mkdeb`, `mkrpm` or `mkbmdeb` commands.

## Secure Boot
With Secure Boot, modules must be signed. DKMS signs with the key and certificate named by
`mok_signing_key` and `mok_certificate` in `/etc/dkms/framework.conf` (the shipped example uses
`/var/lib/dkms/mok.key` and `mok.pub`; if the files do not exist DKMS re-creates both). `dkms generate_mok`
creates them. Enrol the certificate in the firmware's key database as your distribution describes; the
enrolment step is not covered by the DKMS documents.

## Kernel API churn
Guard API differences with `LINUX_VERSION_CODE`/`KERNEL_VERSION(6,4,0)` checks; test against the
oldest and newest kernels you support in CI (build against several header packages).

## Verify
- [ ] Install the package, upgrade the kernel, reboot: `dkms status` shows the module installed for the new kernel and it loads.
- [ ] Builds cleanly against every kernel series listed as supported.

## Checked

2026-10-27, dell/dkms master (dkms.8.in and dkms_framework.conf.in) and the Debian bookworm dh_dkms manual page.
Confirmed in dkms.8.in: sources in /usr/src/<module>-<module-version>/, the build directory /var/lib/dkms/<module>/<module-version>/build/, the command list above (no mkdeb, mkrpm or mkbmdeb), dkms.conf directives BUILT_MODULE_NAME[], DEST_MODULE_LOCATION[], MAKE[0], AUTOINSTALL, BUILD_EXCLUSIVE_KERNEL (a regular expression), and the variables $kernel_source_dir and dkms_tree. Confirmed in dkms_framework.conf.in: mok_signing_key and mok_certificate, defaults under /var/lib/dkms, files re-created if missing. Confirmed in the dh_dkms page: it sets up postinst and postrm scripts and installs debian/<package>.dkms as dkms.conf. Removed the dkms mkdeb command (not present), the make.log file name, the claim that failed autoinstalls do not block kernel upgrades, the Fedora and RHEL packaging advice, the headers meta-package name, and the shim-signed MOK path and mokutil step.

Method: documentation only; no commands were run.
