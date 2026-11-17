---
id: computing-software.cybersecurity-defensive.security-architecture.vrf-segmentation
name: vrf-segmentation
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [vrf-segmentation, vrf-lite, network-segmentation, data-centre-segmentation, route-leaking, mpls-l3vpn, evpn-vxlan]
level: advanced
status: draft
description: "Segment a data centre with VRFs (VRF-lite or EVPN/VXLAN L3VNIs), force inter-VRF traffic through a firewall, and avoid uncontrolled route leaking."
sources: ["https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/93x/vxlan/configuration/guide/b-cisco-nexus-9000-series-nx-os-vxlan-configuration-guide-93x.html", "https://www.juniper.net/documentation/us/en/software/junos/evpn-vxlan/index.html", "https://datatracker.ietf.org/doc/html/rfc4364"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VRF segmentation in the data centre

A VRF is a separate routing table: hosts in different VRFs cannot route to each other unless routes
are leaked or traffic passes a device attached to both. Use VRFs for macro-segments (prod, dev, PCI,
management, OT), and a firewall as the only inter-VRF path.

## VRF-lite (Cisco IOS-XE example)
```
vrf definition PCI
 address-family ipv4
interface Vlan210
 vrf forwarding PCI
 ip address 10.21.0.1 255.255.255.0
! uplink sub-interface to the firewall's PCI zone
interface Te1/0/48.210
 encapsulation dot1Q 210
 vrf forwarding PCI
 ip address 10.255.210.1 255.255.255.252
ip route vrf PCI 0.0.0.0 0.0.0.0 10.255.210.2
```
Each VRF gets a default route to its own firewall interface/zone; the firewall policy defines what
crosses between zones.

## EVPN/VXLAN fabrics
Each tenant VRF maps to an L3VNI; L2 segments map to L2VNIs. Border leaves hand each VRF to the
firewall on a separate sub-interface/VLAN (or BGP peering per VRF).

## Gotchas
- Route leaking (`import route-target`, `route-replicate`, static leaks) silently bypasses the firewall; inventory and justify every leak.
- Management plane should be its own VRF (`mgmt`), not the global table shared with data traffic.
- Overlapping IP space across VRFs is allowed but makes logs ambiguous - include the VRF in syslog/NetFlow exports.
- DHCP relay and NTP/DNS need VRF-aware configuration (`ip helper-address vrf ...`).

## Verify
- [ ] `show ip route vrf PCI` contains only PCI prefixes plus the default to the firewall.
- [ ] Ping from a dev host to a PCI host fails unless the firewall permits it, and the attempt appears in firewall logs.
- [ ] No unexplained route-target imports between VRFs.
