---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.c4-model
name: c4-model
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, technology-architecture, togaf, c4-model, architecture-diagrams, diagrams-as-code, structurizr]
level: practitioner
status: draft
description: "Draw cloud architecture diagrams with the C4 model: context, container, component and deployment views, notation rules, and diagrams-as-code."
sources: ["https://c4model.com/", "https://docs.structurizr.com/dsl", "https://learn.microsoft.com/azure/architecture/icons/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture diagrams with the C4 model

## Views
1. **System context**: the system as one box, its users and external systems. For everyone.
2. **Container**: deployable/runnable units (web app, API, database, queue, function) with
   technology and protocols on arrows. The most useful view for cloud design.
3. **Component**: inside one container; only when it adds value.
4. **Deployment**: maps containers to infrastructure - accounts, VPCs/VNets, subnets, regions,
   AZs, managed services. This is where provider icons belong.
Supplementary: dynamic views for key flows, and system landscape for the estate.

## Notation rules
- Every element has name, type, technology and a one-line responsibility.
- Every arrow is unidirectional with a label (what and how: "Reads orders [JDBC/TLS]").
- Include a key/legend and a title with scope and date.
- Show trust boundaries and network zones on deployment views.

## Diagrams as code
Structurizr DSL (one model, many views, so names stay consistent), PlantUML C4, or Mermaid
C4 in Markdown. Store with the code, render in CI, review in PRs.

## Gotchas
- Mixing abstraction levels (a Lambda function and a business domain in one diagram) confuses.
- Icon-only diagrams without labels or arrows' meaning look nice and say little.

## Verify
- [ ] Context, container and deployment views exist for each production system.
- [ ] Diagrams regenerated from source in CI and dated.
