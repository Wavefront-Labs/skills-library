---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.data-mesh
name: data-mesh
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-styles, data-mesh, data-products, domain-ownership, self-serve-data-platform, federated-computational-governance]
level: advanced
status: draft
description: "Assess and implement data mesh: domain-owned data products, self-serve data platform, federated computational governance, and when a central platform is better."
sources: ["https://martinfowler.com/articles/data-mesh-principles.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/architectures/what-is-data-mesh", "https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-data-mesh-enterprise/introduction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data mesh

## Four principles (Zhamak Dehghani)
1. **Domain ownership**: operational domains own their analytical data.
2. **Data as a product**: discoverable, addressable, trustworthy (SLOs), self-describing,
   interoperable, secure; a product owner per data product.
3. **Self-serve data platform**: platform team provides storage, pipelines, catalog, access
   management, observability as self-service.
4. **Federated computational governance**: global standards (identifiers, classification,
   interoperability, privacy) enforced automatically by the platform.

## Cloud building blocks
Per-domain accounts/workspaces with lake storage, a central catalog (Unity Catalog, AWS Glue Data
Catalog + Lake Formation cross-account sharing, Microsoft Purview / Fabric domains, Dataplex),
standard table formats (Iceberg/Delta), data contracts, lineage.

## Readiness check
- Many domains with real data producers and consumers, and the bottleneck is a central data team.
- Domains willing to staff data product ownership.
- Platform team able to provide self-service.
If not, a well-run central lakehouse with domain-aligned zones is usually better.

## Steps
1. Pilot with 2-3 domains and a few consumer use cases.
2. Define data product spec (schema, contract, SLOs, owner, classification).
3. Build platform capabilities incrementally; automate governance checks.

## Gotchas
- Renaming the central data team's backlog "data products" without domain ownership.
- No interoperability standards -> inconsistent IDs across domains.

## Verify
- [ ] Data products registered in catalog with owner, SLO and contract.
