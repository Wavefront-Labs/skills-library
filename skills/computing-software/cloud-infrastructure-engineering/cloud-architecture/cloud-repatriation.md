---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-repatriation
name: cloud-repatriation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, deployment-models, cloud-repatriation, private-cloud, on-premises, colocation, workload-placement, egress-waiver, steady-state-workloads]
level: advanced
status: draft
description: "Evaluate moving workloads from public cloud to private cloud or colo: candidate profile, full cost incl. people and refresh, capability loss, exit and egress."
sources: ["https://www.finops.org/framework/capabilities/architecting-for-cloud/", "https://csrc.nist.gov/pubs/sp/800/145/final", "https://aws.amazon.com/blogs/aws/free-data-transfer-out-to-internet-when-moving-out-of-aws/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Private cloud / repatriation decision

## Candidate profile
Large, **steady, predictable** usage (storage-heavy archives, constant compute, high egress such
as media delivery), mature ops team, little use of managed/higher-level services. Spiky,
fast-changing or managed-service-heavy workloads are poor candidates.

## Steps
1. **Optimise in place first**: rightsizing, commitments, storage tiering, egress via CDN/
   interconnect, renegotiated discounts. Many repatriation cases disappear here.
2. **Full cost model, 5 years**: hardware with refresh, colo/power, network, licences, spares,
   **people** (hardware ops, on-call, capacity planning), DR site, procurement lead times, vs
   optimised cloud cost.
3. **Capability loss**: managed DBs, global edge, elastic burst, security services, compliance
   attestations — what replaces each and who runs it?
4. **Exit mechanics**: data transfer volume/time, egress costs (major providers offer egress fee
   waivers for customers leaving, subject to conditions — request through support), parallel
   running period, contract commitments outstanding (EDP/MACC, RIs).
5. Consider hybrid: keep elastic/edge/managed parts in cloud, move steady base load.

## Gotchas
- Comparing list cloud prices to discounted hardware quotes.
- Underestimating time to procure and stand up hardware and the skills to run it at cloud-like reliability.

## Verify
- [ ] Decision memo with optimised-cloud vs on-prem 5-year model and sensitivity analysis.
