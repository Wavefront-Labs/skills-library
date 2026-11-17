---
id: computing-software.systems-network-administration.virtualisation.proxmox-usb-passthrough
name: proxmox-usb-passthrough
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-usb-passthrough, usb-passthrough, qemu, proxmox]
level: practitioner
status: docs-checked
description: "Pass USB devices to Proxmox VE VMs by vendor/product ID or port, use resource mappings across nodes, and handle migration and USB 3 limits."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html#qm_usb_passthrough
  - https://pve.proxmox.com/pve-docs/qm.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# USB passthrough to VMs

**Goal:** a VM reliably sees a physical USB device (licence dongle, Zigbee stick, UPS, smartcard reader).

## Identify the device
```bash
lsusb            # Bus 001 Device 004: ID 10c4:ea60 Silicon Labs CP210x
lsusb -t         # topology, to find the physical port path (e.g. 1-1.2)
```

## Pass it through
```bash
qm set 105 -usb0 host=10c4:ea60            # by vendor:product, follows the device to any port
qm set 105 -usb1 host=1-1.2,usb3=1         # by port: whatever is plugged into that port
qm set 105 -usb2 spice                     # SPICE client redirection instead of host device
```
The vendor:product ID form identifies a device model, so two identical devices share the same ID; the bus-port form (for example `1-2.3.4`) identifies a physical port on the host. If a configured device is absent from the host at VM start, the VM still boots, and the device is passed through as soon as it becomes available.

## Resource mappings
Datacenter -> **Resource Mappings** -> USB: define a mapping (for example `dongle`) per node, then `qm set 105 -usb0 mapping=dongle`. Cluster-level mappings work properly with HA, detect hardware changes and let non-root users configure them.

## Gotchas
- A VM with a host USB device cannot be moved online to another host, since the hardware is only available on the node where the VM runs.
- USB 3 devices: set `usb3=1`. `usbN` accepts N from 0 to 4; with machine version 7.1 or newer and ostype l26 or windows newer than 7, N can be up to 14.
- SPICE USB passthrough (`-usbN spice`) redirects a device from your SPICE client and suits temporary use, such as a dongle.

## Verify
In the guest, `lsusb` (Linux) or Device Manager (Windows) shows the device; it survives a VM reboot.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: qm.adoc USB Passthrough and generated qm.conf.5-opts.adoc usb[n]) and confirmed the host=vendor:product and bus-port forms, usb3, mapping and spice values, the usb0-4 and up-to-14 port limits, the online-move restriction and the resource mapping benefits. Removed the unconfirmed PVE 8 gate, offline-migration, re-enumeration and PCI-controller advice.

Method: documentation only; no commands were run.
