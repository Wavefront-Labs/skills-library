---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.environments-and-locations
name: environments-and-locations
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, technology-architecture, environments-and-locations, togaf, phase-d, environment-topology, regions]
level: practitioner
status: draft
description: "Draw the TOGAF environments and locations diagram for cloud: regions, zones, on-prem sites, edge and which environments and applications run where."
sources: ["https://pubs.opengroup.org/togaf-standard/architecture-content/chap04.html", "https://pubs.opengroup.org/togaf-standard/adm/chap07.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/considerations/regions"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Environments and locations diagram

## Steps
1. **List locations**: provider regions and zones, on-prem data centres, colos and on-ramps,
   offices/branches, edge sites, SaaS provider regions holding your data.
2. **List environments**: production, DR, pre-production, test, development, sandbox; per
   environment, the account/subscription/project boundaries.
3. **Map applications and data stores** to environment and location; mark primary vs replica
   vs backup copies and the data classification held there.
4. **Show connectivity** between locations (private links, VPN, internet) at a summary level.
5. **Annotate constraints**: residency (which data may sit where), latency, regulatory
   jurisdiction, provider region pairs used for DR.
6. **Generate from inventory** where possible and review at each architecture change.

## Gotchas
- Backups and logs replicated to another region are often missing from residency diagrams.
- SaaS locations are forgotten; they hold data too.

## Verify
- [ ] Every production data store shown with all locations of its copies.
- [ ] Residency constraints checked against the diagram.
