---
id: computing-software.data-engineering.data-warehouse-architecture.data-ownership-and-stewardship
name: data-ownership-and-stewardship
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-governance, data-stewardship, data-ownership, raci, data-domains, governance-council, operating-model, dmbok]
level: advanced
status: draft
description: "Set up data ownership and stewardship: owner, steward and custodian roles, domain assignment, RACI for common decisions, recording owners in the catalog, and a working governance forum."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://martinfowler.com/articles/data-mesh-principles.html
  - https://datahubproject.io/docs/ownership/ownership-types/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data ownership and stewardship

**Goal:** every important dataset has a named person accountable for it, people who look after its quality and meaning day to day, and a forum that settles disputes — so issues don't bounce between teams.

## 1. Roles (DAMA-DMBOK terms)
| Role | Who | Accountable / responsible for |
|---|---|---|
| Data owner | senior business leader of the domain (e.g. Head of Sales Ops) | access approvals, definitions, quality targets, risk acceptance |
| Business data steward | subject-matter expert in the domain | glossary terms, DQ rules, issue triage, user questions |
| Technical data steward | data engineer/analytics engineer owning the pipelines | lineage, implementation of rules, fixing pipeline defects |
| Data custodian | platform/infra team | storage, security controls, backups, access mechanics |
| Data consumer | analysts, apps | using data per policy, reporting issues |
Owners are business people. "IT owns the data" is the classic failure — IT can't decide what "active customer" means.

## 2. Assign by domain
- Define domains aligned to the business (Sales, Finance, Customer, Product, HR) and map every source system and published dataset to one domain.
- One owner per domain (and optionally per critical dataset); stewards per subdomain. Shared datasets (customer master) still get one accountable owner.
- Start with critical data elements and the datasets behind executive/regulatory reporting.

## 3. RACI for recurring decisions
| Decision | Owner | Business steward | Technical steward | Custodian |
|---|---|---|---|---|
| Grant access to restricted data | A | C | I | R |
| Define/change a business term | A | R | C | I |
| Set DQ thresholds | A | R | R | I |
| Fix a pipeline defect | I | C | A/R | C |
| Retention period | A | C | C | R |

## 4. Make ownership visible and enforced
- Owners and stewards recorded in the catalog per dataset (DataHub ownership types, Unity Catalog owner + tags, dbt `meta.owner`, Snowflake object tags).
- CI rule: new published models must declare an owner; alerts route to the owner's team.
- Access request tools route approvals to the owner automatically.

## 5. Governance forum
- Monthly council: owners + lead stewards + platform. Agenda: open S1/S2 DQ issues, conflicting definitions, policy changes, access exceptions, metrics (scorecard).
- Decision log published; escalation path to a data governance sponsor (CDO/CFO).
- Keep it lightweight: decisions in hours/days, not quarters, or teams route around it.

## 6. Onboarding and continuity
Steward handbook (responsibilities, tools, how-tos), time allocation agreed with managers (stewardship is part of the job, e.g. 10-20%), and ownership reassignment when people change roles — orphaned datasets are flagged by a monthly report.

## Verify
- [ ] 100% of published/critical datasets have an owner and steward in the catalog.
- [ ] Access requests and DQ issues route to owners without manual lookup.
- [ ] Orphaned-ownership report is empty or being worked.
