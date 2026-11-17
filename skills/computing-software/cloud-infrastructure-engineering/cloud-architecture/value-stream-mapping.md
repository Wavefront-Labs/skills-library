---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.value-stream-mapping
name: value-stream-mapping
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, business-architecture, togaf, value-stream-mapping, value-streams, lean]
level: practitioner
status: draft
description: "Map value streams to the capabilities and cloud workloads that enable them, find bottlenecks, and use the result to sequence modernisation."
sources: ["https://pubs.opengroup.org/togaf-standard/business-architecture/value-streams.html", "https://www.lean.org/lexicon-terms/value-stream-mapping/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Value stream mapping to workloads

TOGAF/BIZBOK value streams are end-to-end stages that deliver value to a stakeholder
(Acquire Customer: Attract, Qualify, Onboard, Activate). Lean value-stream mapping adds
process time, wait time and handoffs. Both help decide which workloads matter most.

## Steps
1. **Pick the value stream** and its triggering stakeholder and value item.
2. **Define stages** (4-8) with entry and exit criteria.
3. **Cross-map stages to capabilities**, then capabilities to applications and cloud
   workloads. This gives a stage-by-stage list of systems.
4. **Measure** per stage: lead time, process time, % complete and accurate, failure demand;
   for the IT side: manual steps, batch windows, outage frequency.
5. **Find the constraint**: the stage with the longest wait or most rework. Ask which
   system limits it (overnight batch, manual provisioning, fragile integration).
6. **Prioritise**: workloads supporting the constraint stage go early in modernisation;
   modernising a non-constraint stage rarely improves the end-to-end outcome.

## Gotchas
- Mapping the ideal flow instead of the real one hides the waste.
- Value streams cut across departments; get a sponsor who owns the whole flow.

## Verify
- [ ] Each stage has measured lead time and named supporting workloads.
- [ ] The identified constraint has a modernisation item on the roadmap.
