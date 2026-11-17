---
id: computing-software.systems-network-administration.cisco-networking.static-route-to-ethernet-interface
name: static-route-to-ethernet-interface
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, static-interface-route, static-route, proxy-arp, arp-cache, directly-attached-static]
level: practitioner
status: draft
description: "Avoid the static-route-to-Ethernet-interface trap: why ip route x y Gi0/1 relies on proxy ARP, fills the ARP cache and breaks, and when interface-only statics are right."
sources:
  - https://www.cisco.com/c/en/us/support/docs/dial-access/floating-static-route/118263-technote-nexthop-00.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_pi/configuration/xe-16/iri-xe-16-book/iri-ip-static-route.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Static routes pointing only at an Ethernet interface

```
ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/1          ! looks simple; is a trap
```

## What actually happens
The route says every destination is directly connected on Gi0/1. For each destination IP the router
ARPs for that IP itself. It only works if the upstream router answers with proxy ARP. Effects:
- An ARP entry per destination: thousands of entries for a default route, CPU and memory load.
- When the upstream disables proxy ARP (common hardening), all traffic fails.
- Failover between two upstreams sharing the segment is unpredictable.

## Do this instead
Fully specified (interface + next hop) or next hop only:
```
ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/1 203.0.113.1    ! withdraws if Gi0/1 goes down
ip route 0.0.0.0 0.0.0.0 203.0.113.1                        ! recursive via connected route
```
The fully specified form is best on multi-access links: one ARP entry, and the route leaves the
table when the interface is down.

## When interface-only is correct
- Point-to-point interfaces with no L2 resolution: serial, PPP, GRE/IPsec tunnels, dialer:
  `ip route 10.20.0.0 255.255.0.0 Tunnel0`.
- Null0 discard routes: `ip route 10.0.0.0 255.0.0.0 Null0`.

## Spot it in an existing network
```
show ip route static | include directly connected
show ip arp | count Gi0/1                   ! huge count on one interface is a hint
show ip arp summary
```
Routes shown as `is directly connected, GigabitEthernet0/1` with a non-connected prefix are the
pattern.

## Gotchas
- Cloud and ISP edges often disable proxy ARP; migrating a box that relied on it fails on day one.
- Some firewalls answer proxy ARP for NAT pools and mask the problem until replaced.
- IPv6 equivalent with a link-local next hop must specify the interface:
  `ipv6 route ::/0 GigabitEthernet0/1 FE80::1`.

## Verify
- [ ] `show ip route 0.0.0.0` shows a next-hop address, not "directly connected".
- [ ] ARP table on the interface contains only real neighbours.
