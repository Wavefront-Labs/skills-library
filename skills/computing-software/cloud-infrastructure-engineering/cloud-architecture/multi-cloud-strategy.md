---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-cloud-strategy
name: multi-cloud-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, deployment-models, multi-cloud-strategy, multi-cloud, portability, lowest-common-denominator, best-of-breed, cloud-concentration-risk, dora-regulation]
level: advanced
status: draft
description: "Decide what multi-cloud means for you: workload-per-cloud vs portable vs active-active, real drivers (M&A, regulation, best-of-breed), costs, common platform."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/hybrid/strategy", "https://cloud.google.com/architecture/hybrid-multicloud-patterns", "https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-cloud strategy and its costs

## Levels (pick deliberately)
1. **Workload-per-cloud** (most common): each workload lives on one cloud chosen for fit
   (analytics on one, M365-adjacent apps on Azure, acquired company stays on its cloud). Low cost; shared governance needed.
2. **Portable**: workloads *can* move (containers, Terraform, open data formats), but run on one. Moderate cost.
3. **Active-active across clouds**: same workload live on two clouds. Very expensive — data
   replication, double skills, lowest-common-denominator services. Rarely justified.

## Legitimate drivers
M&A; regulator-driven concentration-risk or exit requirements (e.g. EU DORA requires exit
strategies for critical ICT third parties — usually satisfied by documented, tested exit plans,
not active-active); best-of-breed services; customer requirements (sell into their cloud marketplace);
commercial leverage.

## Costs
Duplicate landing zones, security tooling, skills and on-call; lost volume discounts; egress
between clouds; lowest-common-denominator designs that forgo managed services.

## Minimum common platform
Single IdP, common tagging/cost data (FOCUS), central SIEM, policy-as-code per cloud with shared
control objectives, Terraform for IaC, consistent CI/CD, one service catalogue.

## Verify
- [ ] Written strategy states the level per workload tier and the driver.
- [ ] Exit plans for critical workloads exist and have been tabletop-tested.
