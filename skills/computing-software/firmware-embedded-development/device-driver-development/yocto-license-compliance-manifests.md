---
id: computing-software.firmware-embedded-development.device-driver-development.yocto-license-compliance-manifests
name: yocto-license-compliance-manifests
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [license-manifest, yocto, incompatible-license, spdx-sbom, archiver, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Meet open-source licence obligations with Yocto: license manifests, INCOMPATIBLE_LICENSE for GPLv3-free images, archiver class for source release, and SPDX SBOM generation."
sources:
  - https://docs.yoctoproject.org/dev-manual/licenses.html
  - https://docs.yoctoproject.org/dev-manual/sbom.html
  - https://docs.yoctoproject.org/ref-manual/classes.html#archiver
  - https://docs.yoctoproject.org/ref-manual/variables.html#term-INCOMPATIBLE_LICENSE
  - https://docs.yoctoproject.org/migration-guides/migration-6.0.html
  - https://github.com/openembedded/openembedded-core/blob/master/meta/classes-recipe/license_image.bbclass
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# License compliance manifests

## What the build already records
Every image build writes a licence manifest under
`${DEPLOY_DIR}/licenses/${SSTATE_PKGARCH}/<image name>/` (the image name includes the machine and a
datestamp): `license.manifest` lists each installed package with its version, recipe and `LICENSE`
expression, and `package.manifest` lists the packages.
Ship licence texts in the image if required by the licence: with `COPY_LIC_MANIFEST = "1"`,
`COPY_LIC_DIRS = "1"` and `LICENSE_CREATE_PACKAGE = "1"` the image carries them, and the
licence files end up in `/usr/share/common-licenses` (and a second copy in `/usr/share/license`).

## Keep GPLv3 out of the image (common product requirement)
```bitbake
INCOMPATIBLE_LICENSE = "GPL-3.0* LGPL-3.0* AGPL-3.0*"   # global, or set it inside one image recipe
INCOMPATIBLE_LICENSE_EXCEPTIONS = "bash:GPL-3.0-only"   # package:SPDX-licence pairs, only if you accept it explicitly
```
Set globally, recipes that provide no alternative to the listed licences are skipped or fail; set in an
image recipe, it excludes packages from that image. This setting is the one the project regularly
tests; other values may need you to replace components (for example busybox for coreutils or bash,
gdbserver only in dev images).

## Source release for (L)GPL obligations
```bitbake
INHERIT += "archiver"
ARCHIVER_MODE[src] = "original"      # or "patched" (the default) or "configured"
ARCHIVER_MODE[diff] = "1"
COPYLEFT_LICENSE_INCLUDE = "GPL* LGPL*"
```
Check the deploy directory for the archives. Include build scripts/config needed to reproduce the
binaries (GPLv2 "complete corresponding source"), and for LGPL libraries allow relinking.

## SBOM
The build generates SPDX documents by default through the `create-spdx` class (inherited via
`INHERIT_DISTRO`; disable with `INHERIT_DISTRO:remove = "create-spdx"`). Yocto 6.0 removed SPDX 2.2
support, leaving SPDX 3.0. Building an image gives:
```
tmp/deploy/images/<machine>/acme-image-<machine>.spdx.json   # image SBOM
```
`SPDX_PRETTY` makes the JSON readable and `SPDX_INCLUDE_SOURCES` adds source-file descriptions.
The `cve-check` class was removed in Yocto 6.0; its replacement is the `sbom-cve-check` class, which
analyses the SPDX output with the external sbom-cve-check tool.

## Process
- Review `LICENSE` and `LIC_FILES_CHKSUM` for your own recipes; `CLOSED` for proprietary ones.
- `LICENSE_FLAGS_ACCEPTED` (for recipes whose `LICENSE_FLAGS` mark extra commercial licences, such as `commercial`) only
  after legal review; these are not legal advice and the final call belongs to counsel.
- Archive manifests, SBOM and sources for every release you ship.

## Verify
- [ ] Production image `license.manifest` contains no GPLv3 entries (if required).
- [ ] Source archive and SBOM stored with the release tag.

## Checked

Yocto Project documentation (docs.yoctoproject.org, development tip 6.1 after the 6.0 release) and OE-Core sources, read 2026-10-27.
Confirmed: manifest directory `${DEPLOY_DIR}/licenses/${SSTATE_PKGARCH}/<image name>` with `license.manifest` and `package.manifest` (license_image.bbclass, dev-manual/licenses); COPY_LIC_MANIFEST, COPY_LIC_DIRS, LICENSE_CREATE_PACKAGE and the /usr/share/common-licenses location; INCOMPATIBLE_LICENSE glob example, local-in-image use, and INCOMPATIBLE_LICENSE_EXCEPTIONS as package:licence pairs; ARCHIVER_MODE[src] values and `[diff]`, COPYLEFT_LICENSE_INCLUDE; create-spdx on by default, `<image>-<machine>.spdx.json` in tmp/deploy/images, SPDX_PRETTY and SPDX_INCLUDE_SOURCES.
Wrong or stale claims fixed: `cve-check` was removed in 6.0 (replaced by `sbom-cve-check`); SPDX 2.2 was removed in 6.0; `image_license.manifest` and the per-recipe licence path were not found in the classes or docs and were removed, as were the unconfirmed claims about `meta-gplv2`, the `tmp/deploy/spdx` and `tmp/deploy/sources` paths, and the `pn-` override on the exceptions variable.

Method: documentation only; no commands were run.
