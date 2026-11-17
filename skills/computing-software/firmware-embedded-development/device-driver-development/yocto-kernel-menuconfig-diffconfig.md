---
id: computing-software.firmware-embedded-development.device-driver-development.yocto-kernel-menuconfig-diffconfig
name: yocto-kernel-menuconfig-diffconfig
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [kernel-diffconfig, yocto, menuconfig, config-fragment, kernel-configcheck, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Change Yocto kernel configuration properly: bitbake -c menuconfig, -c diffconfig to produce a .cfg fragment, adding it via bbappend, and checking with do_kernel_configcheck."
sources:
  - https://docs.yoctoproject.org/kernel-dev/common.html
  - https://github.com/openembedded/openembedded-core/blob/master/meta/classes-recipe/cml1.bbclass
  - https://github.com/openembedded/openembedded-core/blob/master/meta/classes-recipe/kernel-yocto.bbclass
  - https://github.com/openembedded/openembedded-core/blob/master/meta/classes-recipe/kernel.bbclass
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel config with menuconfig and diffconfig

Editing `.config` in `tmp/work` or running menuconfig and leaving it there loses the change on
the next clean build. Turn interactive changes into a **configuration fragment** in your layer.

## Workflow
```sh
bitbake virtual/kernel -c kernel_configme -f     # assemble the config from defconfig + fragments
bitbake virtual/kernel -c menuconfig             # interactive changes (opens a terminal)
bitbake virtual/kernel -c diffconfig             # writes fragment.cfg with only the differences
# output: ${WORKDIR}/fragment.cfg (the recipe's work directory)
```
Example fragment:
```
CONFIG_IIO=y
CONFIG_BME680=m
# CONFIG_WLAN is not set
```

## Add the fragment to the build
```bitbake
# meta-acme/recipes-kernel/linux/linux-yocto_%.bbappend  (or your BSP kernel recipe)
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI += "file://acme-sensors.cfg"
```
`.cfg` files in `SRC_URI` are processed as fragments by recipes that inherit `kernel-yocto` (linux-yocto and
many vendor kernels). For kernels that only use the plain `kernel` class (some vendor BSPs), provide a full
`defconfig` via `SRC_URI += "file://defconfig"`; the class copies it to `.config` if none exists. With
`kernel-yocto`, `KBUILD_DEFCONFIG` can name a defconfig in the kernel source tree.

## Validate
```sh
bitbake virtual/kernel -c kernel_configcheck -f
```
At the default `KCONF_AUDIT_LEVEL` of 1 it reports options that were specified but are not in the final
`.config` (for example a missing dependency or a renamed symbol); level 0 reports nothing and level 2
also reports non-hardware options set by a BSP. Set `KMETA_AUDIT_WERROR` to make audit warnings errors.
The task runs after `do_configure` and before `do_compile`.

## Inspect the final config
```sh
bitbake -e virtual/kernel | grep ^B=      # build dir
cat ${B}/.config | grep BME680
# on target (if CONFIG_IKCONFIG_PROC): zcat /proc/config.gz | grep BME680
```

## Tips
- One fragment per feature (`acme-sensors.cfg`, `acme-debug.cfg`) so variants can include subsets.
- Debug options (KASAN, lockdep) in a separate fragment, added only for development builds.
- Re-run `diffconfig` from a clean `kernel_configme` state, or the fragment includes changes made
  earlier in the same work dir.

## Verify
- [ ] Clean build (`bitbake -c cleansstate virtual/kernel && bitbake virtual/kernel`) contains the options.
- [ ] `kernel_configcheck` reports no missing options from your fragments.

## Checked

2026-10-27, OpenEmbedded-Core master (cml1.bbclass, kernel-yocto.bbclass, kernel.bbclass).
Confirmed in cml1.bbclass: do_menuconfig (opens a terminal, runs after do_configure) and do_diffconfig, which writes fragment.cfg into WORKDIR. Confirmed in kernel-yocto.bbclass: do_kernel_configme, do_kernel_configcheck (after do_configure, before do_compile), the meaning of KCONF_AUDIT_LEVEL 0, 1 and 2, KMETA_AUDIT, KMETA_AUDIT_WERROR, .cfg and .scc handling of SRC_URI entries, KBUILD_DEFCONFIG handling, and do_diffconfig being ordered after do_kernel_configme. Confirmed in kernel.bbclass: a defconfig in the unpack directory is copied to .config when none exists. Removed KERNEL_CONFIG_FRAGMENTS (not found in the classes) and replaced the fixed fragment output path. The fragment content example and the on-target /proc/config.gz line are generic Linux behaviour that was not checked here.

Method: documentation only; no commands were run.
