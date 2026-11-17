---
id: computing-software.systems-network-administration.network-design.ipv6-header-and-extension-headers
name: ipv6-header-and-extension-headers
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, ipv6-header, ipv6-extension-headers, flow-label, hop-limit, ipv6-fragmentation, osi-model]
level: practitioner
status: verified
description: "Read the fixed 40-byte IPv6 header and its extension-header chain (hop-by-hop, routing, fragment, ESP/AH) and handle filtering, fragmentation and EH drops on the internet."
sources:
  - https://www.rfc-editor.org/rfc/rfc8200
  - https://www.rfc-editor.org/rfc/rfc7045
  - https://www.rfc-editor.org/rfc/rfc9098
  - https://www.rfc-editor.org/rfc/rfc5095
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6 header and extension headers

## Fixed header (40 bytes, RFC 8200)
| Field | Bits | Notes |
|---|---|---|
| Version | 4 | 6 |
| Traffic class | 8 | DSCP (6) + ECN (2), same meaning as IPv4 |
| Flow label | 20 | per-flow hash input for ECMP/LAG; set by hosts, routers must not rely on it |
| Payload length | 16 | excludes the 40-byte header |
| Next header | 8 | 6 TCP, 17 UDP, 58 ICMPv6, or an extension header type |
| Hop limit | 8 | TTL equivalent |
| Source / destination | 128 + 128 | |

No header checksum, no router fragmentation, no options in the base header.

## Extension headers (chained via Next Header)
| Type | Value | Notes |
|---|---|---|
| Hop-by-Hop Options | 0 | must be first; often punted to slow path or dropped |
| Routing | 43 | Type 0 deprecated (RFC 5095, IANA registry); Type 4 = Segment Routing Header (RFC 8754) |
| Fragment | 44 | only the source fragments; 8-byte header with ID, offset, M flag |
| Destination Options | 60 | |
| ESP / AH | 50 / 51 | IPsec |
| No Next Header | 59 | |

## Operational realities
- Packets carrying extension headers are often dropped on the public Internet (RFC 9098 summarises the reasons and cites the measurements). Design so production traffic does not depend on them.
- Fragmentation only at the source: routers send ICMPv6 Packet Too Big (type 2). Filtering ICMPv6
  type 2 breaks PMTUD; RFC 4890 lists ICMPv6 types you must permit.
- Minimum link MTU is 1280; tunnels that cannot do 1280 must fragment below IPv6.
- Firewalls/ACLs: a long EH chain can push the L4 header out of the first fragment; RFC 7112
  requires the whole header chain in the first fragment. Drop fragments without it.
- RA-Guard can be evaded with extension headers (RFC 7113); use switches that inspect the full chain.

## Wireshark
`ipv6.nxt == 44` (fragments), `ipv6.hopopts`, `icmpv6.type == 2` (Packet Too Big),
`ipv6.flow != 0`. All four parsed and matched exactly the intended frame in tshark on a scapy-built pcap.

## Verify
- [ ] Edge ACLs allow ICMPv6 type 2 and drop RH0 and atomic/incomplete fragments; test PMTU with `ping -6 -M do -s 1452`.
