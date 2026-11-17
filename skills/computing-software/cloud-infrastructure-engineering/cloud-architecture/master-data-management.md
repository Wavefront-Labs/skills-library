---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.master-data-management
name: master-data-management
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, information-systems-architecture, master-data-management, mdm, golden-record, data-stewardship, registry-style, entity-resolution]
level: advanced
status: draft
description: "Choose an MDM architecture style (registry, consolidation, coexistence, centralised), golden-record rules, matching and stewardship for customer/product master data in cloud."
sources: ["https://learn.microsoft.com/azure/architecture/databases/architecture/profisee-master-data-management-data-factory", "https://www.dama.org/cpages/body-of-knowledge", "https://pubs.opengroup.org/togaf-standard/adm/chap05.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Master data management architecture

## Implementation styles (DAMA-DMBOK)
| Style | How | When |
|---|---|---|
| Registry | Index of IDs/cross-references; data stays in sources | Low intrusion, read-only 360 view |
| Consolidation | Copy to hub, build golden record for analytics | Reporting/analytics first |
| Coexistence | Hub golden record synchronised back to sources | Sources keep authoring, need consistency |
| Centralised (transactional) | Hub is the system of entry | Greenfield or strong governance |

## Design steps
1. Pick domains (customer, product, supplier, location) and the business problem (duplicates,
   inconsistent hierarchies, compliance).
2. Define the data model and attributes, plus **survivorship rules** per attribute (source
   priority, most recent, most complete).
3. **Matching**: deterministic keys first (tax ID, email), then probabilistic/fuzzy (name +
   address) with thresholds; human review queue for the grey zone.
4. **Identifiers**: issue a stable master ID; keep cross-reference table to source IDs.
5. **Distribution**: publish changes as events (master-data-changed) and/or APIs; consumers never
   query sources for master attributes.
6. **Stewardship**: data owners and stewards, workflows for merge/unmerge, quality dashboards.

## Gotchas
- Big-bang centralised MDM projects stall; start with registry/consolidation for one domain.
- No unmerge capability: false matches become permanent damage.
- Treating MDM as a tool purchase without stewardship roles.

## Verify
- [ ] Duplicate rate and match precision measured on a labelled sample.
- [ ] Consumers receive master changes within the agreed latency.
