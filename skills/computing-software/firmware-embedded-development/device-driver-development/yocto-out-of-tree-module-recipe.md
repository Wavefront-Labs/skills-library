---
id: computing-software.firmware-embedded-development.device-driver-development.yocto-out-of-tree-module-recipe
name: yocto-out-of-tree-module-recipe
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [module-recipe, yocto, inherit-module, kernel-module, out-of-tree-module, kernel-module-autoload, rprovides, hello-mod, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Package an out-of-tree Linux driver in Yocto with inherit module: Makefile contract, kernel-module-* package naming, autoload and modprobe options, licensing and image inclusion."
sources:
  - https://docs.yoctoproject.org/kernel-dev/common.html
  - https://github.com/openembedded/openembedded-core/blob/master/meta/classes-recipe/module.bbclass
  - https://github.com/openembedded/openembedded-core/blob/master/meta/classes-recipe/kernel-module-split.bbclass
  - https://github.com/openembedded/openembedded-core/blob/master/meta-skeleton/recipes-kernel/hello-mod/hello-mod_0.1.bb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Out-of-tree module recipes

**Goal:** an external kernel driver built against the exact kernel in your image, packaged as
`kernel-module-<name>`, installed and loaded at boot.

## Recipe (recipes-kernel/foo-sensor/foo-sensor_1.0.bb)
```bitbake
SUMMARY = "Foo sensor IIO driver"
LICENSE = "GPL-2.0-only"
LIC_FILES_CHKSUM = "file://COPYING;md5=<md5 of your COPYING>"

inherit module

SRC_URI = "git://git.example.com/foo-sensor.git;protocol=https;branch=main"
SRCREV = "4f1c2e...full-sha"
S = "${WORKDIR}/git"

RPROVIDES:${PN} += "kernel-module-foo-sensor"
KERNEL_MODULE_AUTOLOAD += "foo-sensor"
KERNEL_MODULE_PROBECONF += "foo-sensor"
module_conf_foo-sensor = "options foo-sensor poll_ms=100"
```
For local sources use `SRC_URI = "file://Makefile file://foo-sensor.c file://COPYING"` and set
`S` to the unpack directory (the current OE-core `hello-mod` recipe uses `S = "${UNPACKDIR}"`; older releases
used `${WORKDIR}`, so check your release). Model it on `meta-skeleton/recipes-kernel/hello-mod` in OE-core.

## Makefile contract
The `module` class runs `make` with `KERNEL_SRC` (and `KERNEL_PATH`) pointing at the kernel
build tree, then `make modules_install`:
```make
obj-m := foo-sensor.o
SRC := $(shell pwd)
all:
	$(MAKE) -C $(KERNEL_SRC) M=$(SRC)
modules_install:
	$(MAKE) -C $(KERNEL_SRC) M=$(SRC) modules_install
clean:
	rm -f *.o *~ core .depend .*.cmd *.ko *.mod.c Module.symvers modules.order
```
A Kbuild-only tree works if it honours `KERNEL_SRC`; many upstream out-of-tree Makefiles use
`KDIR` - patch or pass `EXTRA_OEMAKE += "KDIR=${STAGING_KERNEL_DIR}"`.

## Packaging and install
- Modules are split into packages automatically. With the default `KERNEL_MODULE_PACKAGE_SUFFIX`
  (`-${KERNEL_VERSION}`) the package is `kernel-module-<name>-<kernel version>`, and
  `KERNEL_MODULE_PROVIDE_VIRTUAL` (default 1) makes it provide `kernel-module-<name>`. The recipe's own
  package (`${PN}`) is a meta package that depends on all its modules. Add to the image:
  `IMAGE_INSTALL:append = " kernel-module-foo-sensor"` or the recipe name.
- `KERNEL_MODULE_AUTOLOAD` writes `foo-sensor.conf` into `modules-load.d` (`/etc/modules-load.d`, or the
  `nonarch_libdir` one on systemd distros); skip it if the driver binds via devicetree `compatible` and
  udev/modalias autoloads it. `KERNEL_MODULE_PROBECONF` plus `module_conf_<name>` writes the `modprobe.d` file.
- Exported symbols for other external modules: the class installs `Module.symvers` under
  `${includedir}/${BPN}`; a dependent recipe lists the providing recipe in `DEPENDS` (names starting
  with `kernel-module-` get `KBUILD_EXTRA_SYMBOLS` set to its `Module.symvers`).

## Gotchas
- The module is tied to the kernel it is built against; the `module` class builds it against the staged
  kernel build output, so do not prebuild `.ko` files.
- GPL-incompatible licences taint the kernel and lose access to GPL-only symbols.
- A `LIC_FILES_CHKSUM` mismatch fails the build: recompute the checksum of the licence file (`md5sum COPYING`).

## Verify
- [ ] `oe-pkgdata-util list-pkg-files <module package>` shows the `.ko` under the modules directory.
- [ ] On target: `modinfo foo-sensor` vermagic matches `uname -r`; `lsmod` shows it after boot.

## Checked

2026-10-27, OpenEmbedded-Core master (module.bbclass, module-base.bbclass, kernel-module-split.bbclass, meta-skeleton hello-mod).
Confirmed in module.bbclass: EXTRA_OEMAKE gets KERNEL_SRC=${STAGING_KERNEL_DIR}, the compile step passes KERNEL_PATH, MODULES_INSTALL_TARGET defaults to modules_install, Module.symvers is installed under ${includedir}/${BPN}, KBUILD_EXTRA_SYMBOLS is set for DEPENDS entries starting with kernel-module-. Confirmed in kernel-module-split.bbclass: KERNEL_MODULE_AUTOLOAD writes a modules-load.d file (modulesloaddir), KERNEL_MODULE_PROBECONF with module_conf_<name> writes a modprobe.d file, KERNEL_MODULE_PACKAGE_SUFFIX default -${KERNEL_VERSION}, KERNEL_MODULE_PROVIDE_VIRTUAL default 1. Confirmed in hello-mod: inherit module, the Makefile contract (KERNEL_SRC, modules_install), RPROVIDES:${PN} += kernel-module-hello, S = UNPACKDIR. Confirmed in scripts/oe-pkgdata-util: list-pkg-files. Corrected the package naming (version suffix plus virtual provide), the autoload file location and the Module.symvers dependency example. Removed the example licence checksum, the scarthgap version gate and MACHINE_EXTRA_RRECOMMENDS because they were not confirmed.

Method: documentation only; no commands were run.
