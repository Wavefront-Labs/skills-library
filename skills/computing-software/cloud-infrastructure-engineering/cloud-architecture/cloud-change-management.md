---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-change-management
name: cloud-change-management
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-strategy, cloud-change-management, organisational-change, adkar, cloud-adoption]
level: practitioner
status: draft
description: "Manage the organisational change of cloud adoption: stakeholder impact, ADKAR-based plans, role transitions for infra and ops staff, resistance and adoption metrics."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/strategy/", "https://docs.aws.amazon.com/whitepapers/latest/overview-aws-cloud-adoption-framework/people-perspective.html", "https://www.prosci.com/methodology/adkar"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Organisational change management for cloud adoption

## Steps
1. **Impact assessment by group**: infrastructure, operations, security, finance,
   procurement, developers, service desk; what changes in daily work, skills, roles and
   performance measures.
2. **Plan per group with ADKAR**: Awareness (why), Desire (what is in it for them), Knowledge
   (training), Ability (hands-on practice, sandboxes, pairing), Reinforcement (recognition,
   updated job descriptions, metrics).
3. **Role transitions**: map old roles to new (server admin to platform engineer, network
   engineer to cloud network/IaC); publish paths and certification support early.
4. **Sponsorship**: visible executive sponsor and a coalition of respected engineers as
   champions.
5. **Address resistance** directly: job security fears, loss of control; involve sceptics in
   guardrail design.
6. **Measure adoption**: training completion, sandbox usage, teams self-serving, tickets vs
   self-service ratio, engagement survey.

## Gotchas
- Treating cloud as only a technology project; most failed adoptions are people failures.
- Announcing new roles without the training budget breeds resistance.

## Verify
- [ ] Impact assessment and ADKAR plan per group.
- [ ] Adoption metrics reported to the sponsor monthly.
