---
id: computing-software.systems-network-administration.network-design.availability-nines-mtbf-mttr
name: availability-nines-mtbf-mttr
category: computing-software
field: systems-network-administration
product: network-design
tags: [high-availability, availability-nines, mtbf, mttr, serial-parallel-availability, sla-design, redundancy]
level: practitioner
status: verified
description: "Calculate network availability: nines to downtime, MTBF/MTTR, serial vs parallel components, why redundancy needs fast MTTR and independent failures, and setting realistic SLAs."
sources:
  - https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Campus/HA_campus_DG/hacampusdg.html
  - https://sre.google/sre-book/availability-table/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Availability: nines, MTBF and MTTR

## Nines to downtime per year
Recomputed in Python (365-day year, 30.4-day month); the 99.99 % month figure is 4.38 min.
| Availability | Downtime/year | Downtime/month |
|---|---|---|
| 99 % | 3.65 days | 7.3 h |
| 99.9 % | 8.76 h | 43.8 min |
| 99.95 % | 4.38 h | 21.9 min |
| 99.99 % | 52.6 min | 4.4 min |
| 99.999 % | 5.26 min | 26 s |

## Single component
A = MTBF / (MTBF + MTTR).
A switch with MTBF 200,000 h and MTTR 4 h (spare on site): 200000 / 200004 = 99.998 %. Same switch
with next-business-day replacement (MTTR 48 h): 99.976 %. MTTR matters as much as hardware quality.

## Serial (all must work): multiply
Access switch 99.98 % x distribution 99.99 % x core 99.99 % x WAN circuit 99.9 % x firewall 99.98 %
= 99.84 %: ~14 h/year. The weakest link (usually the WAN circuit or a single firewall) dominates.

## Parallel (any one is enough): 1 - product of unavailabilities
Two WAN circuits at 99.9 % each, independent: 1 - (0.001 x 0.001) = 99.9999 %. In practice:
- Failures are not independent (same conduit, same carrier POP, same power feed, same software bug).
  Real dual circuits deliver far less than the six nines the formula gives, by an amount
  you must estimate from shared-risk analysis. Path diversity is what buys independence.
- Failover is not instant: add the convergence time per failure x failure frequency.

## Using it in design
- Model each critical path (user -> application) as a chain; find the components without a parallel
  partner.
- Spend on the biggest contributor first (usually a single WAN link or single firewall), then MTTR
  (spares, monitoring, runbooks).
- Planned maintenance counts against availability unless the SLA excludes it; redundancy lets you
  maintain without downtime.

## Verify
- [ ] Each critical service has a calculated availability with assumptions written down, and the SLA
  offered to the business is at or below it.
