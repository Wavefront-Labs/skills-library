---
id: computing-software.systems-network-administration.virtualisation.proxmox-jumbo-frames-storage-networks
name: proxmox-jumbo-frames-storage-networks
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-jumbo-frames, mtu, proxmox, networking, storage-network]
level: practitioner
status: docs-checked
description: "Configure MTU 9000 jumbo frames on Proxmox VE NICs, bonds, VLANs and bridges for Ceph, NFS or iSCSI networks, let VMs inherit MTU, and test end to end."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#sysadmin_network_configuration
  - https://pve.proxmox.com/pve-docs/qm.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MTU and jumbo frames for storage networks

**Goal:** larger frames on storage paths (Ceph, NFS, iSCSI, migration) with no fragmentation surprises.

## /etc/network/interfaces
Set MTU on every layer: physical ports, bond, VLAN, bridge.
```
auto ens1f0
iface ens1f0 inet manual
	mtu 9000

auto ens1f1
iface ens1f1 inet manual
	mtu 9000

auto bond1
iface bond1 inet manual
	bond-slaves ens1f0 ens1f1
	bond-mode 802.3ad
	bond-xmit-hash-policy layer3+4
	mtu 9000

auto vmbr1
iface vmbr1 inet static
	address 10.10.10.11/24
	bridge-ports bond1
	bridge-stp off
	bridge-fd 0
	mtu 9000
```
Apply with `ifreload -a`.

## Guests
VirtIO NICs inherit the bridge MTU with `mtu=1`: `qm set 101 -net1 virtio,bridge=vmbr1,mtu=1`. Inside the guest, set the interface MTU to 9000 too.

## Test end to end
```bash
ping -M do -s 8972 10.10.10.12      # 9000 - 28 bytes of IP/ICMP headers; must succeed
ping -M do -s 8973 10.10.10.12      # must fail with 'message too long'
ip -d link show bond1 | grep mtu
```
Test every node pair, and from guests if they use the network.

## Checked
2026-11-01. Confirmed in the Proxmox VE admin guide and `qm` manual: VirtIO NIC `mtu` option (setting 1 or empty uses the bridge MTU, VirtIO only), the 9000 MTU ping test sizes, the VXLAN 50-byte overhead. Removed: switch port size, corosync and Ceph symptom claims, DHCP option.
Method: documentation only; no commands were run.

## Gotchas
- The switch ports and any inter-switch links must allow at least the MTU you set on the hosts.
- One device left at 1500 causes stalls on large transfers while small pings work.
- VXLAN encapsulation uses 50 bytes, so SDN VXLAN MTU must be 50 bytes below the outgoing physical interface MTU.
