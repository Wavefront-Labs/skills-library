---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.data-architecture-development
name: data-architecture-development
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [data-architecture-development, adm-phase-c-data, phase c, data architecture, data entity, logical data model, data ownership, data lifecycle, enterprise-architecture]
level: practitioner
status: draft
description: "Define data entities, ownership, lifecycle and the logical data model needed to support the business architecture."
sources:
  - https://pubs.opengroup.org/togaf-standard/
  - https://pubs.opengroup.org/architecture/archimate32-doc/
  - https://www.zachman.com/about-the-zachman-framework
  - https://www.businessarchitectureguild.org/
  - https://www.dodcio.defense.gov/Library/DoD-Architecture-Framework/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Develop baseline and target data architecture

Goal: a data architecture the business and applications can both rely on.

1. Identify data entities from business objects, services and regulations.
2. Assign owner, steward and system of record for each entity.
3. Describe data lifecycle (create, use, archive, delete) and quality needs.
4. Develop a logical data model, then map entities to applications.
5. Define data security classification and retention.

Gotchas:
- Without a named system of record, duplicate masters multiply.
- Regulatory data (personal data, financial records) needs early legal input.

Verify: every entity has an owner and a system of record in the Data Entity/Business Function matrix.
