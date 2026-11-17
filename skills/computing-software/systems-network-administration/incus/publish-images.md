---
id: computing-software.systems-network-administration.incus.publish-images
name: publish-images
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, images, publish, snapshot, distrobuilder, metadata, templates]
level: practitioner
status: docs-checked
description: "Publish an Incus instance or snapshot as an image with incus publish and its flags, clean the instance first, and build custom images with distrobuilder."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/images_create.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publish images

Stop the instance, then:
```
incus publish <instance> [<remote>:]
incus publish <instance>/<snapshot> [<remote>:]
```

Flags: `--alias`, `--expire` (expiry date), `--public`, `--reuse` (overwrite an image of the same name); see `incus publish --help`.

- Publishing tars and compresses the instance, so it is slow and I/O/CPU heavy; Incus serialises publish operations.
- Before publishing remove what should not ship: metadata (`incus config metadata`), file templates (`incus config template`), and instance-specific data such as host SSH keys and the dbus/systemd machine-id.
- OCI containers: update the source image definition and build a new OCI image instead of publishing a modified container.
- Build images from scratch with distrobuilder (github.com/lxc/distrobuilder).

## Checked

2026-11-09. Confirmed against the Incus How to create images page: publish commands and flags, stopped instance, serialised publish operations, OCI note, cleanup list, distrobuilder. Nothing removed.
Method: documentation only; no commands were run.
