---
id: computing-software.data-engineering.data-warehouse-architecture.data-governance-operating-model-and-council
name: data-governance-operating-model-and-council
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, governance-operating-model, data-governance-council, data-owners, data-stewards, raci, federated-governance]
level: practitioner
status: draft
description: "Set up a data governance operating model: structure, council charter, owner and steward roles, decision rights, RACI and adoption metrics."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://www.datamesh-architecture.com/#federated-governance
  - https://edmcouncil.org/frameworks/dcam/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Governance operating model and council

Tools don't govern data; people with decision rights do. The operating model says who decides what, how disputes are settled, and how policies reach pipelines.

## Pick a structure
| Model | Fits | Risk |
|---|---|---|
| Centralised (one governance office) | smaller orgs, heavily regulated single business | bottleneck, seen as police |
| Federated (domains own their data, central sets standards) | data mesh, large multi-business orgs | inconsistency without strong standards |
| Hybrid (central office + domain owners/stewards) | most enterprises | needs clear decision rights |

## Roles
| Role | Responsibility |
|---|---|
| Executive sponsor (CDO/CFO) | funding, escalation, mandate |
| Governance council | approves policies and standards, resolves cross-domain disputes, prioritises |
| Data owner (business leader per domain) | accountable for quality, access approvals, definitions in their domain |
| Data steward (business or technical) | day-to-day definitions, quality issue triage, metadata upkeep |
| Data custodian (platform/engineering) | implements controls: storage, access, backups, pipelines |
| Governance office (small central team) | runs the programme, tooling, metrics, training |

## Council charter essentials
- Purpose and scope (which data, which decisions).
- Membership: domain owners, security/privacy, legal, platform lead; chair; quorum.
- Decision rights: approve policies, data standards, critical data element (CDE) definitions, exceptions; what's delegated to domains.
- Cadence: monthly council; weekly steward forum; ad hoc escalations with SLA.
- Inputs/outputs: issue log, policy backlog, decisions register (published).

## RACI example
| Activity | Owner | Steward | Custodian | Council |
|---|---|---|---|---|
| Define a KPI/CDE | A | R | C | I (A if cross-domain) |
| Grant access to confidential data | A | C | R | I |
| Data quality incident | A | R | R | I |
| New policy | C | C | C | A |

## Making it real
- Start with a few critical data elements (customer, revenue, product) tied to business pain, not the whole estate.
- Embed in delivery: definitions in the catalog/glossary, ownership metadata in dbt/catalog, access requests routed to owners automatically, quality tests on CDEs.
- Policy as code where possible so policies are enforced, not just written.

## Measure
Owners/stewards assigned for CDEs (%), glossary coverage, DQ incidents and time to resolve, access request lead time, policy exceptions open, and adoption (catalog searches, certified datasets used in BI).

## Verify
- [ ] Charter, RACI and decisions register published; every critical dataset has a named owner and steward.
- [ ] Council decisions show up in tooling (catalog definitions, policies, tests) within an agreed time.
