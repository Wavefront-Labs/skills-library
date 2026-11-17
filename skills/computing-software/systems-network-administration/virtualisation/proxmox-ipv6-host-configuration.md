---
id: computing-software.systems-network-administration.virtualisation.proxmox-ipv6-host-configuration
name: proxmox-ipv6-host-configuration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-ipv6, ipv6, proxmox, networking]
level: practitioner
status: docs-checked
description: "Configure IPv6 on Proxmox VE hosts and bridges: static and SLAAC addresses, accept_ra with forwarding, /etc/hosts, cluster links and firewall NDP rules."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#sysadmin_network_configuration
  - https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6 host configuration on Proxmox VE

**Goal:** dual-stack management and guest networking that keeps working after reboots and firewall changes.

## Static address on the management bridge
```
auto vmbr0
iface vmbr0 inet static
	address 192.0.2.11/24
	gateway 192.0.2.1
	bridge-ports eno1
	bridge-stp off
	bridge-fd 0

iface vmbr0 inet6 static
	address 2001:db8:10::11/64
	gateway 2001:db8:10::1
```
`ifreload -a`, then add the IPv6 address to `/etc/hosts` next to the node name if the node should be reached by v6.

## SLAAC / router advertisements
Static addressing is preferred for hypervisors. If you use router advertisements, check the kernel `ip-sysctl` documentation for `accept_ra` behaviour on hosts that forward.

## Guests
Bridged guests get IPv6 from the same LAN (RA/DHCPv6); the host does not need an address on that bridge. The PVE firewall `ndp` option must stay enabled, and the IP filter restricts IPv6 link-local addresses to the one derived from the interface MAC.

## Firewall
Host firewall option `ndp: 1` (default) allows neighbour discovery; keep it on or IPv6 breaks once the firewall is enabled. Rules apply to both families unless you specify addresses of one family.

## Verify
```bash
ip -6 addr show vmbr0
ip -6 route
ping -6 -c3 2001:db8:10::1
curl -6 -k https://[2001:db8:10::11]:8006
```

## Checked
2026-11-01. Confirmed in the Proxmox VE admin guide: firewall `ndp` option (default 1), IP filter behaviour for IPv6 link-local addresses. Removed: the `accept_ra` override, the corosync and Ceph IPv6 statements (not in the docs read).
Method: documentation only; no commands were run.
