---
id: computing-software.systems-network-administration.netbox.virtual-chassis-and-vdc
name: virtual-chassis-and-vdc
category: computing-software
field: systems-network-administration
product: netbox
tags: [virtual-chassis, virtual-device-context, modules]
level: advanced
status: docs-checked
description: "Choose between virtual chassis, VDCs and modules for shared management planes and partitions."
sources: ["https://netboxlabs.com/docs/netbox/features/devices-cabling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Virtual chassis, VDCs and modules

Goal: pick the right construct for non-trivial hardware.

**Virtual chassis.** Used when physical devices share a single management plane. The most common case is stackable switches. Each member is a separate device in NetBox, grouped under one virtual chassis.

**Virtual device contexts.** A VDC is a logical partition within one device. Each VDC operates autonomously but shares a common pool of resources. Each interface can be assigned to one or more VDCs on its device.

**Modules.** Much like device types and devices, module types instantiate discrete modules, which are hardware components installed within a device (such as line cards). Module types may also be organised using profiles.

**Choosing**

- Several boxes, one control plane: virtual chassis.
- One box, several logical routers or switches: VDC.
- Removable hardware in a bay: module.
- A device inside another device's bay: device bay with a child device.

Device bays and module bays are defined in the device type, so decide before creating devices because component instantiation is not retroactive.

**Checklist**

1. Identify the sharing boundary.
2. Assign interfaces to VDCs.
3. Define bays on the device type first.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Devices & Cabling feature page (read in full).
