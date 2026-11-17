---
id: computing-software.systems-network-administration.cisco-networking.ipv6-manual-6in4-tunnels
name: ipv6-manual-6in4-tunnels
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ipv6, 6in4, ipv6-tunnel, ipv6ip, tunnel-mode-ipv6ip, transition, protocol-41]
level: practitioner
status: draft
description: "Build manual 6in4 (IPv6-over-IPv4, protocol 41) tunnels on IOS to a peer or tunnel broker: config, MTU, NAT and firewall requirements, verification."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/interface/configuration/xe-16/ir-xe-16-book/ip6-tunnel.html
  - https://datatracker.ietf.org/doc/html/rfc4213
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Manual 6in4 tunnels

## Config
```
interface Tunnel0
 description 6in4 to broker
 no ip address
 ipv6 address 2001:DB8:FFFF:1::2/64
 ipv6 enable
 tunnel source GigabitEthernet0/0        ! or the public IPv4
 tunnel destination 198.51.100.1
 tunnel mode ipv6ip                      ! protocol 41, no GRE header
 ipv6 mtu 1480
ipv6 route ::/0 Tunnel0
```
`tunnel mode ipv6ip` = static 6in4 (RFC 4213). `tunnel mode gre ip` with IPv6 on the tunnel also
works between Cisco routers and can carry multicast/routing protocols, at 4 bytes more overhead.

## Requirements
- IP protocol 41 must pass every firewall/ACL between the endpoints (not TCP/UDP: no ports).
- NAT: protocol 41 does not traverse most PAT devices. The tunnel endpoint needs a public IP or a
  1:1 NAT/DMZ forward of protocol 41.
- With a dynamic WAN address, tunnel brokers need updating when it changes.

## MTU
Outer IPv4 header = 20 bytes, so IPv6 MTU 1480 over a 1500 path; less over PPPoE (1472).
IPv6 has no in-path fragmentation, so set `ipv6 mtu` correctly and let PMTUD work.

## Gotchas
- `tunnel source` must be the address the peer expects; with NAT, the peer sees the public address.
- IPv6 routing protocols over ipv6ip tunnels work for unicast (OSPFv3 uses multicast which
  6in4 carries point-to-point fine on IOS); confirm with the peer.
- 6to4 and automatic tunnels (`tunnel mode ipv6ip 6to4`) are deprecated (RFC 7526).

## Verify
```
show interfaces Tunnel0              ! up/up, Tunnel protocol/transport IPv6/IP
show ipv6 interface Tunnel0
ping 2001:DB8:FFFF:1::1
traceroute ipv6 2001:4860:4860::8888
```
