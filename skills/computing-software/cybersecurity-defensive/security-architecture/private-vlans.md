---
id: computing-software.cybersecurity-defensive.security-architecture.private-vlans
name: private-vlans
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [network-segmentation, private-vlan, pvlan, isolated-ports, community-vlan, promiscuous-port, layer-2-security, dmz]
level: advanced
status: draft
description: "Use private VLANs to stop same-subnet hosts talking to each other: isolated and community VLANs, promiscuous ports, layer 3 bypass, and DMZ designs."
sources: ["https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/vlan/b_179_vlan_9300_cg/configuring_private_vlans.html", "https://datatracker.ietf.org/doc/html/rfc5517", "https://www.juniper.net/documentation/us/en/software/junos/multicast-l2/topics/topic-map/private-vlans.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Private VLANs

PVLANs (RFC 5517) split one VLAN/subnet into sub-domains so hosts share an IP range and gateway but
cannot reach each other at layer 2. Use case: DMZ servers, hosting, guest/kiosk networks, IoT,
backup networks where east-west traffic between peers should never happen.

## Types
- **Primary VLAN**: the parent.
- **Isolated secondary VLAN**: ports talk only to promiscuous ports. One per primary.
- **Community secondary VLAN**: ports talk to each other within the community and to promiscuous ports.
- **Promiscuous port**: the gateway/firewall, talks to everyone.

## Cisco IOS-XE example
```
vtp mode transparent
vlan 201
 private-vlan isolated
vlan 202
 private-vlan community
vlan 200
 private-vlan primary
 private-vlan association 201,202
!
interface Gi1/0/10
 switchport mode private-vlan host
 switchport private-vlan host-association 200 201
!
interface Gi1/0/48
 description to-firewall
 switchport mode private-vlan promiscuous
 switchport private-vlan mapping 200 201,202
!
interface Vlan200
 private-vlan mapping 201,202     ! if the switch SVI is the gateway
```
Check: `show vlan private-vlan`, `show interfaces Gi1/0/10 switchport`.

## Design notes
- Put the firewall on the promiscuous port so inter-host traffic, if allowed at all, goes through policy.
- Layer 3 bypass: if the router is the gateway, host A can reach host B by sending to the router,
  which routes back into the subnet. Block with an ACL on the SVI (deny subnet-to-subnet) or use
  "local proxy ARP" consciously.
- Across switches: secondary VLANs must exist on all switches and trunks must carry them
  (`private-vlan trunk` modes on some platforms).
- Virtual environments: VMware vDS supports PVLANs; cloud VPCs do not (use security groups instead).

## Alternatives
Port isolation / "protected ports" (`switchport protected`) on a single switch, client isolation on
Wi-Fi, host firewalls, or microsegmentation agents when PVLAN support is lacking.

## Gotchas
- VTP version 3 or transparent mode required on many Cisco platforms.
- Some features (e.g. certain port-security, EtherChannel on host ports) conflict with PVLAN modes.
- DHCP snooping/ARP inspection must be configured for the primary VLAN correctly.

## Verify
From one isolated host, ping/ARP another isolated host (must fail) and the gateway (must work);
test community members can reach each other only within their community.
