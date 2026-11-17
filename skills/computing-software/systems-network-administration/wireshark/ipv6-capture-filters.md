---
id: computing-software.systems-network-administration.wireshark.ipv6-capture-filters
name: ipv6-capture-filters
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, ipv6-capture-filter, bpf, icmp6, extension-headers, neighbor-discovery, capture-filter]
level: practitioner
status: verified
description: "Write capture filters that work for IPv6: host/net with v6 prefixes, icmp6 types for ND/RA, the extension-header blind spot of ip6 protochain, and dual-stack filters."
sources:
  - https://www.tcpdump.org/manpages/pcap-filter.7.html
  - https://www.rfc-editor.org/rfc/rfc4443
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6 capture filters

## Basics
```
ip6                                   # any IPv6
host 2001:db8::10                     # v6 host (host also matches v4 if given a v4 address)
net 2001:db8:100::/48
ip6 and tcp port 443
host 10.0.0.5 or host 2001:db8::5     # dual-stack host
```
`port 443` and `tcp` match both IPv4 and IPv6 automatically.

## ICMPv6 and Neighbour Discovery
```
icmp6                                         # all ICMPv6
icmp6 and ip6[40] == 134                      # Router Advertisement (type 134)
icmp6 and (ip6[40] == 135 or ip6[40] == 136)  # NS / NA
icmp6 and ip6[40] == 133                      # Router Solicitation
```
Newer libpcap understands `icmp6[icmp6type] == icmp6-routeradvert`. `ip6[40]` is the first byte
after a 40-byte IPv6 header, which works only when there are no extension headers.

## The extension header problem
`tcp`, `udp`, `icmp6` primitives look at the IPv6 Next Header field. If a Hop-by-Hop (MLD uses one),
Fragment, or Destination Options header sits in between, simple primitives miss the packet.
```
ip6 protochain 6          # walks the header chain to find TCP; slower but correct
ip6 protochain 58         # ICMPv6 even behind Hop-by-Hop (MLD reports)
ip6[6] == 44              # fragments
```
For broad troubleshooting capture `ip6` and narrow with display filters, which decode the full
chain.

## Multicast
```
ip6 multicast                 # ff00::/8 destinations
dst net ff02::/16             # link-local scope multicast (ND, MLD, OSPFv3, DHCPv6)
udp port 546 or udp port 547  # DHCPv6
```

## Gotchas
- `ether proto 0x86dd` and `ip6` matched the same frames on Ethernet; `ip6` is the portable form (on a loopback
  capture `ether proto` compiled to a loopback-header test instead).
- VLAN-tagged traffic needs `vlan and ip6`.
- Tunnelled IPv6 (6in4 = IP protocol 41): `ip proto 41`.

## Tested
On a synthetic capture (Router Advertisement, an MLD report behind a Hop-by-Hop header, IPv6 TCP): `icmp6` and
`icmp6 and ip6[40] == 134` matched only the RA; `ip6 protochain 58` matched both the RA and the MLD report;
`ip6 protochain 6` matched the TCP packet; `icmp6[icmp6type] == icmp6-routeradvert` compiled and matched the RA.

## Verify
- [ ] Compile with `dumpcap -d -f "..."` and test against a sample containing RA/NS/MLD packets.
