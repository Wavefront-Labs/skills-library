---
id: computing-software.firmware-embedded-development.device-driver-development.yocto-image-recipes
name: yocto-image-recipes
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [image-recipe, yocto, image-install, image-features, packagegroup, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write a custom Yocto image recipe: inherit core-image, IMAGE_INSTALL vs IMAGE_FEATURES, packagegroups, fstypes and rootfs size, and keeping contents out of local.conf."
sources:
  - https://docs.yoctoproject.org/dev-manual/customizing-images.html
  - https://docs.yoctoproject.org/ref-manual/variables.html#term-IMAGE_INSTALL
  - https://docs.yoctoproject.org/ref-manual/features.html#image-features
  - https://docs.yoctoproject.org/migration-guides/migration-5.2.html
  - https://github.com/openembedded/openembedded-core/blob/master/meta/classes-recipe/core-image.bbclass
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image recipes and IMAGE_INSTALL

## A product image in your layer
```bitbake
# meta-acme/recipes-core/images/acme-image.bb
SUMMARY = "Acme gateway production image"
LICENSE = "MIT"
inherit core-image

IMAGE_FEATURES += "ssh-server-dropbear read-only-rootfs"
IMAGE_INSTALL += " \
    packagegroup-core-boot \
    packagegroup-acme-base \
    acme-app \
    kernel-module-acme-sensor \
    ${@bb.utils.contains('DISTRO_FEATURES', 'wifi', 'wpa-supplicant iw', '', d)} \
"
IMAGE_FSTYPES = "wic.zst ext4"
IMAGE_ROOTFS_EXTRA_SPACE = "131072"     # KiB
```
Create a development variant by requiring the base and adding debug features:
```bitbake
# acme-image-dev.bb
require acme-image.bb
IMAGE_FEATURES += "debug-tweaks tools-debug tools-profile dbg-pkgs"
```
(`debug-tweaks` was removed in Yocto 5.2 (walnascar). Where an image needs the same effect, add
`allow-empty-password allow-root-login empty-root-password post-install-logging` explicitly, and
keep them out of production images.)

## IMAGE_INSTALL vs IMAGE_FEATURES
- `IMAGE_INSTALL`: package names to install (and their runtime dependencies).
- `IMAGE_FEATURES`: named feature switches that expand to packages or rootfs tweaks
  (`ssh-server-openssh`, `package-management`, `read-only-rootfs`, `splash`).
- `CORE_IMAGE_EXTRA_INSTALL`: convenience hook for core-image based images, often in local.conf
  for quick experiments.

## Packagegroups
Group related packages in a recipe so images stay readable:
```bitbake
# packagegroup-acme-base.bb
inherit packagegroup
RDEPENDS:${PN} = "busybox chrony mosquitto-clients acme-config"
```

## Pitfalls
- `IMAGE_INSTALL:append = " foo"` in `local.conf` affects every image and isn't versioned with the
  product; put product contents in the image recipe.
- `IMAGE_INSTALL += ` inside an image that inherits `core-image` must come after `inherit`, or use
  `:append`; check with `bitbake -e acme-image | grep ^IMAGE_INSTALL=`.
- Kernel modules: install `kernel-module-<name>` packages (or `kernel-modules` for all); modules
  built in-tree as `=m` aren't installed automatically.
- Package names are not recipe names: `bitbake -e <recipe> | grep ^PACKAGES=` or `oe-pkgdata-util list-pkgs -p <recipe>`.

## Inspect the result
```sh
bitbake acme-image
cat tmp/deploy/images/<machine>/acme-image-<machine>.rootfs.manifest
buildhistory (INHERIT += "buildhistory") shows image content and size diffs per build
```

## Verify
- [ ] Manifest lists exactly the intended packages; no debug tools in the production image.
- [ ] Image boots on the target and runs `acme-app` on startup.

## Checked

Yocto Project documentation (docs.yoctoproject.org, development tip 6.1 after the 6.0 release) and OE-Core sources, read 2026-10-27.
Confirmed: the feature names ssh-server-dropbear, ssh-server-openssh, read-only-rootfs, package-management, splash, tools-debug, tools-profile, dbg-pkgs (ref-manual/features); core-image sets `IMAGE_INSTALL ?=` and `CORE_IMAGE_EXTRA_INSTALL ?= ""`, so `+=` after `inherit core-image` is correct; IMAGE_ROOTFS_EXTRA_SPACE is in Kbytes with default 0; `wic.zst` is a listed IMAGE_FSTYPES value; IMAGE_MANIFEST is `${IMAGE_NAME}${IMAGE_NAME_SUFFIX}.manifest`; `oe-pkgdata-util list-pkgs -p <recipe>`.
Wrong claim fixed: `debug-tweaks` was removed in 5.2 (the migration guide), not 5.0, and its replacement list now includes `post-install-logging`, as in that migration guide.

Method: documentation only; no commands were run.
