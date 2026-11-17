---
id: computing-software.systems-network-administration.proxmox-ve.resource-mappings-cluster-devices
name: resource-mappings-cluster-devices
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [resource-mapping, mapping-pci, mapping-usb, mapping-dir, hostpci-mapping]
level: advanced
status: docs-checked
description: "Define cluster-wide PCI, USB and directory resource mappings so HA and migration pick the right local device."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Raw device addresses are fragile: with HA a different device may sit at the same ID on the target node, and hardware changes can shift paths. A resource mapping gives a device a cluster-unique name that maps to different devices per node, so HA will not start a guest with the wrong device and hardware changes are detected.

Create in the GUI under Datacenter, Resource Mappings, or with the API (types are `pci`, `usb`, `dir`):

```
pvesh create /cluster/mapping/pci --id device1 \
 --map node=node1,path=0000:01:00.0,id=0002:0001 \
 --map node=node2,path=0000:02:00.0,id=0002:0001
```

Repeat `--map` for each node. The map must include all identifying properties (such as vendor and device id) so changed hardware is noticed. For USB, only one device per node per mapping is possible. A PCI mapping may list several devices per node; the first free one is used when the guest starts, in the order given, which suits SR-IOV virtual functions.

Assign to a guest:

```
qm set ID -hostpci0 <name>
qm set <vmid> -usb0 <name>
```

All the usual passthrough options still apply, including `mdev`.

Permissions: creating mappings needs `Mapping.Modify` on `/mapping/<type>/<name>`; using them needs `Mapping.Use` on the same path, plus normal guest edit privileges.

Extra mapping options for PCI: `mdev` marks a device as capable of providing mediated devices (the type is chosen on the guest, created on the first device with free instances), and `live-migration-capable` marks support for live migrating a passed-through device. That is experimental and only known to work with recent NVIDIA GPUs and kernels.

## Checked

2026-11-09. Confirmed against the Proxmox VE docs chapter Qemu/KVM Virtual Machines (chapter-qm), Resource Mapping section: pvesh create /cluster/mapping example, repeated map per node, one USB device per node per mapping, first free PCI device used, Mapping.Modify and Mapping.Use paths, mdev and live-migration-capable options.

Method: documentation only; no commands were run.
