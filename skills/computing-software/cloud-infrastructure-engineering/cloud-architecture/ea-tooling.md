---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.ea-tooling
name: ea-tooling
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-principles, togaf, ea-tooling, archimate, leanix, ardoq, archi, structurizr, diagrams-as-code]
level: practitioner
status: draft
description: "Select enterprise architecture tooling: repository-based EA platforms vs ArchiMate modelling vs diagrams-as-code, with integration, metamodel and adoption criteria."
sources: ["https://www.archimatetool.com/", "https://docs.structurizr.com/", "https://pubs.opengroup.org/togaf-standard/adm/chap02.html", "https://www.opengroup.org/certifications/archimate"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EA tooling selection

## Tool classes
| Class | Examples | Good for |
|---|---|---|
| SaaS EA repository | LeanIX (SAP), Ardoq, Bizzdesign, MEGA HOPEX, Orbus iServer | Application portfolio, capability maps, lifecycle, surveys, reporting to execs |
| ArchiMate modelling | Archi (open source), Sparx EA, Bizzdesign | Rigorous models, viewpoints, standards compliance |
| Diagrams-as-code | Structurizr DSL (C4), PlantUML, Mermaid, D2 | Solution architecture in the repo, versioned with code |
| Discovery-fed | CMDB / cloud asset inventory integrations | Keeping inventory current automatically |

## Criteria
1. **Data freshness**: integrations with CMDB, cloud inventory, SSO app list, ITSM, cost data.
   A repository updated by hand decays within a quarter.
2. **Metamodel fit**: can you configure the element types you chose (and no more)?
3. **Audience**: execs need dashboards; engineers need diagrams near code.
4. **Standards**: ArchiMate exchange format import/export avoids lock-in.
5. **Cost and licences**: per editor vs per viewer pricing.
6. **Governance support**: lifecycle dates, ownership surveys, decision records.

## Procedure
1. Define 3-5 use cases (e.g. application rationalisation, end-of-life reporting, migration wave
   planning) and the data each needs.
2. Shortlist two or three tools; run a time-boxed pilot loading real data via integration.
3. Score; check export path.
4. Start minimal: applications, owners, lifecycle, capabilities. Expand only on demand.

## Gotchas
- Buying a tool before deciding the use cases produces an empty repository.
- Duplicate truth: the EA tool and the CMDB disagreeing about app owners.

## Verify
- [ ] Pilot shows data refreshed automatically from at least one source.
- [ ] Owners for > 90% of applications after rollout.
