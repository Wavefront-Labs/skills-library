---
id: computing-software.systems-network-administration.virtualisation.proxmox-sdn-fabrics-openfabric-ospf
name: proxmox-sdn-fabrics-openfabric-ospf
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [sdn-fabric, openfabric, ospf, sdn, proxmox, frr]
level: advanced
status: docs-checked
description: "Build Proxmox VE SDN fabrics with OpenFabric or OSPF for routed full-mesh Ceph networks and EVPN underlays, and verify them with FRR commands."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvesdn.html
  - https://github.com/proxmox/pve-docs/blob/master/pvesdn.adoc
  - https://docs.frrouting.org/en/latest/fabricd.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SDN fabrics with OpenFabric or OSPF

**Goal:** a routed, self-healing network between nodes (for example a switchless 3-node Ceph mesh, or the underlay for EVPN) managed from the PVE GUI.

## Availability
Fabrics (OpenFabric, OSPF and WireGuard types) are documented in the current SDN chapter; this skill covers OpenFabric and OSPF. The routing layer (FRRouting) is documented as tech preview. The release that introduced fabrics is not stated in the documentation; if your version has no Fabrics panel, configure FRR manually following the *Full Mesh Network for Ceph Server* wiki page.

## Prerequisites
`apt install frr frr-pythontools` on all nodes; `source /etc/network/interfaces.d/*` at the end of `/etc/network/interfaces`. Prefer interfaces without pre-assigned IP addresses; set addresses in the fabric's IP columns if needed.

## Create a fabric
Datacenter -> **SDN** -> *Fabrics* -> Add:
- **OpenFabric**: name `cephmesh` (at most 8 characters), optional IPv4 or IPv6 loopback prefix `10.15.15.0/24` (when set, router IDs are checked against it), optional Hello Interval (default 3 s) and CSNP Interval (default 10 s).
- **OSPF**: name, area (a 32-bit integer or an IP address, for example `0`), optional loopback prefix.

Add each node with the "+" button: a unique Router-ID (an IPv4 address; OpenFabric also accepts IPv6), for example `10.15.15.1`, and the interfaces used to reach the other nodes. A dummy interface carrying the router ID is created automatically as the fabric loopback. Per-interface IP, IPv6 and Hello Multiplier (OpenFabric, default 10) are optional. Apply SDN.

## Use it
- Full-mesh networks for Ceph: the documentation names a fabric as a full-mesh option for Ceph; follow the Ceph chapter for the network settings.
- EVPN controller and VXLAN zone: select the fabric that contains all the nodes (the EVPN peer address uses an IPv4 router ID as VTEP address).

## Verify
```bash
vtysh -c 'show openfabric topology'
vtysh -c 'show openfabric neighbor'
vtysh -c 'show ip ospf neighbor'       # OSPF fabrics
```
Then ping a peer's router ID from each node.

## Gotchas
- IPv6 fabrics (OpenFabric only) need global IPv6 forwarding on all fabric nodes, for example `post-up sysctl -w net.ipv6.conf.all.forwarding=1` on a fabric interface in `/etc/network/interfaces`; this affects SLAAC and router advertisement handling.
- Removing an interface that has an entry with `manual` in `/etc/network/interfaces` does not remove its IP on apply.
- Editing fabric nodes writes `/etc/network/interfaces`, so it needs `Sys.Modify` on the node in addition to `SDN.Allocate`.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, pvesdn.adoc, last pushed 2026-10-17) and FRR doc/user (github.com/FRRouting/frr). Confirmed: install packages, 8 character OpenFabric name, Hello Interval 3 s, CSNP Interval 10 s, Hello Multiplier 10, loopback prefix validation, router-ID rules and dummy loopback interface, OSPF area format, IPv6 forwarding note, `manual` interface warning, permissions, FRR show commands (`show openfabric topology`, `show openfabric neighbor`, `show ip ospf neighbor`). Removed: the 9.1 GUI status claim, the Ceph `public_network` recipe, the link-failure test, the MTU and corosync gotchas and the claim that SDN owns mesh port IPs (not documented).

Method: documentation only; no commands were run.
