---
id: computing-software.systems-network-administration.network-design.missing-routes
name: missing-routes
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-services, missing-route, routing-table, return-path, default-route]
level: practitioner
status: docs-checked
description: "Diagnose missing routes: forward and return path checks, routing table and RIB/FIB inspection, redistribution and filtering gaps, and asymmetric return traffic."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/8651-21.html
  - https://man7.org/linux/man-pages/man8/ip-route.8.html
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/route_ws2008
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Missing routes

## Symptoms
- `Destination net unreachable` from a router (ICMP 3/0) -> that router has no route.
- Timeout with traceroute stopping at a hop -> next hop drops or return path missing.
- One direction works, replies never come back -> **return route** missing on the far side
  (very common with new subnets and VPNs).

## Checks at each hop
```
ip route get 10.50.1.10                   # Linux: chosen route and source
Find-NetRoute -RemoteIPAddress 10.50.1.10 # Windows
route print                               # Windows route table
```
On routers use the platform's route lookup (longest match, source protocol, next hop), its
forwarding-table lookup (what is actually programmed) and the per-VRF lookup.
Work hop by hop in both directions; the first device without a correct route is the fault.

## Typical causes
| Cause | Check |
|---|---|
| New subnet not advertised | network statement / redistribution / interface not enabled in the routing protocol |
| Route filtered | prefix-lists, route-maps, distribute-lists, BGP policy, max-prefix |
| Summary hides or blackholes | summary to a discard route without component routes |
| Static route next hop unreachable | static route table, recursive next-hop failure |
| VPN encryption domain/proxy IDs missing the subnet | tunnel up but subnet not in selectors |
| Cloud route table missing a route to on-prem/VGW, or propagation disabled | VPC/VNet route tables |
| Host has wrong/no default gateway or extra static routes | `route print`, `ip route` |
| VRF leakage not configured | route targets / import maps |

## Verify
- [ ] Route present in RIB and FIB on every hop in both directions; traceroute and application test succeed from both ends.

## Checked

2026-10-28: Confirmed: ip route get (man7 ip-route), Find-NetRoute -RemoteIPAddress (Microsoft Learn), route print (Microsoft Learn route), ICMP net unreachable code 0 (RFC 1122). Removed the Cisco-specific show commands (show ip route, show ip cef, vrf variants, show ip static route) and the passive-interface and Null0 keywords, which no fetched page covered.
Method: documentation only; no commands were run.
