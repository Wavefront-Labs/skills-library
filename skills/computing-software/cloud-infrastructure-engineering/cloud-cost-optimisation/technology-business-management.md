---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.technology-business-management
name: technology-business-management
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-practice-operations, finops-practice, technology-business-management, tbm, itfm, intersecting-disciplines]
level: practitioner
status: docs-checked
description: "Coordinate FinOps with ITFM and TBM teams: shared goals, data, terminology, responsibilities and one reconciled view of cloud cost."
sources: ["https://www.finops.org/framework/capabilities/intersecting-disciplines/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FinOps and ITFM / TBM

The FinOps Framework Intersecting Disciplines capability covers coordinating with allied disciplines, including IT
Financial Management (ITFM, which does IT cost categorisation). It does not tell FinOps teams to adopt those
disciplines, only to work with those in place; some organisations have no separate ITFM team outside Finance.

## Steps
1. **Common goals**: create a shared understanding of organisational goals, align objectives and confirm
   responsibilities and expected outcomes with leadership.
2. **Responsibilities**: define team responsibilities, enablement and interactions, including shared objectives.
3. **Shared data and terms**: define the intersecting data, resources and terminology (for example FOCUS), plus
   metadata, access, data resolution, exchange format and refresh cadence for information sharing.
4. **Workflows**: define common decision workflows, communication channels and cross-team notifications.
5. **One cost story**: at Walk, teams share a view of resource usage and cost and of how it is forecast, budgeted,
   reported and charged back. Reconcile the cloud total across the invoice, the finance ledger, the ITFM tool and the
   FinOps view, with a documented bridge for timing and credits.
6. **Revisit**: the importance of integration changes over time and by FinOps Scope; review the arrangement regularly.

## Gotchas
- Two allocation methods for the same shared cost give finance two answers; agree one.
- Renewal and exit ownership left undefined until a contract nears expiry is a Crawl-stage symptom (Framework).

## Verify
- [ ] Cloud totals agree across invoice, ledger, ITFM and FinOps views for a closed month, with the bridge written down.
- [ ] Owners for shared data and decisions are named.

## Checked
Confirmed on the FinOps Framework Intersecting Disciplines page (read to the Walk stage): ITFM role, coordination
activities, shared data and terminology, maturity descriptions. Removed: the TBM Council taxonomy (cost pools,
towers, solutions; page unreadable), FOCUS ServiceCategory mapping, named ITFM tools, the less-than-1% unmapped
threshold and the claim that TBM data is always monthly and amortised.
Method: docs-checked 2026-11-09 against finops.org Framework Intersecting Disciplines capability page
