---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-virtual-routers-and-static-routes
name: pan-os-virtual-routers-and-static-routes
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [virtual-router, pan-os, static-route, route-lookup, ecmp, path-monitor, fib]
level: practitioner
status: draft
description: "Configure PAN-OS virtual routers, static routes with path monitoring, ECMP, and verify route and FIB lookups from the CLI."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/networking/static-routes"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: deterministic forwarding with failover of default routes.

```
configure
set network virtual-router default interface [ ethernet1/1 ethernet1/3 ]
set network virtual-router default routing-table ip static-route default-isp1 destination 0.0.0.0/0 nexthop ip-address 192.0.2.1 interface ethernet1/1 metric 10
set network virtual-router default routing-table ip static-route default-isp2 destination 0.0.0.0/0 nexthop ip-address 198.51.100.1 interface ethernet1/3 metric 20
set network virtual-router default routing-table ip static-route default-isp1 path-monitor enable yes failure-condition any
commit
```
Path monitoring pings one or more destinations (add them in the GUI under the static route, or `path-monitor monitor-destinations`) and withdraws the route when they fail, so the metric 20 route takes over.

ECMP: enable under Virtual Router > Router Settings > ECMP, set max paths and the method (IP modulo, IP hash, weighted round robin, balanced round robin). Confirm whether your release needs a restart notice.

Lookup order: longest prefix, then administrative distance (static 10, eBGP 20, OSPF internal 30, OSPF external 110, RIP 120, iBGP 200), then metric.

Gotchas
- An interface not added to the virtual router never contributes its connected route.
- A default route with an interface but no next hop on a multi-access link makes the firewall ARP for every destination.

## Verify
```
show routing route
show routing fib
test routing fib-lookup virtual-router default ip 198.51.100.50
show routing path-monitor
```
