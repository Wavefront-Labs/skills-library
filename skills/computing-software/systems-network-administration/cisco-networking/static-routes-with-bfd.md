---
id: computing-software.systems-network-administration.cisco-networking.static-routes-with-bfd
name: static-routes-with-bfd
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, static-bfd, bfd, static-route, fast-failover, ip-route-static-bfd]
level: practitioner
status: draft
description: "Make static routes fail over in under a second with BFD: interface bfd timers, ip route static bfd, single-hop vs multihop, and what the far end must run."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bfd/configuration/xe-16/irb-xe-16-book/irb-bfd-stat-route.html
  - https://www.rfc-editor.org/rfc/rfc5880
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Static routes with BFD

A static route stays in the table as long as its interface is up, even if the next hop is dead
(e.g. through a provider switch). BFD verifies the next hop forwards packets and removes the route
in ~150 ms.

## Configure (single-hop)
```
interface GigabitEthernet0/1
 ip address 203.0.113.2 255.255.255.252
 bfd interval 50 min_rx 50 multiplier 3     ! 150 ms detection

ip route static bfd GigabitEthernet0/1 203.0.113.1
ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/1 203.0.113.1
ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/2 198.51.100.1 250      ! floating backup
```
The `ip route static bfd` line creates the BFD session; any static route using that interface and
next hop is tied to it.

## Far end
The peer must also run BFD for that address: another router (`ip route static bfd` toward us),
a firewall with BFD for static routes, or the ISP PE. Without a peer the session stays down and,
by default, the static route is removed. Check before enabling.

## Multihop (next hop several hops away, e.g. a loopback)
```
bfd map ipv4 192.0.2.10/32 192.0.2.1/32 MH-TEMPLATE
bfd-template multi-hop MH-TEMPLATE
 interval min-tx 300 min-rx 300 multiplier 3
ip route static bfd 192.0.2.10 source 192.0.2.1
```

## Verify
```
show bfd neighbors details
!  State: Up, Registered protocols: STATIC
show ip static route bfd
show ip route static
```
Failover test: drop BFD packets on the far side (ACL deny udp 3784) while the link stays up; the
primary route should vanish and the floating route appear.

## Gotchas
- Aggressive timers on a busy CPU (software BFD on small ISRs) cause false flaps. Use 300 ms x 3 if
  BFD is not hardware offloaded.
- `ip route static bfd ... unassociate` keeps the BFD session without withdrawing routes; useful to
  monitor before enforcing.
- IPv6: `ipv6 route static bfd`.
- Echo mode (default on) needs `no ip redirects` on the interface and uRPF disabled or loose,
  otherwise echo packets are dropped.

## Verify
- [ ] BFD session Up with registered protocol STATIC.
- [ ] Failover under one second on a continuous ping.
