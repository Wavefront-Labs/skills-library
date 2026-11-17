---
id: computing-software.systems-network-administration.cisco-networking.multicast-addressing-and-mac-mapping
name: multicast-addressing-and-mac-mapping
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, multicast, multicast-addressing, multicast-mac, ipv4-multicast, ipv6-multicast, ssm-range, administratively-scoped, 32-to-1-overlap, glop]
level: practitioner
status: docs-checked
description: "Choose multicast group addresses correctly: IPv4 blocks (link-local, SSM, GLOP, scoped 239/8), IPv6 scope values, and the 32:1 IPv4 and IPv6 group-to-MAC mapping and its overlaps."
sources:
  - https://www.iana.org/assignments/multicast-addresses/multicast-addresses.xhtml
  - https://datatracker.ietf.org/doc/html/rfc5771
  - https://www.rfc-editor.org/rfc/rfc1112
  - https://www.rfc-editor.org/rfc/rfc2365
  - https://www.rfc-editor.org/rfc/rfc2464
  - https://www.rfc-editor.org/rfc/rfc4291
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multicast address ranges and MAC mapping

## IPv4 blocks (RFC 5771, IANA registry)
| Range | Designation |
|---|---|
| 224.0.0.0/24 | Local Network Control: protocol control traffic not forwarded off link (for example 224.0.0.5 OSPF All Routers, 224.0.0.6 OSPF Designated Routers, 224.0.0.13 All PIM Routers, 224.0.0.18 VRRP) |
| 224.0.1.0/24 | Internetwork Control: may be forwarded through the Internet (224.0.1.1 NTP, 224.0.1.39 cisco-rp-announce, 224.0.1.40 cisco-rp-discovery) |
| 224.0.2.0-224.0.255.255, 224.3.0.0-224.4.255.255, 233.252.0.0-233.255.255.255 | AD-HOC blocks I, II, III |
| 224.2.0.0/16 | SDP/SAP block, only for SDP/SAP |
| 232.0.0.0/8 | Source-Specific Multicast, explicitly for SSM only |
| 233.0.0.0-233.251.255.255 | GLOP: AS number X.Y maps to 233.X.Y.0/24 for 16-bit ASNs |
| 239.0.0.0/8 | Administratively Scoped, local to a domain, no IANA assignment |
- 233.252.0.0/24 is MCAST-TEST-NET for documentation.
- RFC 2365 scopes inside 239/8: IPv4 Local Scope 239.255.0.0/16; Organization Local Scope 239.192.0.0/14; 239.0.0.0/10,
  239.64.0.0/10 and 239.128.0.0/10 are left unassigned. Packets for 239.255.0.0/16 must not be forwarded across a link
  that is a boundary of that scope.
- RFC 5771 recommends consideration of IPv6 multicast where feasible.

## IPv4 group to MAC (RFC 1112)
The low-order 23 bits of the group address go into the low-order 23 bits of Ethernet address 01-00-5E-00-00-00. An
IPv4 group has 28 significant bits, so more than one group maps to the same MAC: 5 bits are lost, so 32 groups share
each MAC.
- 224.1.1.1, 225.1.1.1, 239.1.1.1 and 239.129.1.1 all map to 01:00:5E:01:01:01 (only the low 7 bits of the second
  octet count).
- 225.0.0.5 maps to 01:00:5E:00:00:05, the same MAC as 224.0.0.5 (OSPF All Routers); 239.128.0.1 maps to
  01:00:5E:00:00:01, the same MAC as 224.0.0.1. Avoid application groups whose second octet is 0 or 128 with zeros in
  the next two octets, so they never share a MAC with link-local control groups (how a given switch treats such
  frames is platform behaviour: check its guide).

## IPv6
- Format FF flags scop (RFC 4291). Scop values: 1 interface-local, 2 link-local, 4 admin-local, 5 site-local,
  8 organisation-local, E global; 0 and F reserved, 3 reserved; the rest unassigned. Routers must not forward beyond
  the scope in the address.
- Group to MAC (RFC 2464): Ethernet address with first two octets 33:33 and the last four octets taken from the last
  four octets of the IPv6 destination address.
- Solicited-node address: low-order 24 bits of the unicast or anycast address appended to FF02:0:0:0:0:1:FF00::/104
  (used by neighbour discovery).

## Practical rules (judgement)
- For internal applications use 239/8, inside the RFC 2365 scopes, and keep a register of groups per application.
- Do not use 224.0.0.0/24 or 224.0.1.0/24, the SSM block (except for SSM) or SDP/SAP block for other purposes.

## Checked
Checked 2026-11-08 against RFC 5771, the IANA IPv4 multicast registry (named group assignments), RFC 1112 (23-bit MAC
mapping), RFC 2365 (239/8 scopes), RFC 2464 (33:33 mapping) and RFC 4291 (scop values, solicited-node). Removed: the
claim that switches flood overlapping groups regardless of IGMP snooping, `show ip igmp snooping groups`, the SSM
IPv6 range, the IGMPv3/MLDv2 advice, and the Cisco multicast configuration page, which does not cover addressing.
Method: documentation only; no commands were run.
