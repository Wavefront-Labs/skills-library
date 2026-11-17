---
id: computing-software.systems-network-administration.cisco-networking.ospf-default-information-originate
name: ospf-default-information-originate
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ospf, default-information-originate, default-route, internet-edge, route-map, e2]
level: practitioner
status: docs-checked
description: "Inject a default route into OSPF correctly: conditional vs always, metric and metric-type for edge preference, route-map conditions, and stub and NSSA area defaults."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/13692-21.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/configuration/xe-16/iro-xe-16-book.html
  - https://www.rfc-editor.org/rfc/rfc2328
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPF default-information originate

By default, OSPF routers in normal areas do not generate a default route, even if they have one.
`default-information originate [always] [metric metric-value] [metric-type type-value] [route-map map-name]`
generates an external link with link-state ID 0.0.0.0 and mask 0.0.0.0 and makes the router an ASBR.
The defaults are metric 1 and metric-type E2.

## Conditional (default)
```
ip route 0.0.0.0 0.0.0.0 203.0.113.1
router ospf 1
 default-information originate metric 10 metric-type 2
```
The router advertises 0/0 only while it has a default route in its own routing table. Lose the
static and the advertisement is withdrawn.

## always
```
 default-information originate always
```
Advertises 0/0 even when the router has no default of its own. Use only on a router that truly
always has a path (for example it fronts a firewall cluster). Otherwise traffic blackholes at this
router when the ISP fails.

## Two internet edges
```
! Edge A (primary)
 default-information originate metric 10 metric-type 1
! Edge B (backup)
 default-information originate metric 100 metric-type 1
```
RFC 2328 describes two external metric types. Type 1 adds the internal path cost to the
advertised metric, so routers prefer the nearer edge for equal external metrics. Type 2 (the
default) ignores internal cost and compares only the external metric. For primary/backup use
different metrics; for nearest-exit use equal metrics with Type 1.

## Make the default depend on something better than a static
A static route to the ISP stays up even when the ISP's upstream is dead. Tie the static to a
tracking object (IP SLA reachability, see the Cisco IP SLA configuration guide), or use
`default-information originate route-map HAS-ISP` with a route-map matching a prefix learned
from the ISP.

## Stub and NSSA areas
- Stub and totally stubby: the ABR generates a summary LSA with link-state ID 0.0.0.0 even if it
  has no default of its own, so you do not need `default-information originate`.
- NSSA: the ABR does not generate a default by default. Force it with
  `area 10 nssa default-information-originate` on the ABR; it sends a Type 7 LSA with
  link-state ID 0.0.0.0 inside the NSSA.

## Verify
```
show ip ospf database external 0.0.0.0
show ip route 0.0.0.0
!  O*E2 0.0.0.0/0 [110/10] via 10.0.12.1
```
- [ ] Shutting the ISP link (or failing the tracked condition) withdraws the LSA from that edge and
  the backup edge's default takes over.

## Checked
2026-10-31. Confirmed against the Cisco OSPF default-route design page (13692-21): the generated
external link, metric 1 and E2 defaults, `always`, route-map option, stub/totally-stubby summary
default and NSSA Type 7 default with `area <id> nssa default-information-originate` (Cisco OSPF
command reference), and RFC 2328 (Type 1 and Type 2 external metrics). Removed: the explicit IP
SLA configuration block and the "within seconds" withdrawal timing, which no fetched page confirms.
Method: documentation only; no commands were run.
