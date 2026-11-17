---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.building-blocks
name: building-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, technology-architecture, togaf, building-blocks, architecture-building-blocks, solution-building-blocks]
level: practitioner
status: draft
description: "Define architecture building blocks and solution building blocks for a cloud platform, with interfaces, specifications and reuse rules."
sources: ["https://pubs.opengroup.org/togaf-standard/architecture-content/chap04.html", "https://pubs.opengroup.org/togaf-standard/adm/chap06.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture and solution building blocks

TOGAF distinguishes **architecture building blocks (ABBs)**, which describe required capability
and are technology-aware but product-neutral ("managed relational database with PITR and
encryption"), from **solution building blocks (SBBs)**, which are the concrete products or
modules implementing them ("Amazon Aurora PostgreSQL via our `rds-aurora` Terraform module").

## Steps
1. **Identify ABBs** from the target architecture: compute runtime, relational store, object
   store, messaging, identity, secrets, observability, network edge.
2. **Specify each ABB**: functions, interfaces, NFRs (availability, RPO), security controls,
   and the standards it must meet.
3. **Map to SBBs** per provider or context; there can be several SBBs per ABB (AWS and Azure
   variants). Record version, owner, IaC module link and support status.
4. **Make SBBs consumable**: versioned modules, documentation, examples, a changelog.
5. **Govern reuse**: designs reference ABBs; deviations from the SBB catalogue need an ADR.
6. **Retire** SBBs with a replacement and migration path.

## Gotchas
- Building blocks defined too finely (every resource) become an unmanageable catalogue.
- ABBs that name products are SBBs in disguise and block provider choice.

## Verify
- [ ] Each ABB has at least one current SBB with owner and module link.
- [ ] Gap analysis references building blocks consistently.
