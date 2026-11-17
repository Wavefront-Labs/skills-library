---
id: computing-software.systems-network-administration.cisco-networking.administrative-distance-tuning-distance-command
name: administrative-distance-tuning-distance-command
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, administrative-distance, distance-command, path-control, floating-static-route, route-preference]
level: practitioner
status: docs-checked
description: "Change route preference on Cisco IOS with the distance command and floating static routes: default AD table, per-source distance, ordering, and the risks of local AD changes."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/15986-admin-distance.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_pi/command/iri-cr-book/iri-cr-a1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tuning administrative distance with the distance command

AD ranks the trustworthiness of route sources. When several sources offer the same destination prefix and prefix length, the lowest AD is installed. AD is local to the router and is not advertised in routing updates.

## Default distances
Connected 0, static 1, EIGRP summary 5, external BGP 20, internal EIGRP 90, IGRP 100, OSPF 110, IS-IS 115, RIP 120, EGP 140, ODR 160, external EIGRP 170, internal BGP 200, unknown 255. A route with AD 255 is not installed.

## Forms
```
router ospf 100
 distance 85                                  ! all routes of this process
router eigrp 109
 distance 90 192.168.7.0 0.0.0.255            ! routes learned from this source
 distance 120 172.16.1.3 0.0.0.255 [ACL]      ! optional standard ACL on incoming updates
ip route 10.0.0.0 255.255.255.0 172.16.1.200 250   ! floating static route (AD 250)
```
- `distance <ad> <ip-address> <wildcard-mask> [standard-acl | name]`: ad is 10 to 255 (0 to 9 reserved). The address is where routes are learned from; the ACL is applied to incoming routing updates when a network is inserted into the routing table. Extended ACLs are not supported; use a standard ACL.
- For EIGRP the plain `distance` command sets only internal routes; use `distance eigrp` for external ones. For BGP it sets the eBGP distance.
- Other variants exist (`distance ospf`, `distance eigrp`, `distance bgp`, IPv6, CLNS) but this skill does not give their syntax; take it from the Cisco command reference entries for each.

## Gotchas
- Order matters: enter per-source `distance` commands from the least to the most specific network. Adding a later `distance 255` over a range overrides the values for all networks in it.
- AD decides which route is installed, not which is used to forward. Longest prefix match is applied later at forwarding, so a lower AD never overrides a longer prefix.
- AD is local; an inconsistent design across routers can cause asymmetric or suboptimal routing, loops or black holes. Validate before and after a change.
- A floating static route needs an AD above the primary source (for example 250 versus OSPF 110) and a resolvable next hop, or it is not installed.

## Verify
- `show ip protocols` shows the default distance of each active process plus user-configured distances (a "Distance: (default is 115)" line followed by address, wildcard mask, distance and list columns).
- `show ip route` shows `[AD/metric]`, for example `[90/130816]`; the route code changes (D to O) when a lowered OSPF AD wins.

## Checked
Date: 2026-11-08
Read in full: Cisco "Understand Administrative Distance" (document 15986, rev 3.0 of 20 Jul 2026). Read in the command reference page (iri-cr-a1): the `distance (IP)` entry from syntax through related commands, found by search of a 274k-character page, not read end to end.
Confirmed: default AD table, 255 not installed, AD local, same prefix length rule, `distance 85` under `router ospf 100` example, floating static `ip route ... 250`, longest-prefix-match note, `distance (IP)` syntax, 10 to 255 range, standard-ACL-only note, least-to-most-specific ordering and the 255 override note, EIGRP internal-only and BGP eBGP-only behaviour, `show ip protocols` output, `[AD/metric]` format.
Removed: `distance ospf external/inter-area/intra-area`, `distance eigrp 90 175`, `distance bgp 20 200 200` and the per-neighbour BGP form (those entries are not on the cited page), the OSPF router-ID source claim, the redistribution and backdoor advice, and the "clear ip route *" claim: none appear on the cited pages.
Method: documentation only; no commands were run.
