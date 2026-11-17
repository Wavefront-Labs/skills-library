---
id: computing-software.systems-network-administration.cisco-networking.routing-table-administrative-distance
name: routing-table-administrative-distance
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, routing-table, forwarding-decision, administrative-distance, longest-prefix-match, route-codes, show-ip-route, metric, gateway-of-last-resort, rib, route-selection, ccna]
level: practitioner
status: docs-checked
description: "Read show ip route: route codes, [AD/metric], how AD picks the installed route, why longest prefix match still decides forwarding, default AD values and floating statics."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/15986-admin-distance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Routing table: AD, longest prefix match, codes

## Anatomy of a line
```
D 192.168.1.0/24 [90/130816] via 172.16.1.100, 00:13:42, GigabitEthernet1
^code ^prefix     ^AD/metric  ^next hop         ^age      ^exit interface
```
The brackets hold `[administrative distance/metric]`. Codes in the legend: C connected, L local, S static,
O OSPF (IA inter area, E1/E2 external, N1/N2 NSSA external), D EIGRP (EX external), B BGP, R RIP, i IS-IS,
`*` candidate default, `+` replicated route, `%` next hop override. The `L` entries in the examples are /32 routes
for the router's own interface addresses.

## Two separate decisions
1. **Installation (RIB): lowest AD wins** when several sources offer the same prefix and length. Each protocol first
   picks its own best path with its own metric; only its best candidate(s) reach the routing table. Equal-cost
   routes can all be installed where ECMP is supported. AD is used only when different sources advertise the same
   prefix.
2. **Forwarding (FIB): longest prefix match.** Packets use the most specific installed route. AD and metric are not
   evaluated at forwarding time, so AD does not override longest prefix match: with 192.168.1.0/24 and
   192.168.0.0/16 installed, a packet to 192.168.1.10 uses the /24.

A route is installed only if it is usable. A route with a next-hop address is resolved recursively to an outgoing
interface; if the next hop cannot be resolved, the route is not installed.

## Default administrative distances
| Source | AD |
|---|---|
| Connected | 0 |
| Static | 1 |
| EIGRP summary | 5 |
| eBGP | 20 |
| EIGRP internal | 90 |
| IGRP | 100 |
| OSPF | 110 |
| IS-IS | 115 |
| RIP | 120 |
| EGP | 140 |
| ODR | 160 |
| EIGRP external | 170 |
| iBGP | 200 |
| Unknown | 255 (never installed) |

AD is local to the router and is not advertised in routing updates.

## Changing AD
- Per routing process: `distance 85` under `router ospf 100` makes OSPF routes (AD 85) beat internal EIGRP (90) on
  that router only. The neighbour keeps its own preference, so inconsistent AD changes can cause asymmetric routing,
  suboptimal paths, loops or black holes. Validate the design before and after.
- Floating static: `ip route 10.0.0.0 255.255.255.0 172.16.1.200 250` stays out of the table while the OSPF route
  (110) exists, and installs when OSPF withdraws it (its next hop must be reachable).

## Ask the router
```
show ip route                 ! codes legend and all installed routes
show ip route ospf            ! only routes from one source
```

## Verify
- [ ] You can explain each test destination as: each protocol's own metric, then lowest AD for installation, then
  longest prefix at forwarding.

## Checked
Date: 2026-11-08. Read in full: Cisco "Understand Administrative Distance" (document 15986, updated July 2026). The
second cited page (EIGRP document 8651-21) was dropped from sources and nothing in the skill relies on it.
Confirmed: [AD/metric] format, route-code legend, two-stage RIB/FIB behaviour, the default AD table (including EGP
140 and ODR 160, now added), AD being local, `distance` and floating-static examples, and the unresolvable next hop
rule.
Removed: the claim that longest prefix match beats "static AD 1 or BGP AD 200" as a worked example (replaced by the
page's own example), `maximum-paths`, gateway-of-last-resort meaning and "not set drops packets", the
`show ip route <ip>`, `longer-prefixes`, `summary` and `show ip cef` commands, `show ip route ospf | i`, the "L routes
are not forwarding entries" note, and the TenGigabitEthernet example line (none on the page).
Method: documentation only; no commands were run.
