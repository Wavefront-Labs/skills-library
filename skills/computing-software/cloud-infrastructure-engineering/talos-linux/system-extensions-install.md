---
id: computing-software.cloud-infrastructure-engineering.talos-linux.system-extensions-install
name: system-extensions-install
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [system-extensions, installer, boot-assets, extension-tiers, unattendedinstallconfig, immutable-rootfs]
level: practitioner
status: docs-checked
description: "Install Talos system extensions via boot assets or a custom installer image: support tiers, ISO and disk-image flows, UnattendedInstallConfig, and talosctl get extensions."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/build-and-extend-talos/custom-images-and-development/system-extensions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
System extensions extend the immutable, read-only Talos root filesystem (container runtimes, firmware, drivers). They are activated only during install or upgrade. Installing them through the `.machine.install` section of the machine config is deprecated; since Talos 1.5 boot media is generated with extensions included.

Official extensions come in tiers: **core** (fully supported by Sidero Labs), **extra** (best effort) and **contrib** (community, disabled if it fails to build). The extension catalog is in the siderolabs/extensions repository.

Boot asset kinds: initial boot assets (ISO, PXE), disk images with Talos pre-installed, and `installer` container images. Depending on the extension (for example a network device driver or a containerd plugin), it may need to be in both the initial assets and the disk image or installer, or only in the installer.

ISO flow (NVIDIA example, installer only):

1. Boot a generic Talos ISO.
2. Build a custom `installer` image with the extension and push it to a registry.
3. Point `installer.image` in the `UnattendedInstallConfig` document at it.
4. Boot the ISO and apply the machine configuration; Talos pulls the installer, installs and reboots.

To upgrade, generate a new installer for the new Talos version and upgrade pointing to it.

Disk image flow (AWS): build an image with the extension, upload and register an AMI, launch from it. Upgrade by replacing the VM from a new AMI or in place with a custom installer.

List what is active:

```bash
talosctl get extensions
```

Authoring an extension means building a container image with a specific folder layout.

## Checked

2026-11-04. Tier table, install flows, UnattendedInstallConfig reference and talosctl get extensions confirmed on the System Extensions page.

Method: documentation only; no commands were run.
