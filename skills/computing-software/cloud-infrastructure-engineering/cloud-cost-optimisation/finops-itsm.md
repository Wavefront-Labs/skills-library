---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.finops-itsm
name: finops-itsm
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-practice-operations, finops-practice, finops-itsm, change-request-costing, cmdb]
level: practitioner
status: docs-checked
description: "Integrate FinOps with ITSM: use service catalogue and CMDB data for ownership, agree shared data and refresh, and route cost decisions through shared workflows."
sources: ["https://www.finops.org/framework/capabilities/intersecting-disciplines/", "https://www.finops.org/framework/capabilities/workload-optimization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FinOps with ITSM and change processes

The FinOps Framework treats ITSM as an intersecting discipline: teams managing delivery of IT services who hold
operational responsibility for some systems. The Framework's aim is to let FinOps coordinate with ITSM where it
exists, not to dictate how ITSM works.

## Integration points
1. **Ownership data**: the Framework lists IT Service Management data (IT service catalogue, CMDB or service
   registry, and service tickets) and the application portfolio master with application or service owner as inputs from
   allied personas. Use them as the source of ownership for allocation, and keep tagging standards aligned to them.
2. **Shared data agreement**: define the shared data, resources and terminology (the Framework cites FOCUS), the key
   metadata, data access, resolution, exchange format and refresh cadence.
3. **Shared workflows**: define common decision-making workflows, communication channels and cross-team
   notifications. Candidates are cost fields in change requests, cost anomalies routed to the owning team's queue,
   and cost shown on service catalogue items; these are design suggestions, not Framework requirements.
4. **Recommendations as work items**: usage optimisation recommendations should be shared with Engineering, with agreed
   timelines and accountability (Usage Optimization page), so putting them in the owning team's ticket queue fits.

## Steps
1. Agree goals and responsibilities with ITSM leadership, and write down who owns what.
2. Establish the data exchange (ownership records into the allocation model).
3. Pilot the workflow with one team, then widen it.
4. Revisit the arrangement regularly: the Framework says the importance of close interaction changes over time and
   differs between FinOps Scopes.

## Maturity (from the Framework)
- Crawl: FinOps and ITSM may have separate reporting structures, are aware of one another, and coordinate only when required.
- Walk: the Framework describes a shared understanding of usage and cost and how costs are forecast, budgeted,
  reported and charged back.

## Gotchas
- Stale ownership records route work to the wrong people; agree who maintains the data.
- Mandatory approval on every change creates a bottleneck; keep approval criteria agreed and proportionate.

## Verify
- [ ] Ownership data for cloud accounts is traceable to a service or application record.
- [ ] The data exchange and refresh cadence are written down and agreed with ITSM.

## Checked
Confirmed on the FinOps Framework Intersecting Disciplines page (ITSM as a discipline, information and data
coordination activities, Crawl and Walk descriptions, ITSM data inputs, revisit over time) and, for work-item
sharing, the Usage Optimization page. Removed: Infracost PR comments, the 5,000 dollar per month approval threshold,
the 100 percent CMDB coverage target, time-to-acknowledge tracking, quarterly HR reconciliation, problem
management guidance and the Practice Operations source (no ITSM content).
Method: docs-checked 2026-11-09 against finops.org Framework Intersecting Disciplines and Usage Optimization capability pages
