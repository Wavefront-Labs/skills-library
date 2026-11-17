---
id: computing-software.systems-network-administration.virtualisation.proxmox-sdn-qinq-zone
name: proxmox-sdn-qinq-zone
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [qinq-zone, sdn, vlan, proxmox, networking]
level: advanced
status: docs-checked
description: "Configure a Proxmox VE SDN QinQ zone with a service VLAN and customer VLAN vnets, set MTU and the 802.1ad protocol, and match switch configuration."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvesdn.html
  - https://github.com/proxmox/pve-docs/blob/master/pvesdn.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SDN QinQ zone

**Goal:** stack customer VLANs inside a service VLAN, so tenants can reuse VLAN IDs over one provider VLAN.

## Prerequisites
- `ifupdown2` (default since Proxmox VE 7.0 on new installs) and the SDN packages (default since 8.1); `source /etc/network/interfaces.d/*` present at the end of `/etc/network/interfaces`.
- A local VLAN-aware bridge (for example `vmbr0`) already configured on every node.
- Physical switches must support stacked VLANs.

## Create
Datacenter -> **SDN** -> *Zones* -> Add -> **QinQ**:
- ID `tenantA`, Bridge `vmbr0`, Service VLAN `100`, Service VLAN Protocol `802.1ad` (the default is `802.1q`), MTU `1496` when the physical interface MTU is 1500 (QinQ adds 4 bytes).

*VNets* -> Add: `tAweb` in zone `tenantA` with Tag `10` (the inner, customer VLAN; VNet IDs are up to 8 characters); `tAdb` with Tag `20`.

Apply (SDN -> *Apply*). After creating a VNet, a local network interface with the same name exists on each node; guests attach to it like a bridge.

## Gotchas
- The extra tag needs 4 more bytes: reduce the MTU (for example 1496 on a 1500 byte link) or raise the physical MTU.
- The physical switches must support stacked VLANs on the ports facing the nodes.

## Verify
Two VMs on `tAweb` on different nodes can ping each other, including with full-size packets.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, pvesdn.adoc, last pushed 2026-10-17). Confirmed: QinQ zone options (bridge, service VLAN, service VLAN protocol with 802.1q default or 802.1ad, MTU 1496 example), inner tag defined by the VNet, switches must support stacked VLANs, VNet ID limit of 8 characters, ifupdown2 and SDN package defaults, the required `source` line. Removed: the example `zones.cfg` stanza and key names, the `ip -d link` verification, the unique-tag-per-zone claim and the dot1q-tunnel switch advice (not documented). VNet names `tA-web` and `tA-db` replaced because they exceed the 8 character limit.

Method: documentation only; no commands were run.
