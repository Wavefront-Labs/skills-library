---
id: computing-software.systems-network-administration.network-design.cast-types-and-broadcast-domains
name: cast-types-and-broadcast-domains
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, broadcast-domain, collision-domain, unicast, multicast, anycast, osi-model]
level: practitioner
status: verified
description: "Distinguish unicast, broadcast, multicast and anycast delivery, size broadcast domains sensibly, and know which devices bound broadcast and collision domains."
sources:
  - https://www.rfc-editor.org/rfc/rfc919
  - https://www.rfc-editor.org/rfc/rfc1112
  - https://www.rfc-editor.org/rfc/rfc4291
  - https://www.rfc-editor.org/rfc/rfc4786
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cast types and broadcast domains

## Delivery types
| Type | IPv4 | IPv6 | L2 destination |
|---|---|---|---|
| Unicast | one host | one interface | host MAC |
| Broadcast | 255.255.255.255 (limited), subnet broadcast (directed) | none (replaced by multicast) | ff:ff:ff:ff:ff:ff |
| Multicast | 224.0.0.0/4 | ff00::/8 | 01:00:5e (v4, low 23 bits of the group), 33:33 (v6, low 32 bits) |
| Anycast | same unicast prefix announced from several places | defined anycast addresses | host MAC |

Anycast (RFC 4786, BCP 126) is a routing technique: nearest site by routing metric wins; used by DNS
root servers, CDNs, public resolvers. Keep anycast services stateless or short-lived (UDP DNS)
because a routing change moves clients mid-session.

## Domains
- **Collision domain**: bounded by every switch port; full-duplex links have no collisions.
  Hubs (legacy) share one.
- **Broadcast domain**: one VLAN / IP subnet. Bounded by routers (L3 interfaces). Switches and
  bridges extend it.

## Sizing a broadcast domain
- Every host processes every broadcast (ARP, DHCP, NetBIOS, mDNS, SSDP). Keep user VLANs to a
  /24 or smaller (~250 hosts) as a rule; wireless and IoT VLANs smaller or with broadcast
  suppression/proxy ARP on the controller.
- Large L2 domains also mean large STP failure domains; route at the access or distribution
  layer instead of spanning VLANs across buildings.
- Measure: broadcast pps per VLAN (interface broadcast counters on your switches); sustained > a few
  hundred pps per host port warrants investigation (loops, chatty devices).

## Multicast in switched networks
Without IGMP snooping multicast floods like broadcast. Enable IGMP snooping with a querier per
VLAN (a router or the switch's own querier feature), or flooding returns when membership times out.

## Verify
- [ ] Each VLAN has a documented subnet size, broadcast rate baseline, and IGMP snooping/querier state.
