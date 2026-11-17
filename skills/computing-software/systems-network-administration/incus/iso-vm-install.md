---
id: computing-software.systems-network-administration.incus.iso-vm-install
name: iso-vm-install
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, iso, vm, empty-instance, boot-priority, vga-console, storage-volume-import]
level: practitioner
status: docs-checked
description: "Install an operating system into an Incus VM from an ISO: create an empty VM, import the ISO as a volume, set boot.priority, use the VGA console, then detach."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/instances_create.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM from an ISO

1. Empty VM: `incus init iso-vm --empty --vm`. Add resources with `-c limits.cpu=2 -c limits.memory=4GiB -d root,size=50GiB`.
2. Import the ISO: `incus storage volume import <pool> /path/to/image.iso iso-volume --type=iso`.
3. Attach with boot priority: `incus config device add iso-vm iso-volume disk pool=<pool> source=iso-volume boot.priority=10`.
4. Start with the serial console: `incus start iso-vm --console` (exit with `ctrl+a-q`).
5. Run the installer in the graphical console: `incus console iso-vm --type=vga`.
6. After installing, detach: `incus storage volume detach <pool> iso-volume iso-vm`, then reboot.

## Checked

2026-11-04: confirmed against the Incus create-instances how-to, boot-from-ISO section (empty VM, ISO import as `iso` volume, `boot.priority=10`, serial then VGA console, `ctrl+a-q`, detach). Nothing removed.

Method: documentation only; no commands were run.
