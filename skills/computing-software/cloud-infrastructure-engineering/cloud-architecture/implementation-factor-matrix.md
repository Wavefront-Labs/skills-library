---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.implementation-factor-matrix
name: implementation-factor-matrix
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, opportunities-and-solutions, implementation-factor-matrix, togaf-phase-e, consolidated-gaps, deduction-matrix, work-package-identification]
level: practitioner
status: draft
description: "Use TOGAF Phase E implementation factor assessment and consolidated gaps, solutions and dependencies matrix to turn gap analysis into scoped work packages."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap06.html", "https://pubs.opengroup.org/togaf-standard/adm-techniques/chap07.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Implementation factor assessment and deduction matrix

## Implementation factor assessment and deduction matrix
A table of factors affecting implementation with columns: **Factor**, **Description**,
**Deduction** (what it means for the plan). Typical factors: risks, issues, assumptions,
dependencies, actions, inertia, organisational change, skills, vendor constraints, freeze periods.

Example rows:
| Factor | Description | Deduction |
|---|---|---|
| Change freeze | Retail freeze Nov-Jan | No customer-facing cutovers in Q4 |
| Skills | No Kubernetes operators in-house | Use managed container service first; training plan |
| Contract | DC lease ends Sept next year | Hard deadline for rehost wave of remaining VMs |

## Consolidated gaps, solutions and dependencies matrix
Rows = gaps from Phases B-D; columns = architecture domain, gap, potential solution, dependencies.
Group related gaps into **work packages** and identify transition architectures.

## Steps
1. Collect gaps from each domain's gap analysis.
2. Propose solutions per gap (reuse/buy/build).
3. Identify dependencies between solutions (data before apps, network before workloads).
4. Fill the factor matrix with programme constraints.
5. Group into work packages; check each is independently valuable where possible.
6. Feed Phase F sequencing.

## Verify
- [ ] Every gap is assigned to a work package or explicitly deferred.
- [ ] Deductions reflected in the migration plan.
