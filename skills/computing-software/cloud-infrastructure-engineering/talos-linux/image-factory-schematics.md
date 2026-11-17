---
id: computing-software.cloud-infrastructure-engineering.talos-linux.image-factory-schematics
name: image-factory-schematics
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [image-factory, schematic, installer-image, extensions, kernel-args, meta]
level: practitioner
status: docs-checked
description: "Use Image Factory schematics: customization YAML, content-addressed IDs, uploading with curl, model frontends (ISO, PXE, installer), schematic ID lookup and restrictions."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/learn-more/image-factory.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/platform-specific-installations/boot-assets.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Image Factory (public at factory.talos.dev) generates Talos assets from a **schematic**, a YAML customization. A schematic applied to a Talos version, type and architecture yields a **model**: ISO, kernel/initramfs, UKI, cloud disk images or `installer` images, served over HTTP, PXE or a container registry.

```yaml
customization:
  extraKernelArgs: # optional
    - vga=791
  meta: # optional, allows to set initial Talos META
    - key: 0xa
      value: "{}"
  systemExtensions: # optional
    officialExtensions: # optional
      - siderolabs/gvisor
      - siderolabs/amd-ucode
overlay: # optional
  name: rpi_generic
  image: siderolabs/sbc-raspberry-pi
  options: # optional, any valid yaml, depends on the overlay implementation
    data: "mydata"
```

The two pages disagree on the Raspberry Pi overlay image: the Image Factory page example uses `siderolabs/sbc-raspberry-pi`, while the Boot Assets page's Raspberry Pi schematic uses `siderolabs/sbc-raspberrypi` (and its imager example uses `ghcr.io/siderolabs/sbc-raspberrypi`). Confirm the overlay name in the Image Factory UI before use.

Schematics are content-addressable, so identical content gives the same ID. The empty ("vanilla") schematic ID is `376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba`. Upload one:

```shell
curl -X POST --data-binary @schematic.yaml https://factory.talos.dev/schematics
```

The installer image form is `factory.talos.dev/metal-installer/<schematic-id>:<version>`; extension versions are chosen automatically to match the Talos release. Upgrade or change extensions by pointing `talosctl upgrade --image` at a new schematic or version.

Find the schematic of a running node: `talosctl get extensions` shows a virtual `schematic` extension whose version is the ID.

Restrictions: `installer` and `initramfs` honour only system extensions (kernel args and META are ignored); `kernel` ignores the schematic; ISO, PXE script and disk images honour everything. The installer in the machine config must use the same schematic as the ISO or PXE image. Factory refuses extensions unsupported for a version and cannot list schematics, as they may hold private kernel arguments.

## Checked

2026-11-04. Schematic YAML, vanilla ID, upload command, installer URL form, restrictions and schematic lookup confirmed on the Image Factory page; upgrade usage on the Boot Assets page.

Method: documentation only; no commands were run.
