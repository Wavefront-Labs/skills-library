---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.n-plus-two-redundancy-planning
name: n-plus-two-redundancy-planning
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, capacity-planning, n-plus-two, n-plus-one-redundancy, failure-domains, maintenance]
level: advanced
status: docs-checked
description: "Plan N+2 redundancy so peak traffic is served while one planned and one unplanned outage are in progress, apply it per failure domain, and verify with drills."
sources: ["https://sre.google/sre-book/service-best-practices/", "https://sre.google/sre-book/software-engineering-in-sre/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# N+2 redundancy planning

**Goal:** peak demand is still served while one unit is down for planned maintenance and another fails unexpectedly.

## Definitions
- **N** = units needed to handle peak traffic.
- **N+2** = the SRE Book's capacity-planning guidance: provision to handle a simultaneous planned and unplanned
  outage without making the user experience unacceptable, so peak traffic can be handled by N instances (possibly
  in degraded mode) while the largest 2 instances are unavailable.
- Redundancy levels are a prioritisation choice: the SRE Book's intent-based capacity planning discussion shows
  teams trading N+2 for one service against N+1 or N+0 for another, and notes N+2 may not be optimal for every
  service.

## Apply per failure domain
Pick the unit (instance, zone, cluster, region). Rule of thumb from the definition: capacity per unit = peak /
(units - 2).
Example (arithmetic only): peak 9,000 QPS over 5 clusters; with any 2 down, 3 must carry peak, so each must
handle 9,000 / 3 = 3,000 QPS.

## Trade-offs
- N+2 on small N costs a large fraction of extra units; on large N it is small.
- Use load shedding and graceful degradation to survive beyond N+2 instead of overprovisioning further.
- Dependencies must match: N+2 frontends over an N+0 database is N+0.

## Verify
- [ ] Capacity plan lists N per failure domain and the computed per-unit capacity.
- [ ] Drill: take one unit out for maintenance and kill another at peak-like load; the SLO holds.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Service Best Practices" (Capacity Planning: "N + 2" definition) and "Software Engineering in SRE" (intent-based capacity planning: N+2 for Foo versus N+1 for Bar).
Removed: PodDisruptionBudget row, zone headroom claim, region and zone examples, percentage overhead figures and the NALSD source (not about N+2).
Method: documentation only; no commands were run.
