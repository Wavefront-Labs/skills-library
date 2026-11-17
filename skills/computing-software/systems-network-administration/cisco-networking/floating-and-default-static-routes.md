---
id: computing-software.systems-network-administration.cisco-networking.floating-and-default-static-routes
name: floating-and-default-static-routes
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, static-route, static-routing, default-route, floating-static-route, administrative-distance, ip-route, recursive-route, fully-specified-static]
level: practitioner
status: docs-checked
description: "Write IPv4 static routes that behave: default routes, floating statics with administrative distance, and recursive vs interface-only vs interface plus next-hop forms."
sources:
  - https://www.cisco.com/c/en/us/support/docs/dial-access/floating-static-route/118263-technote-nexthop-00.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Default and floating static routes

## Forms
```
ip route 172.31.10.0 255.255.255.0 10.10.10.2                  ! next hop only (recursive)
ip route 172.31.10.0 255.255.255.0 Serial1/0                    ! exit interface only (point-to-point)
ip route 0.0.0.0 0.0.0.0 Ethernet0 192.168.1.1                  ! interface plus next hop
ip route 172.31.10.0 255.255.255.0 10.10.20.2 250               ! floating static, AD 250
```

## Next-hop styles
| Style | Behaviour per Cisco's next-hop technote |
|---|---|
| Next-hop IP only | recursive: the route stays in the routing table as long as the router has any route to the next hop, even via another static route |
| Exit interface only | inserted only while the interface is active; fine for point-to-point interfaces; not recommended on Ethernet |
| Interface plus next hop | the router does not ARP for each destination; Cisco recommends specifying both on Ethernet, and the interface alone suffices on a point-to-point link |

On an Ethernet interface with no next hop, the router treats every destination in the route as directly connected and
ARPs for each. With many destinations this can cause high processor use, a very large ARP cache and memory allocation
failures. Specifying only a directly connected next hop without the interface is also not recommended.
If the next hop could become reachable through a recursive route when its interface fails, specify both the next-hop
address and the interface through which it is found; the technote says this makes installation more deterministic.

## Floating static (backup path)
- A static route has administrative distance 1 by default, preferred over any dynamic protocol.
- A static route with a raised distance is a floating static route: it is installed only when the better route
  disappears from the routing table. To sit behind EIGRP (default AD 90 internal, 170 external) use a distance above
  170. A distance of 255 is unreachable and such a route is never installed.
- Worked failure from the technote: a primary static `ip route 172.31.10.0 255.255.255.0 10.10.10.2` and a floating
  `... 10.10.20.2 250`. After the primary link was shut down, the primary static stayed in the table because
  10.10.10.2 still recursed through another static route (`ip route 10.0.0.0 255.0.0.0 192.168.10.2`), so the floating
  route was never installed. The fix was to remove the recursive form and use `ip route 172.31.10.0 255.255.255.0
  Serial1/0`; then the floating route (`[250/0]`) took over. On Ethernet specify both interface and next hop.
- This depends on the primary leaving the table. Where the primary next hop stays reachable, see
  tracked-static-routes-ip-sla.

## Verify
```
show ip route
show ip route 172.31.10.0       ! shows the distance and next hop in use
```
- [ ] Primary route in the table, floating route absent; failing the primary brings the floating route in.
- [ ] No exit-interface-only statics on Ethernet.

## Checked
Checked 2026-11-08 against Cisco's Configure a Next Hop IP Address for Static Routes technote (document 118263,
updated July 2023). The Cisco IOS XE static route configuration chapter returned 404, so these were removed as
unconfirmed: Null0 and host-route forms, `name` and `tag` options, `permanent`, equal-AD ECMP, advertising statics via
redistribution, `no ip unreachables`, `show ip static route`, the 130 distance for OSPF, and the ISP-handoff
IP SLA explanation.
Method: documentation only; no commands were run.
