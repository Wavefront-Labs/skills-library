---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.capability-heatmap
name: capability-heatmap
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, business-architecture, capability-heatmap, capability-mapping, investment-planning, strategic-importance, technology-fit]
level: practitioner
status: draft
description: "Heat-map a business capability map by strategic importance, performance and technology fit to target cloud investment and modernisation where it moves the business."
sources: ["https://pubs.opengroup.org/togaf-standard/business-architecture/business-capabilities.html", "https://www.businessarchitectureguild.org/page/Guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capability heat-mapping for investment decisions

## Steps
1. Start from a level 1-2 capability map (stable, outcome-named: "Manage customer onboarding").
2. Choose 2-4 dimensions and a 3-point scale with written definitions:
   - Strategic importance (differentiating / core / commodity).
   - Business performance (meets / partially / fails needs).
   - Technology fit (apps supporting it: modern / ageing / end-of-life).
   - Cost (relative spend from application cost allocation).
3. Rate with business and IT owners together; record evidence.
4. Map applications to capabilities (from the application portfolio) to show duplication.
5. Read the quadrants:
   - Differentiating + poor performance or fit -> invest / modernise (refactor, build).
   - Commodity + high cost -> replace with SaaS, consolidate.
   - Differentiating + good -> protect, avoid disruption.
   - Commodity + adequate -> leave or rehost cheaply.
6. Feed priorities into the roadmap and migration 7 R decisions.

## Gotchas
- Too many colours and dimensions; nobody can read the map.
- IT-only ratings of business performance.
- Capability names that are really org units or systems.

## Verify
- [ ] Ratings agreed by business owners.
- [ ] Top investment candidates have a recommendation and owner.
