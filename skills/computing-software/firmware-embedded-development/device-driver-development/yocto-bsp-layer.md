---
id: computing-software.firmware-embedded-development.device-driver-development.yocto-bsp-layer
name: yocto-bsp-layer
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [bitbake-layer, yocto, bsp-layer, layer-conf, bitbake-layers, yocto-check-layer, layerseries-compat, openembedded, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Create a Yocto BSP layer for a custom board: bitbake-layers create-layer, layer.conf priority and compat, directory layout, layer dependencies, and yocto-check-layer validation."
sources:
  - https://docs.yoctoproject.org/dev-manual/layers.html
  - https://docs.yoctoproject.org/dev-manual/custom-template-configuration-directory.html
  - https://docs.yoctoproject.org/test-manual/yocto-project-compatible.html
  - https://github.com/openembedded/openembedded-core/blob/master/scripts/yocto-check-layer
  - https://github.com/openembedded/openembedded-core/blob/master/scripts/lib/checklayer/cases/bsp.py
  - https://github.com/openembedded/openembedded-core/blob/master/meta/lib/bblayers/templates/layer.conf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating a BSP layer

**Goal:** all board-specific metadata (machine config, kernel and bootloader changes,
firmware blobs) lives in one versioned layer on top of the vendor BSP, never as edits inside
poky or vendor layers.

## Create and add
```sh
source poky/oe-init-build-env build
bitbake-layers create-layer ../meta-myboard
bitbake-layers add-layer ../meta-myboard
bitbake-layers show-layers
```

## conf/layer.conf
```bitbake
BBPATH .= ":${LAYERDIR}"
BBFILES += "${LAYERDIR}/recipes-*/*/*.bb ${LAYERDIR}/recipes-*/*/*.bbappend"
BBFILE_COLLECTIONS += "myboard"
BBFILE_PATTERN_myboard = "^${LAYERDIR}/"
BBFILE_PRIORITY_myboard = "10"
LAYERDEPENDS_myboard = "core freescale-layer"
LAYERSERIES_COMPAT_myboard = "scarthgap"
```
- `LAYERSERIES_COMPAT` lists the lowercase release codename(s) the layer is compatible with; it lets
  the build detect layers not tested against a newer OE-Core release.
- Give it a `BBFILE_PRIORITY` above the vendor BSP layer: when same-named recipes exist in several
  layers the higher priority number wins. `bitbake-layers create-layer` defaults to 6.
- `LAYERDEPENDS` uses collection names (see each layer's `BBFILE_COLLECTIONS`).

## Layout
```
meta-myboard/
  conf/layer.conf
  conf/machine/myboard.conf            # see yocto-machine-configuration
  recipes-bsp/u-boot/u-boot-vendor_%.bbappend
  recipes-kernel/linux/linux-vendor_%.bbappend + files/*.patch, *.cfg, *.dts
  recipes-kernel/mydriver/mydriver_1.0.bb   # out-of-tree module
  recipes-core/images/myboard-image.bb
  wic/myboard.wks
  README  COPYING.MIT
```
Keep distro policy (init system, package format) out of the BSP layer: that belongs in a
distro layer; image recipes often in a separate product layer.

## Reproducible setup
Pin all layers by commit: `kas` YAML, `repo` manifest, or `bitbake-layers create-layers-setup`
(writes `setup-layers.json` and a `setup-layers` script that replays it). To ship build
configuration, keep a template under `conf/templates/<name>/` in the layer (`bitbake-layers
save-build-conf` creates one) and select it with the `TEMPLATECONF` environment variable.

## Validate
```sh
yocto-check-layer ../meta-myboard --dependency ../meta-freescale
bitbake-layers show-appends | grep myboard
bitbake-layers show-overlayed
```
For a BSP layer (one with `conf/machine`), `yocto-check-layer` checks that it defines machines, does
not change `MACHINE`, that `bitbake world` parses for each machine, and that selecting a machine
only changes signatures of tasks specific to that machine (use `:myboard` overrides). It does not
build anything.

## Verify
- [ ] `MACHINE=qemuarm64` build signatures unchanged with the layer added.
- [ ] `bitbake myboard-image` builds from a clean checkout using the pinned setup.

## Checked

Yocto Project documentation (docs.yoctoproject.org, development tip 6.1 after the 6.0 release), read 2026-10-27.
Confirmed: `bitbake-layers` subcommands create-layer, add-layer, show-layers, show-appends, show-overlayed and create-layers-setup (dev-manual/layers); the create-layer template in OE-Core (BBPATH, BBFILES `recipes-*/*/*.bb` and `.bbappend`, BBFILE_COLLECTIONS/PATTERN/PRIORITY, LAYERDEPENDS core, LAYERSERIES_COMPAT) and its default priority 6 and COPYING.MIT/README output; the meaning of LAYERSERIES_COMPAT in the BitBake manual; `yocto-check-layer` option `--dependency` and its BSP test cases (defines machines, MACHINE unchanged, world parse per machine, machine-specific signatures); `conf/templates/<name>` and TEMPLATECONF.
The `freescale-layer` collection name was read in the meta-freescale layer.conf. Removed the dead bsp-guide link, which now returns 404.

Method: documentation only; no commands were run.
