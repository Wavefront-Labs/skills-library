---
id: computing-software.systems-network-administration.proxmox-ve.vm-boot-order-and-autostart
name: vm-boot-order-and-autostart
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [onboot, boot-order, startup-order, shutdown-timeout, startup-delay]
level: intro
status: docs-checked
description: "Set VM boot device order and automatic start and shutdown ordering on a Proxmox VE node."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Boot device order is the `boot` property:

```
boot: order=scsi0;net0;hostpci0
```

The guest tries scsi0, then network boot from net0, then a passed-through PCIe device. In the GUI use the drag and drop editor. If a guest uses several disks to boot, every one must be marked bootable, because recent SeaBIOS and OVMF only initialise bootable disks. Devices not listed still appear to the guest after its OS boots; the flag only affects firmware and bootloader. For cloud images, `order=scsi0` speeds boot because the BIOS skips checking the CD-ROM.

Start at boot:

```
qm set <vmid> -onboot 1
```

Fine tune with the `startup` property, `[order=]<n>[,up=<n>][,down=<n>]` (Start/Shutdown order, Startup delay, Shutdown timeout in the GUI):
- Start order sets priority; shutdown uses the reverse order, so order 1 starts first and stops last. Equal orders sort by ascending VMID.
- Startup delay is how many seconds to wait before starting later VMs, for example 240.
- Shutdown timeout defaults to 180 seconds, after which the VM is stopped forcefully.

VMs without an order always start after those with one. The order is enforced only among VMs on the same host, not cluster wide. HA-managed VMs ignore start on boot and ordering because the HA manager starts and stops them.

## Checked

2026-11-09. Compared with the Boot Order and Automatic Start and Shutdown sections, the Cloud-Init boot tip and the startup property of https://pve.proxmox.com/pve-docs/chapter-qm.html. Removed the claim that pve-guests waits for quorum, which the page does not state.

Method: documentation only; no commands were run.

