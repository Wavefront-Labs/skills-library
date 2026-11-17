---
id: computing-software.data-engineering.data-warehouse-architecture.data-fabric-and-hub-and-spoke
name: data-fabric-and-hub-and-spoke
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-fabric, hub-and-spoke, data-virtualization, metadata-driven]
level: advanced
status: draft
description: "Understand data fabric and hub-and-spoke architectures: metadata-driven integration, virtualisation vs consolidation, how they relate to data mesh and lakehouse, and trade-offs."
sources:
  - https://www.gartner.com/en/information-technology/glossary/data-fabric
  - https://www.dama.org/cpages/body-of-knowledge
  - https://martinfowler.com/articles/data-mesh-principles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data fabric and hub-and-spoke

**Goal:** choose an integration architecture deliberately and recognise what vendors mean by these labels.

## Hub-and-spoke
- A central **hub** (enterprise data warehouse, integration hub, or MDM) receives data from source spokes and distributes conformed data to consuming spokes (marts, applications).
- Classic Inmon EDW + dependent marts; ESB-era integration.
- Pros: one place for conformance, governance and history. Cons: central team bottleneck, long lead times.

## Data fabric
An architecture approach (not a product) using **active metadata** to automate integration across distributed sources:
- Unified catalog with technical, business and operational metadata.
- Knowledge graph of relationships between datasets.
- Integration styles chosen per use: batch ELT, streaming, CDC, **virtualisation/federation** (query in place).
- Automation from metadata: recommendations for joins, quality rules, policy enforcement everywhere.
- Consistent security and governance policies applied across platforms.

## Relationship to other patterns
| Pattern | Core idea |
|---|---|
| Hub-and-spoke | central integration point |
| Data fabric | technology/metadata layer connecting distributed data |
| Data mesh | organisational: domain ownership, data as a product, self-serve platform, federated governance |
| Lakehouse | storage/compute architecture (open tables + warehouse features) |
They combine: a mesh organisation can run on a lakehouse platform with fabric-style catalog and federation.

## Virtualisation vs consolidation
- Federation (Trino, Lakehouse Federation, Denodo, Starburst) avoids copies and gives fresh data but depends on source performance and availability, and makes history hard.
- Consolidation (copy into lake/warehouse) gives performance, history and isolation at the cost of latency and storage.
Use federation for exploration, low-volume lookups and sources you cannot copy; consolidate for heavy analytics and historical reporting.

## Gotchas
- Buying a "fabric" product does not create metadata quality; ownership and curation do.
- Fully virtual architectures struggle with point-in-time history and heavy joins.

## Verify
Architecture decision record states the chosen pattern, which integration style each major source uses, and why.
