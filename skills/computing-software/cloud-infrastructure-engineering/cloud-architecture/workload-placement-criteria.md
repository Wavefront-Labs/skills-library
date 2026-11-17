---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.workload-placement-criteria
name: workload-placement-criteria
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, deployment-models, workload-placement-criteria, workload-placement, hybrid-cloud, data-gravity]
level: practitioner
status: draft
description: "Decide where each workload runs (public cloud region, private cloud, edge, SaaS) using a weighted criteria matrix: data, latency, compliance, cost and dependencies."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/plan/", "https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-retiring-applications/welcome.html", "https://csrc.nist.gov/pubs/sp/800/145/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Workload placement decision criteria

## Steps
1. **Collect facts per workload**: data classification and residency, latency needs to users
   and to other systems, dependency graph (what it talks to and how chatty), licensing,
   hardware needs (GPU, mainframe, specialist appliances), utilisation profile, criticality.
2. **Criteria and weights** (agree weights with stakeholders before scoring):
   - Regulatory/residency (often a hard gate, not a weight).
   - Data gravity: where the large datasets live; moving compute is cheaper than moving TB.
   - Latency: users, factory floor (edge), trading venues (colo).
   - Dependency affinity: chatty dependencies must be co-located or the network bill and
     latency explode.
   - Cost: steady flat load favours owned capacity; spiky or growing load favours public cloud.
   - Skills and operating model maturity per venue.
   - Exit/lock-in tolerance.
3. **Score venues** (public region A/B, private, edge, SaaS) and apply hard gates first.
4. **Group by dependency clusters** so placement decisions move together (move groups).
5. **Record the decision** with the deciding criteria so it can be revisited when facts change.

## Gotchas
- Splitting a chatty app and its database across venues is the classic placement failure.
- "Strategic" defaults (everything to cloud) without gates miss residency blockers.

## Verify
- [ ] Hard gates applied before weighted scoring.
- [ ] Placement recorded per dependency cluster with rationale.
