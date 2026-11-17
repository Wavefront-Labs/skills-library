---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.critical-flows
name: critical-flows
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, reliability-foundations, critical-flows, user-flows, flow-criticality, business-critical-paths, well-architected-reliability]
level: practitioner
status: docs-checked
description: "Catalogue a workload's user and system flows, link each to business process, owner, escalation path and impact, and rate criticality high, medium or low."
sources: ["https://learn.microsoft.com/azure/well-architected/reliability/identify-flows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identifying and prioritising critical flows

Identify and define flows early in the design phase. Mapping user flows and system flows shows which workload
functionality is most critical, so reliability work goes where failure would hurt most.

## Steps
1. **Catalogue all flows.** Interview stakeholders, users, business analysts and technical teams; review any
   documentation (architecture diagrams, user manuals, process descriptions); observe the running workload
   through logs, metrics and user activity. Split the list into user flows (user interactions) and system flows
   (backend processes and data movement).
2. **Define start and end points** for each flow, break it into steps, and note dependencies on other flows or
   external systems. Document dependencies on shared platform services (identity, networking, messaging,
   monitoring), because their failure can affect many flows. Record alternative paths and distinct outcomes as
   separate catalogue entries.
3. **Draw it.** Flowcharts, UML sequence or use-case diagrams, or a descriptive text list all work. Update the
   catalogue as flows change, split or combine, and validate with stakeholders.
4. **Map each flow to business processes** (for example order fulfilment) using workload outputs, interviews and
   usage monitoring.
5. **Name the process owner** (responsible for the process and its flows) and the stakeholders (involved in the
   workload, dependent on the flow or managing one of its dependencies). An existing RACI matrix may already hold
   these: owners are typically responsible or accountable, stakeholders consulted or informed.
6. **Define escalation paths:** start with the person or group most likely to resolve the issue, then the next
   contact with broader responsibilities who can coordinate more of the organisation.
7. **Assess business impact:** positive impact when the flow runs, negative impact when it fails (quantified
   losses such as revenue, and subjective effects such as reputation and customer trust), and capacity and
   availability assumptions, including RTO and RPO where expected.
8. **Rate criticality** (quantitative or qualitative) using the page's descriptions:
   - High: integral to core business functions, such as customer experience, financial transactions, security,
     human health and safety; failure brings immediate or long-term serious effects.
   - Medium: needed for complete functionality but not directly customer- or business-facing; for example an
     internal data processing flow that can be retried without immediate external effect.
   - Low: no direct or significant effect on core functions or customer experience, such as nightly log
     transfers or optional feedback surveys.
9. **Review criticality periodically** as business priorities, usage patterns and dependencies change.

## Gotchas
- A flow with several outcomes needs separate entries, or the unusual outcome never gets a rating.
- Missing shared-service dependencies hide the failures that hit many flows at once.

## Verify
- [ ] Every flow has start and end points, steps, an owner, stakeholders and an escalation path.
- [ ] Every flow has a business-impact statement and a High, Medium or Low rating with a review date.

## Checked
2026-11-09. Confirmed against the Azure Well-Architected Reliability page on identifying and prioritising flows
(body text read by extracting paragraphs and list items). Removed the "mission-critical, business-critical,
business-operational" tiers, per-flow SLO and latency targets, bulkhead isolation, synthetic checks and the
"define criticality by system" gotcha, which the page does not state. The second cited page (metrics) was not read
and was dropped.
Method: docs-checked 2026-11-09 against https://learn.microsoft.com/azure/well-architected/reliability/identify-flows; documentation only, no commands run.
