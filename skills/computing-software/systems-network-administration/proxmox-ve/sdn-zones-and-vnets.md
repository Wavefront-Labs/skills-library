---
id: computing-software.systems-network-administration.proxmox-ve.sdn-zones-and-vnets
name: sdn-zones-and-vnets
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [sdn, vnet, vlan-zone, vxlan, evpn]
level: advanced
status: docs-checked
description: "Build Proxmox VE software-defined networks with zones, VNets and subnets, and know the zone types and the apply step."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvesdn.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SDN separates guest networks with zones, virtual networks (VNets) and subnets. A zone is a virtually separated network area, a VNet belongs to a zone, and a subnet is an IP range inside a VNet. After you configure a VNet cluster wide it appears on every node as a common Linux bridge that you assign to guests.

Zone types:

- Simple: an isolated bridge not linked to a physical interface; traffic is local to each node, usable for NAT or routed setups.
- VLAN: uses an existing local Linux or OVS bridge and VLAN tags set on the VNet, giving node to node connectivity.
- QinQ: stacked VLANs (IEEE 802.1ad).
- VXLAN: layer 2 over a UDP tunnel, with no encryption of its own.
- EVPN: VXLAN with BGP for layer 3 routing.

Support status: core SDN (VNet management) is fully supported, while IPAM with DHCP, and complex routing via FRRouting and controllers, are tech previews.

Workflow: configuration is in the datacenter SDN section (Zones, VNets, plus options for controllers, DHCP, IPAM and DNS) and stored in `/etc/pve/sdn`, shared across the cluster. Changes are recorded as pending and only roll out as one atomic change when you press Apply in the SDN overview.

Prerequisites on every node: the `libpve-network-perl` package (installed by default since 8.1), `ifupdown2`, and this line at the end of `/etc/network/interfaces`:

```
source /etc/network/interfaces.d/*
```

DHCP integration uses dnsmasq, which is opt-in: install it and run `systemctl disable --now dnsmasq` to turn off the default instance.

## Checked

2026-11-09. Confirmed against the Proxmox VE docs chapter Software-Defined Network (chapter-pvesdn): zone types, VNet as a common Linux bridge, tech-preview status of IPAM/DHCP and FRRouting, libpve-network-perl installed by default since 8.1, atomic Apply, VXLAN without encryption, dnsmasq disable command, /etc/pve/sdn and the interfaces.d source line.

Method: documentation only; no commands were run.
