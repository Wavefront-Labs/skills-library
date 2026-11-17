---
id: computing-software.systems-network-administration.proxmox-ve.vm-machine-type-and-versions
name: vm-machine-type-and-versions
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [machine-type, q35, ovmf, seabios, machine-version]
level: advanced
status: docs-checked
description: "Understand Proxmox VE VM machine types, versions, and OVMF versus SeaBIOS when planning upgrades."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The machine type defines the virtual motherboard. Choose Intel 440FX (default) or Q35, which provides a PCIe bus and is the usual choice for PCIe passthrough. Firmware is SeaBIOS (default) or OVMF (UEFI). Switch to OVMF mainly when planning PCIe passthrough. Arm64 hosts only use OVMF and the `virt` machine type.

Each machine type is versioned in QEMU. Live migration and snapshots with RAM keep the machine version of the running VM so the guest sees identical hardware. Windows guests get their version pinned at creation because Windows is sensitive to virtual hardware changes even across cold boots (for example NIC enumeration). Other guests use "latest", meaning the newest version the QEMU binary supports after a fresh start. Proxmox adds a downstream revision `+pveX`; `pc-q35-9.2` equals `pc-q35-9.2+pve0`, and the revision rises when Proxmox changes the hardware layout.

Deprecation: since QEMU 10.1 upstream drops machine versions after 6 years. For Proxmox VE 9 the baseline is 6.0, expected to increase by 2 major versions per Proxmox VE release. Before a major upgrade, update VMs that use machine versions about to be dropped.

To update: take a working backup first, expect the guest to see changed hardware (you may need to reinstall drivers), and check snapshots that include RAM, recorded in the `runningmachine` entry. A snapshot's machine version cannot be changed, so load the snapshot to salvage its data instead.

```
qm set 100 --machine pc-q35-9.2
```

## Checked

2026-11-09. Compared with the Machine Type, Machine Version, PVE Machine Revision and Deprecation sections of https://pve.proxmox.com/pve-docs/chapter-qm.html. The qm set line is an illustrative command built from the page's pc-q35-9.2 example; the page does not show it.

Method: documentation only; no commands were run.

