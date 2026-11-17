---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.migration-strategy-lift-and-shift-vs-replatform
name: migration-strategy-lift-and-shift-vs-replatform
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-migration, migration-strategy, 7-rs, 6-rs, rehost, lift-and-shift, replatform, lift-tinker-and-shift, refactor, re-architect, repurchase, retire, retain, relocate, application-portfolio, discovery, dependency-mapping, migration-waves, aws-application-migration-service, mgn, azure-migrate, migrate-to-virtual-machines, database-migration-service, dms, cutover, map-program]
level: advanced
status: draft
description: "Choose rehost, replatform, refactor, repurchase, retire or retain per application using a scored portfolio, dependency maps and migration waves, and plan a cutover with rollback."
sources: ["AWS Prescriptive Guidance - Migration strategies (7 Rs)", "Microsoft Cloud Adoption Framework - Migrate", "Google Cloud - Migration to Google Cloud: getting started"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration strategy — lift-and-shift vs replatform vs refactor, per app

**Goal:** a portfolio where every application has a chosen migration path with a reason,
grouped into dependency-safe waves, so the migration finishes on time and doesn't simply
move the data-centre bill to a bigger cloud bill.

## 1. The 7 Rs (AWS naming; Azure/GCP use near-equivalents)
| R | What changes | Speed | When |
|---|---|---|---|
| **Retire** | switch it off | fastest | ~10-20% of portfolios are unused or duplicated |
| **Retain** | stays on-prem for now | — | hard dependencies, recent hardware, licence lock |
| **Relocate** | hypervisor-level move (VMware Cloud on AWS, Azure VMware Solution, GCVE) | fast | large VMware estates on a deadline |
| **Rehost** (lift and shift) | VM → cloud VM, no code change | fast | deadline-driven exits, low-value apps |
| **Replatform** (lift-tinker-shift) | swap a component for managed: self-run DB → RDS/Azure SQL/Cloud SQL, app → containers, cron → managed scheduler | medium | the common sweet spot |
| **Repurchase** | move to SaaS | medium | commodity functions (CRM, HR, ticketing) |
| **Refactor** | re-architect (serverless, microservices, event-driven) | slow | apps with real business reasons to change |

## 2. Discover before deciding
- Inventory with agents or agentless discovery (AWS Application Discovery Service / Migration
  Evaluator, Azure Migrate, Google Migration Center): CPU/memory **utilisation**, not
  allocation, plus OS, licences, network flows.
- **Dependency mapping** from netflow/connection data — interviews miss the nightly job that
  reads a share on another server. Group apps that talk at low latency into the same wave.

## 3. Score each app
Simple scoring sheet (1-5 each): business value, rate of change planned, technical debt,
licensing constraints, team skill, data gravity/latency sensitivity, compliance.
Rules of thumb:
- Low value, little change planned → **rehost** (or retire).
- Self-managed database, OS patching burden, standard engine → **replatform** the data tier first; it pays back fastest in ops time.
- Heavy roadmap investment anyway → **refactor**, but not as part of the move deadline.
- Commercial off-the-shelf with vendor SaaS → **repurchase**.

"Rehost now, optimise later" is legitimate only with a dated optimisation backlog — "later" often never comes and rehosted VMs run 24/7 at on-prem sizing.

## 4. Waves and cutover
- Wave 0: pilot with 2-3 low-risk apps to prove landing zone, networking, tooling, runbooks.
- Waves of ~10-30 apps grouped by dependency and owning team; each with a cutover window.
- Rehost tooling: AWS Application Migration Service (block-level continuous replication,
  test launches), Azure Migrate, Migrate to Virtual Machines (GCP).
- Data: DMS / Azure DMS / Database Migration Service with CDC for near-zero downtime;
  validate row counts and checksums before cutover.
- Cutover runbook: freeze, final sync, DNS/LB switch (lower TTL days before), smoke tests,
  **go/no-go criteria and a timed rollback point** (on-prem kept read-only until after it).

## Gotchas
- Lifted VMs sized like on-prem hosts cost more — rightsize from utilisation at migration time.
- Licences: BYOL rules (Windows Server, SQL Server, Oracle) differ by provider and tenancy; dedicated hosts may be required. Check before choosing the target.
- Hybrid latency: an app moved without its database now does every query over a WAN link.
- Hard-coded IPs and hostnames in configs, firewall allow-lists at partners, and SMTP relays break at cutover.
- Egress costs for the transition period when data flows back on-prem.

## Verify
- [ ] Every app has an R, a reason and an owner; retire candidates were actually confirmed unused.
- [ ] Dependency map came from observed traffic, not only interviews.
- [ ] Each wave has a tested runbook with go/no-go and rollback criteria.
- [ ] Data migrations validated by counts/checksums before cutover.
- [ ] Rehosted apps have a dated optimisation (rightsize/replatform) ticket.

Uncertain: the retire percentage and wave sizes are common practitioner ranges, not a standard.
Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-account-landing-zone, computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.rightsizing-compute-workloads
