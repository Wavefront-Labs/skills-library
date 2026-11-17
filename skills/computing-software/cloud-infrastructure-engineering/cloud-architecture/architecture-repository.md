---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-repository
name: architecture-repository
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, togaf, architecture-principles, architecture-repository, enterprise-continuum, reference-library, architecture-documentation]
level: practitioner
status: draft
description: "Set up an architecture repository and reference library: TOGAF structure, what to store, docs-as-code tooling, ownership and keeping content current."
sources: ["https://pubs.opengroup.org/togaf-standard/architecture-content/chap05.html", "https://adr.github.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture repository and reference library

TOGAF's Architecture Repository holds the architecture metamodel, capability, landscape,
standards information base, reference library, governance log and requirements repository.
Most cloud teams need a lightweight version that engineers actually open.

## Structure (practical mapping)
| TOGAF area | Practical content |
|---|---|
| Architecture landscape | current and target diagrams per domain and workload |
| Standards information base | technology radar, approved services list, patterns |
| Reference library | reference architectures, landing-zone docs, templates |
| Governance log | ADRs, review outcomes, waivers, compliance assessments |
| Requirements repository | NFR catalogue, regulatory requirements |

## Steps
1. Choose tooling: docs-as-code in git (Markdown + diagrams-as-code such as Structurizr or
   Mermaid) rendered to a portal (Backstage TechDocs, MkDocs) works well for engineering
   audiences; an EA tool (Sparx, LeanIX, Ardoq) suits portfolio-level metadata.
2. Define a folder and metadata convention: owner, status (draft/approved/retired),
   review-by date.
3. Seed with the highest-value artefacts: principles, landing-zone design, 3-5 reference
   architectures, the ADR log.
4. Link from where people work: PR templates, design review checklist, service catalogue.
5. Run a quarterly freshness check: anything past review-by date gets reviewed or retired.

## Gotchas
- A wiki without owners rots in months.
- Duplicating facts held elsewhere (CMDB, service catalogue) causes drift; link instead.

## Verify
- [ ] Every artefact has an owner and review-by date.
- [ ] Search for a common pattern returns a current page.
