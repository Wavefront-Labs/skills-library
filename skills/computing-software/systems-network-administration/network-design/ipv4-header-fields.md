---
id: computing-software.systems-network-administration.network-design.ipv4-header-fields
name: ipv4-header-fields
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, ipv4-header, ttl, dscp, ecn, fragmentation, ip-protocol-numbers, osi-model]
level: practitioner
status: verified
description: "Interpret every IPv4 header field (IHL, DSCP/ECN, total length, ID/flags/offset, TTL, protocol, checksum, options) to diagnose loops, fragmentation and marking issues."
sources:
  - https://www.rfc-editor.org/rfc/rfc791
  - https://www.rfc-editor.org/rfc/rfc2474
  - https://www.rfc-editor.org/rfc/rfc3168
  - https://www.rfc-editor.org/rfc/rfc6864
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv4 header fields

| Field | Bits | What to look for |
|---|---|---|
| Version | 4 | always 4 |
| IHL | 4 | header length in 32-bit words; 5 = 20 bytes (no options); > 5 means options present |
| DSCP | 6 | QoS marking (EF = 46, AF41 = 34, CS6 = 48); RFC 2474 replaced the old ToS byte |
| ECN | 2 | 00 not-ECT, 01 ECT(1), 10 ECT(0), 11 CE (congestion experienced, RFC 3168) |
| Total length | 16 | header + data, max 65535 |
| Identification | 16 | groups fragments of one datagram; RFC 6864 says the value is only defined when a datagram is actually fragmented |
| Flags | 3 | bit 1 DF (don't fragment), bit 2 MF (more fragments) |
| Fragment offset | 13 | in 8-byte units |
| TTL | 8 | decremented per router hop; 0 = drop + ICMP time exceeded |
| Protocol | 8 | 1 ICMP, 6 TCP, 17 UDP, 47 GRE, 50 ESP, 51 AH, 89 OSPF, 112 VRRP, 132 SCTP |
| Header checksum | 16 | recomputed every hop because TTL changes |
| Source / destination | 32 + 32 | |
| Options | variable | record route, timestamp, source route (block at edges) |

## Diagnostics from the header
- **TTL**: initial values vary by OS and device: Linux defaults to 64 (`ip_default_ttl`, "as recommended by RFC1700"), Windows replied with TTL=128 in a test, other systems differ (some network gear starts higher; check the platform). A received TTL of
  52 from a Linux server means 12 hops. TTL dropping steadily in a capture of the same flow = routing
  loop; the same packet seen repeatedly with TTL -1 each time confirms it.
- **DF + large total length + ICMP 3/4 replies** -> PMTUD in action; DF and no ICMP -> black hole.
- **MF set or offset > 0** -> fragmentation happening; firewalls and some cloud LBs drop non-first
  fragments. Wireshark: `ip.flags.mf == 1 || ip.frag_offset > 0`.
- **DSCP rewritten to 0** between two capture points -> a device is re-marking (trust boundary,
  provider bleaching).
- **Bad checksum** warnings on transmitted packets in a local capture are usually checksum offload,
  not real errors.

Every field width, the DSCP/ECN split, the protocol numbers (IANA registry CSV) and the Wireshark filters
above were checked: filters parsed and matched the expected frames in tshark on a scapy-built pcap
(fragments, DF, DSCP 46).

## Verify
- [ ] Given a capture, state hop count from TTL, whether fragmentation/DF is involved, and the DSCP class.
