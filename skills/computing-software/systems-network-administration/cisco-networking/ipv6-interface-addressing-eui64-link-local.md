---
id: computing-software.systems-network-administration.cisco-networking.ipv6-interface-addressing-eui64-link-local
name: ipv6-interface-addressing-eui64-link-local
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ipv6, ipv6-configuration, ipv6-unicast-routing, eui-64, link-local, ipv6-address, ipv6-enable, solicited-node-multicast, anycast, ipv6-address-types, show-ipv6-interface]
level: practitioner
status: draft
description: "Address IOS interfaces for IPv6: manual, EUI-64 and link-local addresses, how EUI-64 is derived, the multicast groups joined, address types, and verifying with show ipv6 interface."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipv6_basic/configuration/xe-16/ip6b-xe-16-book/ip6-add-basic-conn-xe.html
  - https://datatracker.ietf.org/doc/html/rfc4291
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IPv6 interface addressing: manual, EUI-64, link-local

## Configure
```
ipv6 unicast-routing
interface GigabitEthernet0/1
 ipv6 address 2001:db8:10:1::1/64           ! manual
 ipv6 address 2001:db8:10:2::/64 eui-64     ! host part from the MAC
 ipv6 address FE80::1 link-local            ! predictable link-local
interface GigabitEthernet0/2
 ipv6 enable                                ! link-local only (e.g. unnumbered transit)
```
Every IPv6-enabled interface has a link-local (FE80::/10) automatically; routing protocols and
RAs use it.

## EUI-64 derivation
MAC `0050.56AB.CDEF` -> split `0050.56` | `AB.CDEF`, insert `FFFE` -> `0050:56FF:FEAB:CDEF`,
flip the 7th bit of the first byte (00 -> 02) -> interface ID `0250:56FF:FEAB:CDEF`.
Result: `2001:db8:10:2:250:56ff:feab:cdef/64`. Hosts today mostly use random/stable-privacy
IDs (RFC 7217/8981) instead; EUI-64 remains common on router interfaces in labs.

## Address types to recognise (CCNA 1.9)
| Prefix | Type |
|---|---|
| 2000::/3 | global unicast |
| FC00::/7 (FD00::/8 in practice) | unique local |
| FE80::/10 | link-local |
| FF00::/8 | multicast (FF02::1 all nodes, FF02::2 all routers, FF02::1:FFxx:xxxx solicited-node) |
| ::1, :: | loopback, unspecified |
| 2001:db8::/32 | documentation |
Anycast addresses are unicast addresses assigned to several devices: `ipv6 address
2001:db8::53/128 anycast`.

## Verify
```
show ipv6 interface brief
show ipv6 interface GigabitEthernet0/1   ! link-local, global addresses, joined groups (FF02::1, FF02::2, FF02::1:FF00:1), ND settings
ping FE80::2                             ! IOS prompts for the output interface
```

## Gotchas
- A /64 is required for SLAAC; use /127 for point-to-point router links (RFC 6164).
- Duplicate address detection: an address marked `[DUP]` is not used; fix the conflict and
  `shutdown/no shutdown`.
- `ipv6 address autoconfig` makes the router a SLAAC client (needs RAs from another router).

## Verify
- [ ] `show ipv6 interface brief` shows expected global and link-local addresses, none `[DUP]`.
- [ ] Neighbour pings via link-local and global succeed.
