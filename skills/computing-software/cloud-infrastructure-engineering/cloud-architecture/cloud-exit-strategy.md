---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-exit-strategy
name: cloud-exit-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-ecosystem, cloud-exit-strategy, vendor-lock-in, portability, exit-plan, dora]
level: advanced
status: draft
description: "Assess vendor lock-in per workload and write a tested cloud exit plan: lock-in register, portability choices, data egress, and regulator expectations such as DORA."
sources: ["https://www.eba.europa.eu/regulation-and-policy/internal-governance/guidelines-on-outsourcing-arrangements", "https://eur-lex.europa.eu/eli/reg/2022/2554/oj", "https://learn.microsoft.com/azure/cloud-adoption-framework/strategy/business-outcomes/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vendor lock-in assessment and exit strategy

Lock-in is a cost, not a sin. The goal is to know what leaving would cost per workload and to
keep that cost acceptable for critical services.

## Steps
1. **Lock-in register** per workload: proprietary services used (managed DB engine, queues,
   serverless runtime, IAM model, data warehouse), data volume, contractual terms
   (commitments, notice periods), skills. Rate switching effort (S/M/L/XL) and time.
2. **Decide deliberately.** For each proprietary service note the benefit gained. Accept
   lock-in where benefit is high and exit cost moderate; add an abstraction only where the
   workload is critical and exit is plausible.
3. **Portability levers**: open data formats (Parquet, PostgreSQL-compatible engines),
   containers and Kubernetes for compute, IaC with modules per provider, OpenTelemetry for
   telemetry, standard identity (SAML/OIDC).
4. **Exit plan** for critical or regulated services (EBA outsourcing guidelines and DORA
   require documented, tested exit strategies for critical ICT third-party services):
   triggers (provider failure, price change, regulatory order), target (other cloud or
   on-prem), data extraction method and egress cost, timeline, roles, contract clauses
   (data return, assistance period, deletion certificates).
5. **Test it**: export full data sets periodically and restore them outside the provider;
   time it. A desk-top walkthrough at minimum annually.

## Gotchas
- Data gravity: petabytes of egress take weeks and real money; know the number.
- Multi-cloud everything to avoid lock-in usually costs more than the exit would.
- Contracts without data-return assistance clauses make exit slow even when technically easy.

## Verify
- [ ] Every critical workload has a lock-in rating and exit plan owner.
- [ ] Last data export and restore test date recorded.
