---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.migration-readiness-assessment
name: migration-readiness-assessment
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-assessment, migration-readiness-assessment, mra, cloud-readiness, cloud-adoption-framework]
level: practitioner
status: draft
description: "Run a migration readiness assessment across business, people, governance, platform, security and operations, and turn gaps into a readiness plan."
sources: ["https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-readiness/welcome.html", "https://docs.aws.amazon.com/whitepapers/latest/overview-aws-cloud-adoption-framework/foundational-capabilities.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration readiness assessment

Based on the AWS Migration Readiness Assessment (MRA) structured around CAF perspectives:
business, people, governance, platform, security, operations.

## Steps
1. **Workshop** with leadership, finance, security, operations, application owners (1-2 days).
2. **Score each perspective** (1-5) with evidence:
   - Business: clear drivers, executive sponsor, business case, funding.
   - People: skills plan, CCoE, change management, organisational design.
   - Governance: portfolio management, FinOps, risk and compliance mapping.
   - Platform: landing zone, network connectivity, IaC, CI/CD.
   - Security: identity federation, logging, detective controls, data protection.
   - Operations: monitoring, incident, backup, patching, service management in cloud.
3. **Identify blockers** (must fix before wave 1) vs improvements (can mature during waves).
4. **Readiness plan**: actions, owners, dates; typically a mobilise phase of 2-4 months
   building landing zone, skills, migration factory and a pilot migration.
5. **Re-assess** after the pilot and before scaling to large waves.

## Gotchas
- Scoring on intentions ("we plan to") inflates readiness; ask for evidence.
- Operations readiness is the most frequently skipped and causes post-migration incidents.

## Verify
- [ ] Each perspective scored with evidence and owner.
- [ ] Blockers closed before wave 1 start.
