---
id: computing-software.data-engineering.data-modelling.mdm-tool-selection
name: mdm-tool-selection
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, mdm-tools, master-data-management, informatica-mdm, reltio, profisee, tool-selection]
level: practitioner
status: draft
description: "Select a master data management tool: style fit, matching and survivorship, stewardship, integration, cost and a scored proof of concept."
sources:
  - https://www.gartner.com/en/information-technology/glossary/master-data-management-mdm
  - https://www.dama.org/cpages/body-of-knowledge
  - https://docs.informatica.com/master-data-management-cloud.html
  - https://docs.reltio.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# MDM tool selection

Decide the **implementation style and scope first**, then the tool. Many failed MDM programmes bought a platform before agreeing which domain, which systems, and who stewards the data.

## Clarify requirements
- Domains: customer, product, supplier, location, employee, asset; single or multi-domain.
- Style (DMBOK): registry (index of cross-references), consolidation (golden record for analytics), coexistence (golden record synced back to sources), centralised (MDM is the system of entry).
- Volume and latency: millions of records, real-time API lookups vs batch.
- Stewardship: number of stewards, workflows (approvals, data quality tasks), hierarchy management needs.
- Integration: sources (ERP, CRM, e-commerce), events/streaming, APIs for apps, warehouse sync.
- Regulatory: residency, audit trail, consent, GDPR erasure.

## Market landscape (examples, not endorsements)
| Category | Examples |
|---|---|
| Enterprise multi-domain | Informatica MDM (IDMC), SAP Master Data Governance, Stibo STEP (product-heavy), TIBCO EBX, IBM Match 360 |
| Cloud-native SaaS | Reltio, Profisee (Azure-aligned), Semarchy xDM, Syndigo/Riversand (product) |
| Warehouse-native / composable | entity resolution with Splink/Zingg/AWS Entity Resolution + dbt + stewardship app; CDPs for customer-only use cases |
Composable builds suit analytical consolidation with strong engineering teams; operational coexistence/centralised styles usually justify a platform.

## Evaluation criteria (score 1-5, weight by priority)
- Matching quality on **your** data (precision/recall on a labelled sample), tunability, explainability of matches.
- Survivorship rule flexibility per attribute, lineage of golden values.
- Data model flexibility (custom entities, relationships, hierarchies) and change effort.
- Stewardship UX: merge/unmerge, task queues, bulk edits, audit.
- Integration: APIs, CDC/event support, connectors to your ERP/CRM, warehouse outputs.
- Non-functional: scale, latency SLAs, multi-region, residency, SSO/RBAC, certifications.
- TCO: licence model (records, domains, users), infrastructure, implementation partner cost, internal FTEs.
- Vendor viability and roadmap; exit plan (data export formats).

## Proof of concept
- 4-6 weeks, 2-3 vendors, same dataset (anonymised real data, including dirty edge cases).
- Scripted scenarios: initial load, match tuning, steward merges/unmerges, new source onboarding, hierarchy change, API lookup latency, erasure request.
- Measure match precision/recall against a hand-labelled set, steward task time, and engineering effort.

## Verify
- [ ] Decision record lists style, scope, weighted scores, PoC metrics and TCO for each candidate.
- [ ] Stewardship operating model (owners, stewards, SLAs) agreed before contract signature.
