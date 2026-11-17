---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-operating-model
name: cloud-operating-model
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-strategy, cloud-operating-model, centralised-vs-federated, platform-team, cloud-adoption-framework]
level: advanced
status: draft
description: "Choose and design a cloud operating model: centralised, enterprise, distributed or federated, with responsibilities, platform team and guardrails."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/operating-model/compare", "https://docs.aws.amazon.com/whitepapers/latest/building-cloud-operating-model/building-cloud-operating-model.html", "https://teamtopologies.com/key-concepts"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud operating model

CAF compares operating models by who owns governance, platform and workload operations:
**decentralised**, **centralised**, **enterprise** (centralised platform with workload teams
operating their apps) and **distributed**. Most large organisations settle on a federated
"platform plus product teams" shape.

## Steps
1. **Assess context**: number of teams, regulatory pressure, maturity, speed expectations,
   existing IT structure.
2. **Assign responsibilities** across central functions (governance, security baseline,
   landing zone, identity, network, FinOps) and workload teams (architecture, deploy, run,
   cost) in a RACI.
3. **Platform team** as an internal product: landing zone, golden paths, self-service
   account vending; measured by adoption and lead time, not tickets closed.
4. **Guardrails over gates**: preventive policy at the organisation level, detective
   controls, and freedom inside them.
5. **Funding**: platform costs as shared overhead allocated by a driver; workload costs to teams.
6. **Support model**: who is on call for what; escalation from workload team to platform team.
7. Revisit as maturity increases; many start centralised and federate.

## Gotchas
- Fully decentralised without guardrails creates 50 different landing zones.
- Central teams that do everything for workload teams become the bottleneck that cloud was meant to remove.

## Verify
- [ ] RACI agreed and published.
- [ ] Self-service paths exist for the most common requests.
