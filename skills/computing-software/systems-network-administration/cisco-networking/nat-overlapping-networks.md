---
id: computing-software.systems-network-administration.cisco-networking.nat-overlapping-networks
name: nat-overlapping-networks
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, overlapping-networks, twice-nat, static-network-nat, ip-nat-outside-source, merger, vpn]
level: practitioner
status: draft
description: "Connect two networks that use the same address space: static network NAT in both directions, ip nat outside source, DNS doctoring, and routing the translated ranges."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/13774-3.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_nat/configuration/xe-16/nat-xe-16-book.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NAT for overlapping networks

Both sites use 10.1.0.0/16 (merger, partner VPN, cloned lab). Each side must see the other under a
unique "proxy" range.

## Plan the ranges
- Site A real 10.1.0.0/16, presented to B as 172.20.0.0/16.
- Site B real 10.1.0.0/16, presented to A as 172.21.0.0/16.
Hosts at A talk to 172.21.x.y to reach B's 10.1.x.y.

## One router doing both translations (on A's side of the link)
```
interface Gi0/0      ! towards site A LAN
 ip nat inside
interface Tunnel0    ! towards site B
 ip nat outside

ip nat inside source static network 10.1.0.0 172.20.0.0 /16
ip nat outside source static network 10.1.0.0 172.21.0.0 /16 add-route
```
- `inside source`: A's packets leave with source 172.20.x.y.
- `outside source`: B's packets arrive with source 172.21.x.y; A's replies to 172.21.x.y are
  translated back to 10.1.x.y on the way out.
- `add-route` installs a route for the outside local range so traffic to 172.21/16 goes out the
  tunnel. Otherwise add `ip route 172.21.0.0 255.255.0.0 Tunnel0`.

## Routing
Site A routes 172.21.0.0/16 to the NAT router. Site B routes 172.20.0.0/16 back over the tunnel
(B never sees A's real 10.1/16).

## DNS
Users type names, not IPs. Either serve split DNS (A's view of B's names returns 172.21 addresses),
or rely on NAT DNS ALG which rewrites A records in DNS replies crossing the NAT (`ip nat service
dns-tcp` for TCP). Explicit DNS views are more predictable.

## Verify
```
show ip nat translations | include 172.2
show ip route 172.21.0.0
ping 172.21.5.10 source Gi0/0
```

## Gotchas
- Protocols embedding IPs (SIP, FTP active, some AD/Kerberos flows) need ALGs or break; AD domain
  joins across twice-NAT are fragile.
- Static network NAT is 1:1; ranges must be the same size.
- Long term, renumber one side; NAT is a bridge, not a destination.

## Verify
- [ ] Hosts at A reach B by 172.21 addresses and B sees A as 172.20 addresses (check server logs).
