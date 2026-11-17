---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.technology-portfolio
name: technology-portfolio
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, technology-architecture, technology-portfolio, togaf, phase-d, platform-decomposition, technology-lifecycle]
level: practitioner
status: draft
description: "Maintain a technology portfolio catalogue and platform decomposition diagram: products, versions, lifecycle status, owners and which applications run on each."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap07.html", "https://pubs.opengroup.org/togaf-standard/architecture-content/chap04.html", "https://endoflife.date/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Technology portfolio catalogue and platform decomposition

## Steps
1. **Catalogue technology components**: OS, databases, middleware, runtimes, cloud services,
   network and security products, SaaS. Record product, version, vendor, licence model,
   owner, lifecycle status (emerging / current / contained / retiring), vendor end-of-support.
2. **Populate from discovery**, not memory: CMDB, cloud inventory APIs (Config, Resource
   Graph, Cloud Asset Inventory), SBOMs and agents.
3. **Platform decomposition diagram**: layers (hardware/IaaS, platform services, runtime,
   application services) and which technology components implement each.
4. **Application/technology matrix**: which applications depend on each component and version.
   This turns end-of-support dates into an impact list.
5. **Target state**: mark which components the cloud target retires (e.g. self-managed
   Oracle to managed Postgres) and link to the roadmap.
6. **Review** against the technology radar and standards quarterly.

## Gotchas
- Version sprawl hides in "Java" or "Linux" entries; record major versions.
- SaaS and cloud managed services count as portfolio items too.

## Verify
- [ ] Every component has owner, lifecycle and end-of-support date.
- [ ] Application/technology matrix produces an EOL impact list on demand.
