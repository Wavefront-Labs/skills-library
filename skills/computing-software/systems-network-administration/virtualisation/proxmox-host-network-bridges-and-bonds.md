---
id: computing-software.systems-network-administration.virtualisation.proxmox-host-network-bridges-and-bonds
name: proxmox-host-network-bridges-and-bonds
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ifupdown2, vmbr0, pve-bond, lacp-bond, vlan-aware-bridge, linux-bridge, etc-network-interfaces, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Configure Proxmox VE host networking in /etc/network/interfaces: vmbr bridges, bonds (active-backup, LACP), VLAN-aware bridges, separate cluster/storage networks, ifreload."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#sysadmin_network_configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox host networking: bridges, bonds and VLANs

**Goal:** a host network where management, cluster (corosync), storage and VM traffic are
separated and redundant, applied without losing the node.

## Example `/etc/network/interfaces`
```
auto lo
iface lo inet loopback

auto eno1
iface eno1 inet manual
auto eno2
iface eno2 inet manual

auto bond0
iface bond0 inet manual
    bond-slaves eno1 eno2
    bond-mode 802.3ad            # LACP; needs switch port-channel. Else active-backup
    bond-miimon 100
    bond-xmit-hash-policy layer3+4

auto vmbr0
iface vmbr0 inet static
    address 192.0.2.11/24
    gateway 192.0.2.1
    bridge-ports bond0
    bridge-stp off
    bridge-fd 0
    bridge-vlan-aware yes
    bridge-vids 2-4094

auto vmbr0.50                    # storage VLAN interface for the host itself
iface vmbr0.50 inet static
    address 10.50.0.11/24

auto eno3                        # dedicated corosync link, no bridge
iface eno3 inet static
    address 10.99.0.11/24
```
VMs on `vmbr0` set their VLAN tag in the NIC settings (`tag=120`).

## Apply safely
PVE uses **ifupdown2**: GUI changes are staged in `/etc/network/interfaces.new` and applied
with "Apply Configuration" (`ifreload -a`) without reboot. Keep IPMI console open; one
typo in `gateway` or bridge-ports can cut management.

## Bond modes
| Mode | Switch requirement | Note |
|---|---|---|
| active-backup | none | Simple, safe for corosync and management |
| 802.3ad (LACP) | port-channel/MLAG | Best for VM and storage throughput |
| balance-tlb/alb | none | No special switch support required |
Give corosync its own dedicated network, separate from storage and VM traffic, as the admin guide advises.

## Gotchas
- The admin guide's VLAN-aware example uses `bridge-vids 2-4094`.
- MTU: set on bond, bridge and VLAN interfaces consistently for jumbo storage networks.
- Interface names can change after kernel/hardware changes; pin with systemd `.link`
  files (see `pve-network-interface-pinning` in the admin guide).

## Verify
`ip -br a`, `cat /proc/net/bonding/bond0` (all slaves up, LACP partner present), ping
gateway and storage, VM on a tagged VLAN reaches its gateway.

## Checked

2026-10-28

Confirmed: Admin guide network chapter: interfaces.new staging, ifreload -a, bridge-vlan-aware and bridge-vids example, bond modes, bond-xmit-hash-policy, tag on VM NICs.

Removed or corrected: bridge-vids default claim, balance-alb bridge warning, unbonded-corosync claim, version gate for the pinning tool.

Method: documentation only; no commands were run.
