---
id: computing-software.systems-network-administration.cisco-networking.ospf-max-lsa-lsdb-protection
name: ospf-max-lsa-lsdb-protection
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ospf, max-lsa, lsdb-protection, redistribution-limit, ospf-hardening]
level: practitioner
status: draft
description: "Protect OSPF routers from LSDB explosions with max-lsa and redistribution maximum-prefix, choose thresholds and recover from ignore state."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/configuration/xe-16/iro-xe-16-book/iro-limit-lsa.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/m1.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LSDB protection with max-lsa

## The risk
A misconfiguration (redistributing a full BGP table into OSPF, a looping redistribution) can
flood thousands of LSAs, exhaust memory and CPU on every router in the domain.

## max-lsa
```
router ospf 1
 max-lsa 12000 75 ignore-time 5 ignore-count 5 reset-time 10
```
| Parameter | Meaning |
|---|---|
| 12000 | maximum non-self-generated LSAs |
| 75 | warning threshold percent (log at 75%) |
| `ignore-time 5` | minutes the process stays shut (ignore state) after exceeding |
| `ignore-count 5` | after this many ignore cycles the process stays down permanently |
| `reset-time 10` | minutes of normal operation after which the ignore count resets |
| `warning-only` | log, do not shut down |

When exceeded, OSPF drops all adjacencies and stays down for ignore-time, then retries.
Logs: `%OSPF-4-OSPF_MAX_LSA_THR`, `%OSPF-3-OSPF_MAX_LSA`.

## Limit redistribution at the source
```
router ospf 1
 redistribute maximum-prefix 2000 80 warning-only
```
Limits the number of externals this ASBR generates; without `warning-only`, extra prefixes are not redistributed.

## Choosing numbers
- Baseline: `show ip ospf database database-summary` total, times 2-3 headroom.
- Start with `warning-only` for a few weeks, then enforce.
- Same limit on all routers in an area, or the smallest-limit router isolates itself.

## Recovery
After the source is fixed, `clear ip ospf process` (or wait the ignore-time). If ignore-count
was reached the process stays down until cleared.

## Verify
```
show ip ospf | include LSA|Maximum
show ip ospf database database-summary
```
- [ ] Warning thresholds reach syslog/monitoring.
