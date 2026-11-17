---
id: computing-software.cloud-infrastructure-engineering.talos-linux.pxe-and-iso-bare-metal-boot
name: pxe-and-iso-bare-metal-boot
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [pxe, iso, bare-metal, maintenance-mode, ipxe, boot-order]
level: intro
status: docs-checked
description: "Boot Talos on bare metal from ISO or PXE: required kernel parameters, maintenance mode, disk-before-network boot order, the two ISO flavors and Image Factory PXE."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/platform-specific-installations/bare-metal-platforms/pxe.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/platform-specific-installations/bare-metal-platforms/iso.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
PXE: download the `vmlinuz` and `initramfs` assets from the Talos releases page, set machines to PXE boot (BIOS or UEFI, iPXE or not, depending on hardware) and pass at least these kernel parameters on first boot:

- `talos.platform=metal`
- `slab_nomerge`
- `pti=on`

Booted from the network with no machine configuration, Talos starts in maintenance mode; follow the getting started guide to install. If Talos is already on the disk, a network boot will boot into that installation, so the boot order should prefer disk over network. A metadata service can supply configuration per node:

```text
talos.config=https://metadata.service/talos/config?mac=${mac}
```

Other substitution variables are in the kernel reference. PXE booting can also be done via Image Factory.

ISO: images for `amd64` and `arm64` are on the releases page. Talos does not install to disk until a machine configuration is applied. As with PXE, an existing installation wins even if the ISO is attached, so prefer disk in the boot order or remove the ISO after install.

Two flavors:

- `metal-<arch>.iso` boots BIOS and UEFI systems (UEFI only for arm64).
- `metal-<arch>-secureboot.iso` boots UEFI in SecureBoot mode only, obtained via Image Factory.

## Checked

2026-11-04. Kernel parameters, maintenance mode, boot-order notes, talos.config example and ISO flavors confirmed on the PXE and ISO pages.

Method: documentation only; no commands were run.
