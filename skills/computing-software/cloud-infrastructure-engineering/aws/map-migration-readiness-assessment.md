---
id: computing-software.cloud-infrastructure-engineering.aws.map-migration-readiness-assessment
name: map-migration-readiness-assessment
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, migration, map-program, migration-acceleration-program, readiness-assessment, migration-readiness-assessment, mra, cart, cloud-adoption-readiness-tool, migration-evaluator, business-case, map-migrated-tag, cloud-adoption-framework]
level: advanced
status: draft
description: "Run the AWS Migration Acceleration Program: readiness assessment (MRA, CART, Migration Evaluator business case), mobilize-phase landing zone and skills, and MAP credit tagging."
sources: ["https://aws.amazon.com/migration-acceleration-program/", "https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-migration/overview.html", "https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-readiness/welcome.html", "https://docs.aws.amazon.com/migrationhub/latest/ug/tagging-for-map.html", "https://aws.amazon.com/migration-evaluator/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration Acceleration Program and readiness assessment

**Goal:** a large migration starts with an honest readiness picture and a business case,
gets AWS (and partner) funding through MAP, and does not lose credits because resources
were never tagged.

## 1. MAP phases
| Phase | Output | Tools |
|---|---|---|
| **Assess** | Readiness gaps, TCO/business case, portfolio inventory | Migration Readiness Assessment (MRA), CART, Migration Evaluator, Application Discovery Service |
| **Mobilize** | Landing zone, operating model, skills, pilot migrations, detailed wave plan | Control Tower, Migration Hub, MGN pilots, training |
| **Migrate & modernize** | Waves executed, workloads optimised | MGN, DMS, DataSync, modernisation services |
MAP funding (credits, partner/ProServe cost offsets) is negotiated per engagement with the
AWS account team or a MAP-qualified partner; terms vary by deal size.

## 2. Readiness assessment
- **CART (Cloud Adoption Readiness Tool)**: a short online questionnaire across the six
  Cloud Adoption Framework perspectives (Business, People, Governance, Platform, Security,
  Operations); produces a readiness score and report. Good first pass.
- **MRA**: a facilitated workshop (AWS or partner) over the same perspectives, with
  evidence and a heat map of gaps (e.g. no landing zone, no cloud ops model, licensing
  unknowns). Output feeds the Mobilize plan.
- Typical high-impact gaps: identity federation, network connectivity (DX/VPN), security
  baseline and approvals, operations runbooks, skills, application owners' availability.

## 3. Business case
- **Migration Evaluator** (agentless collector or imports from CMDB/RVTools exports)
  measures actual utilisation and produces right-sized, licence-aware TCO projections.
- Combine with Application Discovery Service dependency data to group applications into
  waves; size each wave's cost and benefit.
- Present ranges, not single numbers; include dual-running costs during migration.

## 4. MAP tagging (credits depend on it)
- After the MAP agreement, you receive a **Migration Program Engagement ID (MPE ID)**.
- Tag every migrated resource with key `map-migrated` and the value given in the
  agreement (format such as `mig12345` or the server-ID based form from Migration Hub);
  activate `map-migrated` as a **cost allocation tag**.
- Enforce with a tag policy and Config rule in migration accounts; MGN launch templates and
  IaC modules should add the tag automatically.
- Untagged spend is not eligible; credits are computed from tagged usage.

## Gotchas
- MAP is a commercial program; eligibility (minimum spend, workload types, new vs existing
  workloads) and current tag format are defined in the agreement — read it, not a blog.
- Tags added late do not retroactively count for past months.
- An MRA with no executive sponsor produces a report nobody acts on; book the sponsor
  read-out up front.

## Verify
- [ ] CART/MRA report with owners assigned to each gap and target dates.
- [ ] Business case approved with dual-running costs included.
- [ ] `map-migrated` activated as a cost allocation tag; Cost Explorer grouped by it shows migrated spend.
- [ ] Config rule shows ≥ 95% of resources in migration accounts tagged.
