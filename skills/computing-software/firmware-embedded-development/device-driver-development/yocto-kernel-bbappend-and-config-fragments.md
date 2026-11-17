---
id: computing-software.firmware-embedded-development.device-driver-development.yocto-kernel-bbappend-and-config-fragments
name: yocto-kernel-bbappend-and-config-fragments
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [bbappend, yocto, kernel-config-fragment, linux-yocto, filesextrapaths, diffconfig, kernel-patches, custom-device-tree, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Customise the Yocto kernel from your layer: linux bbappend with FILESEXTRAPATHS, patches and .cfg fragments, menuconfig/diffconfig, custom DTS, and checking the config was applied."
sources:
  - https://docs.yoctoproject.org/kernel-dev/common.html
  - https://github.com/openembedded/openembedded-core/blob/master/meta/classes-recipe/kernel-yocto.bbclass
  - https://github.com/openembedded/openembedded-core/blob/master/meta/classes-recipe/kernel-devicetree.bbclass
  - https://github.com/openembedded/bitbake/blob/master/doc/bitbake-user-manual/bitbake-user-manual-fetching.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel bbappend patches and config fragments

**Goal:** kernel driver patches, config options and device trees for your board applied from a
bbappend in your BSP layer, surviving vendor BSP upgrades.

## The bbappend
`meta-myboard/recipes-kernel/linux/linux-yocto_%.bbappend` (match the actual kernel recipe
name: `linux-imx`, `linux-raspberrypi`, `linux-ti-staging`...; `bitbake -e virtual/kernel | grep ^PN=`):
```bitbake
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI:append:myboard = " \
    file://0001-iio-add-foo-sensor-driver.patch \
    file://foo-sensor.cfg \
    file://myboard.dts;subdir=git/arch/arm64/boot/dts/myvendor \
"
KERNEL_DEVICETREE:append:myboard = " myvendor/myboard.dtb"
```
- `FILESEXTRAPATHS` tells the fetcher where your `files/` directory is.
- Machine override (`:myboard`) keeps other machines unaffected.
- Generate patches with `git format-patch` against the exact kernel commit the recipe uses (`SRCREV`).

## Config fragments
`files/foo-sensor.cfg`:
```
CONFIG_IIO=y
CONFIG_FOO_SENSOR=m
# CONFIG_DEBUG_INFO is not set
```
- `linux-yocto` and recipes inheriting `kernel-yocto` merge `.cfg` files from SRC_URI with
  `merge_config.sh`. Vendor kernels that only use a `defconfig` may ignore fragments - then
  provide `file://defconfig` instead (check the recipe).
- Generate a fragment from interactive changes:
```sh
bitbake -c kernel_configme -f virtual/kernel
bitbake -c menuconfig virtual/kernel
bitbake -c diffconfig virtual/kernel     # writes fragment.cfg into ${WORKDIR}
```
- Options whose dependencies are unmet are silently dropped. Check with
  `bitbake -c kernel_configcheck -f virtual/kernel` (warnings list requested vs actual values).

## Inspect the result
```sh
bitbake -c compile -f virtual/kernel && bitbake virtual/kernel
grep FOO_SENSOR tmp/work/*/linux-*/*/build/.config
```
On target: `zcat /proc/config.gz` (needs `CONFIG_IKCONFIG_PROC`).

## Gotchas
- `SRC_URI +=` in a bbappend with a non-override form applies to all machines - fine for shared
  fixes, wrong for board-only changes.
- For iterative driver development use `devtool modify` (see `yocto-devtool-modify-workflow`),
  then turn the result into patches here.

## Verify
- [ ] `.config` contains each fragment option with the intended value.
- [ ] `bitbake-layers show-appends` lists your bbappend against the kernel recipe.

## Checked

2026-10-27, OpenEmbedded-Core and BitBake master.
Confirmed in kernel-yocto.bbclass: .cfg and .scc files in SRC_URI are processed, merge_config is used, do_kernel_configme, do_kernel_configcheck, and do_diffconfig runs after do_kernel_configme. Confirmed in cml1.bbclass: do_menuconfig and do_diffconfig writing fragment.cfg to WORKDIR. Confirmed in the BitBake fetching manual: the subdir URL parameter unpacks into a subdirectory. Confirmed in kernel-devicetree.bbclass: KERNEL_DEVICETREE is the device tree variable. Confirmed in bitbake lib/bblayers/query.py: show-appends. Removed the claim that the colon and := forms are required, the SRC_URI patch ordering claim and the rebuild-trigger claim, which were not confirmed. The FILESEXTRAPATHS:prepend := "...:" form is used in OE-Core recipes (util-linux.inc) and the layerappend selftest.

Method: documentation only; no commands were run.
