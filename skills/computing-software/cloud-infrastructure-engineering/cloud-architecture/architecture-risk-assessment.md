---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-risk-assessment
name: architecture-risk-assessment
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-planning, transition-architecture, togaf, architecture-risk-assessment, risk-register, residual-risk]
level: advanced
status: draft
description: "Assess architecture risk for a cloud programme: identify, classify impact and likelihood, mitigate, record residual risk and review it at phase gates."
sources: ["https://pubs.opengroup.org/togaf-standard/adm-techniques/chap09.html", "https://csrc.nist.gov/pubs/sp/800/30/r1/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture risk assessment

TOGAF risk management: identify risks, classify them, determine **initial** risk (before
mitigation), mitigate, then determine **residual** risk and monitor.

## Steps
1. **Identify** across categories: technical (unproven service, scaling limit), delivery
   (skills, dependencies), security and compliance (residency, new attack surface),
   operational (on-call readiness), commercial (lock-in, price change), organisational.
   Use ATAM-style sensitivity and trade-off points from design reviews as sources.
2. **Classify** impact (catastrophic, critical, marginal, negligible) and frequency
   (frequent, likely, occasional, seldom, unlikely); derive effect (extremely high to low)
   from a matrix agreed with enterprise risk.
3. **Mitigate**: avoid (change design), reduce (PoC, redundancy, training), transfer
   (contract, insurance), accept (with sign-off by an accountable owner).
4. **Residual risk**: re-score after mitigation; anything still high needs sponsor acceptance.
5. **Record** in the risk register: ID, description, owner, scores, mitigation, due date,
   status, link to ADRs.
6. **Review** at each phase gate and before cutovers.

## Gotchas
- Risks without owners never get mitigated.
- Copy-paste generic risks ("project may overrun") crowd out real architecture risks.

## Verify
- [ ] Top risks each have owner, mitigation and residual score.
- [ ] Accepted high residual risks have documented sponsor sign-off.
