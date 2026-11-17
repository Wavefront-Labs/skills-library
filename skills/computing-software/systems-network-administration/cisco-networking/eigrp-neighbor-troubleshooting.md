---
id: computing-software.systems-network-administration.cisco-networking.eigrp-neighbor-troubleshooting
name: eigrp-neighbor-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, eigrp, eigrp-neighbor, k-value-mismatch, as-mismatch, passive-interface, retry-limit, adjacency]
level: practitioner
status: draft
description: "Fix EIGRP neighbours that never form or keep resetting: AS and K-value mismatches, subnet and passive issues, authentication, retry limit exceeded, and unicast/multicast blocking."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/21324-trouble-eigrp.html
  - https://www.rfc-editor.org/rfc/rfc7868
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EIGRP neighbour troubleshooting

## Start here
```
show ip eigrp neighbors
!  H  Address     Interface  Hold Uptime  SRTT  RTO  Q Cnt Seq Num
show ip eigrp interfaces detail
show ip protocols | section eigrp
show logging | include DUAL
```
`%DUAL-5-NBRCHANGE` messages carry the reason (`K-value mismatch`, `retry limit exceeded`,
`holding time expired`, `Interface PEER-TERMINATION received`, `authentication failure`).

## Never forms
| Check | Requirement |
|---|---|
| AS number (classic) / autonomous-system (named af) | must match |
| K values | must match (`metric weights 0 1 0 1 0 0` default) |
| Subnet | primary addresses in the same subnet (secondaries do not form neighbours) |
| Interface enabled | `network` statement covers it; not `passive-interface` |
| Authentication | same key chain key ID and string, valid lifetime (needs NTP) |
| Multicast 224.0.0.10 | not blocked by ACL, firewall, or provider (use `neighbor x.x.x.x Gi0/1` for unicast) |

A one-way neighbour (one side sees it, other does not) is often an ACL dropping multicast in one
direction or a unicast `neighbor` statement configured on only one side (that also disables
multicast hellos on the interface).

## Keeps resetting
- `retry limit exceeded`: hellos work (multicast) but reliable unicast updates are not
  acknowledged. MTU problems, unicast blocked, or one-way link. Check `Q Cnt` non-zero and rising.
- `holding time expired`: hellos lost; congestion, CPU, or a flapping path. Compare hold times.
- `stuck in active`: queries not answered in 3 minutes; see SIA troubleshooting.

## Debugs (lab or with a conditional ACL)
```
debug eigrp packets hello
debug ip eigrp neighbor 10.0.12.2
```

## Gotchas
- Named mode vs classic interoperate on the wire; configuration differs only locally.
- Wide metrics (named mode) and classic metrics interoperate with the RIB scaling; K6 must match.
- Router ID duplicates break external route acceptance (externals from a router with your own RID
  are dropped), not the adjacency.

## Verify
- [ ] Neighbour uptime increasing, Q Cnt 0, SRTT stable.
- [ ] `show ip eigrp topology` shows expected successors.
