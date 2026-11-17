---
id: computing-software.systems-network-administration.virtualisation.proxmox-sdn-evpn-zone
name: proxmox-sdn-evpn-zone
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [evpn-zone, exit-node, pve-sdn, proxmox-sdn, vxlan-zone, frr, bgp, proxmox]
level: advanced
status: docs-checked
description: "Build a Proxmox SDN EVPN zone: controller, VRF VXLAN ID, vnets with anycast gateways, exit nodes and SNAT for routed L3 overlays between nodes, plus verification with FRR."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvesdn.html
  - https://github.com/proxmox/pve-docs/blob/master/pvesdn.adoc
  - https://docs.frrouting.org/en/latest/evpn.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SDN EVPN zone

EVPN zones give routed overlays: each vnet is a VXLAN with a distributed anycast gateway
on every node, routes exchanged by BGP EVPN (FRR). Use for multi-tenant L3 isolation
without VLAN changes on the physical network.

## Prereqs
On all nodes `apt install frr-pythontools` and `systemctl enable frr.service` (the FRRouting integration is opt-in and documented as tech preview; only the core SDN packages are installed by default since Proxmox VE 8.1), underlay IP reachability between nodes, and an MTU 50 bytes below the outgoing physical interface (VXLAN encapsulation uses 50 bytes; the zone MTU defaults to 1450). `source /etc/network/interfaces.d/*` must be present at the end of `/etc/network/interfaces`.

## Configure (Datacenter → SDN)
1. **Controller** → Add → EVPN: a unique private ASN (for example 65000), peers = node underlay IPs (or an SDN fabric containing all nodes).
2. **Zone** → Add → EVPN: primary controller, **VRF VXLAN ID** (for example 10000; it must differ from the VXLAN IDs of the vnets), MTU, optional **exit nodes**, **primary exit node** (needed for SNAT or if the upstream router lacks ECMP), **exit nodes local routing**, **advertise subnets** (for silent guests) and **disable ARP ND suppression** (for floating IPs).
3. **VNet** → Add: zone, VXLAN tag per vnet (for example 11000).
4. **Subnet** on the vnet: CIDR 10.50.1.0/24, gateway 10.50.1.1 (the gateway is the same anycast address on every node), optional SNAT, which on EVPN zones is forwarded on the exit (gateway) nodes.
5. **Apply** (SDN → Apply): the pending changes are rolled out to all nodes and the FRR configuration is merged into `/etc/frr/frr.conf`.

## North-south
- Exit nodes announce a default route in the EVPN network and by default only forward traffic between the real network and the EVPN network.
- With multiple exit nodes, disable strict reverse path filtering (`net.ipv4.conf.default.rp_filter=0` and `net.ipv4.conf.all.rp_filter=0`, for example in `/etc/sysctl.d/99-rp-filter.conf`), because packets can arrive at one node and leave from another.
- A BGP controller can be added to exchange routes with external routers.

## Verify with FRR
```sh
vtysh -c "show bgp l2vpn evpn summary"     # BGP sessions for the EVPN address family
vtysh -c "show evpn vni"                   # VNIs known to zebra
vtysh -c "show ip route vrf <vrf-name>"    # routes in the zone's VRF
```
Test: two VMs on the same vnet on different nodes ping each other; a VM pings its gateway; a VM reaches the outside through an exit node.

## Gotchas
- `/etc/frr/frr.conf` is generated; node-local additions go in `/etc/frr/frr.conf.local`, which is appended.
- The underlay must allow UDP 4789 (the VXLAN default destination port) and BGP (TCP 179) between nodes.
- VXLAN on its own provides no encryption.
- Each controller and zone option only applies after the SDN configuration is applied.

## Verify
BGP sessions are established, cross-node VM traffic works and the exit path works.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, pvesdn.adoc, last pushed 2026-10-17) and FRR doc/user (github.com/FRRouting/frr). Confirmed: FRR opt-in install (`frr-pythontools`, `frr.service`), tech-preview status, core SDN packages default since 8.1; EVPN zone and controller options and their meanings; EVPN MTU default 1450 and 50 byte VXLAN overhead; VXLAN UDP 4789; rp_filter note for multiple exit nodes; `/etc/frr/frr.conf.local`; FRR commands `show bgp l2vpn evpn summary`, `show evpn vni`, `show ip route vrf`. Removed: the claim that FRR is installed by default since 8.1 (wrong: only the core SDN packages are), the `interfaces.d/sdn` file name, the vtysh VRF name pattern, `ip -d link` grep and the claim about how physical routers learn tenant subnets (not documented).

Method: documentation only; no commands were run.
