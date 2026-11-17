---
id: computing-software.systems-network-administration.cisco-networking.bgp-default-originate-and-partial-tables
name: bgp-default-originate-and-partial-tables
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, bgp, default-originate, partial-table, full-table, maximum-prefix, isp]
level: practitioner
status: docs-checked
description: "Choose between default-only, partial and full BGP tables from ISPs, and originate defaults to neighbours conditionally with default-originate route-map."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/command/irg-cr-book/bgp-m1.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/command/irg-cr-book/bgp-n1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP default-originate and partial tables

## What to ask the ISP for
| Feed | Memory/CPU | Path choice | Use when |
|---|---|---|---|
| Default only | tiny | none; outbound by local pref/AD | single-homed or simple active/standby |
| Partial (customer routes + default) | small | best exit to ISP customers | dual ISP, modest router |
| Full table | large (size it for the current table) | optimal per prefix | multi-homed, router sized for it |

## Sending a default to a neighbour
```
router bgp 65010
 address-family ipv4
  neighbor 10.0.0.2 default-originate
```
Syntax: `neighbor {ip-address | peer-group-name} default-originate [route-map map-name]`. By default no
default route is sent. The command does not need 0.0.0.0 in the local routing table.

Conditional (only while the upstream is healthy):
```
access-list 10 permit 198.51.100.0
route-map DEFAULT-IF-UPSTREAM permit 10
 match ip address 10
router bgp 65010
 address-family ipv4
  neighbor 10.0.0.2 default-originate route-map DEFAULT-IF-UPSTREAM
```
With a route map, 0.0.0.0 is injected only if the route map has a `match ip address` clause and a
route exists that matches the access list exactly. The route map can contain other match clauses
too. Standard or extended access lists are documented for this command.

## Advertising a default from the table
Redistributing an IGP default into BGP is not allowed unless `default-information originate` is
configured under BGP.

## Receiving partial tables
Filter what you accept to protect memory:
```
neighbor 203.0.113.1 prefix-list ISP-IN in
neighbor 203.0.113.1 maximum-prefix 950000 90 restart 30
```
`maximum-prefix maximum [threshold] [restart restart-interval]`: with `restart`, the router
re-establishes a session that was disabled because the limit was exceeded, after the interval.

## Verify
```
show ip bgp neighbors 10.0.0.2 advertised-routes
show ip bgp 0.0.0.0
```
- [ ] Downstream sees the default only while the condition holds (test by shutting the upstream).

## Checked
2026-10-31. Confirmed in the Cisco BGP command reference: `neighbor default-originate [route-map]`
syntax, default (nothing sent), no local 0.0.0.0 needed, route-map `match ip address` exact-match
condition, `neighbor maximum-prefix` with `restart`, and the `default-information originate`
requirement for redistributed defaults. Removed: the "~1M IPv4 + 200k+ IPv6" table sizes, the
`network 0.0.0.0` RIB remark and the prefix-list form of the condition (the reference documents
access lists), because no fetched page confirms them.
Method: documentation only; no commands were run.
