---
id: computing-software.systems-network-administration.cisco-networking.ospf-ecmp-maximum-paths
name: ospf-ecmp-maximum-paths
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ospf, maximum-paths, ecmp, equal-cost-multipath, cef-load-sharing, ospf-cost]
level: practitioner
status: draft
description: "Make OSPF install equal-cost paths: maximum-paths, matching costs, CEF per-destination hashing, and why traffic still uses one link."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/m1.html
  - https://www.cisco.com/c/en/us/support/docs/ip/express-forwarding-cef/18285-loadbal-cef.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OSPF ECMP and maximum-paths

## Behaviour
OSPF installs all equal-cost paths up to `maximum-paths` (IOS default 4, max 16 or 32 by platform).
OSPF does no unequal-cost load balancing.
```
router ospf 1
 maximum-paths 8
show ip route 10.30.0.0
  O 10.30.0.0/16 [110/20] via 10.0.1.2, Gi0/1
                 [110/20] via 10.0.2.2, Gi0/2
```

## Getting equal costs
- Cost = reference bandwidth / interface bandwidth. Set `auto-cost reference-bandwidth 100000`
  (100 Gbps) on **every** router so 10G and 40G links are not all cost 1.
- Paths must be equal end to end: one link with a different `ip ospf cost` breaks ECMP.
- Inter-area/external: the same route type (O, O IA, E1, E2) and for E2 the same forward metric.

## How traffic is spread
CEF hashes per destination (source+destination IP by default, optional L4 ports):
```
ip cef load-sharing algorithm universal
show ip cef 10.30.5.5 internal     ! hash buckets per path
show ip cef exact-route 10.1.1.10 10.30.5.5   ! which path this flow takes
```
A few large flows can still land on one link (polarisation). Mix in L4 ports with
`ip cef load-sharing algorithm include-ports source destination` where supported.

## Gotchas
- `maximum-paths 1` disables ECMP: used to force deterministic paths.
- ECMP over links with different MTUs or latency causes reordering-sensitive app issues.
- On Catalyst, the hardware ECMP limit can be lower than the configured value; check platform docs.

## Verify
- [ ] `show ip route <prefix>` lists every expected next hop.
- [ ] Interface counters on parallel links roughly balanced under load.
