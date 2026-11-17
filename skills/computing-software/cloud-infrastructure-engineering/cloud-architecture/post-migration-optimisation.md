---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.post-migration-optimisation
name: post-migration-optimisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-execution, post-migration-optimisation, rightsizing, modernisation-backlog, optimise-phase]
level: practitioner
status: draft
description: "Optimise workloads after migration: rightsize from real cloud metrics, commit discounts, storage tiering, schedule non-prod and build the modernisation backlog."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/migrate/optimize-and-promote", "https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-retiring-applications/welcome.html", "https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post-migration optimisation

## Steps
1. **Wait for a representative window**: 2-4 weeks including a month-end for business apps
   before rightsizing.
2. **Rightsize compute** from cloud metrics (CPU, memory via agent, network); use provider
   recommenders (Compute Optimizer, Azure Advisor, Google Recommender) and validate against
   peaks.
3. **Storage**: switch to current-generation volumes (e.g. gp3), lower provisioned IOPS that
   is unused, apply object lifecycle tiers, delete migration snapshots and staging copies.
4. **Schedules**: stop non-production outside working hours.
5. **Commit discounts** only after rightsizing settles the baseline.
6. **Operational hardening**: backups verified, monitoring and alerts tuned, patching in the
   new tooling.
7. **Modernisation backlog**: capture replatform/refactor candidates found during migration
   with expected benefit; promote to the roadmap.

## Gotchas
- Buying reservations for unrightsized lift-and-shift instances locks in waste.
- Memory metrics are not collected by default on most VMs; install the agent first.

## Verify
- [ ] Rightsizing actions applied with before/after cost.
- [ ] Migration leftovers (snapshots, staging) removed.
