---
id: computing-software.systems-network-administration.wireshark.ipv4-ipv6-statistics
name: ipv4-ipv6-statistics
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, ip-statistics, ipv4, ipv6, statistics, address-distribution]
level: practitioner
status: verified
description: "Use Wireshark IPv4/IPv6 Statistics (all addresses, destinations and ports, IP protocol types, source and destination) to profile who talks to whom."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatIPv4.html
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv4/IPv6 statistics

Statistics > IPv4 Statistics and IPv6 Statistics each provide:
- **All Addresses**: packet counts per address.
- **Destinations and Ports**: per destination, broken down by TCP/UDP port.
- **IP Protocol Types**: TCP/UDP/ICMP/GRE/ESP share.
- **Source and Destination Addresses**: separate source and destination tallies.

## tshark
```
tshark -r in.pcapng -q -z ip_hosts,tree
tshark -r in.pcapng -q -z dests,tree
tshark -r in.pcapng -q -z ptype,tree
tshark -r in.pcapng -q -z ip_srcdst,tree
tshark -r in.pcapng -q -z ipv6_hosts,tree
tshark -r in.pcapng -q -z ipv6_dests,tree
```

## Uses
- Unknown traffic on a link: Destinations and Ports shows the top destination/port pairs fast.
- Dual-stack checks: compare IPv4 vs IPv6 volumes to see whether clients prefer IPv6 (Happy Eyeballs).
- Security triage: one source contacting many destinations on one port (scan or worm); GRE/ESP seen in the
  Protocol Hierarchy when you expected none (unauthorised tunnels).

All six `tshark -z` commands above ran on a synthetic capture (`ip_hosts`, `dests`, `ptype`, `ip_srcdst`, `ipv6_hosts`,
`ipv6_dests`); `dests` listed TCP and UDP ports under each destination.

## Compared with Conversations/Endpoints
Endpoints gives bytes and duration; these trees give packet counts with percentages and the
port breakdown in one view. Use both.

## Gotchas
- Counts are packets, not bytes. A few big flows may dominate bandwidth while being small here.
- Tunnelled traffic counts both outer and inner addresses in the address trees (a GRE packet carrying 10.1.1.5 to
  10.9.9.9 added 10.9.9.9 to `ip_hosts`), but `ptype` classified that GRE packet by its inner UDP and showed no GRE
  row at all in the test, so it cannot be used alone to spot GRE tunnels; use the Protocol Hierarchy (`io,phs`) or
  `ip.proto == 47` instead.

## Verify
- [ ] The top talkers match Statistics > Endpoints sorted by packets.
