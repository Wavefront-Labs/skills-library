---
id: computing-software.systems-network-administration.virtualisation.proxmox-sdn-zones-and-vnets
name: proxmox-sdn-zones-and-vnets
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-sdn, proxmox-sdn, sdn-zone, vnet, vxlan, evpn, qinq, simple-zone, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Use Proxmox SDN: zone types (Simple, VLAN, QinQ, VXLAN, EVPN), creating vnets and subnets, applying config cluster-wide, MTU for overlays, and permissions on vnets."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvesdn.html
  - https://github.com/proxmox/pve-docs/blob/master/pvesdn.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox SDN zones and vnets

**Goal:** define guest networks once at datacenter level and have every node configured
consistently, including overlays that span L3.

## Zone types
| Zone | Use |
|---|---|
| Simple | Isolated bridge, not linked to a physical interface, local to each node; usable for NAT or routed setups (the only zone with automatic DHCP) |
| VLAN | Uses an existing local Linux or OVS bridge and VLAN tags set in the VNet; connects VMs across nodes |
| QinQ | Stacked VLANs: the zone sets the service (outer) VLAN, the VNet the inner tag |
| VXLAN | L2 overlay in UDP datagrams (default destination port 4789) over an underlay you configure |
| EVPN | VXLAN with BGP EVPN: routable L3, anycast gateway, VRF across zones |

## Configure (Datacenter → SDN)
1. **Zones** → Add VLAN zone: ID `prod`, bridge `vmbr0` (must already exist on every node).
2. **VNets** → Add: ID `app120` (up to 8 characters), zone `prod`, tag `120`. Each node then has a local interface `app120`; assign it to guests like a bridge.
3. **Subnets** (optional, for IPAM/DHCP/SNAT): `10.0.120.0/24`, gateway.
4. **Apply** (SDN → Apply): changes are pending until then and are rolled out to every node.

Prerequisites: the core SDN packages (default since Proxmox VE 8.1; `libpve-network-perl` on older installs), `ifupdown2`, and `source /etc/network/interfaces.d/*` at the end of `/etc/network/interfaces`.

## VXLAN/EVPN notes
- MTU: VXLAN encapsulation uses 50 bytes, so the MTU must be 50 bytes less than the outgoing physical interface (EVPN zone default 1450).
- EVPN needs FRR (`apt install frr-pythontools`, `systemctl enable frr.service`; opt-in, tech preview), an EVPN controller (unique ASN, peers) and optionally exit nodes for traffic leaving the overlay.
- VXLAN has no encryption of its own; use a site-to-site VPN or IPsec between sites.

## Permissions
Zones are restricted to nodes and assigned permissions so users reach only certain zones and their VNets. The built-in roles are `PVESDNAdmin` (manage SDN configuration) and `PVESDNUser` (access to bridges and vnets).

## Gotchas
- Pending changes do nothing until Apply.
- Some VNet options may have no effect or not work in certain zones.
- Isolate Ports is local to each host: use the VNet firewall to isolate traffic across nodes, and restart affected guests for it to take effect.

## Verify
A local interface named after each VNet exists on every node, and two VMs on the same vnet on different nodes can ping each other.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, pvesdn.adoc, last pushed 2026-10-17) and pveum.adoc (role list). Confirmed: zone type descriptions, VLAN, VXLAN (4789) and EVPN (MTU 1450) options, 8 character VNet ID, local interface per VNet, pending/apply model, package and `source` line prerequisites, roles `PVESDNAdmin` and `PVESDNUser`, Isolate Ports behaviour, FRR opt-in. Removed: the `pvesh` zone commands, the ACL path `/sdn/zones/<zone>/<vnet>`, the interfaces.d file name, the SDN status `available` wording and the bridge-mixing advice (not documented).

Method: documentation only; no commands were run.
