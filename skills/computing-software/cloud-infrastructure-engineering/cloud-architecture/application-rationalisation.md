---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.application-rationalisation
name: application-rationalisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, information-systems-architecture, togaf, application-rationalisation, time-model, application-portfolio-management]
level: practitioner
status: draft
description: "Rationalise an application portfolio with the Gartner TIME model: collect fact sheets, score business and technical fit, and decide tolerate, invest, migrate or eliminate."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap05.html", "https://www.gartner.com/en/information-technology/glossary/application-portfolio-management-apm", "https://learn.microsoft.com/azure/cloud-adoption-framework/plan/contoso-migration-rationalize"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Application portfolio rationalisation

## Steps
1. **Inventory with fact sheets**: owner, users, capability supported, technology stack, age,
   licence and run cost, integrations, data classification, incidents, contract end dates.
2. **Score business fit** (functional fit, strategic importance, usage) and **technical fit**
   (supportability, security posture, scalability, skills availability) on 1-5 with criteria.
3. **TIME quadrant**:
   - **Tolerate**: high technical, low business fit - keep, minimise spend.
   - **Invest**: high business, high technical - modernise and extend.
   - **Migrate**: high business, low technical - re-platform or replace.
   - **Eliminate**: low on both - retire; move data to archive.
4. **Find redundancy**: multiple apps per capability (three CRMs after acquisitions)
   - consolidate to one.
5. **Feed cloud dispositions**: Eliminate maps to retire; Tolerate to retain or rehost;
   Migrate to replatform/repurchase; Invest to refactor.
6. **Track savings**: licence, infrastructure and support cost removed per retirement.

## Gotchas
- Retirement stalls on data retention needs; plan an archive (read-only store) early.
- Shadow IT and SaaS apps missing from the CMDB; use SSO logs and expense data to find them.

## Verify
- [ ] Every in-scope app has an owner and a TIME decision.
- [ ] Retirements have a data-archive plan and a decommission date.
