---
id: computing-software.systems-network-administration.cisco-networking.igmp-snooping-and-querier
name: igmp-snooping-and-querier
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, multicast, igmp, igmp-snooping, igmp-querier, igmpv3, mrouter-port, multicast-flooding, mld-snooping]
level: practitioner
status: docs-checked
description: "How IGMP and MLD snooping switches behave per RFC 4541: router ports, the Querier, 224.0.0.x flooding, unregistered streams and IGMPv3 pitfalls."
sources:
  - https://datatracker.ietf.org/doc/html/rfc4541
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IGMP snooping and the querier

RFC 4541 (informational) describes what snooping switches should do. Vendor behaviour can differ; check the vendor's
configuration guide for the exact commands and defaults on your platform.

## Why snooping
Without it a switch floods multicast to all ports in the VLAN, wasting bandwidth. A snooping switch forwards
non-link-local, non-IGMP multicast according to group-based port membership tables, and also on router ports.

## Router ports
The switch may build its router-port list by any combination of:
- sending Multicast Router Solicitation messages (MRDISC) and snooping Multicast Router Advertisements,
- the arrival port of IGMP Queries whose source address is not 0.0.0.0 (0.0.0.0 marks proxy queries from a switch
  that is not the Querier; they are not from a multicast router and are excluded from Querier election),
- ports explicitly configured by management as IGMP-forwarding ports.

## Membership timeouts and the querier
A snooping switch must not rely only on Leave messages to remove entries; it should implement a membership timeout
like the router side of IGMP/MLD on all non-router ports, and the timeout should be configurable. Entries therefore
depend on Queries being sent in the VLAN: if no router or switch acts as the Querier, receivers' entries can age
out. A non-Querier switch that proxies General Queries (for example after a spanning-tree port change) should use the
all-zeros source address, and should not inject an IGMPv2 Query into an IGMPv3 network.

## Forwarding rules (section 2.1.2)
- Destinations in 224.0.0.X that are not IGMP must be forwarded on all ports. Many hosts do not join these
  addresses and some routers use them without joining.
- An unregistered packet matches no group in earlier Membership Reports. It must be forwarded on all ports to which
  an IGMP router is attached; a switch may default to flooding it on all ports. A switch that does not must provide a
  way to force flooding on specified ports.
- Mixed IGMPv3 hosts and non-IGMPv3 snooping switches: failure to flood unregistered streams can stop v3 hosts
  receiving traffic. If the switch supports all versions in use, flooding can overwhelm hosts so they miss Queries.
  Snooping switches are encouraged to at least process IGMPv3 Join Reports.
- Forwarding tables keyed by IP address are preferred over MAC address, because Ethernet maps 1 address to 32 IP
  multicast addresses.
- Non-IPv4 multicast packets continue to be flooded to all ports in the forwarding state.
- Unrecognised IGMP messages must be flooded to all other ports.

## Verify
- [ ] A Querier exists in every multicast VLAN (a multicast router or a switch configured as querier).
- [ ] Group membership appears only on receiver ports and router ports.
- [ ] Streams continue past several query intervals on a receiver.

## Checked
Checked 2026-11-08 against RFC 4541 (sections 2.1.1 and 2.1.2). Removed: Cisco Catalyst commands, the 260 s timer,
lowest-IP querier election detail, explicit tracking and immediate-leave, 239.0.0.x MAC overlap range, and MLD
snooping commands, because the Cisco Catalyst page returned 404 and the RFC does not state them.
Method: documentation only; no commands were run.
