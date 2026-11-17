---
id: computing-software.cloud-infrastructure-engineering.aws.migration-portfolio-assessment-and-7r-decisions
name: migration-portfolio-assessment-and-7r-decisions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, migration, 7rs, portfolio-assessment, application-inventory, wave-planning]
level: advanced
status: docs-checked
description: "Run a migration portfolio assessment: build the app inventory, assign one of the 7 Rs with a decision order, group into waves, and avoid common misclassifications."
sources: ["https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html", "https://docs.aws.amazon.com/prescriptive-guidance/latest/application-portfolio-assessment-guide/introduction.html", "https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-migration/assess-phase.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migration portfolio assessment and 7R decisions

## 1. The 7 Rs (AWS migration strategies)
| R | Meaning |
|---|---|
| **Retire** | decommission, for example zombie (very low CPU and memory use) and idle applications found with discovery utilisation data |
| **Retain** | keep where it is for now |
| **Rehost** | lift and shift |
| **Relocate** | move without buying hardware, rewriting or changing operations; the application keeps serving users, so disruption is minimal |
| **Repurchase** | replace with a different product, typically SaaS |
| **Replatform** | move to a managed or serverless service, VMs to containers, avoid licence costs |
| **Refactor / re-architect** | modernise during migration; most complex and costly |
Per the large-migration guide, common strategies for large migrations are rehost, replatform, relocate and retire; refactor
only when the others are not acceptable, and modernise after migration where possible.

## 2. Build the inventory
Sources: CMDB, discovery tooling and utilisation data, interviews. Per application capture business owner,
criticality, users, stack and versions, servers and sizing, data volume, dependencies, licensing, compliance,
change frequency, pain points and end-of-life dates.

## 3. Decision order (practical judgement, not an AWS rule)
1. Unused or no longer needed: **Retire**, confirmed with utilisation data and the owner.
2. A suitable SaaS exists and contracts allow it: **Repurchase**.
3. Hard constraints to stay: **Retain** with a revisit date.
4. Need to move a virtualised estate unchanged and fast: **Relocate**.
5. The business needs capability the architecture blocks: **Refactor**, budgeted separately.
6. A small change gives clear benefit (managed database, containers, OS upgrade): **Replatform**.
7. Otherwise **Rehost**, then optimise in the cloud.

## 4. Scoring and waves
- Score business value against migration complexity (dependencies, data size, stack age, compliance); start with
  low-complexity applications to build the migration process.
- Group tightly coupled applications (chatty dependencies, shared databases) into the same wave.
- Validate any tool-generated recommendation with the application owners.

## 5. Common mistakes
- Refactoring by default: slow and risky.
- Ignoring licensing when choosing rehost versus replatform.
- Missing hidden dependencies (batch jobs, file shares, hard-coded IPs, directory services).
- "Retain" without a review date becomes permanent.

## Verify
- [ ] Inventory complete with owner sign-off per application and an R assigned with rationale.
- [ ] Dependencies validated by discovery data; waves group coupled applications.
- [ ] Retire list confirmed with usage evidence; retain list has revisit dates.

## Checked
2026-10-28. Confirmed on "About the migration strategies" (large migration guide): the seven strategy names,
retire/zombie/idle wording, relocate description, replatform description, refactor guidance and the large-migration
recommendation. Removed: "10-20% of portfolios" (wrong: the guide gives CPU and memory utilisation thresholds, not a
portfolio share, and those numbers are omitted here), MGN, VMware Cloud on AWS and EVS naming for relocate,
Migration Hub Strategy Recommendations and Migration Evaluator references. The retiring-applications source 404s and
was replaced.
Method: documentation only; no commands were run.
